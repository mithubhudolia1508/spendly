# Spec: Login and Logout

## Overview
Implement login and logout so registered users can authenticate and end their session. This step upgrades the existing stub `GET /login` route into a fully functional form that accepts a POST, verifies credentials against the `users` table, and stores the authenticated user's ID in the Flask session. The stub `GET /logout` route is replaced with a handler that clears the session and redirects to the landing page. After this step, all future features (profile, expense CRUD) can gate access behind a session check.

## Depends on
- Step 01 — Database setup (`users` table, `get_db()`)
- Step 02 — Registration (`create_user()`, verified password hashing)

## Routes
- `GET /login` — render login form — public (already exists as stub, upgrade it)
- `POST /login` — validate credentials, set session, redirect to `/expenses` or next — public
- `GET /logout` — clear session, redirect to `/` — logged-in (already exists as stub, upgrade it)

## Database changes
No new tables or columns.

A new DB helper must be added to `database/db.py`:
- `get_user_by_email(email)` — returns a single `sqlite3.Row` from `users` where email matches, or `None` if not found. Used by the login route to look up the user and verify the password.

## Templates
- **Modify**: `templates/login.html`
  - Change the form `action` to `url_for('login')` with `method="post"`
  - Add `name` attributes to inputs: `email`, `password`
  - Add a block to display flash error messages (e.g. "Invalid email or password")
  - Keep all existing visual design
- **Modify**: `templates/base.html`
  - Update the navbar: show **Logout** link (`url_for('logout')`) when `session.user_id` is set; show **Login** and **Register** links when not logged in

## Files to change
- `app.py` — upgrade `login()` to handle `GET` and `POST`; upgrade `logout()` to clear session and redirect; import `session` from Flask; import `get_user_by_email` from `database.db`
- `database/db.py` — add `get_user_by_email(email)` helper
- `templates/login.html` — wire up form action/method and flash message display
- `templates/base.html` — add conditional nav links based on session state

## Files to create
None.

## New dependencies
No new dependencies. Uses `werkzeug.security.check_password_hash` (already installed) and Flask's built-in `session`, `flash`, `redirect`, `url_for`.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — never use f-strings in SQL
- Verify passwords with `werkzeug.security.check_password_hash` — never compare plaintext
- Store only `session['user_id'] = user['id']` in the Flask session — never store the full user row or password hash
- On login failure, always return the generic message "Invalid email or password" — never reveal which field was wrong
- On login success, redirect to `url_for('expenses')` (placeholder route) or `/` if that route doesn't exist yet
- `logout()` must call `session.clear()` before redirecting — do not just delete `user_id`
- All templates extend `base.html`
- Use CSS variables — never hardcode hex values
- Use `url_for()` for every internal link — never hardcode URLs

## Definition of done
- [ ] `GET /login` renders the login form without errors
- [ ] Submitting valid credentials sets `session['user_id']` and redirects away from `/login`
- [ ] Submitting an unregistered email re-renders the form with "Invalid email or password" — no session set
- [ ] Submitting a wrong password for a valid email re-renders the form with "Invalid email or password" — no session set
- [ ] Submitting with empty fields re-renders the form with a validation error — no session set
- [ ] `GET /logout` clears the session and redirects to `/`
- [ ] After logout, navigating to `/login` shows the login form (session is gone)
- [ ] Navbar shows Login/Register when logged out and Logout when logged in
