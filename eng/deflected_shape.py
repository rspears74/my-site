import numpy

x = [0, 10, 20]
defl = [0, -0.313262, 0]
rot = [0, -7.60345e-04, 3.95379e-02]

def main(data):

    x = data['x']
    defl = data['defl']
    rot = data['rot']

    n = len(x)

    coefs = []
    x_vals = []
    y_vals = []
    for i in range(n-1):
        A = []
        y = []
        coef = []

        val = x[i]
        A_line = [val**3, val**2, val, 1]
        A.append(A_line)

        A_line = [3*val**2, 2*val, 1, 0]
        A.append(A_line)

        val = x[i+1]
        A_line = [val**3, val**2, val, 1]
        A.append(A_line)

        A_line = [3*val**2, 2*val, 1, 0]
        A.append(A_line)

        val = defl[i]
        y.append([val])

        val = rot[i]
        y.append([val])

        val = defl[i+1]
        y.append([val])

        val = rot[i+1]
        y.append([val])

        A = numpy.asarray(A)
        y = numpy.asarray(y)


        coef = numpy.linalg.solve(A.transpose().dot(A), A.transpose().dot(y))
        coefs.append(coef)

        xs = list(range(x[i], x[i+1]+1, 1))
        ys = []
        for x_val in xs:
            ys.append(coef[0,0]*x_val**3+coef[1,0]*x_val**2+coef[2,0]*x_val+coef[3,0])
        x_vals.append(xs)
        y_vals.append(ys)

    return {
        'x': x_vals,
        'y': y_vals
    }
