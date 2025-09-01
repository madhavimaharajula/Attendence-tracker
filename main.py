import csv
import matplotlib.pyplot as plt
from datetime import date

attendance_file = "attendance.csv"

# Initialize file with headers if not present
def init_file():
    try:
        with open(attendance_file, "x", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Name", "Status"])
    except FileExistsError:
        pass

def mark_attendance():
    today = date.today().strftime("%Y-%m-%d")
    name = input("Enter student name: ")
    status = input("Enter status (Present/Absent): ").strip().lower()

    # Normalize input
    if status in ["p", "present"]:
        status = "Present"
    elif status in ["a", "absent"]:
        status = "Absent"
    else:
        print("❌ Invalid status! Use Present/Absent (or p/a).")
        return

    with open(attendance_file, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([today, name, status])
    print("✅ Attendance saved successfully!")

def view_attendance():
    with open(attendance_file, "r") as file:
        print("\nAttendance Records:")
        print(file.read())

def generate_report():
    data = {}
    with open(attendance_file, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row["Name"].strip()
            status = row["Status"].strip().lower()

            # Normalize saved data
            if status in ["p", "present"]:
                status = "Present"
            elif status in ["a", "absent"]:
                status = "Absent"
            else:
                continue  # skip invalid rows

            if name not in data:
                data[name] = {"Present": 0, "Absent": 0}
            data[name][status] += 1

    if not data:
        print("\n⚠️ No attendance data available.")
        return

    print("\n📊 Attendance Report:")
    for name, stats in data.items():
        print(f"{name} → Present: {stats['Present']}, Absent: {stats['Absent']}")

    # Plot Graph
    names = list(data.keys())
    presents = [stats["Present"] for stats in data.values()]
    absents = [stats["Absent"] for stats in data.values()]

    plt.bar(names, presents, label="Present", color="green")
    plt.bar(names, absents, bottom=presents, label="Absent", color="red")
    plt.xlabel("Students")
    plt.ylabel("Days")
    plt.title("Attendance Report")
    plt.legend()
    plt.show()
    total_present = sum(presents)
    total_absent = sum(absents)
    if total_present + total_absent > 0:
        plt.figure(figsize=(6,6))
        plt.pie(
            [total_present, total_absent],
            labels=["Present", "Absent"],
            colors=["green", "red"],
            autopct="%1.1f%%"
        )
        plt.title("Overall Attendance % (All Students)")
        plt.show()
     # --- Pie Chart for each student ---
    '''for name, stats in data.items():
        total = stats["Present"] + stats["Absent"]
        if total > 0:
            plt.figure(figsize=(5,5))
            plt.pie(
                [stats["Present"], stats["Absent"]],
                labels=["Present", "Absent"],
                colors=["green", "red"],
                autopct="%1.1f%%"
            )
            plt.title(f"Attendance % for {name}")
            plt.show()'''
            

def menu():
    init_file()
    while True:
        print("\n--- Attendance Tracker ---")
        print("1. Mark Attendance")
        print("2. View Attendance")
        print("3. Generate Report & Graph")
        print("4. Exit")
        choice = input("Enter choice: ")
        if choice == "1":
            mark_attendance()
        elif choice == "2":
            view_attendance()
        elif choice == "3":
            generate_report()
        elif choice == "4":
            print("Exiting... 👋")
            break
        else:
            print("Invalid choice!")

menu()
