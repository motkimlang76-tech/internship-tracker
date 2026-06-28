import sqlite3
from pathlib import Path

from flask import Flask, redirect, render_template, request, url_for


app = Flask(__name__)
DATABASE = Path(__file__).with_name("tracker.db")


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


def get_status_counts():
    statuses = ["Saved", "Applied", "Interview", "Offer"]
    connection = get_db_connection()
    total = connection.execute("SELECT COUNT(*) FROM jobs").fetchone()[0]

    counts = []
    for status in statuses:
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
    statuses = ["All", "Saved", "Applied", "Interview", "Offer"]
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
        sql += " AND (LOWER(company) LIKE ? OR LOWER(role) LIKE ?)"
        search_pattern = f"%{search_query.lower()}%"
        params.extend([search_pattern, search_pattern])

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
        company = request.form.get("company", "").strip()
        role = request.form.get("role", "").strip()
        location = request.form.get("location", "").strip()
        website = request.form.get("website", "").strip()
        status = request.form.get("status", "Saved").strip()
        deadline = request.form.get("deadline", "").strip()
        notes = request.form.get("notes", "").strip()

        connection = get_db_connection()
        connection.execute(
            """
            INSERT INTO jobs (company, role, location, website, status, deadline, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (company, role, location, website, status, deadline, notes),
        )
        connection.commit()
        connection.close()

        return redirect(url_for("jobs"))

    return render_template("new_job.html")


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
        company = request.form.get("company", "").strip()
        role = request.form.get("role", "").strip()
        location = request.form.get("location", "").strip()
        website = request.form.get("website", "").strip()
        status = request.form.get("status", "Saved").strip()
        deadline = request.form.get("deadline", "").strip()
        notes = request.form.get("notes", "").strip()

        connection.execute(
            """
            UPDATE jobs
            SET company = ?, role = ?, location = ?, website = ?, status = ?, deadline = ?, notes = ?
            WHERE id = ?
            """,
            (company, role, location, website, status, deadline, notes, job_id),
        )
        connection.commit()
        connection.close()

        return redirect(url_for("jobs"))

    connection.close()
    return render_template("edit_job.html", job=job)


@app.route("/jobs/<int:job_id>/delete", methods=["POST"])
def delete_job(job_id):
    connection = get_db_connection()
    connection.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
    connection.commit()
    connection.close()

    return redirect(url_for("jobs"))


if __name__ == "__main__":
    app.run(debug=True)
