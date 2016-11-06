from copy import deepcopy
import numpy as np

data = {
    'nodes': {
        '1': {
            'location': 0,
            'displacement': 1,
            'rotation': 0
        },
        '2': {
            'location': 10,
            'displacement': 0,
            'rotation': 0
        },
        '3': {
            'location': 30,
            'displacement': 1,
            'rotation': 0
        }
    },
    'loads': {
        '1': {
            'type': 'distributed',
            'load': 10,
            'loc1': 0,
            'loc2': 14
        },
        '2': {
            'type': 'point',
            'load': 20,
            'loc': 10
        },
        '3': {
            'type': 'point',
            'load': 100,
            'loc': 15
        }
    },
    'properties': {
        'momentOfInertia': 1000,
        'material': 'steel'
    }
}

def model(nodes, loads):
    """
    Sets up the 'model', using a node list to create a
    member dict, then adds properties to each member in the member dict,
    such as length, begin node, end node, and loads.
    """

    # ---------sort nodes by location and create a node list---------- #
    node_list = sorted([nodes[node_id] for node_id in nodes],
                       key=lambda x: x['location'])

    # --------------------------label dofs--------------------------- #
    # first run labels all free dofs ('rotation' or 'displacement' keys == 0)
    dof_label = 1
    for node in node_list:
        if node['displacement'] == 0:
            node['displacement_id'] = dof_label
            dof_label += 1
        if node['rotation'] == 0:
            node['rotation_id'] = dof_label
            dof_label += 1

    # this run labels all the non-free dofs
    for node in node_list:
        if not 'displacement_id' in node:
            node['displacement_id'] = dof_label
            dof_label += 1
        if not 'rotation_id' in node:
            node['rotation_id'] = dof_label
            dof_label += 1

    # -----------create a member list from the node list----------- #
    members = {str(i+1): {'begin': node_list[i], 'end': node_list[i+1]} for i in
                   range(len(node_list)-1)}

    # ----------------give members a length property------------------ #
    for member_id in members:
        members[member_id]['length'] = members[member_id]['end']['location'] - \
                                       members[member_id]['begin']['location']

    # ------------add the loads to their respective members------------ #
    for member_id in members:

        for load_id in loads:

            # define some variables to make comparisons shorter
            member = members[member_id]
            begin_loc = member['begin']['location']
            end_loc = member['end']['location']
            load = loads[load_id]

            # point load
            if load['type'] == 'point':

                # if the location of the load is between the beginning and end
                # of the member, we add the load to the member dict
                if end_loc > load['loc'] > begin_loc:

                    # if the key 'loads' is already present in the member dict
                    # we append the new load to the load list. if the key isn't
                    # in the member dict, we create a new entry for it
                    if 'loads' in member:
                        member['loads'].append(deepcopy(load))
                    else:
                        member['loads'] = [deepcopy(load)]

            # distributed load
            elif load['type'] == 'distributed':

                # if distributed load loc1 and loc 2 are both on the member,
                # we add the load to the member dict as-is
                if (end_loc > load['loc1'] >= begin_loc) and (
                        end_loc >= load['loc2'] > begin_loc):

                    # if the key 'loads' is already present in the member dict
                    # we append the new load to the load list. if the key isn't
                    # in the member dict, we create a new entry for it
                    if 'loads' in member:
                        member['loads'].append(deepcopy(load))
                    else:
                        member['loads'] = [deepcopy(load)]

                # if only loc1 is on the member, we add the load to the member
                # dict, and then change the loc2 to be the end of the member
                elif end_loc > load['loc1'] >= begin_loc:

                    # if the key 'loads' is already present in the member dict
                    # we append the new load to the load list. if the key isn't
                    # in the member dict, we create a new entry for it
                    if 'loads' in member:
                        member['loads'].append(deepcopy(load))
                    else:
                        member['loads'] = [deepcopy(load)]
                    member['loads'][-1]['loc2'] = end_loc

                # if only loc2 is on the member, we add the load to the member
                # dict, and then change the loc1 to be the beginning of the
                # member
                elif end_loc >= load['loc2'] > begin_loc:

                    # if the key 'loads' is already present in the member dict
                    # we append the new load to the load list. if the key isn't
                    # in the member dict, we create a new entry for it
                    if 'loads' in member:
                        member['loads'].append(deepcopy(load))
                    else:
                        member['loads'] = [deepcopy(load)]
                    member['loads'][-1]['loc1'] = begin_loc

    return members, node_list


def assemble_matrices(nodes, members, properties, loads):
    """
    Assembles the stiffness and force matrices for each member,
    and then combines these local matrices into global stiffness and force
    matrices.
    """

    # --------------get properties from input data--------------- #
    e_value = properties['momentOfInertia']
    i_value = 29000 if properties['material'] == 'steel' else 5000 # NEED TO FIX

    # ----------------compute member stiffness matrix----------------- #
    for member_id in members:
        # convert length to inches to be consistent with E and I
        l = members[member_id]['length']*12
        k = (e_value*i_value/l**3)*np.array(
            [[12, 6*l, -12, 6*l],
            [6*l, 4*l**2, -6*l, 2*l**2],
            [-12, -6*l, 12, -6*l],
            [6*l, 2*l**2, -6*l, 4*l**2]]
            )
        members[member_id]['k'] = k


    # --------------------fixed end force equations-------------------- #
    fixed_end_forces = {
        'point': {
            'fsb': lambda p, l, l_1, l_2: ((p*l_2**2)/(l**3))*(3*l_1+l_2),
            'fmb': lambda p, l, l_1, l_2: (p*l_1*l_2**2)/(l**2),
            'fse': lambda p, l, l_1, l_2: ((p*l_1**2)/(l**3))*(3*l_2+l_1),
            'fme': lambda p, l, l_1, l_2: -(p*l_1**2*l_2)/(l**2)
        },
        'distributed': {
            'fsb': lambda w, l, l_1, l_2: (w*l/2)*(1-(l_1/l**4)*(2*l**3-2*l_1**2*l+l_1**3)-(l_2**3/l**4)*(2*l-l_2)),
            'fmb': lambda w, l, l_1, l_2: (w*l**2/12)*(1-(l_1**2/l**4)*(6*l**2-8*l_1*l+3*l_1**2)-(l_2**3/l**4)*(4*l-3*l_2)),
            'fse': lambda w, l, l_1, l_2: (w*l/2)*(1-(l_2/l**4)*(2*l**3-2*l_2**2*l+l_2**3)-(l_1**3/l**4)*(2*l-l_1)),
            'fme': lambda w, l, l_1, l_2: -(w*l**2/12)*(1-(l_2**2/l**4)*(6*l**2-8*l_2*l+3*l_2**2)-(l_1**3/l**4)*(4*l-3*l_1))
        }
    }

    # -------------add fixed end forces to member dicts------------- #
    for member_id in members:
        member = members[member_id]

        # initiate member fixed end force vector
        member['qf'] = [0, 0, 0, 0]
        if 'loads' in member:
            for load in member['loads']:

                # fixed end forces for point loads
                if load['type'] == 'point':
                    p = load['load'] # kips
                    l = member['length']*12 # in
                    l_1 = load['loc']*12 - member['begin']['location']*12 # in
                    l_2 = member['end']['location']*12 - load['loc']*12 # in
                    member['qf'][0] += fixed_end_forces['point']['fsb'](p, l, l_1, l_2) #kips
                    member['qf'][1] += fixed_end_forces['point']['fmb'](p, l, l_1, l_2) #kip-in
                    member['qf'][2] += fixed_end_forces['point']['fse'](p, l, l_1, l_2) #kips
                    member['qf'][3] += fixed_end_forces['point']['fme'](p, l, l_1, l_2) #kip-in

                # fixed end forces for distributed loads
                if load['type'] == 'distributed':
                    w = load['load']/12 # kips/in
                    l = member['length']*12 # in
                    l_1 = load['loc1']*12 - member['begin']['location']*12 # in
                    l_2 = member['end']['location']*12 - load['loc2']*12 # in
                    member['qf'][0] += fixed_end_forces['distributed']['fsb'](w, l, l_1, l_2) #kips
                    member['qf'][1] += fixed_end_forces['distributed']['fmb'](w, l, l_1, l_2) #kip-in
                    member['qf'][2] += fixed_end_forces['distributed']['fse'](w, l, l_1, l_2) #kips
                    member['qf'][3] += fixed_end_forces['distributed']['fme'](w, l, l_1, l_2) #kip-in

        # make Qf array a numpy array
        member['qf'] = np.asarray(member['qf'])

        # reshape into a column vector
        member['qf'] = member['qf'].reshape(4, 1)

    # ---------------------------calculate ndof------------------------- #
    # ndof_calc function is in the 'Helper functions' section at the bottom
    ndof = ndof_calc(nodes)


    # -------------------define member code numbers------------------- #
    for member_id in members:
        code_nums = [0, 0, 0, 0]
        code_nums[0] = members[member_id]['begin']['displacement_id']
        code_nums[1] = members[member_id]['begin']['rotation_id']
        code_nums[2] = members[member_id]['end']['displacement_id']
        code_nums[3] = members[member_id]['end']['rotation_id']
        members[member_id]['code_nums'] = code_nums


    # ---initiate structure stiffness matrix and fixed end force vector--- #
    s = np.zeros((ndof, ndof))
    pf = np.zeros((ndof, 1))

    # ------------add stiffness values from local stiffness-------------- #
    # ------------matrices to structure stiffness matrix----------------- #
    for member_id in members:
        code_nums = members[member_id]['code_nums']
        k = members[member_id]['k']
        qf = members[member_id]['qf']
        for i in range(len(code_nums)):
            for j in range(len(code_nums)):
                try:
                    s[code_nums[i]-1, code_nums[j]-1] += k[i, j]
                except IndexError:
                    continue
            try:
                pf[code_nums[i]-1, 0] += qf[i, 0]
            except IndexError:
                continue


    # -------------construct joint loads vector P--------------- #
    p = np.zeros((ndof, 1))
    i = 0
    while i < ndof:
        for node in nodes:
            if node['displacement'] == 0:
                for load_id in loads:
                    load = loads[load_id]
                    if load['type'] == 'point' and load['loc'] == node['location']:
                        p[i] += -load['load']
                i += 1
            if node['rotation'] == 0:
                i += 1
    return s, pf, p


def joint_disp_global(s, pf, p):
    """
    Uses the global matrices to calculate the joint
    displacements and rotations at each node.
    """

    d = np.linalg.solve(s, (p - pf))
    return d

def joint_disp_local(d, members):
    """
    Takes the global displacements and, using the member code
    numbers, places them in member-specific joint displacement vectors.
    """

    for member_id in members:
        member = members[member_id]
        member['u'] = np.asarray([0., 0., 0., 0.]).reshape((4, 1))
        code_nums = member['code_nums']
        for i, num in enumerate(code_nums):
            if num-1 in range(np.size(d)):
                member['u'][i, 0] += d[num-1, 0]

    return members


def member_end_forces(members):
    """
    Uses the joint displacements to calculate the member end
    forces.
    """

    for member_id in members:
        member = members[member_id]
        k = member['k']
        u = member['u']
        qf = member['qf']
        q = k.dot(u) + qf
        member['q'] = q

    return members


def beam_reactions(members, nodes):
    """
    Takes the member end forces and assigns them to global
    nodes, creating an overall beam reactions vector.
    """

    ndof = ndof_calc(nodes)

    code_nums_restrained = list(range(ndof+1, 2*nj+1))

    r = np.zeros(2*nj-ndof).reshape(2*nj-ndof, 1)
    for member_id in members:
        member = members[member_id]
        code_nums = member['code_nums']
        q = members[member_id]['q']
        for i in range(len(code_nums)):
            for j in range(len(code_nums_restrained)):
                if code_nums[i] == code_nums_restrained[j]:
                    r[j] += q[i]
    return r




def main(data):
    members, nodes = model(data['nodes'], data['loads'])
    s, pf, p = assemble_matrices(nodes, members, data['properties'], data['loads'])
    d = joint_disp_global(s, pf, p)
    members = joint_disp_local(d, members)
    members = member_end_forces(members)
    r = beam_reactions(members, nodes)

    return r




# Helper functions

def ndof_calc(node_list):
    """
    Takes a node_list array and returns the number of degrees
    of freedom in the system.
    """

    # for each node, we add 2 dofs, and then subtract out 1 dof for each
    # instance of '1' in either rotation or displacement (1 indicates that the
    # dof is restrained)
    nj = len(node_list)
    ndof = 2*nj
    for node in node_list:
        if node['displacement'] == 1:
            ndof -= 1
        if node['rotation'] == 1:
            ndof -= 1
    return ndof






# Testing/debugging shit

#    print('S =\n', s)
#    print('Pf =\n', pf)
#    print('P =\n', p)
#    print('d =\n', d)
#    for member_id in members:
#        print('Q'+member_id, '=\n', members[member_id]['q'])
#    print('R =\n', r)
