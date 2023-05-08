#
# CLI Grade calculator in Python
# Over-OOP-ed
# Usage: python3 pytranscript.py
#       > 1
#


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


def my_input(input_type: type) -> type:
    try:
        return input_type(input("> "))
    except ValueError:
        print(ShColors.RED + "Hey watch your input" + ShColors.ENDC)
        return my_input(input_type)


class Course:
    def __init__(self, name: str, grade: str, crhr: int) -> None:
        """Initialize a single course instance"""
        self.name = name        # Name of the course
        self.grade = grade      # Grade received
        self.crhr = crhr        # Credit hour

    def __str__(self) -> str:
        """Return a formatted string as a part of the Semester table"""
        return f"| {self.name:10} | {self.grade:5} | {self.crhr:5} |\n"


class Semester:
    def __init__(self, num: int, courses: Course) -> None:
        """Initialize a Semester object with list of Courses"""
        self.num = num          # Number of semester (1, 2, etc.)
        self.courses = courses  # Course array

    def total_cr(self) -> int:
        """Calculate total credit hour"""
        return sum([course.crhr for course in self.courses])

    def total_gpa_hr(self) -> float:
        """Calculate total GPA hour: Sigma (crhr * grade point)"""
        return sum([course.crhr * GRADE_TABLE[course.grade.upper()]
                    for course in self.courses])

    def gpa_calc(self) -> float:
        """Calculate semester GPA"""
        return self.total_gpa_hr() / self.total_cr()

    def __str__(self) -> str:
        """Return a .md table representation of this semester's grade info"""
        repr = (f"-------- Semester: {self.num:2} --------\n"
                "| CLASS      | GRADE | CR HR |\n"
                "|------------|-------|-------|\n")
        for course in self.courses:
            repr += course.__str__()
        repr += f"| TOTAL      | {self.gpa_calc():5} | {self.total_cr():5} |\n"
        return repr


class Transcript:
    def __init__(self, semesters: Semester) -> None:
        """Initialize a Semester object with list of Semesters"""
        self.semesters = semesters

    def __str__(self) -> str:
        """Append multiple Semester grade tables separated by new line"""
        return '\n'.join([semester.__str__() for semester in self.semesters])


def read_transcript():
    print(ShColors.CYAN + "Enter the file name" + ShColors.ENDC)
    hi = my_input(str)
    print(hi)


def menu():
    # Table in the form of:
    # Num: ["Prompt", func_to_execute]
    opts = {
        1: ["Read the current transcript", read_transcript],
        2: ["Add a new semester to the transcript", print],
        3: ["Exit (or Ctrl+c)", "EXIT"]
    }

    usr_input = -1
    usr_slct = ""
    while True:
        for key, val in opts.items():
            print(f"{key}. {val[0]}")
        # Get input
        usr_input = my_input(int)
        try:
            usr_slct = opts[usr_input][1]
        except KeyError:
            print(ShColors.RED + "Read the prompt again" + ShColors.ENDC)
            continue
        # Check for exit
        if type(usr_slct) == str and usr_slct == "EXIT":
            raise KeyboardInterrupt
        # Execute the use choice
        usr_slct()


def main():
    try:
        print(ShColors.GREEN
              + "You really can't wait two days for the grades to be out huh"
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
