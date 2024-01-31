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
        is_done BOOLEAN,
        created_at DATETIME,
        created_by TEXT,
        category TEXT
    )
    """
)

# Data Model with Extended Fields
class Task(BaseModel):
    name: str
    description: str
    is_done: bool = False
    created_at: datetime = datetime.now()
    created_by: str
    category: str

# Toggle is_done Function
def toggle_is_done(row_id):
    cur.execute("UPDATE tasks SET is_done = NOT is_done WHERE id = ?", (row_id,))

# Delete Task Function
def delete_task(row_id):
    cur.execute("DELETE FROM tasks WHERE id = ?", (row_id,))

# Main App Function
def main():
    st.title("Todo App")

    # Search and Filter
    search_query = st.text_input("Search tasks")
    filter_category = st.selectbox("Filter by category", options=[""] + ['school', 'work', 'personal'])

    # Form to Add New Task
    with st.form(key="task_form"):
        data = sp.pydantic_form(key="my_form", model=Task)
        submit_button = st.form_submit_button(label='Add Task')
    
    if submit_button and data:
        cur.execute(
            "INSERT INTO tasks (name, description, is_done, created_at, created_by, category) VALUES (?, ?, ?, ?, ?, ?)",
            (data.name, data.description, data.is_done, data.created_at.strftime("%Y-%m-%d %H:%M:%S"), data.created_by, data.category),
        )

    # Display Tasks
    st.write("## Task List")
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
        cols[3].checkbox("Done", value=row[3], key=f"done_{row[0]}", on_change=toggle_is_done, args=(row[0],))
        cols[4].write(row[4])  # created_at
        cols[5].write(row[5])  # created_by
        cols[6].write(row[6])  # category
        cols[7].button("Delete", key=f"delete_{row[0]}", on_click=delete_task, args=(row[0],))

main()
