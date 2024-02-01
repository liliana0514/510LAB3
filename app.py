import sqlite3
import streamlit as st
from pydantic import BaseModel
import streamlit_pydantic as sp
from datetime import datetime
from enum import Enum

# Database Connection
con = sqlite3.connect("todoapp.sqlite", check_same_thread=False, isolation_level=None)
cur = con.cursor()

# Create Table with New Schema
cur.execute(
    """
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        name TEXT,
        description TEXT,
        state TEXT,
        created_at DATETIME,
        created_by TEXT,
        category TEXT
    )
    """
)

# Enum for Task State
class State(Enum):
    planned = "planned"
    in_progress = "in-progress"
    done = "done"

# Data Model with Extended Fields
class Task(BaseModel):
    name: str
    description: str
    state: State = State.planned
    created_at: datetime = datetime.now()
    created_by: str
    category: str

# Function to Retrieve Unique Categories
def get_unique_categories():
    cur.execute("SELECT DISTINCT category FROM tasks WHERE category IS NOT NULL AND category != ''")
    return [row[0] for row in cur.fetchall()]

# Toggle State Function
def toggle_state(row_id, current_state):
    new_state = "done" if current_state != "done" else "planned"
    cur.execute("UPDATE tasks SET state = ? WHERE id = ?", (new_state, row_id))

# Delete Task Function
def delete_task(row_id):
    cur.execute("DELETE FROM tasks WHERE id = ?", (row_id,))

# Initialize session state for submission status
if 'submitted' not in st.session_state:
    st.session_state['submitted'] = False

# Main App Function
def main():
    st.title("Todo App")

    # Form to Add New Task
    task_data = sp.pydantic_form(key="task_form", model=Task)
    if task_data:
        cur.execute(
            "INSERT INTO tasks (name, description, state, created_at, created_by, category) VALUES (?, ?, ?, ?, ?, ?)",
            (task_data.name, task_data.description, task_data.state.value, task_data.created_at.strftime("%Y-%m-%d %H:%M:%S"), task_data.created_by, task_data.category),
        )
        st.session_state['submitted'] = True

    if st.session_state['submitted']:
        st.info("Task added successfully!")

    # Display Tasks Heading
    st.write("## Task List")

    # Search and Filter
    search_query = st.text_input("Search tasks")
    unique_categories = get_unique_categories()
    filter_category = st.selectbox("Filter by category", options=[""] + unique_categories)

    # Task List Display
    query = "SELECT * FROM tasks WHERE (name LIKE ? OR description LIKE ?)"
    params = [f"%{search_query}%", f"%{search_query}%"]
    if filter_category:
        query += " AND category = ?"
        params.append(filter_category)
    tasks = cur.execute(query, params).fetchall()

    for row in tasks:
        cols = st.columns([1, 3, 3, 1, 2, 2, 2, 1, 1])
        cols[0].write(row[0])  # id
        cols[1].write(row[1])  # name
        cols[2].write(row[2])  # description
        state_label = str(row[3]) if row[3] else 'planned'  # Convert state to string for button label
        cols[3].button(str(state_label), key=f"state_{row[0]}", on_click=toggle_state, args=(row[0], state_label))
        cols[4].write(row[4])  # created_at
        cols[5].write(row[5])  # created_by
        cols[6].write(row[6])  # category
        cols[7].button("Delete", key=f"delete_{row[0]}", on_click=delete_task, args=(row[0],))

main()
