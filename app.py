import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from database.db import init_db, seed_db, create_user, get_user_by_email

app = Flask(__name__)
app.secret_key = "spendly-dev-secret"


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        return redirect(url_for("landing"))
    if request.method == "POST":
        name     = request.form.get("name", "").strip()
        email    = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm  = request.form.get("confirm_password", "")

        if not name or not email or not password or not confirm:
            return render_template("register.html", error="All fields are required.", name=name, email=email), 400

        if password != confirm:
            return render_template("register.html", error="Passwords do not match.", name=name, email=email), 400

        try:
            create_user(name, email, password)
        except sqlite3.IntegrityError:
            return render_template("register.html", error="Email already registered.", name=name, email=email), 400

        flash("Account created! Please sign in.")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("landing"))
    if request.method == "POST":
        email    = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not email or not password:
            return render_template("login.html", error="All fields are required."), 400

        user = get_user_by_email(email)
        if user is None or not check_password_hash(user["password_hash"], password):
            return render_template("login.html", error="Invalid email or password."), 401

        session.clear()
        session["user_id"] = user["id"]
        return redirect(url_for("profile"))

    return render_template("login.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))


@app.route("/profile")
def profile():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    user = {
        "name": "Demo User",
        "email": "demo@spendly.com",
        "initials": "D",
        "member_since": "01 May 2026",
    }

    stats = {
        "total_spent": "₹6,110",
        "transactions": 8,
        "top_category": "Shopping",
    }

    expenses = [
        {"date": "18 May 2026", "description": "Miscellaneous",   "category": "Other",         "amount": "₹600"},
        {"date": "15 May 2026", "description": "Metro recharge",   "category": "Transport",     "amount": "₹90"},
        {"date": "12 May 2026", "description": "Grocery haul",     "category": "Shopping",      "amount": "₹2,500"},
        {"date": "10 May 2026", "description": "Movie tickets",    "category": "Entertainment", "amount": "₹350"},
        {"date": "08 May 2026", "description": "Pharmacy",         "category": "Health",        "amount": "₹800"},
        {"date": "05 May 2026", "description": "Electricity bill", "category": "Bills",         "amount": "₹1,200"},
        {"date": "03 May 2026", "description": "Auto to office",   "category": "Transport",     "amount": "₹120"},
        {"date": "01 May 2026", "description": "Lunch at café",    "category": "Food",          "amount": "₹450"},
    ]

    categories = [
        {"name": "Shopping",      "amount": "₹2,500", "pct": 41},
        {"name": "Bills",         "amount": "₹1,200", "pct": 20},
        {"name": "Health",        "amount": "₹800",   "pct": 13},
        {"name": "Other",         "amount": "₹600",   "pct": 10},
        {"name": "Food",          "amount": "₹450",   "pct": 7},
        {"name": "Entertainment", "amount": "₹350",   "pct": 6},
        {"name": "Transport",     "amount": "₹210",   "pct": 3},
    ]

    return render_template("profile.html", user=user, stats=stats,
                           expenses=expenses, categories=categories)


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    init_db()
    seed_db()
    app.run(debug=True, port=5001)
