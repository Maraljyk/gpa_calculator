from itertools import product

NOTES = {"AA": 4.0, "BA": 3.5, "BB": 3.0, "CB": 2.5,
         "CC": 2.0, "DC": 1.5, "DD": 1.0, "FF": 0.0}

PASSING = ["AA", "BA", "BB", "CB", "CC", "DC", "DD"]

SCENARIOS = {"Best": "AA", "Average": "CB", "Worst": "DD"}

#       CALCULATION :

def totals(courses):
    point = akts = removed_point = removed_akts = 0
    for name, c_akts, note, old_note in courses:
        point += c_akts * NOTES[note]
        akts += c_akts

        if old_note:
            removed_point += c_akts * NOTES[old_note]
            removed_akts += c_akts
    return point, akts, removed_point, removed_akts

def semester_gpa(courses):
    point, akts, _, _ = totals(courses)
    return point / akts

def total_gpa(courses, prev_gpa, prev_akts):
    point, akts, removed_point, removed_akts = totals(courses)
    return (prev_gpa * prev_akts + point - removed_point) / (prev_akts + akts - removed_akts)

#       INPUT HELPERS :

def ask_int(prompt, minimum=1):
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("Please Enter an Integer Number")
            continue
        if value >= minimum:
            return value
        print(f"Please Enter a Number of at least {minimum}")

def ask_float(prompt, minimum=0.0, maximum=4.0):
    while True:
        try:
            value = float(input(prompt))
        except ValueError:
            print("Please Enter a Number (e.g 3.25)")
            continue
        if minimum <= value <= maximum:
            return value
        print(f"Please Enter a Number between {minimum} and {maximum}")

def ask_note(prompt):
    while True:
        note = input(prompt).upper()
        if note in NOTES:
            return note
        print("Invalid Grade. Use AA, BA, BB, CB, CC, DC, DD or FF")

def ask_yes_no(prompt):
    while True:
        answer = input(prompt).lower()
        if answer in ("y", "n"):
            return answer == "y"
        print("Please Enter y or n")

def get_courses(ask_grade = True):
    courses = []
    number_of_courses = ask_int("Enter the amount of courses: ")

    for i in range(number_of_courses):
        name = input("Course name: ")
        akts = ask_int("Course AKTS: ")
        note = None
        if ask_grade:
            note = ask_note("Course note (AA, BA...): ")
        old_note = None
        if ask_yes_no("Retake?(y/n): "):
            old_note = ask_note("Old note: ")
        courses.append((name, akts, note, old_note))
    return courses

def ask_previous():
    prev_gpa = ask_float("Enter total GPA of previous semesters: ")
    prev_akts = ask_int("Enter the total amount of AKTS from previous semesters(failed included): ", minimum=0)
    return prev_gpa, prev_akts

#       OPTIONS :

def option_average():
    courses = get_courses()
    print(f"Semester GPA: {semester_gpa(courses):.2f}")

    prev_gpa, prev_akts = ask_previous()
    print(f"Total GPA:  {total_gpa(courses, prev_gpa, prev_akts):.2f}")

def assign_grade(planned, grade):
    courses = []
    for name, akts, _, old_note in planned:
        courses.append((name, akts, grade, old_note))
    return courses

def option_estimate():
    planned = get_courses(ask_grade = False)
    prev_gpa, prev_akts = ask_previous()

    for label, grade in SCENARIOS.items():
        courses = assign_grade(planned, grade)
        print(f"{label} ({grade}): Semester {semester_gpa(courses):.2f} | Total {total_gpa(courses, prev_gpa, prev_akts):.2f}")

def required_semester_gpa(planned, prev_gpa, prev_akts, target):
    courses = assign_grade(planned, "AA")
    _, akts, removed_point, removed_akts = totals(courses)
    needed_point = target * (prev_akts + akts - removed_akts) - prev_gpa * prev_akts + removed_point
    return needed_point / akts

def nearby_grades(required, count=3):
    ranked = []
    for grade in PASSING:
        distance = abs(NOTES[grade] - required)
        ranked.append((distance, grade))
    ranked.sort()

    nearest = []
    for _, grade in ranked[:count]:
        nearest.append(grade)
    return nearest

def spread(courses):
    points = []
    for _, _, note, _ in courses:
        points.append(NOTES[note])
    return max(points) - min(points)

def sort_key(scenario):
    gpa, courses = scenario
    return (round(gpa, 2), spread(courses))

def find_scenarios(planned, prev_gpa, prev_akts, target, limit=10):
    required = required_semester_gpa(planned, prev_gpa, prev_akts, target)
    grades = nearby_grades(required)
    results = []
    for combo in product(grades, repeat=len(planned)):
        courses = []
        for i in range(len(planned)):
            name, akts, _, old_note = planned[i]
            courses.append((name, akts, combo[i], old_note))
        gpa = total_gpa(courses, prev_gpa, prev_akts)
        if gpa >= target:
            results.append((gpa, courses))
    results.sort(key=sort_key)
    return results[:limit]

def option_target():
    planned = get_courses(ask_grade = False)
    prev_gpa, prev_akts = ask_previous()
    target = ask_float("Enter your target GPA: ")

    if required_semester_gpa(planned, prev_gpa, prev_akts, target) > 4.0:
        print("Impossible this semester, even with all AA's.")
        return

    for gpa, courses in find_scenarios(planned, prev_gpa, prev_akts, target):
        line = f"{gpa:.2f} -> "
        for name, _, note, _ in courses:
            line += f"{name}: {note}  "
        print(line)

#       MENU :

def main():
    while True:
        print("\n === GPA CALCULATOR ===\n")
        print("1. Calculate GPA")
        print("2. Target GPA Scenarios")
        print("3. Best/ average/ worst estimate")
        print("0. Exit\n")
        choice = input("Choose Option: ")

        if choice == "1":
            option_average()
        elif choice == "2":
            option_target()
        elif choice == "3":
            option_estimate()
        elif choice == "0":
            print("GOODBYE!")
            break
        else:
            print("Invalid choice. Try again!")

main()