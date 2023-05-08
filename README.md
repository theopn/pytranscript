# Pytranscript

It is Sunday 7 May 2023. I just wrapped up my fourth semester this week, but I am still unsure about grades for two of my classes. Grades are officially due on Tuesday 9 May 2023 for instructors, so I have two options:

1. Touch some grass, hang out with my friends and family, and give myself some time to relax after a tough semester
2. Sit in the room with Diet Coke and make a grade calculator to "automate" process of calculating what happens to my GPA if I get an A- instead of an A in the philosophy class

Option 2 it is then.

## Usage

Dependencies:

- Python 3
- JSON package for Python
- Working computer with more than 3KB of storage
- Input device

```bash
git clone https://github.com/theopn/pytranscript.git
cd pytranscript
python3 pytranscript.py
```

In pytranscript.py:

```
1. Read a JSON transcript
2. ...
> 1
Enter the JSON file name
> transcript.json

1. ...
2. ...
3. Add a new semester to the transcript
> 3
Enter the semester number:
> 5
Enter Course informations.
Do not include courses with no GPA value (i.e. Pass/Not Pass)
When you are done, use Control + c to termimate
Course name:
> CS690
Grade (A+, A, A-, etc.):
> A+
Credit hour:
> 5.0
Course name:
> ^C
Breaking out of the adding course mode...

1. ...
2. Print the current transcript
> 2
-------- Semester:  n --------
| ...                        |

-------- Semester:  5 --------
| CLASS      | GRADE | CR HR |
|------------|-------|-------|
| CS690      | A+    |   5.0 |
| TOTAL      |  4.00 |   5.0 |

Total GPA Hour: 180.30
Total Credit: 47.00
Overall GPA: 3.84
```

## Oops

As I finished making this, I just realized that I took databases class this semester and I could've just used SQL.

```sql
CREATE TABLE SemesterFour (
    ClassName VARCHAR(255),
    GPA DOUBLE,
    ...
)
INSERT INTO SemesterFour VALUES ('CS252', 4.0, ...)
SELECT AVG(GPA) FROM SemesterFour;
```

