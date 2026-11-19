"""3x3 matrix operations implemented with Python lists only."""
SIZE = 3

def validate(matrix):
    if len(matrix) != SIZE or any(len(row) != SIZE for row in matrix):
        raise ValueError("A matrix must contain exactly 3 rows and 3 columns.")
    return [[float(x) for x in row] for row in matrix]

def add(a, b):
    a, b = validate(a), validate(b)
    return [[a[i][j] + b[i][j] for j in range(SIZE)] for i in range(SIZE)]

def subtract(a, b):
    a, b = validate(a), validate(b)
    return [[a[i][j] - b[i][j] for j in range(SIZE)] for i in range(SIZE)]

def multiply(a, b):
    a, b = validate(a), validate(b)
    return [[sum(a[i][k] * b[k][j] for k in range(SIZE))
             for j in range(SIZE)] for i in range(SIZE)]

def transpose(a):
    a = validate(a)
    return [[a[j][i] for j in range(SIZE)] for i in range(SIZE)]

def determinant(a):
    a = validate(a)
    return (a[0][0] * (a[1][1]*a[2][2] - a[1][2]*a[2][1])
          - a[0][1] * (a[1][0]*a[2][2] - a[1][2]*a[2][0])
          + a[0][2] * (a[1][0]*a[2][1] - a[1][1]*a[2][0]))

def inverse(a):
    a = validate(a)
    det = determinant(a)
    if abs(det) < 1e-10:
        raise ValueError("Inverse does not exist: determinant is zero.")
    cof = [[0.0]*SIZE for _ in range(SIZE)]
    for i in range(SIZE):
        for j in range(SIZE):
            minor = [ [a[r][c] for c in range(SIZE) if c != j]
                      for r in range(SIZE) if r != i ]
            cof[i][j] = ((-1)**(i+j)) * (
                minor[0][0]*minor[1][1] - minor[0][1]*minor[1][0])
    adj = transpose(cof)
    return [[adj[i][j]/det for j in range(SIZE)] for i in range(SIZE)]

def scalar_multiply(a, scalar):
    a = validate(a)
    return [[x * float(scalar) for x in row] for row in a]

def trace(a):
    a = validate(a)
    return sum(a[i][i] for i in range(SIZE))
