import json
import sys

#
# CLI Grade calculator in Python
# Unnecessary OOP because everything is an object if you think deeply
# Usage: python3 pytranscript.py
#

TRANSCRIPT_FILE = ""  # Path to the current transcript file
TRANSCRIPT = []       # Global transcript list containing all semester info

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


def my_input(input_type: type, *args) -> type:
    """General purpose type-checking input func. Takes optional msg to print"""
    for msg in args:
        print(msg)
    try:
        return input_type(input("> "))
    except ValueError:
        print(ShColors.RED + "Hey watch your input" + ShColors.ENDC)
        return my_input(input_type)


def course_dict_str(crs: dict) -> str:
    """
    Course dictionaries are in the format of:
    { "name": "CS252", "grade": "A", "crhr": 4.0 }
    This func returns a formatted string to be a part of the Semester table
    | CS252      | A    | 4.0     |
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

    def total_qlty_pt(self) -> float:
        """Calculate total quality points: Sigma (crhr * grade point)"""
        try:
            return sum([course["crhr"] * GRADE_TABLE[course["grade"].upper()]
                        for course in self.courses])
        except KeyError:
            print(ShColors.RED
                  + f"There was an error with a grade in semester {self.num}. "
                  + "Make sure to only have a valid grade in your JSON file."
                  + ShColors.ENDC)
            return 0.0

    def gpa(self) -> float:
        """Calculate semester GPA"""
        return self.total_qlty_pt() / self.total_cr()

    def __str__(self) -> str:
        """Return a .md table representation of this semester's grade info"""
        repr = (f"-------- Semester: {self.num:2} --------\n"
                "| CLASS      | GRADE | CR HR |\n"
                "|------------|-------|-------|\n")
        for course in self.courses:
            repr += course_dict_str(course)
        repr += f"| TOTAL      | {self.gpa():5.2f} | {self.total_cr():5} |\n"
        return repr


def check_transcript_existence() -> bool:
    """Helper function to check if trnascript data exists"""
    if not TRANSCRIPT or not TRANSCRIPT_FILE:
        print(ShColors.RED +
              "Transcript is empty! " +
              "Use 'Read Transcript' option to read a JSON file" +
              "Or add a new semester to the transcript" +
              ShColors.ENDC)
        return False
    return True


def save_transcript():
    """Writes the current transcript data to a file"""
    if not check_transcript_existence():
        return
    with open(TRANSCRIPT_FILE, "w") as fp:
        sem_dict_list = []
        for sem in TRANSCRIPT:
            sem_dict_list.append(vars(sem))
        json.dump(sem_dict_list, fp, indent=4)


def print_transcript():
    """Print the current transcript and calculate overall GPA"""
    if not check_transcript_existence():
        return

    # Print semester transcript
    for semester in TRANSCRIPT:
        print(semester)

    # Calculate GPA stats
    total_qlty_pt = 0.0
    total_cr = 0.0
    for sem in TRANSCRIPT:
        total_qlty_pt += sem.total_qlty_pt()
        total_cr += sem.total_cr()
    overall_gpa = total_qlty_pt / total_cr
    print(
        ShColors.CYAN +
        f"Total Quality Points: {total_qlty_pt:.2f}\n" +
        f"Total Credit: {total_cr:.2f}\n" +
        f"Overall GPA: {overall_gpa:.2f}\n" +
        ShColors.ENDC
    )


def open_transcript(**kwargs):
    """Read the transcript from a given file or get a user input"""
    # Definition of a variable in Python is local by default
    global TRANSCRIPT_FILE
    global TRANSCRIPT

    # Check if file name was supplied
    if "filename" in kwargs:
        file_name = kwargs["filename"]
    else:
        file_name = my_input(
            str, ShColors.CYAN + "Enter the JSON file name" + ShColors.ENDC)

    TRANSCRIPT_FILE = file_name
    # Read the file. Data should be a list of dictionary repr of Semester
    try:
        with open(file_name, "r") as fp:
            datum = json.load(fp)
    except FileNotFoundError:
        print(ShColors.YELLOW
              + "File not found. "
              + f"{file_name} will be used to save data if new data is added."
              + ShColors.ENDC)
        return

    # Reset current transcript
    TRANSCRIPT = []
    # Add each Semester object to the global TRANSCRIPT list
    for data in datum:
        TRANSCRIPT.append(Semester(data))

    # Print semester information
    print_transcript()


def add_new_sem():
    """Add a new semester object to the current transcript var and save"""
    if not TRANSCRIPT_FILE:
        print(ShColors.RED + "No transcript file has been specified!\n" +
              "Please use 'Read Transcript' to add a file" + ShColors.ENDC)
        return

    sem_num = my_input(int, "Enter the semester number:")
    print(ShColors.CYAN + "Course Info Enter Mode:\n" + ShColors.ENDC
          + "Do not include courses with no GPA value (i.e. Pass/Not Pass).\n"
          + ShColors.RED + "When you are done, use Control + c to terminate."
          + ShColors.ENDC)
    courses = []
    while True:
        try:
            name = my_input(str, "Course name:").upper()
            grade = my_input(str, "Grade (A+, A, A-, etc.):").upper()
            crhr = my_input(float, "Credit hour:")
            courses.append({"name": name, "grade": grade, "crhr": crhr})
        except KeyboardInterrupt:
            print("\nEnding the Course Info Enter Mode...")
            break
    TRANSCRIPT.append(Semester(sem_num, courses))
    save_transcript()


def modify_transcript():
    """It's supposed to modify the transcript, it doesn't"""
    print("Ngl, it's faster to just modify the JSON file itself.")


def menu():
    """Infinitely prompt user for selection until EXIT code was given"""
    # Table in the form of:
    # Num: ["Prompt", func_to_execute]
    opts = {
        1: ["Open (or create) a JSON transcript", open_transcript],
        2: ["Print the current transcript", print_transcript],
        3: ["Add a new semester to the transcript", add_new_sem],
        4: ["Modify transcript", modify_transcript],
        0: ["Exit (or Ctrl+c)", "EXIT"]
    }

    usr_input = -1
    exec = ""
    while True:
        # Display the current open file
        if not TRANSCRIPT_FILE:
            print(ShColors.BLUE + "No file currently open" + ShColors.ENDC)
        else:
            print(ShColors.BLUE +
                  f"Current transcript: {TRANSCRIPT_FILE}" + ShColors.ENDC)
        # Prompt menus
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
            return
        # Execute the user choice
        exec()


def main():
    """Main function to call menu and handle KeyboardInterrupt"""
    try:
        print(ShColors.GREEN +
              "You really can't wait two days for the grades to be out huh" +
              ShColors.ENDC)
        # Check for a arg and import if one was supplied
        if len(sys.argv) > 1:
            open_transcript(filename=sys.argv[1])
        # Proceed with menu
        menu()
    except KeyboardInterrupt:
        print(ShColors.YELLOW + "\nBye" + ShColors.ENDC)


if __name__ == "__main__":
    main()
