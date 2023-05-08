import json

#
# CLI Grade calculator in Python
# Over-OOP-ed
# Usage: python3 pytranscript.py
#       > 1
#

TRANSCRIPT_PATH = ""  # Path to the current transcript file
TRANSCRIPT = []  # Global transcript list containing all semester info

# Table for grade conversion: According to Purdue and countless other colleges
GRADE_TABLE = {
    "A+": 4.0, "A": 4.0, "A-": 3.7, "B+": 3.3, "B": 3.0, "B-": 2.7,
    "C+": 2.3, "C": 2.0, "C-": 1.7, "D+": 1.3, "D": 1.0, "D-": 0.7,
    "F": 0.0
}


# Error message should be in red
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
    """General purpose type-checking input func"""
    try:
        return input_type(input("> "))
    except ValueError:
        print(ShColors.RED + "Hey watch your input" + ShColors.ENDC)
        return my_input(input_type)


def course_dict_str(crs: dict) -> str:
    """
    Course dictionaries are in the format of:
    { "name": "CS252", "grade": "A+", "crhr": 4 }
    This func returns a formatted string to be a part of the Semester table
    """
    return f"| {crs['name']:10} | {crs['grade']:5} | {crs['crhr']:5} |\n"


class Semester:
    def __init__(self, *args) -> None:
        if len(args) == 2 and isinstance(args[0], int) \
                and isinstance(args[1], list):
            """Initialize a Semester object with list of Courses"""
            self.num = args[0]      # Number of semester (1, 2, etc.)
            self.courses = args[1]  # Course list
        elif len(args) == 1 and isinstance(args[0], dict):
            """
            Initialize a Semester object with dict read from JSON file
            e.g.:
            {'num': 1, 'courses': [{'name': 'MA261', 'grade': 'A+', 'crhr': 4},
                                   {'name': 'CS180', 'grade': 'A', 'crhr': 3}]}
            """
            for key in args[0]:
                # Yes, json.load() even converts dictionaries within a list
                setattr(self, key, args[0][key])

    def total_cr(self) -> int:
        """Calculate total credit hour"""
        return sum([course["crhr"] for course in self.courses])

    def total_gpa_hr(self) -> float:
        """Calculate total GPA hour: Sigma (crhr * grade point)"""
        return sum([course["crhr"] * GRADE_TABLE[course["grade"].upper()]
                    for course in self.courses])

    def gpa(self) -> float:
        """Calculate semester GPA"""
        return self.total_gpa_hr() / self.total_cr()

    def __str__(self) -> str:
        """Return a .md table representation of this semester's grade info"""
        repr = (f"-------- Semester: {self.num:2} --------\n"
                "| CLASS      | GRADE | CR HR |\n"
                "|------------|-------|-------|\n")
        for course in self.courses:
            repr += course_dict_str(course)
        repr += f"| TOTAL      | {self.gpa():5.2f} | {self.total_cr():5} |\n"
        return repr


def print_transcript():
    """Print the current transcript and calculate overall GPA"""
    if not TRANSCRIPT:
        print(ShColors.YELLOW +
              "Transcript is empty! " +
              "Use 'Read Transcript' option to read a JSON file" +
              ShColors.ENDC)
        return

    for semester in TRANSCRIPT:
        print(semester)

    total_gpa_hr = 0.0
    total_cr = 0.0
    for sem in TRANSCRIPT:
        total_gpa_hr += sem.total_gpa_hr()
        total_cr += sem.total_cr()
    overall_gpa = total_gpa_hr / total_cr

    print(
        ShColors.CYAN +
        f"Overall GPA: {overall_gpa:.2f}\n" +
        f"Total GPA Hour: {total_gpa_hr:.2f}\n" +
        f"Total Credit: {total_cr:.2f}\n" +
        ShColors.ENDC
    )


def read_transcript():
    """Read the transcript from a given file"""
    print(ShColors.CYAN + "Enter the JSON file name" + ShColors.ENDC)
    file_name = my_input(str)
    # Read the file. Data should be a list of dictionary repr of Semester
    with open(file_name, "r") as fp:
        datum = json.load(fp)
    # Add each Semester object to the global TRANSCRIPT list
    for data in datum:
        TRANSCRIPT.append(Semester(data))

    # Print semester information
    print_transcript()


def add_new_sem():
    """Add a new semester object to the """
    print("I'm working on it bro")
    pass
    # with open("hi.json", "w") as fp:
    #     json.dump(TRANSCRIPT, fp)


def menu():
    """Infinitely prompt user for selection until EXIT code was given"""
    # Table in the form of:
    # Num: ["Prompt", func_to_execute]
    opts = {
        1: ["Read a JSON transcript", read_transcript],
        2: ["Print the current transcript", print_transcript],
        3: ["Add a new semester to the transcript", add_new_sem],
        0: ["Exit (or Ctrl+c)", "EXIT"]
    }

    usr_input = -1
    exec = ""
    while True:
        for key, val in opts.items():
            print(f"{key}. {val[0]}")
        # Get input
        usr_input = my_input(int)
        try:
            exec = opts[usr_input][1]
        except KeyError:
            print(ShColors.RED + "Read the prompt again" + ShColors.ENDC)
            continue
        # Check for exit
        if isinstance(exec, str) and exec == "EXIT":
            raise KeyboardInterrupt
        # Execute the user choice
        exec()


def main():
    """Main function to call menu and handle KeyboardInterrupt"""
    try:
        print(ShColors.GREEN +
              "You really can't wait two days for the grades to be out huh" +
              ShColors.ENDC)
        menu()
    except KeyboardInterrupt:
        print(ShColors.YELLOW + "\nBye" + ShColors.ENDC)


if __name__ == "__main__":
    main()
