import sqlite3
import streamlit as st
from pydantic import BaseModel
import streamlit_pydantic as sp
from datetime import datetime
from enum import Enum

# Database Connection
con = sqlite3.connect("todoapp.sqlite", isolation_level=None)
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

# Data Model with Extended Fields
class State(Enum):
    planned = "planned"
    in_progress = "in-progress"
    done = "done"

class Task(BaseModel):
    name: str
    description: str
    state: State
    created_at: datetime = datetime.now()
    created_by: str
    category: str

# Toggle State Function
def toggle_state(state, row_id):
    new_state = "done" if state != "done" else "planned"
    cur.execute("UPDATE tasks SET state = ? WHERE id = ?", (new_state, row_id))

# Delete Task Function
def delete_task(row_id):
    cur.execute("DELETE FROM tasks WHERE id = ?", (row_id,))

# Main App Function
def main():
    st.title("Todo App")

    # Form to Add New Task
    with st.form(key="task_form"):
        data = sp.pydantic_form(key="my_form", model=Task)
        submit_button = st.form_submit_button(label='Add Task')

    if submit_button and data:
        cur.execute(
            "INSERT INTO tasks (name, description, state, created_at, created_by, category) VALUES (?, ?, ?, ?, ?, ?)",
            (data.name, data.description, data.state.value, data.created_at.strftime("%Y-%m-%d %H:%M:%S"), data.created_by, data.category),
        )

    # Display Tasks
    st.write("## Task List")
    tasks = cur.execute("SELECT * FROM tasks").fetchall()
    for row in tasks:
        cols = st.columns([1, 2, 3, 2, 2, 1, 1])
        cols[0].write(row[0])
        cols[1].write(row[1])
        cols[2].write(row[2])
        cols[3].write(row[3])
        cols[4].write(row[4])
        cols[5].button("Toggle State", key=f"toggle_{row[0]}", on_click=toggle_state, args=(row[3], row[0]))
        cols[6].button("Delete", key=f"delete_{row[0]}", on_click=delete_task, args=(row[0],))

main()
