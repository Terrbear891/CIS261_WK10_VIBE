#Terrah Benjamin
#CIS261
#WK10 VIBE Coding
"""Student Grade Calculator.

Data structure choice: Option B, a Student class.
"""

from dataclasses import dataclass
import os
import sys


FILE_NAME = "student_grades.txt"


@dataclass
class Student:
	"""Store one student's scores and calculated grade information."""

	name: str
	student_id: str
	test1: float
	test2: float
	test3: float

	def __post_init__(self):
		self.average = (self.test1 + self.test2 + self.test3) / 3
		self.grade = calculate_letter_grade(self.average)

	def to_file_line(self):
		return (
			f"{self.name}|{self.student_id}|{self.test1:.2f}|"
			f"{self.test2:.2f}|{self.test3:.2f}|{self.average:.2f}|{self.grade}\n"
		)


def calculate_letter_grade(average):
	"""Return the letter grade for an average score."""
	if average >= 90:
		return "A"
	if average >= 80:
		return "B"
	if average >= 70:
		return "C"
	if average >= 60:
		return "D"
	return "F"


def load_students():
	"""Load student records from the pipe-delimited data file."""
	students = []
	if not os.path.exists(FILE_NAME):
		return students

	try:
		with open(FILE_NAME, "r", encoding="utf-8") as file:
			for line_number, line in enumerate(file, start=1):
				parts = line.rstrip("\n").split("|")
				if len(parts) != 7:
					print(f"Skipped invalid record on line {line_number}.")
					continue
				try:
					student = Student(
						parts[0],
						parts[1],
						float(parts[2]),
						float(parts[3]),
						float(parts[4]),
					)
					students.append(student)
				except ValueError:
					print(f"Skipped invalid scores on line {line_number}.")
	except OSError as error:
		print(f"Unable to load {FILE_NAME}: {error}")
	return students


def save_students(students):
	"""Save all student records to the data file."""
	try:
		with open(FILE_NAME, "w", encoding="utf-8") as file:
			for student in students:
				file.write(student.to_file_line())
		return True
	except OSError as error:
		print(f"Unable to save {FILE_NAME}: {error}")
		return False


def get_score(test_number):
	"""Prompt until a valid score from 0 through 100 is entered."""
	while True:
		try:
			score = float(input(f"Test {test_number} score (0-100): "))
			if 0 <= score <= 100:
				return score
			print("Please enter a score from 0 through 100.")
		except ValueError:
			print("Please enter a valid number.")


def add_student(students):
	"""Prompt for and add one student record."""
	print("\nAdd Student")
	name = input("Student name: ").strip()
	student_id = input("Student ID: ").strip()
	if not name or not student_id:
		print("Name and student ID cannot be blank.")
		return

	scores = [get_score(number) for number in range(1, 4)]
	student = Student(name, student_id, *scores)
	students.append(student)
	if save_students(students):
		print(f"Added {student.name} with an average of {student.average:.2f} ({student.grade}).")


def display_students(students):
	"""Display all student records in a formatted table."""
	if not students:
		print("\nNo student records found.")
		return

	print("\nStudent Records")
	print("-" * 88)
	print(f"{'Name':<22}{'ID':<14}{'Test 1':>10}{'Test 2':>10}{'Test 3':>10}{'Average':>10}{'Grade':>8}")
	print("-" * 88)
	for student in students:
		print(
			f"{student.name:<22.22}{student.student_id:<14.14}"
			f"{student.test1:>10.2f}{student.test2:>10.2f}"
			f"{student.test3:>10.2f}{student.average:>10.2f}{student.grade:>8}"
		)
	print("-" * 88)


def display_statistics(students):
	"""Display the highest, lowest, and class average scores."""
	if not students:
		print("\nNo student records available for statistics.")
		return

	averages = [student.average for student in students]
	highest = max(students, key=lambda student: student.average)
	lowest = min(students, key=lambda student: student.average)
	print("\nClass Statistics")
	print(f"Highest average: {highest.average:.2f} ({highest.name})")
	print(f"Lowest average:  {lowest.average:.2f} ({lowest.name})")
	print(f"Class average:   {sum(averages) / len(averages):.2f}")


def search_student(students):
	"""Search for students by name without regard to letter case."""
	search_name = input("\nEnter a student name to search: ").strip().lower()
	matches = [student for student in students if search_name in student.name.lower()]
	if matches:
		display_students(matches)
	else:
		print("No matching student found.")


def get_menu_choice():
	"""Read a menu choice, including ESC followed by Enter as an exit."""
	return input(
		"\nChoose an option (1-5), or press ESC then Enter to exit: "
	).strip()


def main():
	"""Run the student grade calculator menu."""
	students = load_students()
	print("Student Grade Calculator")
	print(f"Loaded {len(students)} student record(s).")

	while True:
		print("\n1. Add a student")
		print("2. Display all students")
		print("3. Display class statistics")
		print("4. Search by student name")
		print("5. Save records")
		choice = get_menu_choice()

		if choice in ("\x1b", "esc", "ESC"):
			save_students(students)
			print("Records saved. Goodbye!")
			return
		if choice == "1":
			add_student(students)
		elif choice == "2":
			display_students(students)
		elif choice == "3":
			display_statistics(students)
		elif choice == "4":
			search_student(students)
		elif choice == "5":
			if save_students(students):
				print("Student records saved successfully.")
		else:
			print("Invalid choice. Please select an option from 1 through 5.")


if __name__ == "__main__":
	main()