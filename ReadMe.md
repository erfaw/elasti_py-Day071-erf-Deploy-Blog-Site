
# Personal Blog 🌶️📝✍️

This is a project which outputted from **[elasti_py/ Day071](https://github.com/erfaw/elasti_py/tree/master/Day071-erf)** repo.

| [Explain the path till here...](https://github.com/erfaw/elasti_py-Day071-erf-Deploy-Blog-Site#explain-the-path-till-here) 
| [Overview](https://github.com/erfaw/elasti_py-Day071-erf-Deploy-Blog-Site#overview) 
| [How to Run](https://github.com/erfaw/elasti_py-Day071-erf-Deploy-Blog-Site#-how-to-run) 
| [ER-Diagram](https://github.com/erfaw/elasti_py-Day071-erf-Deploy-Blog-Site#er-diagram) 
| [What I Learned](https://github.com/erfaw/elasti_py-Day071-erf-Deploy-Blog-Site#-what-i-learned) 
|



---
---
---
<br>
<br>
<br>
<br>

## Explain the path till here...
This project made at **[elasti_py/ Day057/ 3. Capstone Project](https://github.com/erfaw/elasti_py/tree/master/Day057-erf/3.%20Capstone%20Project)** for first time and improved many times in **[elasti_py/ Day059/ Upgraded Blog](https://github.com/erfaw/elasti_py/tree/master/Day059-erf/Upgraded%20Blog)** && **[elasti_py/ Day060/ 2. blog with contact form](https://github.com/erfaw/elasti_py/tree/master/Day060-erf/2.%20blog%20with%20contact%20form)** && **[elasti_py/ Day067/ Upgraded Upgraded Blog Site](https://github.com/erfaw/elasti_py/tree/master/Day067-erf/Upgraded%20Upgraded%20Blog%20Site)** with what we learned about `Flask` framework in general to learn through the Udemy course [`Udemy – 100-days-of-code: Python - Angela Yu`](https://www.udemy.com/course/100-days-of-code/).


## Overview
This project is a **personal blog web application** built with `Flask` and its related extensions.
Users can **create accounts**, **log in securely**, **publish blog posts**, **leave comments**, and interact with content shared by other users.
The application focuses on user authentication, content management, database integration, and building dynamic web experiences using Flask.

### Key Technologies Used:
* Flask
    * Flask-SQLAlchemy
    * Bootstrap-Flask
    * Flask-CKEditor
    * Flask-WTF
    * Flask-Login
    * Jinja2
    * Wekzeug Security
* SQLAlchemy
* SQLite
* Bootstrap 5
* HTML, CSS, JavaScript

### ER-Diagram
<img src="./assets/er-diagram/er-diagram-dark.jpg" width=50%>

## 🚀 How to Run
1. Ensure you have Python installed.

2. Clone the repository: 
    ```
    git clone https://github.com/erfaw/elasti_py-Day071-erf-Deploy-Blog-Site
    ```

3. Make Virtual Environment: 
    ```
    python -m venv .venv
    ```

    then on Git Bash: 
    ```
    source ./.venv/Scripts/activate
    ```

4. Install dependencies: 
    ```
    pip install requirements.txt
    ```

5. Make `.env` for `SECRET_KEY`:
    ```
    touch .env
    ```
    then inside it make a key-value pare like this: 
    ```
    SECRET_KEY="PUT_YOUR_KEY_HERE"
    ```
    then **fill it with a STRONG one!**

6. Run local (`DEBUG = True`): 
    ```
    python main.py
    ```

## 💡 What I Learned
* Building a ***full-stack web application*** using `Flask` and **its ecosystem**.
* Working with `SQLAlchemy ORM` and **designing relational database schemas**.
* Gaining a deeper understanding of SQLAlchemy `models`, `relationships`, and **database operations**.
* Implementing <u>**user authentication**</u>, <u>**registration**</u>, and <u>**login**</u> systems.
* Understanding **password security concepts**, including `hashing` and `salting`.
* Learning the importance of **securely storing user credentials** and sensitive data.
* Using `Jinja2` templates and understanding Python web application **templating systems**.
* Creating secure web forms with **CSRF protection** using `Flask-WTF`.
* Understanding `CSRF attacks` and **common web security vulnerabilities**.
* Developing greater awareness of fundamental `cybersecurity principles` in web applications.
* Applying `web design principles`, including **color theory**, **typography**, **user interface (UI)**, and **user experience (UX)** design.
* Managing form validation and browser-side `validation behavior` for greater control over application logic.
* Understanding the role of `WSGI` and `Gunicorn` in deploying Python web applications.
