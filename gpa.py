NOTES = {"AA": 4.0, "BA": 3.5, "BB": 3.0, "CB": 2.5,
         "CC": 2.0, "DC": 1.5, "DD": 1.0, "FF": 0.0}

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

def get_courses():
    courses = []
    number_of_courses = int(input("Enter the amount of courses: "))

    for i in range(number_of_courses):
        name = input("Course name: ")
        akts = int(input("Course AKTS: "))
        note = input("Course note (AA, BA...): ").upper()
        old_note = None 
        if input("Retake?(y/n): ").lower()=="y":
            old_note =input("Old note: ").upper()
        courses.append((name, akts, note, old_note))
    return courses

courses = get_courses()
print(f"Semester GPA: {semester_gpa(courses):.2f}")

prev_gpa = float(input("Enter total GPA of previous semesters: "))
prev_akts = int(input("Enter the total amount of AKTS from previous semesters(failed included): "))
print(f"Total GPA:  {total_gpa(courses, prev_gpa, prev_akts):.2f}")                       