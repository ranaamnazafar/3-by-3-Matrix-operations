
import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkfont
import math

# =========================================
# NUMBER FORMATTING
# =========================================

def format_number(value):

    value = round(float(value), 6)

    if abs(value) < 0.000001:
        value = 0

    if value == int(value):
        return str(int(value))

    return f"{value:.6f}".rstrip("0").rstrip(".")

# =========================================
# PURE PYTHON MATRIX OPERATIONS
# =========================================

def add(a, b):
    return [
        [a[i][j] + b[i][j] for j in range(3)]
        for i in range(3)
    ]

def subtract(a, b):
    return [
        [a[i][j] - b[i][j] for j in range(3)]
        for i in range(3)
    ]

def multiply(a, b):

    result = []

    for i in range(3):

        row = []

        for j in range(3):

            value = 0

            for k in range(3):
                value += a[i][k] * b[k][j]

            row.append(value)

        result.append(row)

    return result

def transpose(a):
    return [
        [a[j][i] for j in range(3)]
        for i in range(3)
    ]

def determinant(a):

    return (
        a[0][0] * (
            a[1][1] * a[2][2]
            - a[1][2] * a[2][1]
        )
        - a[0][1] * (
            a[1][0] * a[2][2]
            - a[1][2] * a[2][0]
        )
        + a[0][2] * (
            a[1][0] * a[2][1]
            - a[1][1] * a[2][0]
        )
    )

def inverse(a):

    det = determinant(a)

    if abs(det) < 1e-10:
        raise ValueError(
            "Inverse does not exist because determinant is zero."
        )

    cofactors = []

    for i in range(3):

        row = []

        for j in range(3):

            minor = [
                [a[r][c] for c in range(3) if c != j]
                for r in range(3) if r != i
            ]

            value = (
                minor[0][0] * minor[1][1]
                - minor[0][1] * minor[1][0]
            )

            if (i + j) % 2 != 0:
                value = -value

            row.append(value)

        cofactors.append(row)

    adjoint = transpose(cofactors)

    return [
        [adjoint[i][j] / det for j in range(3)]
        for i in range(3)
    ]

def scalar_multiply(a, scalar):

    return [
        [a[i][j] * scalar for j in range(3)]
        for i in range(3)
    ]

def trace(a):

    return a[0][0] + a[1][1] + a[2][2]

# =========================================
# MATRIX CALCULATOR GUI
# =========================================

class MatrixApp:

    def __init__(self, root):

        self.root = root
        self.root.title("Matrix Calculator | Pure Python")
        self.root.configure(bg="#080B10")
        self.root.geometry("1100x760")
        self.root.minsize(850, 650)

        try:
            self.root.state("zoomed")
        except tk.TclError:
            pass

        # COLORS

        self.bg = "#080B10"
        self.panel = "#121A24"
        self.card = "#192532"
        self.green = "#00E5A0"
        self.blue = "#00C2FF"
        self.white = "#FFFFFF"
        self.gray = "#94A3B8"
        self.red = "#FF4757"

        self.current_result = None
        self.current_operation = None
        self.welcome = True

        # MAIN FRAME

        main = tk.Frame(root, bg=self.bg)

        main.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=5
        )

        # =====================================
        # HEADER
        # =====================================

        tk.Label(
            main,
            text="MATRIX CALCULATOR",
            font=("Arial", 25, "bold"),
            bg=self.bg,
            fg=self.green
        ).pack(pady=(3, 0))

        tk.Label(
            main,
            text="ADVANCED 3 x 3 MATRIX OPERATIONS | PURE PYTHON",
            font=("Arial", 10, "bold"),
            bg=self.bg,
            fg=self.gray
        ).pack(pady=(2, 6))

        # =====================================
        # MATRIX INPUT AREA
        # =====================================

        matrix_area = tk.Frame(main, bg=self.bg)
        matrix_area.pack(fill="x", pady=4)

        self.entries = []

        for name in ["MATRIX A", "MATRIX B"]:

            frame = tk.LabelFrame(
                matrix_area,
                text=name,
                font=("Arial", 12, "bold"),
                bg=self.panel,
                fg=self.green,
                padx=10,
                pady=6,
                bd=1,
                relief="solid"
            )

            frame.pack(
                side="left",
                expand=True,
                fill="both",
                padx=8
            )

            grid = []

            for i in range(3):

                row = []

                for j in range(3):

                    entry = tk.Entry(
                        frame,
                        width=9,
                        font=("Arial", 12, "bold"),
                        justify="center",
                        bg=self.bg,
                        fg=self.green,
                        insertbackground=self.green,
                        relief="flat"
                    )

                    entry.grid(
                        row=i,
                        column=j,
                        padx=5,
                        pady=4,
                        ipady=3
                    )

                    row.append(entry)

                grid.append(row)

            self.entries.append(grid)

        # =====================================
        # SCALAR INPUT
        # =====================================

        scalar_frame = tk.Frame(main, bg=self.bg)
        scalar_frame.pack(pady=5)

        tk.Label(
            scalar_frame,
            text="SCALAR VALUE:",
            font=("Arial", 11, "bold"),
            bg=self.bg,
            fg=self.gray
        ).pack(side="left", padx=8)

        self.scalar = tk.Entry(
            scalar_frame,
            width=10,
            font=("Arial", 12, "bold"),
            justify="center",
            bg=self.panel,
            fg=self.green,
            insertbackground=self.green,
            relief="flat"
        )

        self.scalar.pack(side="left", ipady=4)
        self.scalar.insert(0, "2")

        # =====================================
        # OPERATIONS HEADING
        # =====================================

        tk.Label(
            main,
            text="SELECT OPERATION",
            font=("Arial", 14, "bold"),
            bg=self.bg,
            fg=self.white
        ).pack(pady=4)

        # =====================================
        # OPERATION BUTTONS
        # =====================================

        button_frame = tk.Frame(main, bg=self.bg)
        button_frame.pack(pady=3)

        operations = [
            ("ADDITION", "add"),
            ("SUBTRACTION", "subtract"),
            ("MULTIPLICATION", "multiply"),
            ("TRANSPOSE", "transpose"),
            ("DETERMINANT", "determinant"),
            ("INVERSE", "inverse"),
            ("SCALAR MULTIPLY", "scalar"),
            ("TRACE", "trace")
        ]

        for index, (label, operation) in enumerate(operations):

            btn = tk.Button(
                button_frame,
                text=label,
                font=("Arial", 9, "bold"),
                bg=self.card,
                fg=self.green,
                activebackground=self.green,
                activeforeground=self.bg,
                width=19,
                height=2,
                bd=0,
                cursor="hand2",
                command=lambda op=operation: self.calculate(op)
            )

            btn.grid(
                row=index // 4,
                column=index % 4,
                padx=5,
                pady=3
            )

            btn.bind(
                "<Enter>",
                lambda e, b=btn: b.config(
                    bg=self.green,
                    fg=self.bg
                )
            )

            btn.bind(
                "<Leave>",
                lambda e, b=btn: b.config(
                    bg=self.card,
                    fg=self.green
                )
            )

        # =====================================
        # CONTROL BUTTONS
        # =====================================

        control = tk.Frame(main, bg=self.bg)
        control.pack(pady=5)

        tk.Button(
            control,
            text="LOAD SAMPLE DATA",
            font=("Arial", 10, "bold"),
            bg=self.blue,
            fg=self.bg,
            width=19,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.sample_data
        ).pack(side="left", padx=7)

        tk.Button(
            control,
            text="CLEAR ALL",
            font=("Arial", 10, "bold"),
            bg=self.red,
            fg=self.white,
            width=15,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.clear_all
        ).pack(side="left", padx=7)

        # =====================================
        # RESULT DASHBOARD
        # =====================================

        result_frame = tk.LabelFrame(
            main,
            text="  CALCULATION RESULT  ",
            font=("Arial", 13, "bold"),
            bg=self.panel,
            fg=self.green,
            bd=1,
            relief="solid",
            padx=10,
            pady=5
        )

        result_frame.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=5
        )

        # RESULT STATUS

        self.result_title = tk.Label(
            result_frame,
            text="READY TO CALCULATE",
            font=("Arial", 11, "bold"),
            bg=self.panel,
            fg=self.blue
        )

        self.result_title.pack(
            anchor="w",
            pady=4
        )

        # CANVAS RESULT DISPLAY

        self.result_canvas = tk.Canvas(
            result_frame,
            bg=self.bg,
            highlightthickness=0,
            height=190
        )

        self.result_canvas.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=3
        )

        self.result_canvas.bind(
            "<Configure>",
            lambda event: self.render_result()
        )

        self.show_welcome()

        # =====================================
        # FOOTER
        # =====================================

        tk.Label(
            main,
            text="PYTHON PROJECT | PURE PYTHON MATRIX CALCULATOR",
            font=("Arial", 9, "bold"),
            bg=self.bg,
            fg=self.gray
        ).pack(pady=2)

    # =====================================
    # RENDER RESULT ON CANVAS
    # =====================================

    def render_result(self):

        canvas = self.result_canvas
        canvas.delete("all")

        width = canvas.winfo_width()
        height = canvas.winfo_height()

        if width < 100 or height < 80:
            return

        center_x = width / 2
        center_y = height / 2

        # WELCOME MESSAGE

        if self.welcome:

            canvas.create_text(
                center_x,
                center_y - 20,
                text="WELCOME TO MATRIX CALCULATOR!",
                fill=self.blue,
                font=("Arial", 14, "bold")
            )

            canvas.create_text(
                center_x,
                center_y + 15,
                text="Enter matrix values and select an operation.",
                fill=self.gray,
                font=("Arial", 10)
            )

            return

        # RESULT HEADING

        canvas.create_text(
            center_x,
            center_y - 65,
            text="RESULT MATRIX",
            fill=self.blue,
            font=("Arial", 12, "bold")
        )

        result = self.current_result

        # =====================================
        # MATRIX RESULT
        # =====================================

        if (
            isinstance(result, (list, tuple))
            and len(result) > 0
            and isinstance(result[0], (list, tuple))
        ):

            formatted = [
                [format_number(x) for x in row]
                for row in result
            ]

            rows = len(formatted)
            cols = len(formatted[0])

            if any(len(row) != cols for row in formatted):
                return

            # FONT SIZE

            font_size = 19

            matrix_font = tkfont.Font(
                family="Consolas",
                size=font_size,
                weight="bold"
            )

            widths = []

            for j in range(cols):

                max_width = max(
                    matrix_font.measure(formatted[i][j])
                    for i in range(rows)
                )

                widths.append(max_width + 12)

            gap = 12

            total_width = sum(widths) + gap * (cols - 1)

            # FIT MATRIX TO CANVAS

            while (
                total_width + 70 > width
                and font_size > 9
            ):

                font_size -= 1

                matrix_font = tkfont.Font(
                    family="Consolas",
                    size=font_size,
                    weight="bold"
                )

                widths = []

                for j in range(cols):

                    max_width = max(
                        matrix_font.measure(formatted[i][j])
                        for i in range(rows)
                    )

                    widths.append(max_width + 12)

                total_width = sum(widths) + gap * (cols - 1)

            # MATRIX POSITION

            matrix_left = center_x - total_width / 2
            matrix_top = center_y - 35

            row_gap = min(
                38,
                max(25, (height - 75) / max(rows, 1))
            )

            matrix_height = row_gap * (rows - 1)

            top = matrix_top - 12
            bottom = matrix_top + matrix_height + 12

            left_x = matrix_left - 15
            right_x = matrix_left + total_width + 15

            # =================================
            # ONE CONTINUOUS LEFT BRACKET [
            # =================================

            canvas.create_line(
                left_x + 12, top,
                left_x, top,
                left_x, bottom,
                left_x + 12, bottom,
                fill=self.green,
                width=3,
                capstyle=tk.PROJECTING,
                joinstyle=tk.MITER
            )

            # =================================
            # ONE CONTINUOUS RIGHT BRACKET ]
            # =================================

            canvas.create_line(
                right_x - 12, top,
                right_x, top,
                right_x, bottom,
                right_x - 12, bottom,
                fill=self.green,
                width=3,
                capstyle=tk.PROJECTING,
                joinstyle=tk.MITER
            )

            # =================================
            # MATRIX VALUES
            # =================================

            x_position = matrix_left

            column_centers = []

            for j in range(cols):

                column_centers.append(
                    x_position + widths[j] / 2
                )

                x_position += widths[j] + gap

            for i in range(rows):

                y_position = matrix_top + i * row_gap

                for j in range(cols):

                    canvas.create_text(
                        column_centers[j],
                        y_position,
                        text=formatted[i][j],
                        fill=self.green,
                        font=matrix_font
                    )

        # =====================================
        # SINGLE VALUE RESULT
        # =====================================

        else:

            canvas.create_text(
                center_x,
                center_y + 10,
                text=format_number(result),
                fill=self.green,
                font=("Consolas", 24, "bold")
            )

    # =====================================
    # SHOW WELCOME
    # =====================================

    def show_welcome(self):

        self.welcome = True
        self.current_result = None
        self.current_operation = None

        self.render_result()

    # =====================================
    # GET MATRIX INPUT
    # =====================================

    def get_matrix(self, index):

        matrix = []

        for row in self.entries[index]:

            values = []

            for entry in row:

                value = entry.get().strip()

                if value == "":
                    raise ValueError(
                        "Please enter all 9 matrix values."
                    )

                number = float(value)

                if not math.isfinite(number):
                    raise ValueError(
                        "Please enter valid finite numbers."
                    )

                values.append(number)

            matrix.append(values)

        return matrix

    # =====================================
    # DISPLAY RESULT
    # =====================================

    def display_result(self, result, operation):

        if result is None:
            raise ValueError("No result returned.")

        self.welcome = False
        self.current_result = result
        self.current_operation = operation

        self.result_title.config(
            text=f"SUCCESSFULLY COMPLETED: {operation.upper()}",
            fg=self.green
        )

        self.render_result()

    # =====================================
    # CALCULATE OPERATIONS
    # =====================================

    def calculate(self, operation):

        try:

            a = self.get_matrix(0)

            if operation in [
                "add",
                "subtract",
                "multiply"
            ]:
                b = self.get_matrix(1)

            if operation == "add":
                result = add(a, b)

            elif operation == "subtract":
                result = subtract(a, b)

            elif operation == "multiply":
                result = multiply(a, b)

            elif operation == "transpose":
                result = transpose(a)

            elif operation == "determinant":
                result = determinant(a)

            elif operation == "inverse":
                result = inverse(a)

            elif operation == "scalar":

                scalar_value = self.scalar.get().strip()

                if not scalar_value:
                    raise ValueError(
                        "Please enter a scalar value."
                    )

                scalar_value = float(scalar_value)

                if not math.isfinite(scalar_value):
                    raise ValueError(
                        "Please enter a valid scalar value."
                    )

                result = scalar_multiply(a, scalar_value)

            elif operation == "trace":
                result = trace(a)

            else:
                raise ValueError("Invalid operation.")

            self.display_result(result, operation)

        except (ValueError, TypeError, OverflowError) as error:

            self.result_title.config(
                text="CALCULATION FAILED",
                fg=self.red
            )

            messagebox.showerror(
                "Calculation Error",
                str(error),
                parent=self.root
            )

        except Exception as error:

            self.result_title.config(
                text="CALCULATION FAILED",
                fg=self.red
            )

            messagebox.showerror(
                "Unexpected Error",
                str(error),
                parent=self.root
            )

    # =====================================
    # LOAD SAMPLE DATA
    # =====================================

    def sample_data(self):

        matrix_a = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]

        matrix_b = [
            [9, 8, 7],
            [6, 5, 4],
            [3, 2, 1]
        ]

        for index, matrix in enumerate(
            [matrix_a, matrix_b]
        ):

            for i in range(3):

                for j in range(3):

                    entry = self.entries[index][i][j]

                    entry.delete(0, "end")
                    entry.insert(0, str(matrix[i][j]))

        self.result_title.config(
            text="SAMPLE MATRICES LOADED",
            fg=self.blue
        )

        self.welcome = True
        self.current_result = None

        self.result_canvas.delete("all")

        self.result_canvas.create_text(
            self.result_canvas.winfo_width() / 2,
            self.result_canvas.winfo_height() / 2,
            text="SAMPLE DATA LOADED SUCCESSFULLY!",
            fill=self.green,
            font=("Arial", 12, "bold")
        )

    # =====================================
    # CLEAR ALL
    # =====================================

    def clear_all(self):

        for matrix in self.entries:

            for row in matrix:

                for entry in row:
                    entry.delete(0, "end")

        self.scalar.delete(0, "end")
        self.scalar.insert(0, "2")

        self.result_title.config(
            text="READY TO CALCULATE",
            fg=self.blue
        )

        self.show_welcome()

# =========================================
# RUN APPLICATION
# =========================================

if __name__ == "__main__":

    root = tk.Tk()

    app = MatrixApp(root)

    root.mainloop()