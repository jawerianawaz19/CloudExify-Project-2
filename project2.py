# grade_system.py
# CloudExify Python Internship - Month 1 Project 2 (Simple Version)
# NAME: JAWERIA NAWAZ - RegNo: CX-INT-2026-PY-0119

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
    print(f"\nAdded {name} | Average: {avg:.1f} | {status}")


def view_all_students():
    if not students:
        print("\nNo students yet!")
        return

    print("\n--- ALL STUDENTS ---")
    print(f"{'ID':<5}{'Name':<20}", end="")
    for sub in SUBJECTS:
        print(f"{sub[:5]:<7}", end="")
    print(f"{'Avg':<8}{'Status'}")
    print("-" * 75)

    for s in students:
        avg = sum(s["grades"].values()) / len(s["grades"])
        status = "PASS" if avg >= PASS_MARK else "FAIL"
        print(f"{s['id']:<5}{s['name']:<20}", end="")
        for sub in SUBJECTS:
            grade = s["grades"].get(sub, 0)
            print(f"{grade:<7.1f}", end="")
        print(f"{avg:<8.1f}{status}")


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
        print(f"  {rank}. {name:<20} {avg:.2f}")


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

def delete_student():
    if not students:
        print("\nNo students yet!")
        return

    print("\n--- STUDENTS ---")
    for s in students:
        print(f"  ID {s['id']}: {s['name']}")

    try:
        target_id = int(input("\nEnter Student ID to delete: ").strip())
    except ValueError:
        print("Invalid ID!")
        return

    target = None
    for s in students:
        if s["id"] == target_id:
            target = s
            break

    if not target:
        print("Student ID not found!")
        return

    confirm = input(f"Are you sure you want to delete '{target['name']}'? (y/n): ").strip().lower()
    if confirm == "y":
        students.remove(target)
        print(f"Deleted {target['name']}")
    else:
        print("Cancelled.")

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
        print("4. Delete Student")
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
            delete_student()
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
