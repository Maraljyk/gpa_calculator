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

def get_courses(ask_grade = True):
    courses = []
    number_of_courses = int(input("Enter the amount of courses: "))

    for i in range(number_of_courses):
        name = input("Course name: ")
        akts = int(input("Course AKTS: "))
        note = None 
        if ask_grade:
         note = input("Course note (AA, BA...): ").upper()
        old_note = None 
        if input("Retake?(y/n): ").lower()=="y":
            old_note =input("Old note: ").upper()
        courses.append((name, akts, note, old_note))
    return courses

def option_average():
    courses = get_courses()
    print(f"Semester GPA: {semester_gpa(courses):.2f}")

    prev_gpa = float(input("Enter total GPA of previous semesters: "))
    prev_akts = int(input("Enter the total amount of AKTS from previous semesters(failed included): "))
    print(f"Total GPA:  {total_gpa(courses, prev_gpa, prev_akts):.2f}")                       

def assign_grade(planned, grade):
    courses = []
    for name, akts, _, old_note in planned:
        courses.append((name, akts, grade, old_note))
    return courses

def option_estimate():
    planned = get_courses(ask_grade = False)
    prev_gpa = float(input("Enter total GPA of previous semesters: "))
    prev_akts = int(input("Enter the total amount of AKTS from previous semesters(failed included): "))

    for label, grade in SCENARIOS.items():
        courses = assign_grade(planned, grade)
        print(f"{label} ({grade}): Semester {semester_gpa(courses):.2f} | Total {total_gpa(courses, prev_gpa, prev_akts):.2f}")

#option_estimate() # temporary

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
        if gpa >= target :
            results.append((gpa, courses))
    results.sort(key = sort_key)
    return results[:limit]

def option_target():
    planned = get_courses(ask_grade = False)
    prev_gpa = float(input("Enter total GPA of previous semesters: "))
    prev_akts = int(input("Enter the total amount of AKTS from previous semesters(failed included): "))
    target = float(input("Enter your target GPA: "))

    if (required_semester_gpa(planned, prev_gpa, prev_akts, target) > 4.0 ):
        print ("Impossible this semester, even with all AA's.")
        return

    for gpa, courses in find_scenarios(planned, prev_gpa, prev_akts, target):
        line = f"{gpa:.2f} -> "
        for name, _, note, _ in courses:
            line += f"{name}: {note}  "
        print(line)

option_target() # temp exit
