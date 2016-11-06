from copy import deepcopy

members = {
    '1': {
        'begin': {
            'location': 0
        },
        'end': {
            'location': 10
        }
    },
    '2': {
        'begin': {
            'location': 10
        },
        'end': {
            'location': 30
        }
    }
}

loads = {
    '1': {
        'type': 'point',
        'loc': 20,
    },
    '2': {
        'type': 'distributed',
        'loc1': 0,
        'loc2': 14
    }
}

for a_member in members:

    for a_load in loads:

        # define some variables to make comparisons shorter
        member = members[a_member]
        begin_loc = member['begin']['location']
        end_loc = member['end']['location']
        load = loads[a_load]

        # point load
        if load['type'] == 'point':

            # if the location of the load is between the beginning and end
            # of the member, we add the load to the member dict
            if end_loc > load['loc'] > begin_loc:

                # if the key 'loads' is already present in the member dict
                # we append the new load to the load list. if the key isn't
                # in the member dict, we create a new entry for it
                if 'loads' in member:
                    members[a_member]['loads'].append(deepcopy(load))
                else:
                    members[a_member]['loads'] = [deepcopy(load)]

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
                    members[a_member]['loads'].append(deepcopy(load))
                else:
                    members[a_member]['loads'] = [deepcopy(load)]

            # if only loc1 is on the member, we add the load to the member
            # dict, and then change the loc2 to be the end of the member
            elif end_loc > load['loc1'] >= begin_loc:
                print(a_member, a_load, 'first') # debugging

                # if the key 'loads' is already present in the member dict
                # we append the new load to the load list. if the key isn't
                # in the member dict, we create a new entry for it
                if 'loads' in member:
                    members[a_member]['loads'].append(deepcopy(load))
                else:
                    members[a_member]['loads'] = [deepcopy(load)]
                members[a_member]['loads'][-1]['loc2'] = end_loc

            # if only loc2 is on the member, we add the load to the member
            # dict, and then change the loc1 to be the beginning of the
            # member
            elif end_loc >= load['loc2'] > begin_loc:
                print(a_member, a_load, 'second') # debugging

                # if the key 'loads' is already present in the member dict
                # we append the new load to the load list. if the key isn't
                # in the member dict, we create a new entry for it
                if 'loads' in member:
                    members[a_member]['loads'].append(deepcopy(load))
                else:
                    members[a_member]['loads'] = [deepcopy(load)]
                members[a_member]['loads'][-1]['loc1'] = begin_loc

print(members)
