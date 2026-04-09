import json
import os

students = []

if os.path.exists("students.json"):
    file = open("students.json", "r")
    students = json.load(file)
    file.close()

def save():
    file = open("students.json", "w")
    json.dump(students, file, indent=2)
    file.close()

def add_student():
    reg = input("Reg No: ")
    name = input("Name: ")
    cgpa = input("CGPA: ")
    
    new_student = {"reg": reg, "name": name, "cgpa": cgpa}
    
    students.append(new_student)
    save()
    print("Student added successfully!")

def view_students():
    if len(students) == 0:
        print("No students found.")
    else:
        print("\n--- Student List ---")
        for s in students:
            print("Reg: " + s["reg"] + " | Name: " + s["name"] + " | CGPA: " + s["cgpa"])
        print("--------------------")

def delete_student():
    reg_to_delete = input("Enter Reg No to delete: ")
    found = False
    
    for s in students:
        if s["reg"] == reg_to_delete:
            students.remove(s)
            save()
            print("Student deleted!")
            found = True
            break
            
    if found == False:
        print("Student not found.")

def update_student():
    reg_to_update = input("Enter Reg No to update: ")
    found = False
    
    for s in students:
        if s["reg"] == reg_to_update:
            found = True
            print("Current Name:", s["name"])
            print("Current CGPA:", s["cgpa"])
            
            print("Press 1 to update Name")
            print("Press 2 to update CGPA")
            choice = input("Enter choice: ")
            
            if choice == "1":
                s["name"] = input("Enter new name: ")
                save()
                print("Name updated!")
            elif choice == "2":
                s["cgpa"] = input("Enter new CGPA: ")
                save()
                print("CGPA updated!")
            else:
                print("Invalid choice.")
                
            break
            
    if found == False:
        print("Student not found.")

while True:
    print("\n=== Main Menu ===")
    print("1. Add Student")
    print("2. View Students")
    print("3. Delete Student")
    print("4. Update Student")
    print("5. Exit")
    
    choice = input("Enter your choice: ")
    
    if choice == "1":
        add_student()
    elif choice == "2":
        view_students()
    elif choice == "3":
        delete_student()
    elif choice == "4":
        update_student()
    elif choice == "5":
        print("Exiting program...")
        break
    else:
        print("Invalid choice. Try again.")
