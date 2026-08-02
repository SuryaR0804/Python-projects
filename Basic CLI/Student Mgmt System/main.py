from students import Student

def menu():
    while True:
        print("\n ========== Student Mgmt System ==========")
        print("1. Add student")
        print("2. Update marks")
        print("3. Show all students")
        print("4. Exit")

        choice=input("\nEnter Your Option(1-4): ")

        match choice:
            case '1':
                Student.add_students()
            case '2':
                Student.update_student_marks()
            case '3':
                Student.show_all_students()
            case '4':
                print("Exiting mgmt system. Goodbye")
                break
            case _:
                print("Invalid Choice.")

if __name__=="__main__":
    menu()
            
