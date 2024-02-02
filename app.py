import sqlite3
from datetime import datetime
import streamlit as st
from pydantic import BaseModel, Field
from enum import Enum
import streamlit_pydantic as sp 

# Set page config to centered mode
st.set_page_config(layout="centered")

# Enums for task state and category
class State(str, Enum):
    planned = "Planned"
    in_progress = "In-Progress"
    done = "Done"

class Category(str, Enum):
    school = "School"
    work = "Work"
    personal = "Personal"

# Database connection setup
DB_PATH = "todoapp.sqlite"
con = sqlite3.connect(DB_PATH, check_same_thread=False)
con.row_factory = sqlite3.Row  # Enables accessing columns by name
cur = con.cursor()

# Create tasks table with the corrected schema
cur.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT NOT NULL,
        state TEXT NOT NULL,
        created_at TEXT NOT NULL,
        created_by TEXT NOT NULL,
        created_due TEXT NOT NULL,
        category TEXT NOT NULL
    )
""")

# Pydantic model to define the structure of a task
class Task(BaseModel):
    name: str
    description: str
    state: State = Field(default=State.planned)
    created_at: datetime = Field(default_factory=datetime.now)
    created_by: str
    created_due: datetime = Field(default_factory=datetime.now)
    category: Category

# Function to delete a task by ID
def delete_task(task_id: int):
    cur.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    con.commit()

def main():
    st.title("Todo App")

    # Create a Form using the streamlit-pydantic package, just pass it the Task Class
    task_data = sp.pydantic_form(key="task_form", model=Task)
    if task_data:
        # Convert Pydantic model to dict for SQLite insertion
        task_dict = task_data.dict()
        task_dict["created_at"] = task_dict["created_at"].strftime("%Y-%m-%d %H:%M:%S")
        task_dict["created_due"] = task_dict["created_due"].strftime("%Y-%m-%d %H:%M:%S")
        cur.execute("""
            INSERT INTO tasks (name, description, state, created_at, created_by, created_due, category)
            VALUES (:name, :description, :state, :created_at, :created_by, :created_due, :category)
        """, task_dict)
        con.commit()
        st.success("Task added successfully!")

    # Task search and filter with an "All" category option
    search_query = st.text_input("Search by name")
    filter_category = st.selectbox("Filter by category", ["All"] + [e.value for e in Category])

    # Display tasks with column titles
    st.write("## Task List")
    title_cols = st.columns([1, 2, 2, 2, 2, 2, 2, 2, 2])
    titles = ["ID", "Name", "Description", "State", "Created at", "Created by", "Due date", "Category", "Delete"]
    for col, title in zip(title_cols, titles):
        col.write(title)

    if filter_category == "All":
        query = "SELECT * FROM tasks WHERE name LIKE '%' || :search_query || '%'"
        params = {"search_query": search_query}
    else:
        query = "SELECT * FROM tasks WHERE name LIKE '%' || :search_query || '%' AND category = :filter_category"
        params = {"search_query": search_query, "filter_category": filter_category}

    tasks = cur.execute(query, params).fetchall()
    for task in tasks:
        cols = st.columns([1, 2, 2, 2, 2, 2, 2, 2, 2])
        cols[0].write(task["id"])
        cols[1].write(task["name"])
        cols[2].write(task["description"])
        cols[3].write(task["state"])
        cols[4].write(task["created_at"])
        cols[5].write(task["created_by"])
        cols[6].write(task["created_due"])
        cols[7].write(task["category"])
        if cols[8].button("Delete", key=f"delete_{task['id']}"):
            delete_task(task["id"])
            st.experimental_rerun()

if __name__ == "__main__":
    main()

