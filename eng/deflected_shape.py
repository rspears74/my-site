import numpy

x = [0, 10, 20]
defl = [0, -0.313262, 0]
rot = [0, -7.60345e-04, 3.95379e-02]

A = []
for val in x:
    A_line = [val**4, val**3, val**2, val, 1]
    A.append(A_line)

for val in x:
    A_line = [4*val**3, 3*val**2, 2*val, 1, 0]
    A.append(A_line)

y = []
for val in defl:
    y.append([val])

for val in rot:
    y.append([val])

A = numpy.asarray(A)
y = numpy.asarray(y)


coefs = numpy.linalg.solve(A.transpose().dot(A), A.transpose().dot(y))
print(coefs)
