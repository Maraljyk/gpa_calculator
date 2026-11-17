notes = {"AA": 4.0, "BA": 3.5, "BB": 3.0, "CB": 2.5,
         "CC": 2.0, "DC": 1.5, "DD": 1.0, "FF": 0.0}
courses = []
removed_point = 0   
removed_akts = 0    

number_of_courses = int(input("Enter the amount of courses: "))
for i in range(number_of_courses):
    name = input("Course name: ")
    akts = int(input("Course AKTS: "))
    course_note = input("Course note (AA, BA...): ").upper()
    courses.append((name, akts, course_note))

    retake = input("Retake? (y/n): ").lower()          
    if retake == "y":                                   
        old_note = input("Old note: ").upper()          
        removed_point += akts * notes[old_note]         
        removed_akts += akts                           

# for current semester
semester_point = 0
semester_akts = 0
for name, akts, course_note in courses:
    semester_point += akts * notes[course_note]
    semester_akts += akts

print(f"Semester GPA: {semester_point / semester_akts:.2f}")

# for all semesters
prev_gpa = float(input("Enter total GPA of previous semesters: "))
prev_akts = int(input("Enter the total amount of AKTS from previous semesters: "))

new_gpa = (prev_gpa * prev_akts + semester_point - removed_point) / (prev_akts + semester_akts - removed_akts)   # 🆕 değişti
print(f"Total GPA: {new_gpa:.2f}")