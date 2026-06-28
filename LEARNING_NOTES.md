# Learning Notes / កំណត់ត្រាមេរៀន

These are the notes from our `app.py` walkthrough.
នេះជាកំណត់ត្រាពីការអាន `app.py` ជាមួយគ្នា។

## Main Idea

This project is a small full-stack web app:
Project នេះជា full-stack web app តូចមួយ:

- Frontend: HTML and CSS pages in `templates/` and `static/`.
- Backend: Python Flask code in `app.py`.
- Database: SQLite file created as `tracker.db` when the app runs.

## app.py Summary

- `tracker.db` is the SQLite database file.
- `get_db_connection()` opens a connection between Python and SQLite.
- `init_db()` prepares the database and creates the `jobs` table.
- `jobs` table is like a spreadsheet for job applications.
- `commit()` saves database changes.
- Route means URL maps to a Python function.
- `render_template()` shows an HTML file in the browser.

ខ្លីៗ:

- `tracker.db` គឺជា database file។
- `get_db_connection()` គឺ function សម្រាប់ connect Python ទៅ SQLite។
- `init_db()` រៀបចំ database និងបង្កើត `jobs` table។
- `jobs` table ដូចជា spreadsheet សម្រាប់រក្សាទិន្នន័យ job។
- `commit()` មានន័យថា save changes។
- Route គឺ URL ភ្ជាប់ទៅ Python function។
- `render_template()` បង្ហាញ HTML file នៅ browser។

## Flask Flow

```text
Browser URL -> Flask route -> Python function -> HTML page
```

Examples:

```text
/          -> home()      -> home.html
/dashboard -> dashboard() -> dashboard.html
/jobs      -> jobs()      -> jobs.html
```

## Full-Stack Flow / Flow សំខាន់

```text
HTML ផ្ញើ data ទៅ Flask។
Flask save data ទៅ SQLite។
Flask យក data ពី SQLite។
HTML បង្ហាញ data ឲ្យ user។
```

Short version:

```text
Form -> Flask -> SQLite -> Flask -> HTML page
```

## Add Job Flow

```text
User បញ្ចូល form
-> ចុច Save job
-> Flask route /jobs/new ទទួល data
-> Flask ប្រើ request.form យក data
-> INSERT ទៅ SQLite
-> redirect ទៅ /jobs
-> jobs.html បង្ហាញ job ថ្មី
```

## Edit Job Flow

```text
User ចុច Edit
-> Flask route /jobs/<id>/edit យក job មួយពី SQLite
-> edit_job.html បង្ហាញ data ចាស់
-> User ប្តូរ data
-> Flask UPDATE job នៅ SQLite
-> redirect ទៅ /jobs
-> jobs.html បង្ហាញ data ថ្មី
```

## Delete Job Flow

```text
User ចុច Delete
-> Browser សួរ confirm
-> Form ផ្ញើ POST ទៅ /jobs/<id>/delete
-> Flask DELETE job ពី SQLite
-> redirect ទៅ /jobs
-> jobs.html មិនបង្ហាញ job នោះទៀត
```

## Company Website Feature

To add a new field like `website`, we changed these parts:

- Database: add `website` column.
- Add form: add `input name="website"`.
- Flask add route: read `request.form.get("website")` and INSERT it.
- Edit form: show old website value.
- Flask edit route: UPDATE `website`.
- Jobs/dashboard pages: show `{{ job.website }}` as a link.

ចាំ pattern នេះ:

```text
New field = database + form + Flask save/update + display
```

## Database Words

- `SELECT` reads data.
- `INSERT` creates new data.
- `UPDATE` edits existing data.
- `DELETE` removes data.
- `WHERE` chooses the exact row.
- `COUNT(*)` counts rows.
- `LIKE` searches similar text.

## Form Words

- `GET` opens a page or form.
- `POST` submits form data.
- `request.form["company"]` reads the `company` input from the form.
- `redirect(url_for("jobs"))` sends the user back to the jobs list page.

ចងចាំ:

- `GET` = open page/form។
- `POST` = submit form data។
- `request.form["company"]` = យក value ពី input field `company`។
- `redirect(url_for("jobs"))` = នាំ user ទៅ jobs list page។

## Important Safety Rule

Always use `WHERE id = ?` when updating or deleting one job.

Without `WHERE`, SQL can update or delete every row in the table.

ត្រូវចាំជានិច្ច: ពេល `UPDATE` ឬ `DELETE` job មួយ ត្រូវប្រើ `WHERE id = ?`។

បើគ្មាន `WHERE`, SQL អាច update ឬ delete data ទាំងអស់ក្នុង table។
