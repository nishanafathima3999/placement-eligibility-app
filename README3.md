## 🔧 Backend Logic

The backend is implemented using a SQLite database (`students.db`) and SQL queries embedded inside the Streamlit app (`main.py`). The app uses `pd.read_sql_query()` to filter eligible students dynamically based on user input.

### ✅ Features Used:
- SQL query filtering with joins across 4 tables (`students`, `programming`, `soft_skills`, `placements`)
- Object-Oriented modules used in `studenttable.ipynb`
- Streamlit used for interactive UI in `main.py`

### 🗂️ Backend File: [`main.py`](./main.py)
