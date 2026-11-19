# 3x3 Matrix Operations Project

## Features
Four versions are included:
1. Pure Python CLI
2. NumPy CLI
3. Pure Python Tkinter GUI
4. NumPy Tkinter GUI

Operations: addition, subtraction, matrix multiplication, transpose, determinant, inverse, scalar multiplication, and trace.

## Requirements
- Python 3.9+
- Tkinter (usually included with standard Python)
- NumPy only for the NumPy versions

Install NumPy:
```bash
python -m pip install numpy
```

## Run from the project folder
```bash
cd src
python cli_pure.py
python cli_numpy.py
python gui_pure.py
python gui_numpy.py
```
The pure-Python versions do not require NumPy. Use numeric values in all 9 cells. The inverse is unavailable when determinant is zero.

## Suggested test matrices
A = [[1,2,3],[0,1,4],[5,6,0]]
B = [[2,0,1],[1,3,2],[4,1,0]]
