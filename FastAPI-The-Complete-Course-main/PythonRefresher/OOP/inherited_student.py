class Student:
    def __init__(self, first_name: str, last_name: str) -> None:
        self.first_name = first_name
        self.last_name = last_name

    def greetings(self) -> str:
        return f"Hello my name is {self.first_name} {self.last_name}"


class CollegeStudent(Student):
    def __init__(self, first_name: str, last_name: str, major: str) -> None:
        super().__init__(first_name, last_name)
        self.major = major

    def greetings(self) -> str:
        return f"{self.first_name} {self.last_name} is a college student"


class NonCollegeStudent(Student):
    def __init__(self, first_name: str, last_name: str, future_job: str) -> None:
        super().__init__(first_name, last_name)
        self.future_job = future_job

    def grow_up(self):
        return f"I want to be {self.future_job}"


class PhDStudent(CollegeStudent):
    def __init__(self, first_name: str, last_name: str, major: str, book: str) -> None:
        super().__init__(first_name, last_name, major)
        self.book = book


student_1 = CollegeStudent(first_name="Lukasz", last_name="Ch", major="PE")
student_2 = Student(first_name="Daniel", last_name="Ch")
student_3 = NonCollegeStudent(first_name="David", last_name="David", future_job="David")

print(student_1.greetings())
print(student_2.greetings())
print(student_3.grow_up())
