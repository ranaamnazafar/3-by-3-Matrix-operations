
"""Command-line interface: Pure Python version."""

import matrix_core_pure as m


# Function to input a 3x3 matrix
def read_matrix(label):

    print(f"\nEnter {label}, one row at a time (3 numbers separated by spaces):")

    rows = []

    for i in range(3):

        while True:

            try:
                row = [float(x) for x in input(f"Row {i+1}: ").split()]

                if len(row) != 3:
                    raise ValueError

                rows.append(row)
                break

            except ValueError:
                print("Please enter exactly three numeric values.")


    return rows


# Function to display results
def show(value):

    if isinstance(value, list):

        for row in value:
            print("  ".join(f"{x:10.3f}" for x in row))

    else:
        print(f"{value:.6f}")


# Main function
def main():

    print("\n3x3 MATRIX OPERATIONS — PURE PYTHON")

    print("\n1. Addition")
    print("2. Subtraction")
    print("3. Matrix Multiplication")
    print("4. Transpose")
    print("5. Determinant")
    print("6. Inverse")
    print("7. Scalar Multiplication")
    print("8. Trace")

    try:

        choice = int(input("\nChoose operation (1-8): "))

        a = read_matrix("Matrix A")

        if choice in (1, 2, 3):

            b = read_matrix("Matrix B")

            operations = {
                1: m.add,
                2: m.subtract,
                3: m.multiply
            }

            result = operations[choice](a, b)

        elif choice == 4:

            result = m.transpose(a)

        elif choice == 5:

            result = m.determinant(a)

        elif choice == 6:

            result = m.inverse(a)

        elif choice == 7:

            scalar = input("Enter scalar value: ")

            result = m.scalar_multiply(a, scalar)

        elif choice == 8:

            result = m.trace(a)

        else:

            raise ValueError("Please choose a number between 1 and 8.")


        print("\n========== RESULT ==========")

        show(result)

        print("============================")


    except (ValueError, KeyError) as e:

        print("\nError:", e)


# Program execution
if __name__ == "__main__":

    main()
