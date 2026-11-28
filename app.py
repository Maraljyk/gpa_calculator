import streamlit as st
import pandas as pd
from gpa import (NOTES, SCENARIOS, semester_gpa, total_gpa, assign_grade,
                 required_semester_gpa, find_scenarios)

#       SETTINGS :

COL_COURSE = "Course"
COL_AKTS = "AKTS"
COL_GRADE = "Grade"
COL_OLD = "Old grade"

st.set_page_config(page_title="GPA Calculator", page_icon="🌐")

#       HELPERS :

def course_table(key, with_grade):
    columns = {COL_COURSE: [""], COL_AKTS: [None]}
    config = {
        "_index": st.column_config.NumberColumn("#", disabled=True),
        COL_AKTS: st.column_config.NumberColumn(min_value=1, step=1),
    }
    if with_grade:
        columns[COL_GRADE] = [None]
        config[COL_GRADE] = st.column_config.SelectboxColumn(options=list(NOTES))
    columns[COL_OLD] = [None]
    config[COL_OLD] = st.column_config.SelectboxColumn(
        options=list(NOTES), help="Only for retaken courses")
    empty_table = pd.DataFrame(columns, index=pd.RangeIndex(start=1, stop=2))
    return st.data_editor(empty_table, num_rows="dynamic", hide_index=False,
                          column_config=config, key=key)


def table_to_courses(table, with_grade):
    courses = []
    for row in table.to_dict("records"):
        if not row[COL_COURSE] or pd.isna(row[COL_AKTS]):
            continue
        note = None
        if with_grade:
            if row[COL_GRADE] not in NOTES:
                continue
            note = row[COL_GRADE]
        old_note = row[COL_OLD] if row[COL_OLD] in NOTES else None
        courses.append((row[COL_COURSE], int(row[COL_AKTS]), note, old_note))
    return courses


def previous_inputs(key):
    col1, col2 = st.columns(2)
    prev_gpa = col1.number_input("Previous GPA", min_value=0.0, max_value=4.0,
                                 step=0.01, value=None, placeholder="e.g. 2.81",
                                 key=f"{key}_gpa")
    prev_akts = col2.number_input("Previous total AKTS (failed included)",
                                  min_value=0, step=1, value=None,
                                  placeholder="e.g. 89", key=f"{key}_akts")
    return prev_gpa, prev_akts


def check_inputs(courses, prev_gpa, prev_akts):
    if not courses:
        st.warning("Please fill in at least one course completely.")
        return False
    if prev_gpa is None or prev_akts is None:
        st.warning("Please enter your previous GPA and AKTS "
                   "(enter 0 for both if this is your first semester).")
        return False
    return True

#       PAGE :

st.title("GPA CALCULATOR")

tab_average, tab_target, tab_estimate = st.tabs(
    ["🧮 Calculate GPA", "💡 Target GPA Scenarios", "🔮 Best/Worst Case"])

with tab_average:
    table = course_table("average_table", with_grade=True)
    prev_gpa, prev_akts = previous_inputs("average")

    if st.button("Calculate", key="average_btn"):
        courses = table_to_courses(table, with_grade=True)
        if check_inputs(courses, prev_gpa, prev_akts):
            res1, res2 = st.columns(2)
            res1.metric("Semester GPA", f"{semester_gpa(courses):.2f}")
            res2.metric("Total GPA", f"{total_gpa(courses, prev_gpa, prev_akts):.2f}")

with tab_target:
    table = course_table("target_table", with_grade=False)
    prev_gpa, prev_akts = previous_inputs("target")
    target = st.number_input("Target GPA", min_value=0.0, max_value=4.0,
                             step=0.01, value=None, placeholder="e.g. 3.00",
                             key="target_goal")

    if st.button("Find scenarios", key="target_btn"):
        planned = table_to_courses(table, with_grade=False)
        if not check_inputs(planned, prev_gpa, prev_akts):
            pass
        elif target is None:
            st.warning("Please enter your target GPA.")
        elif required_semester_gpa(planned, prev_gpa, prev_akts, target) > 4.0:
            st.error("Impossible this semester, even with all AA's.")
        else:
            with st.spinner("Calculating scenarios..."):
                scenarios = find_scenarios(planned, prev_gpa, prev_akts, target)
            rows = []
            for gpa, courses in scenarios:
                row = {"Total GPA": f"{gpa:.2f}"}
                for name, _, note, _ in courses:
                    row[name] = note
                rows.append(row)
            st.success(f"Top {len(rows)} closest scenarios")
            st.dataframe(pd.DataFrame(rows, index=range(1, len(rows) + 1)))

with tab_estimate:
    table = course_table("estimate_table", with_grade=False)
    prev_gpa, prev_akts = previous_inputs("estimate")

    if st.button("Estimate", key="estimate_btn"):
        planned = table_to_courses(table, with_grade=False)
        if check_inputs(planned, prev_gpa, prev_akts):
            columns = st.columns(len(SCENARIOS))
            for col, (label, grade) in zip(columns, SCENARIOS.items()):
                courses = assign_grade(planned, grade)
                col.metric(f"{label} (all {grade})",
                           f"{total_gpa(courses, prev_gpa, prev_akts):.2f}")
                col.caption(f"Semester: {semester_gpa(courses):.2f}")