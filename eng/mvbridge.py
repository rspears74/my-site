"""All calculations for shear moment calulator"""

import operator
import matplotlib
matplotlib.use('Agg')
import mpld3
import matplotlib.pyplot as plt


def max_mv_bridge(span_length, x_loc, feet_or_frac, incr, impact_factor,
              dist_factor):

    #Check input types
    if (type(span_length) is str or type(x_loc) is str or type(incr) is str or\
        type(impact_factor) is str or type(dist_factor) is str or\
        x_loc > span_length):
        return {'data': None, 'error': 'Invalid input. Try again.'}
    # Get values from input
    x_loc = x_loc * span_length if feet_or_frac == 'frac' else x_loc
    incr = incr/12

    # Cooper E-80 Axle Layout
    axle_loads = [40, 80, 80, 80, 80, 52, 52, 52, 52,
                  40, 80, 80, 80, 80, 52, 52, 52, 52,
                  8]

    axle_spaces = [0, 8, 5, 5, 5, 9, 5, 6, 5,
                   8, 8, 5, 5, 5, 9, 5, 6, 5,
                   5.5]

    # Add trailing live load up to length of span
    train_len = sum(axle_spaces)
    while (sum(axle_spaces) - train_len) < span_length:
        axle_spaces.append(1)
        axle_loads.append(8)

    num_axles = len(axle_loads)

    train_tot = sum(axle_spaces)

    # Initialize train positions array
    positions = []
    point = -span_length
    while point <= train_tot:
        positions.append(point)
        point += incr

    # Initialize arrays to hold total moment and shear values.
    # These arrays will be used to store the moment and shear values per
    # position of the train. We will run the "max" function to find max
    # values in these arrays
    m_array = []
    v_array = []

    for i in range(len(positions)):
        # a and b arrays store a and b values or each axle
        # r1 and r2 arrays store reactions at ends 1 and 2 for each axle
        # m and v arrays store m and v caused by each axle
        a = []
        b = []
        r1 = []
        r2 = []
        m = []
        v = []

        # This loop calculates individual values for each of the above
        # arrays and appends each value to the array.
        for j in range(num_axles):
            a_val = span_length + positions[i] - sum(axle_spaces[:j+1])
            a.append(a_val)

            b_val = span_length - a_val
            b.append(b_val)

            if 0 < b_val < span_length and a_val > x_loc:
                m_val = axle_loads[j]*(a_val - x_loc)
            else:
                m_val = 0
            m.append(m_val)

            if 0 < b_val < span_length and a_val < x_loc:
                v_val = axle_loads[j]
            else:
                v_val = 0
            v.append(v_val)

            if 0 < b_val < span_length:
                r1_val = axle_loads[j]*b_val/span_length
            else:
                r1_val = 0
            r1.append(r1_val)

            if 0 < a_val < span_length:
                r2_val = axle_loads[j]*a_val/span_length
            else:
                r2_val = 0
            r2.append(r2_val)

        # Calculate the moment and shear at the respective x location
        # caused by the train at position i and push these values to the
        # global moment and shear arrays
        m_tot = sum(r2)*(span_length-x_loc) - sum(m)
        v_tot = abs(sum(r1) - sum(v))
        m_array.append(m_tot)
        v_array.append(v_tot)

    # Find max and position of train to cause max
    m_loc_index, m_max = max(enumerate(m_array), key=operator.itemgetter(1))
    v_loc_index, v_max = max(enumerate(v_array), key=operator.itemgetter(1))
    m_max = m_max*(1 + impact_factor)*dist_factor
    v_max = v_max*(1 + impact_factor)*dist_factor
    m_max_loc = positions[m_loc_index]
    v_max_loc = positions[v_loc_index]

    # Set values in GUI to calculated values
    results = {'mmax': round(m_max, 2), 'vmax': round(v_max, 2),
               'mmaxloc': round(m_max_loc, 2), 'vmaxloc': round(v_max_loc, 2)}
    return {'data': results, 'error': None}


def max_pier_reaction(span_l_1, span_l_2, incr, impact_factor,
                      dist_factor):

    if (type(span_l_1) is str or type(span_l_2) is str or type(incr)\
        is str or type(impact_factor) is str or type(dist_factor) is str):

        return {'data': None, 'error': 'Invalid input. Try again.'}

    span_length_1, span_length_2 = span_l_1, span_l_2
    total_length = span_length_1 + span_length_2

    # Cooper E-80 Axle Layout
    axle_loads = [40, 80, 80, 80, 80, 52, 52, 52, 52,
                  40, 80, 80, 80, 80, 52, 52, 52, 52,
                  8]

    axle_spaces = [0, 8, 5, 5, 5, 9, 5, 6, 5,
                   8, 8, 5, 5, 5, 9, 5, 6, 5,
                   5.5]

    # Add trailing live load up to length of span
    train_len = sum(axle_spaces)
    while (sum(axle_spaces) - train_len) < total_length:
        axle_spaces.append(1)
        axle_loads.append(8)

    num_axles = len(axle_loads)

    train_tot = sum(axle_spaces)

    # Initialize train positions array
    positions = []
    point = -total_length
    while point <= train_tot:
        positions.append(point)
        point += incr

    pier_react = []
    span_1_react = []

    for i in range(len(positions)):

        a = []
        b = []
        r1 = []
        r2 = []
        r3 = []
        r4 = []

        for j in range(num_axles):

            a_val = sum(axle_spaces[:j+1]) - positions[i]
            a.append(a_val)

            b_val = total_length - a_val
            b.append(b_val)

            if b_val < total_length and b_val > span_length_2:
                r1_val = (axle_loads[j] - span_length_2) * b_val / span_length_1
            else:
                r1_val = 0
            r1.append(r1_val)

            if a_val < span_length_1 and a_val > 0:
                r2_val = axle_loads[j] * a_val / span_length_1
            elif a_val == span_length_1:
                r2_val = axle_loads[j] / 2
            else:
                r2_val = 0
            r2.append(r2_val)

            if b_val < span_length_2 and b_val > 0:
                r3_val = b_val * axle_loads[j] / span_length_2
            elif b_val == span_length_2:
                r3_val = axle_loads[j] / 2
            else:
                r3_val = 0
            r3.append(r3_val)

            if a_val < total_length and a_val > span_length_1:
                r4_val = axle_loads[j] * (a_val - span_length_1) / span_length_2
            else:
                r4_val = 0
            r4.append(r4_val)

        r1_tot = sum(r1)
        r2_tot = sum(r2)
        r3_tot = sum(r3)
        r4_tot = sum(r4)
        pier_react.append(r2_tot + r3_tot)
        span_1_react.append(r2_tot)

    pier_react_loc_index1, max_pier_react1 = max(enumerate(pier_react),
                                                 key=operator.itemgetter(1))
    max_pier_react1 = max_pier_react1 * (1 + impact_factor) * dist_factor
    max_pier_react_loc1 = positions[pier_react_loc_index1]
    span_1_contribution1 = span_1_react[pier_react_loc_index1] *\
                          (1 + impact_factor) * dist_factor
    span_2_contribution1 = max_pier_react1 - span_1_contribution1


    span_length_1, span_length_2 = span_l_2, span_l_1
    pier_react = []
    span_1_react = []

    for i in range(len(positions)):

        a = []
        b = []
        r1 = []
        r2 = []
        r3 = []
        r4 = []

        for j in range(num_axles):

            a_val = sum(axle_spaces[:j+1]) - positions[i]
            a.append(a_val)

            b_val = total_length - a_val
            b.append(b_val)

            if b_val < total_length and b_val > span_length_2:
                r1_val = (axle_loads[j] - span_length_2) * b_val / span_length_1
            else:
                r1_val = 0
            r1.append(r1_val)

            if a_val < span_length_1 and a_val > 0:
                r2_val = axle_loads[j] * a_val / span_length_1
            elif a_val == span_length_1:
                r2_val = axle_loads[j] / 2
            else:
                r2_val = 0
            r2.append(r2_val)

            if b_val < span_length_2 and b_val > 0:
                r3_val = b_val * axle_loads[j] / span_length_2
            elif b_val == span_length_2:
                r3_val = axle_loads[j] / 2
            else:
                r3_val = 0
            r3.append(r3_val)

            if a_val < total_length and a_val > span_length_1:
                r4_val = axle_loads[j] * (a_val - span_length_1) / span_length_2
            else:
                r4_val = 0
            r4.append(r4_val)

        r1_tot = sum(r1)
        r2_tot = sum(r2)
        r3_tot = sum(r3)
        r4_tot = sum(r4)
        pier_react.append(r2_tot + r3_tot)
        span_1_react.append(r2_tot)

    pier_react_loc_index2, max_pier_react2 = max(enumerate(pier_react),
                                                 key=operator.itemgetter(1))
    max_pier_react2 = max_pier_react2 * (1 + impact_factor) * dist_factor
    max_pier_react_loc2 = positions[pier_react_loc_index2]
    span_1_contribution2 = span_1_react[pier_react_loc_index2] *\
                          (1 + impact_factor) * dist_factor
    span_2_contribution2 = max_pier_react2 - span_1_contribution2

    if max_pier_react1 > max_pier_react2:
        max_pier_react = max_pier_react1
        max_pier_react_loc = max_pier_react_loc1
        span_1_contribution = span_1_contribution1
        span_2_contribution = span_2_contribution1
    else:
        max_pier_react = max_pier_react2
        max_pier_react_loc = max_pier_react_loc2
        span_1_contribution = span_1_contribution2
        span_2_contribution = span_2_contribution2

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    span = ax.plot([0, total_length], [0, 0], 'b')

    bound1 = ax.plot(0, -0.7, 'b^')
    bound3 = ax.plot(total_length, -0.7, 'bo')
    if max_pier_react1 > max_pier_react2:
        bound2 = ax.plot(span_l_2, -0.7, 'bo')
    else:
        bound2 = ax.plot(span_l_1, -0.7, 'bo')

    axle_pos = total_length + max_pier_react_loc

    axle_loads = [40, 80, 80, 80, 80, 52, 52, 52, 52,
                  40, 80, 80, 80, 80, 52, 52, 52, 52,
                  8]

    axle_spaces = [0, 8, 5, 5, 5, 9, 5, 6, 5,
                   8, 8, 5, 5, 5, 9, 5, 6, 5,
                   5.5]

    train_len = sum(axle_spaces)
    while (sum(axle_spaces) - train_len) < total_length:
        axle_spaces.append(1)
        axle_loads.append(8)

    for pos, spac in enumerate(axle_spaces):
        axle_pos = axle_pos - spac
        axle_load = 1 + axle_loads[pos] / 4
        axle = ax.plot([axle_pos, axle_pos], [1, axle_load], 'r')
        axle_label = ax.text(axle_pos - 1.5,
                             axle_load + 2,
                             str(axle_loads[pos]) + 'k',
                             fontsize=8,
                             color='r')
        axle_end = ax.plot(axle_pos, 1, 'rv')
    ax.set_xlim(-20, total_length + 20)
    ax.set_ylim(-30, 60)
    ax.set_title('Train Position for Max Pier Reaction')
    loc_plot = mpld3.fig_to_dict(fig)

    results = {
               'maxPierReact': round(max_pier_react, 2),
               'span1': round(span_1_contribution, 2),
               'span2': round(span_2_contribution, 2),
               'location': round(max_pier_react_loc, 2),
               'locPlot': loc_plot
               }
    return {'data': results, 'error': None}


def show_plot_moment(span_length, x_loc, feet_or_frac, max_moment_loc):

    axle_pos = max_moment_loc
    x_loc = x_loc * span_length if feet_or_frac == 'frac' else x_loc

    # Plot span
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    span = ax.plot([0, span_length], [0, 0], 'b')

    # Add boundaries to span
    # tri_width = (span_length*1.2+20)/120
    # bound1 = plt.plot([0, -tri_width, tri_width, 0], [0, -2, -2, 0])
    bound1 = ax.plot(0, -0.7, 'b^')
    bound2 = ax.plot(span_length, -0.7, 'bo')

    axle_pos += span_length

    # Cooper E-80 Axle Layout
    axle_loads = [40, 80, 80, 80, 80, 52, 52, 52, 52,
                  40, 80, 80, 80, 80, 52, 52, 52, 52,
                  8]

    axle_spaces = [0, 8, 5, 5, 5, 9, 5, 6, 5,
                   8, 8, 5, 5, 5, 9, 5, 6, 5,
                   5.5]

    train_len = sum(axle_spaces)
    while (sum(axle_spaces) - train_len) < span_length:
        axle_spaces.append(1)
        axle_loads.append(8)

    for pos, spac in enumerate(axle_spaces):
        axle_pos = axle_pos - spac
        axle_load = 1 + axle_loads[pos] / 4
        axle = ax.plot([axle_pos, axle_pos], [1, axle_load], 'r')
        axle_label = ax.text(axle_pos - 1.5,
                             axle_load + 2,
                             str(axle_loads[pos]) + 'k',
                             fontsize=8,
                             color='r')
        axle_end = ax.plot(axle_pos, 1, 'rv')
    xplot = ax.plot([x_loc, x_loc], [-1, -5], 'y')
    xplotarr = ax.plot(x_loc, -1, 'y^')
    ax.set_xlim(-20, span_length + 20)
    ax.set_ylim(-30, 60)
    ax.set_title('Train Position for Max Moment')
    return mpld3.fig_to_dict(fig)


def show_plot_shear(span_length, x_loc, feet_or_frac, max_shear_loc):

    axle_pos = max_shear_loc
    x_loc = x_loc * span_length if feet_or_frac == 'frac' else x_loc


    # Plot span
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    span = ax.plot([0, span_length], [0, 0], 'b')

    # Add boundaries to span
    # tri_width = (span_length*1.2+20)/120
    # bound1 = plt.plot([0, -tri_width, tri_width, 0], [0, -2, -2, 0])
    bound1 = ax.plot(0, -0.7, 'b^')
    bound2 = ax.plot(span_length, -0.7, 'bo')

    axle_pos += span_length

    # Cooper E-80 Axle Layout
    axle_loads = [40, 80, 80, 80, 80, 52, 52, 52, 52,
                  40, 80, 80, 80, 80, 52, 52, 52, 52,
                  8]

    axle_spaces = [0, 8, 5, 5, 5, 9, 5, 6, 5,
                   8, 8, 5, 5, 5, 9, 5, 6, 5,
                   5.5]

    train_len = sum(axle_spaces)
    while (sum(axle_spaces) - train_len) < span_length:
        axle_spaces.append(1)
        axle_loads.append(8)

    for pos, spac in enumerate(axle_spaces):
        axle_pos = axle_pos - spac
        axle_load = 1 + axle_loads[pos] / 4
        axle = ax.plot([axle_pos, axle_pos], [1, axle_load], 'r')
        axle_label = ax.text(axle_pos - 1.5,
                             axle_load + 2,
                             str(axle_loads[pos]) + 'k',
                             fontsize=8,
                             color='r')
        axle_end = ax.plot(axle_pos, 1, 'rv')
    xplot = ax.plot([x_loc, x_loc], [-1, -5], 'y')
    xplotarr = ax.plot(x_loc, -1 ,'y^')
    ax.set_xlim(-20, span_length + 20)
    ax.set_ylim(-30, 60)
    ax.set_title('Train Position for Max Shear')
    return mpld3.fig_to_dict(fig)


def nth_point_moment(span_length, num_points, incr, impact_factor, dist_factor):

    #Check input types
    if (type(span_length) is str or type(num_points) is not int or type(incr)\
        is str or type(impact_factor) is str or type(dist_factor) is str):
        return {'data': None, 'error': 'Invalid input. Try again.'}

    n = num_points

    x_locs = [i*span_length/n for i in range(n+1)]

    # Cooper E-80 Axle Layout
    axle_loads = [40, 80, 80, 80, 80, 52, 52, 52, 52,
                  40, 80, 80, 80, 80, 52, 52, 52, 52,
                  8]

    axle_spaces = [0, 8, 5, 5, 5, 9, 5, 6, 5,
                   8, 8, 5, 5, 5, 9, 5, 6, 5,
                   5.5]
    train_len = sum(axle_spaces)
    while (sum(axle_spaces) - train_len) < span_length:
        axle_spaces.append(1)
        axle_loads.append(8)

    num_axles = len(axle_loads)

    train_tot = sum(axle_spaces)
    # Initialize train positions array
    positions = []
    point = -span_length
    while point <= train_tot:
        positions.append(point)
        point += incr

    # Initialize arrays to hold total moment and shear values.
    # These arrays will be used to store the moment and shear values per
    # position of the train. We will run the "max" function to find max
    # values in these arrays
    m_maxs = []

    for loc in x_locs:
        m_array = []

        for i in range(len(positions)):
            # a and b arrays store a and b values or each axle
            # r1 and r2 arrays store reactions at ends 1 and 2 for each axle
            # m and v arrays store m and v caused by each axle
            a = []
            b = []
            r2 = []
            m = []

            # This loop calculates individual values for each of the above
            # arrays and appends each value to the array.
            for j in range(num_axles):
                a_val = span_length + positions[i] - sum(axle_spaces[:j+1])
                a.append(a_val)

                b_val = span_length - a_val
                b.append(b_val)

                if 0 < b_val < span_length and a_val > loc:
                    m_val = axle_loads[j]*(a_val - loc)
                else:
                    m_val = 0
                m.append(m_val)

                if 0 < a_val < span_length:
                    r2_val = axle_loads[j]*a_val/span_length
                else:
                    r2_val = 0
                r2.append(r2_val)

            # Calculate the moment and shear at the respective x location
            # caused by the train at position i and push these values to the
            # global moment and shear arrays
            m_tot = sum(r2)*(span_length-loc) - sum(m)
            m_array.append(m_tot)

        # Find max and position of train to cause max
        m_max = max(m_array)
        m_max = m_max*(1 + impact_factor)*dist_factor
        m_maxs.append(m_max)

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)

    ax.plot(x_locs, m_maxs)
    ax.set_ylabel('Maximum Moment, kip-ft')
    ax.set_xlabel('Span Position, ft')
    ax.set_title('Maximum Moment at '+str(n)+'th Points Along Span')

    return {'data': mpld3.fig_to_dict(fig), 'error': None}


def nth_point_shear(span_length, num_points, incr, impact_factor, dist_factor):

    #Check input types
    if (type(span_length) is str or type(num_points) is not int or type(incr)\
        is str or type(impact_factor) is str or type(dist_factor) is str):
        return {'data': None, 'error': 'Invalid input. Try again.'}

    n = num_points

    x_locs = [i*span_length/n for i in range(n+1)]

    # Cooper E-80 Axle Layout
    axle_loads = [40, 80, 80, 80, 80, 52, 52, 52, 52,
                  40, 80, 80, 80, 80, 52, 52, 52, 52,
                  8]

    axle_spaces = [0, 8, 5, 5, 5, 9, 5, 6, 5,
                   8, 8, 5, 5, 5, 9, 5, 6, 5,
                   5.5]
    train_len = sum(axle_spaces)
    while (sum(axle_spaces) - train_len) < span_length:
        axle_spaces.append(1)
        axle_loads.append(8)

    num_axles = len(axle_loads)

    train_tot = sum(axle_spaces)
    # Initialize train positions array
    positions = []
    point = -span_length
    while point <= train_tot:
        positions.append(point)
        point += incr

    # Initialize arrays to hold total moment and shear values.
    # These arrays will be used to store the moment and shear values per
    # position of the train. We will run the "max" function to find max
    # values in these arrays
    v_maxs = []

    for loc in x_locs:
        v_array = []

        for i in range(len(positions)):
            # a and b arrays store a and b values or each axle
            # r1 and r2 arrays store reactions at ends 1 and 2 for each axle
            # m and v arrays store m and v caused by each axle
            a = []
            b = []
            r1 = []
            v = []

            # This loop calculates individual values for each of the above
            # arrays and appends each value to the array.
            for j in range(num_axles):
                a_val = span_length + positions[i] - sum(axle_spaces[:j+1])
                a.append(a_val)

                b_val = span_length - a_val
                b.append(b_val)

                if 0 < b_val < span_length and a_val < loc:
                    v_val = axle_loads[j]
                else:
                    v_val = 0
                v.append(v_val)

                if 0 < b_val < span_length:
                    r1_val = axle_loads[j]*b_val/span_length
                else:
                    r1_val = 0
                r1.append(r1_val)

            # Calculate the moment and shear at the respective x location
            # caused by the train at position i and push these values to the
            # global moment and shear arrays
            v_tot = abs(sum(r1) - sum(v))
            v_array.append(v_tot)

        # Find max and position of train to cause max
        v_max = max(v_array)
        v_max = v_max*(1 + impact_factor)*dist_factor
        v_maxs.append(v_max)

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)

    ax.plot(x_locs, v_maxs, 'r')
    ax.set_ylabel('Maximum Shear, kips')
    ax.set_xlabel('Span Position, ft')
    ax.set_title('Maximum Shear at '+str(n)+'th Points Along Span')

    return {'data': mpld3.fig_to_dict(fig), 'error': None}
