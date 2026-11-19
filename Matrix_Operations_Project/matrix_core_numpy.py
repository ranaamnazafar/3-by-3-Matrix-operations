"""3x3 matrix operations implemented with NumPy."""
import numpy as np

def validate(matrix):
    arr = np.array(matrix, dtype=float)
    if arr.shape != (3, 3):
        raise ValueError("A matrix must contain exactly 3 rows and 3 columns.")
    return arr

def add(a, b): return validate(a) + validate(b)
def subtract(a, b): return validate(a) - validate(b)
def multiply(a, b): return validate(a) @ validate(b)
def transpose(a): return validate(a).T
def determinant(a): return float(np.linalg.det(validate(a)))
def inverse(a):
    arr = validate(a)
    if abs(float(np.linalg.det(arr))) < 1e-10:
        raise ValueError("Inverse does not exist: determinant is zero.")
    return np.linalg.inv(arr)
def scalar_multiply(a, scalar): return validate(a) * float(scalar)
def trace(a): return float(np.trace(validate(a)))
