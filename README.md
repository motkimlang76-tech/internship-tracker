# Internship Application Tracker

A beginner full-stack project built with Python, Flask, HTML, CSS, and SQLite.

This app helps a student or job seeker track internship and job applications in one place.

## Tech Stack

- Python
- Flask
- SQLite
- HTML
- CSS
- Jinja templates

## Features

- Add internship or job applications.
- View all saved applications.
- Search applications by company or role.
- Filter applications by status.
- Edit an application.
- Delete an application.
- Save a company website link.
- See a dashboard with totals and recent jobs.

## App Flow

```text
HTML form -> Flask route -> SQLite database -> Flask template -> HTML page
```

Example add-job flow:

```text
User fills the Add Job form
-> Browser sends POST data to Flask
-> Flask reads request.form
-> Flask inserts the job into SQLite
-> Flask redirects to the jobs page
-> jobs.html displays the saved job
```

## First Run

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install Flask:

```bash
python -m pip install -r requirements.txt
```

Run the app:

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## What This First Version Teaches

- `app.py` creates the Flask app.
- `@app.route("/")` creates the home page route.
- `render_template("home.html")` sends an HTML file to the browser.
- `GET` opens a page or form.
- `POST` submits form data.
- `SELECT`, `INSERT`, `UPDATE`, and `DELETE` are used to work with database data.
- `WHERE` chooses the exact row to read, update, or delete.
- `commit()` saves database changes.
- `home.html`, `jobs.html`, and other template files are the page structure.
- `styles.css` controls the design.

## Project Explanation

I built an Internship Application Tracker using Flask, SQLite, HTML, and CSS.
The app can add, view, search, filter, edit, and delete internship applications.
I learned how HTML forms send data to Flask, how Flask saves data to SQLite,
and how templates show database data back to the user.

## Learning Notes

See `LEARNING_NOTES.md` for the Khmer notes from the code walkthrough.
