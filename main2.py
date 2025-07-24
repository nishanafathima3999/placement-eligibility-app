import streamlit as st
import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect("students.db")

st.title("🎓 Placement Eligibility - SQL Query Explorer")

# Dropdown to choose a query
query_options = {
    "1. Students with CGPA ≥ 7 and no backlogs":
        "SELECT * FROM students WHERE cgpa >= 7.0 AND backlogs = 0;",

    "2. Students with programming score ≥ 80":
        """
        SELECT s.student_id, s.name, p.programming_score
        FROM students s
        JOIN programming p ON s.student_id = p.student_id
        WHERE p.programming_score >= 80;
        """,

    "3. Students with excellent soft skills (≥8 all)":
        """
        SELECT s.student_id, s.name, ss.*
        FROM students s
        JOIN soft_skills ss ON s.student_id = ss.student_id
        WHERE ss.communication >= 8 AND ss.teamwork >= 8 AND ss.leadership >= 8;
        """,

    "4. Students with CGPA ≥ 6.5 and Programming ≥ 70":
        """
        SELECT s.name, s.cgpa, p.programming_score
        FROM students s
        JOIN programming p ON s.student_id = p.student_id
        WHERE s.cgpa >= 6.5 AND p.programming_score >= 70;
        """,

    "5. Students placed in companies with salary ≥ ₹5L":
        """
        SELECT s.name, pl.company, pl.salary
        FROM students s
        JOIN placements pl ON s.student_id = pl.student_id
        WHERE pl.salary >= 500000;
        """,

    "6. Top 5 Students with Highest CGPA":
        "SELECT name, cgpa FROM students ORDER BY cgpa DESC LIMIT 5;",

    "7. Count of Students by Backlogs":
        """
        SELECT backlogs, COUNT(*) AS student_count
        FROM students
        GROUP BY backlogs
        ORDER BY backlogs;
        """,

    "8. Avg Programming Score (Placed vs Not Placed)":
        """
        SELECT 
          CASE 
            WHEN pl.company IS NOT NULL THEN 'Placed' 
            ELSE 'Not Placed' 
          END AS placement_status,
          AVG(p.programming_score) AS avg_programming_score
        FROM students s
        LEFT JOIN programming p ON s.student_id = p.student_id
        LEFT JOIN placements pl ON s.student_id = pl.student_id
        GROUP BY placement_status;
        """,

    "9. All-Rounder Students":
        """
        SELECT s.name
        FROM students s
        JOIN programming p ON s.student_id = p.student_id
        JOIN soft_skills ss ON s.student_id = ss.student_id
        WHERE s.cgpa >= 8 AND p.programming_score >= 85 AND
              ss.communication >= 8 AND ss.teamwork >= 8 AND ss.leadership >= 8;
        """,

    "10. Students Not Yet Placed":
        """
        SELECT s.student_id, s.name
        FROM students s
        LEFT JOIN placements pl ON s.student_id = pl.student_id
        WHERE pl.company IS NULL;
        """
}

# Select box for choosing a query
selected_query = st.selectbox("📌 Choose a Query to Run:", list(query_options.keys()))

# Run the selected query
df = pd.read_sql_query(query_options[selected_query], conn)

# Show result
st.dataframe(df)

# Close connection
conn.close()
