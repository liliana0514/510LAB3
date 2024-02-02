# TECHIN 510 Lab 3

Data storage and retrieval using Python.

## Overview
Hi! This is the repository for my personal To-Do list for TECHIN 510.  
This code outlines a Streamlit web application for managing tasks, showcasing the use of SQLite for storage, Pydantic for data validation, and Streamlit for the web interface.  
It demonstrates key concepts like database operations, form handling, and dynamic content update in a web app.
[Click](https://ph46-techin510-lab3.azurewebsites.net/)) here to my website.

## How to Run
Create a gitignore as your first step! Put the following In your gitignore file! Do NOT commit the sqlite files!
```
*.sqlite
*.sqlite3
*.db
```

Put the following in your requirements.txt file
```
streamlit-pydantic
pydantic==1.10.14
psycopg2-binary==2.9.9
```

Open the terminal and run the following commands:
```    
pip install -r requirements.txt 
pip install streamlit
pip install pydantic
pip install streamlit-pydantic
pip install psycopg2
```

Run the app using the command in the terminal
```bash
streamlit run app.py
```
## Detailed Comment for Every Part
- Streamlit Configuration
- Enums for Task States and Categories
- Database Connection and Table Setup
- Pydantic Model for Task Structure
- Delete Task Function
- Main Function

## Lessons Learned

- The application demonstrates how to integrate SQLite, Pydantic, and Streamlit to build a simple yet functional web application.
- Learn about creating and interacting with SQLite databases using Python's `sqlite3` module, including creating tables, inserting data, and querying the database.
- The use of Pydantic models for data validation and structure definition is illustrated. 

## Questions / Uncertainties

- How does Streamlit manage state, especially in response to user actions like deleting a task? 


## Contact

- Liliana Hsu
# TECHIN510
