class Student:
    school = "Rockhurst"

    def __init__(self, first_name: str, last_name: str, major: str) -> None:
        self.first_name = first_name
        self.last_name = last_name

        self.major = major

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @classmethod
    def set_online_school(cls, new_school):
        cls.school = new_school

    @classmethod
    def split_students(cls, student_str: str):
        first, last, maj = student_str.split(".")
        return cls(first, last, maj)


student_1 = Student(first_name="eric", last_name="lukasz", major="comp")


print(student_1.school)

student_1.set_online_school(new_school="FAU")

print(student_1.school)

new_student = "Adil.Yutzy.English"
student_2 = Student.split_students(new_student)

print(student_2.full_name())
