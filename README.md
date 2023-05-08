# Pytranscript

It is Sunday 7 May 2023. I just wrapped up my fourth semester this week, but I am still unsure about grades for two of my classes. Grades are officially due on Tuesday 9 May 2023 for instructors, so I have two options:

1. Touch some grass, hang out with my friends and family, and give myself some time to relax after a tough semester
2. Sit in the room with Diet Coke and make a grade calculator to "automate" process of calculating what happens to my GPA if I get an A- instead of an A in the philosophy class

Option 2 it is then.

## Usage

Make sure you have Python version >= 3.6 (I'm sure lower version works fine, but you really should start upgrading your system if you are still using < 3.6), working computer with more than 3KB of storage, and some input device (keyboard preferred).

```bash
git clone https://github.com/theopn/pytranscript.git
cd pytranscript
python3 pytranscript.py
```

In the pytranscript:

```

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

