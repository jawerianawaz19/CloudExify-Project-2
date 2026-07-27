# grade_system.py
# CloudExify Python Internship - Month 1 Project 2 (With Bonus Features)

import csv
import os

SUBJECTS = ["Math", "Physics", "English", "Computer", "Urdu"]
PASS_MARK = 50

students = []
next_id = 1


def get_next_id():
    global next_id
    current = next_id
    next_id += 1
    return current


def get_grade_letter(avg):
    if avg >= 90:
        return "A"
    elif avg >= 80:
        return "B"
    elif avg >= 70:
        return "C"
    elif avg >= 60:
        return "D"
    elif avg >= PASS_MARK:
        return "E"
    else:
        return "F"


def add_student():
    print("\n--- ADD NEW STUDENT ---")
    name = input("Student Name: ").strip()
    if not name:
        print("Name cannot be empty!")
        return

    for s in students:
        if s["name"].lower() == name.lower():
            print(f"Student '{name}' already exists!")
            return

    grades = {}
    print(f"\nEnter grades for {name}:")
    for subject in SUBJECTS:
        while True:
            try:
                grade = float(input(f"  {subject}: "))
                if 0 <= grade <= 100:
                    grades[subject] = grade
                    break
                print("  Grade must be 0-100!")
            except ValueError:
                print("  Please enter a valid number!")

    student = {
        "id": get_next_id(),
        "name": name,
        "grades": grades
    }
    students.append(student)

    avg = sum(grades.values()) / len(grades)
    status = "PASS" if avg >= PASS_MARK else "FAIL"
    letter = get_grade_letter(avg)
    print(f"\nAdded {name} | Average: {avg:.1f} | Grade: {letter} | {status}")


def view_all_students():
    if not students:
        print("\nNo students yet!")
        return

    print("\n--- ALL STUDENTS ---")
    print(f"{'ID':<5}{'Name':<20}", end="")
    for sub in SUBJECTS:
        print(f"{sub[:5]:<7}", end="")
    print(f"{'Avg':<8}{'Grade':<7}{'Status'}")
    print("-" * 80)

    for s in students:
        avg = sum(s["grades"].values()) / len(s["grades"])
        status = "PASS" if avg >= PASS_MARK else "FAIL"
        letter = get_grade_letter(avg)
        print(f"{s['id']:<5}{s['name']:<20}", end="")
        for sub in SUBJECTS:
            grade = s["grades"].get(sub, 0)
            print(f"{grade:<7.1f}", end="")
        print(f"{avg:<8.1f}{letter:<7}{status}")


def class_report():
    if not students:
        print("\nNo students to report!")
        return

    ranked = []
    for s in students:
        avg = sum(s["grades"].values()) / len(s["grades"])
        ranked.append((s["name"], avg))

    ranked.sort(key=lambda x: x[1], reverse=True)

    all_avgs = [r[1] for r in ranked]
    class_avg = sum(all_avgs) / len(all_avgs)
    highest = max(all_avgs)
    lowest = min(all_avgs)
    passed = sum(1 for avg in all_avgs if avg >= PASS_MARK)
    failed = len(all_avgs) - passed

    print("\n=== CLASS REPORT ===")
    print(f"Total Students : {len(students)}")
    print(f"Class Average  : {class_avg:.2f}")
    print(f"Highest Average: {highest:.2f}")
    print(f"Lowest Average : {lowest:.2f}")
    print(f"Passed         : {passed}")
    print(f"Failed         : {failed}")

    print("\n--- RANKINGS ---")
    for rank, (name, avg) in enumerate(ranked, 1):
        letter = get_grade_letter(avg)
        print(f"  {rank}. {name:<20} {avg:.2f}  ({letter})")

    # BONUS: subject-wise class average
    print("\n--- SUBJECT-WISE CLASS AVERAGE ---")
    for sub in SUBJECTS:
        sub_scores = [s["grades"].get(sub, 0) for s in students]
        sub_avg = sum(sub_scores) / len(sub_scores)
        print(f"  {sub:<12}: {sub_avg:.2f}")


def individual_report_card():
    if not students:
        print("\nNo students yet!")
        return

    name = input("\nEnter student name for report card: ").strip().lower()
    target = None
    for s in students:
        if s["name"].lower() == name:
            target = s
            break

    if not target:
        print("Student not found!")
        return

    avg = sum(target["grades"].values()) / len(target["grades"])
    status = "PASS" if avg >= PASS_MARK else "FAIL"
    letter = get_grade_letter(avg)

    # rank among all students
    all_avgs = []
    for s in students:
        s_avg = sum(s["grades"].values()) / len(s["grades"])
        all_avgs.append((s["name"], s_avg))
    all_avgs.sort(key=lambda x: x[1], reverse=True)
    rank = [i for i, (n, a) in enumerate(all_avgs, 1) if n == target["name"]][0]

    lines = []
    lines.append("=" * 40)
    lines.append("       STUDENT REPORT CARD")
    lines.append("=" * 40)
    lines.append(f"ID       : {target['id']}")
    lines.append(f"Name     : {target['name']}")
    lines.append("-" * 40)
    for sub, grade in target["grades"].items():
        lines.append(f"  {sub:<12}: {grade:.1f}")
    lines.append("-" * 40)
    lines.append(f"Average  : {avg:.2f}")
    lines.append(f"Grade    : {letter}")
    lines.append(f"Status   : {status}")
    lines.append(f"Rank     : {rank} of {len(students)}")
    lines.append("=" * 40)

    report_text = "\n".join(lines)
    print("\n" + report_text)

    # BONUS: export report as text file
    save_choice = input("\nExport this report as .txt file? (y/n): ").strip().lower()
    if save_choice == "y":
        filename = f"report_{target['name'].replace(' ', '_')}.txt"
        with open(filename, "w") as f:
            f.write(report_text)
        print(f"Report saved as {filename}")


def save_to_csv():
    filename = "students.csv"
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Name"] + SUBJECTS)
        for s in students:
            row = [s["id"], s["name"]]
            for sub in SUBJECTS:
                row.append(s["grades"].get(sub, 0))
            writer.writerow(row)
    print(f"Saved {len(students)} students to {filename}")


def load_from_csv():
    global next_id
    filename = "students.csv"
    if not os.path.exists(filename):
        return

    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            grades = {}
            for sub in SUBJECTS:
                grades[sub] = float(row[sub])
            student = {
                "id": int(row["ID"]),
                "name": row["Name"],
                "grades": grades
            }
            students.append(student)
            next_id = max(next_id, int(row["ID"]) + 1)
    print(f"Loaded {len(students)} students from file")


def main_menu():
    load_from_csv()
    while True:
        print("\n===== STUDENT GRADE MANAGEMENT SYSTEM =====")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Class Report")
        print("4. Individual Report Card")
        print("5. Save to CSV")
        print("6. Exit")

        choice = input("Enter choice (1-6): ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            view_all_students()
        elif choice == "3":
            class_report()
        elif choice == "4":
            individual_report_card()
        elif choice == "5":
            save_to_csv()
        elif choice == "6":
            save_to_csv()
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again!")


if __name__ == "__main__":
    main_menu()
