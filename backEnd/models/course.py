class Course:
    def __init__(self, id: int, name: str, credits: int):
        self.id = id
        self.name = name
        self.credits = credits # Bu fanning reytingdagi vazni

    def __repr__(self):
        return f"<Course {self.name} ({self.credits} credits)>"
