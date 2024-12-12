import csv
from typing import List
import tkinter as tk
from tkinter import ttk, messagebox

def calculate_grade(score: float, best_score: float) -> str:
    """Calculates the grade based on the score and the best score."""
    if score >= best_score - 10:
        return 'A'
    elif score >= best_score - 20:
        return 'B'
    elif score >= best_score - 30:
        return 'C'
    elif score >= best_score - 40:
        return 'D'
    else:
        return 'F'

def calculate_average(scores: List[float]) -> float:
    """Calculates the average of a list of scores."""
    return sum(scores) / len(scores)

class StudentGradeManager:
    def __init__(self, csv_file: str = "grades.csv"):
        self.csv_file = csv_file
        self.headers = ["Name", "Test Scores", "Lowest", "Highest", "Average", "Final Grade"]
        self._initialize_csv()

    def _initialize_csv(self):
        """Initializes the CSV file with headers if it does not exist."""
        try:
            with open(self.csv_file, mode="x", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(self.headers)
        except FileExistsError:
            pass

    def add_student(self, name: str, scores: List[float]):
        """Adds a student's grades to the CSV file."""
        if not scores:
            raise ValueError("Scores list cannot be empty.")

        lowest = min(scores)
        highest = max(scores)
        average = calculate_average(scores)
        final_grade = calculate_grade(average, highest)

        with open(self.csv_file, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                name,
                ", ".join(map(str, scores)),
                f"{lowest:.2f}",
                f"{highest:.2f}",
                f"{average:.2f}",
                final_grade
            ])

    def display_grades(self):
        """Returns all grades from the CSV file as a list of rows."""
        with open(self.csv_file, mode="r") as file:
            reader = csv.reader(file)
            return list(reader)

class GradeManagerApp:
    def __init__(self, root):
        self.manager = StudentGradeManager()
        self.root = root
        self.root.title("Grade Manager")
        self.attempts = 0  # Track invalid attempts
        self.max_attempts = 4  # Maximum allowed attempts
        self.create_widgets()

    def create_widgets(self):
        """Creates the GUI components."""
        input_frame = ttk.LabelFrame(self.root, text="Add Student")
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ttk.Label(input_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.name_entry = ttk.Entry(input_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Scores (comma-separated):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.scores_entry = ttk.Entry(input_frame, width=30)
        self.scores_entry.grid(row=1, column=1, padx=5, pady=5)

        add_button = ttk.Button(input_frame, text="Add Student", command=self.add_student)
        add_button.grid(row=2, column=0, columnspan=2, pady=10)

        grades_frame = ttk.LabelFrame(self.root, text="Student Grades")
        grades_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.grades_tree = ttk.Treeview(grades_frame, columns=self.manager.headers, show="headings")
        for header in self.manager.headers:
            self.grades_tree.heading(header, text=header)
            self.grades_tree.column(header, width=100)
        self.grades_tree.pack(fill="both", expand=True)

        view_button = ttk.Button(self.root, text="View Grades", command=self.view_grades)
        view_button.grid(row=2, column=0, pady=10)

    def add_student(self):
        if self.attempts >= self.max_attempts:
            messagebox.showerror("Error", "Maximum attempts reached. Please restart the application.")
            return

        name = self.name_entry.get().strip()
        scores_input = self.scores_entry.get().strip()

        if not name:
            messagebox.showerror("Error", "Name cannot be empty.")
            self.attempts += 1
            return

        try:
            scores = list(map(float, scores_input.split(",")))
            if any(score < 0 or score > 100 for score in scores):
                raise ValueError("Scores must be between 0 and 100.")

            self.manager.add_student(name, scores)
            messagebox.showinfo("Success", f"Grades for {name} added successfully.")
            self.name_entry.delete(0, tk.END)
            self.scores_entry.delete(0, tk.END)
            self.attempts = 0  
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            self.attempts += 1

    def view_grades(self):
        for row in self.grades_tree.get_children():
            self.grades_tree.delete(row)

        grades = self.manager.display_grades()
        for grade_row in grades:
            self.grades_tree.insert("", tk.END, values=grade_row)

def main():
    root = tk.Tk()
    app = GradeManagerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
