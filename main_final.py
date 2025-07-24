import streamlit as st
import sqlite3
import pandas as pd

# Connect to DB
conn = sqlite3.connect("students.db")

# Streamlit Config
st.set_page_config(page_title="🎓 Placement App", layout="wide")
st.title("🎓 Placement Eligibility Streamlit App")

# Sidebar Filters
st.sidebar.header("📊 Filter Criteria")
cgpa = st.sidebar.slider("Minimum CGPA", 0.0, 10.0, 7.0)
backlogs = st.sidebar.slider("Max Backlogs", 0, 10, 1)
programming_score = st.sidebar.slider("Min Programming Score", 0, 100, 60)
comm_score = st.sidebar.slider("Min Communication", 1, 10, 5)
teamwork_score = st.sidebar.slider("Min Teamwork", 1, 10, 5)
leadership_score = st.sidebar.slider("Min Leadership", 1, 10, 5)

# Main Filter Query
query = f"""
SELECT s.*, p.programming_score, ss.communication, ss.teamwork, ss.leadership, pl.company, pl.salary
FROM students s
JOIN programming p ON s.student_id = p.student_id
JOIN soft_skills ss ON s.student_id = ss.student_id
JOIN placements pl ON s.student_id = pl.student_id
WHERE s.cgpa >= {cgpa}
  AND s.backlogs <= {backlogs}
  AND p.programming_score >= {programming_score}
  AND ss.communication >= {comm_score}
  AND ss.teamwork >= {teamwork_score}
  AND ss.leadership >= {leadership_score}
"""

df = pd.read_sql_query(query, conn)

st.subheader("🎯 Eligible Students")
st.dataframe(df)

# Insights
col1, col2 = st.columns(2)
with col1:
    st.metric("Eligible Students", df.shape[0])
with col2:
    avg_salary = df["salary"].mean() if not df.empty else 0
    st.metric("Avg Salary", f"₹ {int(avg_salary):,}")

# BONUS: SQL Queries
st.subheader("💎 Bonus SQL Insights")

query1 = "SELECT name, cgpa FROM students WHERE cgpa > 9"
st.markdown("**1. CGPA > 9**")
st.dataframe(pd.read_sql_query(query1, conn))

query2 = """
SELECT s.name, p.programming_score 
FROM students s 
JOIN programming p ON s.student_id = p.student_id 
WHERE p.programming_score > 90
"""
st.markdown("**2. Programming Score > 90**")
st.dataframe(pd.read_sql_query(query2, conn))

query3 = """
SELECT s.name, ss.teamwork 
FROM students s 
JOIN soft_skills ss ON s.student_id = ss.student_id 
WHERE ss.teamwork = 10
"""
st.markdown("**3. Perfect Teamwork = 10**")
st.dataframe(pd.read_sql_query(query3, conn))

# Add other queries up to 10...

# Close DB
conn.close()
