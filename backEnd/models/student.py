class Student:
    def __init__(self, id: int, full_name: str, major: str):
        self.id = id
        self.full_name = full_name
        self.major = major

    def __repr__(self):
        return f"<Student {self.full_name}>"
