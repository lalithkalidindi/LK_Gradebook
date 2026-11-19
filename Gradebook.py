# Gradebook Manager

# Data storage
gradebook = {}      # {student: {assignment: raw_score or None}}
assignments = {}    # {assignment: max_score}

# Grading scale (checked from highest to lowest)
grading_scale = {
    'A+': 98.0, 'A': 93.0, 'A-': 90.0,
    'B+': 87.0, 'B': 83.0, 'B-': 80.0,
    'C+': 77.0, 'C': 73.0, 'C-': 70.0,
    'D+': 67.0, 'D': 63.0, 'D-': 60.0,
    'F': 0.0,  # Anything below 60 is an F
}


def convert_to_letter_grade(percent):
    for grade, threshold in grading_scale.items():
        if percent >= threshold:
            return grade
    return 'F'


def to_percent(assignment_name, score):
    return score / assignments[assignment_name] * 100


# 1. Add a student
def add_student(student_name):
    if student_name in gradebook:
        print(f"{student_name} already exists in the gradebook.")
        return
    # New students get every existing assignment, ungraded
    gradebook[student_name] = {a: None for a in assignments}
    print(f"{student_name} has been added.")


# 2. Remove a student
def remove_student(student_name):
    if student_name in gradebook:
        del gradebook[student_name]
        print(f"{student_name} has been removed.")
    else:
        print(f"{student_name} does not exist in the gradebook.")


# 3. Add an assignment for all students
def add_assignment(assignment_name, max_score):
    if assignment_name in assignments:
        print(f"Assignment '{assignment_name}' already exists.")
        return
    if max_score <= 0:
        print("Max score must be greater than 0.")
        return
    assignments[assignment_name] = max_score
    for student in gradebook:
        gradebook[student][assignment_name] = None
    print(f"Assignment '{assignment_name}' has been added with a max score of {max_score}.")


# 4. Enter grade for a student
def enter_grade(student_name, assignment_name, score):
    if student_name not in gradebook:
        print(f"Error: student '{student_name}' does not exist.")
    elif assignment_name not in assignments:
        print(f"Error: assignment '{assignment_name}' does not exist.")
    elif not 0 <= score <= assignments[assignment_name]:
        print(f"Error: score must be between 0 and {assignments[assignment_name]}.")
    else:
        gradebook[student_name][assignment_name] = score
        print(f"Grade of {score} has been entered for {student_name} on '{assignment_name}'.")


# 5. Student average (as a percentage across graded assignments)
def calculate_student_average(student_name, verbose=True):
    if student_name not in gradebook:
        if verbose:
            print(f"{student_name} does not exist.")
        return None
    percents = [to_percent(a, s) for a, s in gradebook[student_name].items() if s is not None]
    if not percents:
        if verbose:
            print(f"{student_name} has no grades entered yet.")
        return None
    average = sum(percents) / len(percents)
    if verbose:
        print(f"{student_name}'s average grade is {average:.2f}% ({convert_to_letter_grade(average)})")
    return average


# 6. Class average for an assignment (as a percentage)
def calculate_assignment_average(assignment_name):
    if assignment_name not in assignments:
        print(f"Assignment '{assignment_name}' does not exist.")
        return None
    percents = [to_percent(assignment_name, g[assignment_name])
                for g in gradebook.values() if g.get(assignment_name) is not None]
    if not percents:
        print(f"No grades entered for '{assignment_name}'.")
        return None
    average = sum(percents) / len(percents)
    print(f"The class average for '{assignment_name}' is {average:.2f}%")
    return average


# 7. Student report
def display_student_report(student_name):
    if student_name not in gradebook:
        print(f"{student_name} does not exist.")
        return
    print(f"\nReport for {student_name}:")
    for assignment, score in gradebook[student_name].items():
        if score is None:
            print(f"{assignment}: No grade entered")
        else:
            pct = to_percent(assignment, score)
            print(f"{assignment}: {score}/{assignments[assignment]} "
                  f"({pct:.1f}%, {convert_to_letter_grade(pct)})")


# 8. All students' grades on one assignment
def display_class_grades(assignment_name):
    if assignment_name not in assignments:
        print(f"Assignment '{assignment_name}' does not exist.")
        return
    print(f"\nGrades for '{assignment_name}':")
    for student, graded in gradebook.items():
        score = graded.get(assignment_name)
        if score is None:
            print(f"{student}: No grade entered")
        else:
            pct = to_percent(assignment_name, score)
            print(f"{student}: {score}/{assignments[assignment_name]} "
                  f"({pct:.1f}%, {convert_to_letter_grade(pct)})")


# 9. Top student
def top_student():
    best_name, best_avg = None, None
    for student in gradebook:
        avg = calculate_student_average(student, verbose=False)
        if avg is not None and (best_avg is None or avg > best_avg):
            best_name, best_avg = student, avg
    if best_name:
        print(f"The top student is {best_name} with an average of "
              f"{best_avg:.2f}% ({convert_to_letter_grade(best_avg)})")
    else:
        print("No grades available to determine the top student.")


# 10. Failing students (average below 60%)
def failing_students():
    print("\nFailing Students (Average below 60%):")
    found = False
    for student in gradebook:
        avg = calculate_student_average(student, verbose=False)
        if avg is not None and avg < 60:
            found = True
            print(f"{student} with an average of {avg:.2f}% ({convert_to_letter_grade(avg)})")
    if not found:
        print("None.")


def read_number(prompt):
    """Prompt until the user enters a valid number."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a valid number.")


def menu():
    while True:
        print("\nGradebook Manager")
        print("1. Add Student")
        print("2. Remove Student")
        print("3. Add Assignment")
        print("4. Enter Grade")
        print("5. Calculate Student Average")
        print("6. Calculate Class Average for Assignment")
        print("7. Display Student Report")
        print("8. Display Class Grades")
        print("9. Identify Top Student")
        print("10. Show Failing Students")
        print("11. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            add_student(input("Enter student name: ").strip())
        elif choice == "2":
            remove_student(input("Enter student name: ").strip())
        elif choice == "3":
            name = input("Enter assignment name: ").strip()
            add_assignment(name, read_number("Enter max score for the assignment: "))
        elif choice == "4":
            student = input("Enter student name: ").strip()
            assignment = input("Enter assignment name: ").strip()
            enter_grade(student, assignment, read_number("Enter grade: "))
        elif choice == "5":
            calculate_student_average(input("Enter student name: ").strip())
        elif choice == "6":
            calculate_assignment_average(input("Enter assignment name: ").strip())
        elif choice == "7":
            display_student_report(input("Enter student name: ").strip())
        elif choice == "8":
            display_class_grades(input("Enter assignment name: ").strip())
        elif choice == "9":
            top_student()
        elif choice == "10":
            failing_students()
        elif choice == "11":
            print("Exiting Gradebook Manager.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    menu()