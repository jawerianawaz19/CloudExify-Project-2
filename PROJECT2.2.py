
#GRADINGSYSTEM with bonus functionalities final version
#name: jaweria nawaz  RegNo: CX-INT-2026-PY-0119


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


def get_attendance_percent(student):
    total = student["attendance"]["total"]
    if total == 0:
        return 0.0
    return (student["attendance"]["present"] / total) * 100


def add_subject():
    print("\n--- ADD NEW SUBJECT ---")
    new_sub = input("Enter new subject name: ").strip()
    if not new_sub:
        print("Subject name cannot be empty!")
        return

    for sub in SUBJECTS:
        if sub.lower() == new_sub.lower():
            print(f"Subject '{new_sub}' already exists!")
            return

    SUBJECTS.append(new_sub)
    print(f"Subject '{new_sub}' added!")

    if students:
        print(f"\nExisting students found. Enter '{new_sub}' grade for each:")
        for s in students:
            while True:
                try:
                    grade = float(input(f"  {s['name']}: "))
                    if 0 <= grade <= 100:
                        s["grades"][new_sub] = grade
                        break
                    print("  Grade must be 0-100!")
                except ValueError:
                    print("  Please enter a valid number!")


def view_subjects():
    print("\n--- CURRENT SUBJECTS ---")
    for i, sub in enumerate(SUBJECTS, 1):
        print(f"  {i}. {sub}")


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
        "grades": grades,
        "attendance": {"present": 0, "total": 0}
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
    print(f"{'Avg':<8}{'Grade':<7}{'Status':<8}{'Attend%'}")
    print("-" * 90)

    for s in students:
        avg = sum(s["grades"].values()) / len(s["grades"])
        status = "PASS" if avg >= PASS_MARK else "FAIL"
        letter = get_grade_letter(avg)
        att = get_attendance_percent(s)
        print(f"{s['id']:<5}{s['name']:<20}", end="")
        for sub in SUBJECTS:
            grade = s["grades"].get(sub, 0)
            print(f"{grade:<7.1f}", end="")
        print(f"{avg:<8.1f}{letter:<7}{status:<8}{att:.1f}%")


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

    print("\n--- SUBJECT-WISE CLASS AVERAGE ---")
    for sub in SUBJECTS:
        sub_scores = [s["grades"].get(sub, 0) for s in students]
        sub_avg = sum(sub_scores) / len(sub_scores)
        print(f"  {sub:<12}: {sub_avg:.2f}")

    att_values = [get_attendance_percent(s) for s in students]
    class_att_avg = sum(att_values) / len(att_values)
    print(f"\nClass Average Attendance: {class_att_avg:.2f}%")


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
    att = get_attendance_percent(target)

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
    lines.append(f"ID         : {target['id']}")
    lines.append(f"Name       : {target['name']}")
    lines.append("-" * 40)
    for sub, grade in target["grades"].items():
        lines.append(f"  {sub:<12}: {grade:.1f}")
    lines.append("-" * 40)
    lines.append(f"Average    : {avg:.2f}")
    lines.append(f"Grade      : {letter}")
    lines.append(f"Status     : {status}")
    lines.append(f"Attendance : {att:.1f}% ({target['attendance']['present']}/{target['attendance']['total']} days)")
    lines.append(f"Rank       : {rank} of {len(students)}")
    lines.append("=" * 40)

    report_text = "\n".join(lines)
    print("\n" + report_text)

    save_choice = input("\nExport this report as .txt file? (y/n): ").strip().lower()
    if save_choice == "y":
        filename = f"report_{target['name'].replace(' ', '_')}.txt"
        with open(filename, "w") as f:
            f.write(report_text)
        print(f"Report saved as {filename}")


def mark_attendance():
    if not students:
        print("\nNo students yet!")
        return

    print("\n--- MARK TODAY'S ATTENDANCE ---")
    for s in students:
        while True:
            ans = input(f"  {s['name']} present? (y/n): ").strip().lower()
            if ans in ("y", "n"):
                s["attendance"]["total"] += 1
                if ans == "y":
                    s["attendance"]["present"] += 1
                break
            print("  Please enter y or n!")

    print("\nAttendance marked for all students.")


def view_attendance():
    if not students:
        print("\nNo students yet!")
        return

    print("\n--- ATTENDANCE REPORT ---")
    print(f"{'ID':<5}{'Name':<20}{'Present':<10}{'Total':<8}{'Percent'}")
    print("-" * 55)
    for s in students:
        pct = get_attendance_percent(s)
        print(f"{s['id']:<5}{s['name']:<20}{s['attendance']['present']:<10}"
              f"{s['attendance']['total']:<8}{pct:.1f}%")


def save_to_csv():
    filename = "students.csv"
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Name"] + SUBJECTS + ["Present", "Total"])
        for s in students:
            row = [s["id"], s["name"]]
            for sub in SUBJECTS:
                row.append(s["grades"].get(sub, 0))
            row.append(s["attendance"]["present"])
            row.append(s["attendance"]["total"])
            writer.writerow(row)
    print(f"Saved {len(students)} students to {filename}")


def load_from_csv():
    global next_id, SUBJECTS
    filename = "students.csv"
    if not os.path.exists(filename):
        return

    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames:
            all_cols = reader.fieldnames
            SUBJECTS = [col for col in all_cols if col not in ("ID", "Name", "Present", "Total")]

        for row in reader:
            grades = {}
            for sub in SUBJECTS:
                grades[sub] = float(row[sub])
            student = {
                "id": int(row["ID"]),
                "name": row["Name"],
                "grades": grades,
                "attendance": {
                    "present": int(row.get("Present", 0)),
                    "total": int(row.get("Total", 0))
                }
            }
            students.append(student)
            next_id = max(next_id, int(row["ID"]) + 1)
    print(f"Loaded {len(students)} students from file (Subjects: {', '.join(SUBJECTS)})")


def main_menu():
    load_from_csv()
    while True:
        print("\n===== STUDENT GRADE MANAGEMENT SYSTEM =====")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Class Report")
        print("4. Individual Report Card")
        print("5. Mark Attendance")
        print("6. View Attendance Report")
        print("7. Add New Subject")
        print("8. View Current Subjects")
        print("9. Save to CSV")
        print("10. Exit")

        choice = input("Enter choice (1-10): ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            view_all_students()
        elif choice == "3":
            class_report()
        elif choice == "4":
            individual_report_card()
        elif choice == "5":
            mark_attendance()
        elif choice == "6":
            view_attendance()
        elif choice == "7":
            add_subject()
        elif choice == "8":
            view_subjects()
        elif choice == "9":
            save_to_csv()
        elif choice == "10":
            save_to_csv()
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again!")


if __name__ == "__main__":
    main_menu()
