import sqlite3
from pathlib import Path

from flask import Flask, redirect, render_template, request, url_for


app = Flask(__name__)
DATABASE = Path(__file__).with_name("tracker.db")
STATUSES = ["Saved", "Applied", "Interview", "Offer", "Rejected"]


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_db_connection()
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            role TEXT NOT NULL,
            location TEXT,
            website TEXT,
            status TEXT NOT NULL,
            deadline TEXT,
            notes TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    columns = connection.execute("PRAGMA table_info(jobs)").fetchall()
    column_names = {column["name"] for column in columns}

    if "notes" not in column_names:
        connection.execute("ALTER TABLE jobs ADD COLUMN notes TEXT")

    if "deadline" not in column_names:
        connection.execute("ALTER TABLE jobs ADD COLUMN deadline TEXT")

    if "website" not in column_names:
        connection.execute("ALTER TABLE jobs ADD COLUMN website TEXT")

    connection.commit()
    connection.close()


init_db()


def empty_job_form():
    return {
        "company": "",
        "role": "",
        "location": "",
        "website": "",
        "status": "Saved",
        "deadline": "",
        "notes": "",
    }


def get_job_form_data():
    website = request.form.get("website", "").strip()
    if website and not website.startswith(("http://", "https://")):
        website = f"https://{website}"

    status = request.form.get("status", "Saved").strip()
    if status not in STATUSES:
        status = "Saved"

    return {
        "company": request.form.get("company", "").strip(),
        "role": request.form.get("role", "").strip(),
        "location": request.form.get("location", "").strip(),
        "website": website,
        "status": status,
        "deadline": request.form.get("deadline", "").strip(),
        "notes": request.form.get("notes", "").strip(),
    }


def validate_job_form(form_data):
    if not form_data["company"] or not form_data["role"]:
        return "Company and role are required."

    return None


def get_status_counts():
    connection = get_db_connection()
    total = connection.execute("SELECT COUNT(*) FROM jobs").fetchone()[0]

    counts = []
    for status in STATUSES:
        count = connection.execute(
            "SELECT COUNT(*) FROM jobs WHERE status = ?", (status,)
        ).fetchone()[0]
        counts.append({"label": status, "count": count})

    connection.close()
    return total, counts


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/dashboard")
def dashboard():
    total_jobs, status_counts = get_status_counts()

    connection = get_db_connection()
    recent_jobs = connection.execute(
        "SELECT * FROM jobs ORDER BY created_at DESC LIMIT 5"
    ).fetchall()
    connection.close()

    return render_template(
        "dashboard.html",
        total_jobs=total_jobs,
        status_counts=status_counts,
        recent_jobs=recent_jobs,
    )


@app.route("/jobs")
def jobs():
    statuses = ["All", *STATUSES]
    selected_status = request.args.get("status", "All")
    search_query = request.args.get("q", "").strip()

    if selected_status not in statuses:
        selected_status = "All"

    connection = get_db_connection()
    sql = "SELECT * FROM jobs WHERE 1 = 1"
    params = []

    if selected_status != "All":
        sql += " AND status = ?"
        params.append(selected_status)

    if search_query:
        sql += (
            " AND (LOWER(company) LIKE ? OR LOWER(role) LIKE ? "
            "OR LOWER(location) LIKE ?)"
        )
        search_pattern = f"%{search_query.lower()}%"
        params.extend([search_pattern, search_pattern, search_pattern])

    sql += " ORDER BY created_at DESC"
    all_jobs = connection.execute(sql, params).fetchall()

    connection.close()

    return render_template(
        "jobs.html",
        jobs=all_jobs,
        selected_status=selected_status,
        search_query=search_query,
        statuses=statuses,
    )


@app.route("/jobs/new", methods=["GET", "POST"])
def new_job():
    if request.method == "POST":
        form_data = get_job_form_data()
        error = validate_job_form(form_data)

        if error:
            return render_template(
                "new_job.html",
                error=error,
                form_data=form_data,
                statuses=STATUSES,
            )

        connection = get_db_connection()
        connection.execute(
            """
            INSERT INTO jobs (company, role, location, website, status, deadline, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                form_data["company"],
                form_data["role"],
                form_data["location"],
                form_data["website"],
                form_data["status"],
                form_data["deadline"],
                form_data["notes"],
            ),
        )
        connection.commit()
        connection.close()

        return redirect(url_for("jobs"))

    return render_template(
        "new_job.html",
        error=None,
        form_data=empty_job_form(),
        statuses=STATUSES,
    )


@app.route("/jobs/<int:job_id>/edit", methods=["GET", "POST"])
def edit_job(job_id):
    connection = get_db_connection()
    job = connection.execute(
        "SELECT * FROM jobs WHERE id = ?", (job_id,)
    ).fetchone()

    if job is None:
        connection.close()
        return redirect(url_for("jobs"))

    if request.method == "POST":
        form_data = get_job_form_data()
        error = validate_job_form(form_data)

        if error:
            connection.close()
            return render_template(
                "edit_job.html",
                error=error,
                job=form_data,
                statuses=STATUSES,
            )

        connection.execute(
            """
            UPDATE jobs
            SET company = ?, role = ?, location = ?, website = ?, status = ?, deadline = ?, notes = ?
            WHERE id = ?
            """,
            (
                form_data["company"],
                form_data["role"],
                form_data["location"],
                form_data["website"],
                form_data["status"],
                form_data["deadline"],
                form_data["notes"],
                job_id,
            ),
        )
        connection.commit()
        connection.close()

        return redirect(url_for("jobs"))

    connection.close()
    return render_template("edit_job.html", error=None, job=job, statuses=STATUSES)


@app.route("/jobs/<int:job_id>/delete", methods=["POST"])
def delete_job(job_id):
    connection = get_db_connection()
    connection.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
    connection.commit()
    connection.close()

    return redirect(url_for("jobs"))


if __name__ == "__main__":
    app.run(debug=True)
