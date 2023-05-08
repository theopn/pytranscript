GRADE_TABLE = {
    "A+": 4.0, "A": 4.0, "A-": 3.7, "B+": 3.3, "B": 3.0, "B-": 2.7,
    "C+": 2.3, "C": 2.0, "C-": 1.7, "D+": 1.3, "D": 1.0, "D-": 0.7,
    "F": 0.0
}


class ShColors:
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    WHITE = "\033[0;37m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDLINE = "\033[4m"


class Course:
    def __init__(self, name: str, grade: str, crhr: int) -> None:
        self.name = name        # Name of the course
        self.grade = grade      # Grade received
        self.crhr = crhr        # Credit hour

    def __str__(self) -> str:
        return f"| {self.name:10} | {self.grade:5} | {self.crhr:5} |\n"


class Semester:
    def __init__(self, num: int, courses: Course) -> None:
        self.num = num          # Number of semester (1, 2, etc.)
        self.courses = courses  # Course array

    def total_cr(self) -> int:
        return sum([course.crhr for course in self.courses])

    def total_gpa_hr(self) -> float:
        return sum([course.crhr * GRADE_TABLE[course.grade.upper()]
                    for course in self.courses])

    def gpa_calc(self) -> float:
        return self.total_gpa_hr() / self.total_cr()

    def __str__(self) -> str:
        repr = (f"-------- Semester: {self.num:2} --------\n"
                "| CLASS      | GRADE | CR HR |\n"
                "|------------|-------|-------|\n")
        for course in self.courses:
            repr += course.__str__()
        repr += f"| TOTAL      | {self.gpa_calc():5} | {self.total_cr():5} |\n"
        return repr


class Transcript:
    def __init__(self, semesters: Semester) -> None:
        self.semesters = semesters

    def __str__(self) -> str:
        return "\n".join([semester.__str__() for semester in self.semesters])


def read_transcript():
    pass


def menu():
    opts = {
        1: ["1. Read the current transcript", print],
        2: ["2. Add a new semester to the transcript", print],
        3: ["3. Exit (or Ctrl+c)", "EXIT"]
    }

    usr_input = -1
    usr_slct = ""
    while True:
        for usr_input in opts:
            print(opts[usr_input][0])
        # Get input
        try:
            usr_input = int(input("Select: "))
            usr_slct = opts[usr_input][1]
        except (ValueError, KeyError):
            print(ShColors.RED + "Hey be careful with input" + ShColors.ENDC)
            continue
        # Check for exit
        if type(usr_slct) == str and usr_slct == "EXIT":
            raise KeyboardInterrupt
        # Execute the use choice
        usr_slct()


def main():
    try:
        print(ShColors.BOLD + ShColors.GREEN
              + "You really cannot wait a week for transcript to be out huh"
              + ShColors.ENDC)
        menu()
    except KeyboardInterrupt:
        print(ShColors.YELLOW + "\nBye" + ShColors.ENDC)

    ma261 = Course("MA261", "B+", 4)
    cs180 = Course("cs180", "A", 3)
    sem1 = Semester(1, [ma261, cs180])
    ts = Transcript([sem1, sem1])
    print(ts)


if __name__ == "__main__":
    main()
