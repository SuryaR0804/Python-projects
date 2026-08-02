class Student:
    all_students=[]
    def __init__(self, name, roll_no, marks):
        self.name=name
        self.roll_no=roll_no
        self.marks=marks

    def update_marks(self, new_marks):
        self.marks=new_marks

    def show_details(self):
        print(f"\nRollNo: {self.roll_no}")
        print(f"Name: {self.name}")
        print(f"Marks: {self.marks}")

    @classmethod
    def find_student_by_roll(cls,roll):
        for student in cls.all_students:
            if student.roll_no==roll:
                return student
        return None

    @classmethod
    def add_students(cls):
        name= input("Enter student name: ")
        roll_no=input("Enter student roll number: ")
        marks=int(input("Enter student marks: "))
        student=cls(name, roll_no, marks)
        cls.all_students.append(student)
        print(f"Student {name} added successfully!")
            
    @classmethod
    def update_student_marks(cls):
        roll=input("Enter student roll number tp update marks: ")
        student=cls.find_student_by_roll(roll)
        if student:
            new_marks=int(input("Enter new marks: "))
            student.update_marks(new_marks)
        else:
            print("Student not found.")

    @classmethod
    def show_all_students(cls):
        if not cls.all_students:
            return
        for student in cls.all_students:
            student.show_details()

