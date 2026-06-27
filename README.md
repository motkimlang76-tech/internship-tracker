# Internship Application Tracker

A beginner full-stack project built with Python, Flask, HTML, CSS, and SQLite.

## Features

- Add internship or job applications.
- View all saved applications.
- Search applications by company or role.
- Filter applications by status.
- Edit an application.
- Delete an application.
- See a dashboard with totals and recent jobs.

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

## Learning Notes

See `LEARNING_NOTES.md` for the Khmer notes from the code walkthrough.
