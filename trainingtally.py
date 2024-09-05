#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session
from sqlalchemy import text
from models import *
from helpers import *


app = Flask(__name__)
app.secret_key = '97e55e1619aefaa8128ce991145ab3aa'
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:///database.db"
)
db.init_app(app)


def login_required(f):
    """
    A decorator function that checks if a user is logged in before allowing access to a route.

    Parameters:
    - f: The function to be decorated

    Returns:
    - decorated_function: The decorated function that checks if the user is logged in before executing the original function.

    Usage:
    @login_required
    def my_route():
        # Code for the route
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


@app.route("/create-database")
def create_database():
    """
    Creates a database if it does not already exist.

    If the database file "./instance/database.db" exists, it prints a message indicating that the database already exists 
    and advises the user to contact the administrator to reset the database. 
    Otherwise, it creates the database schema using the `create_database_schema` function from the `helpers` module.

    Returns:
        A rendered template indicating whether the database was created or not. 
        If the database already exists, the template will have the `dbexist` parameter set to `True`, otherwise it will be set to `False`.
    """

    if os.path.exists("./instance/database.db"):
        print('Database already exists. Contact your administrator to reset the database.')
        return render_template("dbcreated.html", dbexist=True)

    create_database_schema()
    return render_template("dbcreated.html", dbexist=False)


@app.route("/")
def home():
    """
    Redirects the user to the dashboard route.

    Returns:
        A redirect response to the dashboard route.
    """

    return redirect(url_for("dashboard"))


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Route for handling user login.

    This route is responsible for authenticating the user's login credentials.
    If the request method is POST, it retrieves the username and password from the form data.
    If the username is "admin" and the password is "admin", it sets the session variables
    "logged_in" to True, "user" to the username, and "fullname" to "Gym Administrator".
    Finally, it redirects the user to the dashboard route.
    If the request method is not POST, it renders the login.html template.

    Returns:
        If the request method is POST, it redirects the user to the dashboard route.
        If the request method is not POST, it renders the login.html template.
    """

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == "admin" and password == "admin":
            session["logged_in"] = True
            session["user"] = username
            session["fullname"] = "Gym Administrator"
        return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    """
    Clears the session and redirects the user to the login page.

    Returns:
        A redirect response to the login page.
    """

    session.clear()
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    """
    Route handler for the dashboard page.

    Retrieves the count of athletes, competitions, training sessions, and coaching sessions from the database.
    Renders the dashboard.html template with the retrieved data.

    Returns:
        The rendered template for the dashboard page.
    """

    athletes = Athlete.query.count()
    competitions = Competition.query.count()
    training_sessions = TrainingSession.query.count()
    coaching_sessions = CoachingSession.query.count()

    data = {
        "athletes": athletes,
        "competitions": competitions,
        "training_sessions": training_sessions,
        "coaching_sessions": coaching_sessions
    }
    return render_template("dashboard.html", data=data, pageIs='dashboard')


@app.route("/add-athlete", methods=["GET", "POST"])
@login_required
def add_athlete():
    """
    Handles the addition of a new athlete to the database.

    GET:
        Renders a form to add a new athlete. The form includes a list of all available training plans.

    POST:
        Processes the form submission to add a new athlete. Retrieves the form data, creates a new athlete
        instance, and saves it to the database. Redirects the user to the list of athletes upon successful addition.

    Returns:
        render_template: The rendered template for adding an athlete (GET).
        redirect: Redirects to the list of athletes upon successful addition (POST).
    """

    if request.method == "GET":
        TrainingPlans = TrainingPlan.query.all()
        return render_template("add-athlete.html", pageIs='athletes', training_plans=TrainingPlans)

    # Get form data
    fullname = request.form["fullname"]
    gender = request.form["gender"]
    age = int(request.form["age"])
    weight = float(request.form["weight"])
    training_plan = request.form["training_plan"]

    # Create new athlete
    athlete = Athlete(
        fullname=fullname,
        gender=gender,
        weight=weight,
        age=age,
        training_plan=training_plan
    )
    db.session.add(athlete)
    db.session.commit()

    return redirect(url_for("list_athletes"))


@app.route("/update-athlete", methods=["POST"])
@login_required
def update_athlete():
    """
    Update the details of an athlete in the database.

    Parameters:
    - athlete_id (int): The ID of the athlete to be updated.
    - fullname (str): The full name of the athlete.
    - gender (str): The gender of the athlete.
    - age (int): The age of the athlete.
    - weight (float): The weight of the athlete.

    Returns:
    - redirect: Redirects to the view_athlete route with the updated athlete's ID.
    """

    # Get form data
    athlete_id = request.form["athlete_id"]
    fullname = request.form["fullname"]
    gender = request.form["gender"]
    age = int(request.form["age"])
    weight = float(request.form["weight"])

    # Update athlete details
    athlete = Athlete.query.filter_by(id=athlete_id).first()
    athlete.fullname = fullname
    athlete.gender = gender
    athlete.age = age
    athlete.weight = weight
    db.session.commit()

    return redirect(url_for("view_athlete", athlete_id=athlete_id))


@app.route("/view-athlete/<int:athlete_id>", methods=["GET"])
@login_required
def view_athlete(athlete_id):
    """
    Renders the view-athlete page with different tabs based on the active_tab parameter.

    This route handler retrieves the athlete's details and renders the "view-athlete.html" template. It also
    determines which tab should be active based on the "tab" query parameter. If the "tab" parameter is not
    provided or is invalid, the default tab "profile" is selected.

    Parameters:
        athlete_id (int): The ID of the athlete to be viewed.

    Returns:
        render_template: The rendered "view-athlete.html" template with the appropriate tab content based on the active_tab parameter.
    """

    # Select active tab
    allowed_tabs = ["profile", "training-sessions",
                    "private-coaching", "payments", "competitions"]

    active_tab = request.args.get("tab", None)
    if not active_tab or active_tab not in allowed_tabs:
        active_tab = "profile"

    # Get athlete details. Required in all tabs
    athlete = Athlete.query.filter_by(id=athlete_id).first()

    # Render the profile tab
    #
    if active_tab == "profile":

        # Get all training plans
        training_plans = TrainingPlan.query.all()

        return render_template("view-athlete.html",
                               pageIs='athletes',
                               active_tab=active_tab,
                               athlete=athlete,
                               training_plans=training_plans)

    # Render training sessions tab
    #
    if active_tab == "training-sessions":
        training_sessions = TrainingSession.query.filter_by(
            athlete_id=athlete_id).all()

        return render_template("view-athlete.html",
                               pageIs='athletes',
                               active_tab=active_tab,
                               athlete=athlete,
                               training_sessions=training_sessions)

    # Render private coaching tab
    #
    if active_tab == "private-coaching":
        coaching_sessions = CoachingSession.query.filter_by(
            athlete_id=athlete_id).all()

        return render_template("view-athlete.html",
                               pageIs='athletes',
                               active_tab=active_tab,
                               athlete=athlete,
                               coaching_sessions=coaching_sessions)

    # Render competitions tab
    #
    if active_tab == "competitions":
        competitions = get_competitions_summary(athlete_id)

        return render_template("view-athlete.html",
                               pageIs='athletes',
                               active_tab=active_tab,
                               athlete=athlete,
                               competitions=competitions)

    # Render payments tab
    #
    if active_tab == "payments":

        athlete_plan_fee = get_training_plan(
            get_athelete_training_plan(athlete_id)).price

        training_summary = training_sessions_per_week(athlete_id)
        training_fees = calculate_training_fees(athlete_id)

        coaching_summary_fees = coaching_sessions_per_week(athlete_id)
        coaching_fees = sum([coaching[4]
                            for coaching in coaching_summary_fees])

        competitions_summary = get_competitions_summary(athlete_id)
        competition_fees = calculate_competition_fees(athlete_id)

        total_payment = training_fees + coaching_fees + competition_fees

        return render_template("view-athlete.html",
                               pageIs='athletes',
                               active_tab=active_tab,
                               athlete=athlete,
                               athlete_plan_fee=athlete_plan_fee,
                               training_summary=training_summary,
                               training_fees=training_fees,
                               coaching_summary_fees=coaching_summary_fees,
                               competitions_summary=competitions_summary,
                               competition_fees=competition_fees,
                               total_payment=total_payment)


@app.route("/list-athletes", methods=["GET"])
@login_required
def list_athletes():
    """
    Retrieves list of athletes from the database and renders them in a template.

    Returns:
        render_template: The rendered template containing the list of athletes.
    """

    with db.engine.connect() as conn:
        query = """
        select a.id, a.fullname, a.gender, a.age, 
        a.weight, t.name as 'training_plan', t.can_attend_competitions as 'can_attend_competitions'
        from athletes as a join training_plans as t on a.training_plan = t.id
        """

        athletes = conn.execute(text(query))
        results = athletes.all()

    return render_template("list-athletes.html", pageIs='athletes', athletes=results)


@app.route("/list-training-sessions", methods=["GET"])
@login_required
def list_training_sessions():
    """
    Retrieves a list of training sessions from the database and renders them in a template.

    This route handler connects to the database and executes a query to retrieve the count of training sessions
    for each athlete. The results are then passed to the "list-training-sessions.html" template for rendering.

    Returns:
        render_template: The rendered template containing the list of training sessions.
    """

    with db.engine.connect() as conn:
        query = """
        select a.id, fullname, count(*) as 'sessions' 
            from training_sessions as c 
            join athletes as a on c.athlete_id = a.id 
            group by athlete_id
        """
        training_sessions = conn.execute(text(query))
        results = training_sessions.all()

    return render_template("list-training-sessions.html", pageIs='training', training_sessions=results)


@app.route("/log-training-session", methods=["GET", "POST"])
@login_required
def log_training_session():
    """
    Handles the logging of a new training session for an athlete.

    GET:
        Renders a form to log a new training session. The form includes a list of all athletes.

    POST:
        Processes the form submission to log a new training session. Validates if the athlete can register
        a new session for the given date. If validation fails, an error message is displayed. If successful,
        the new training session is added to the database and the user is redirected to the list of training sessions.

    Returns:
        render_template: The rendered template for logging a training session (GET) or displaying an error (POST).
        redirect: Redirects to the list of training sessions upon successful logging of a session.
    """

    if request.method == "GET":
        athletes = Athlete.query.all()
        return render_template("log-training-session.html", pageIs='training', athletes=athletes)

    athlete_id = request.form["athlete_id"]
    session_dt = request.form["session_dt"]

    if not can_athlete_register_training_session(athlete_id, session_dt):
        return render_template("log-training-session.html", pageIs='training',
                               error="Athlete has reached the maximum number of sessions for the week.")

    training_session = TrainingSession(
        athlete_id=athlete_id,
        date=datetime.strptime(session_dt, "%Y-%m-%d")
    )

    db.session.add(training_session)
    db.session.commit()

    return redirect(url_for("list_training_sessions"))


@app.route("/add-competition", methods=["GET", "POST"])
@login_required
def add_competition():
    """
    Handles the addition of a new competition.

    GET:
        Renders a form to add a new competition. The form includes a list of all weight categories.

    POST:
        Processes the form submission to add a new competition. Validates the input data, ensuring that the
        competition date is the second Saturday of the month. If validation fails, an error message is displayed.
        If successful, the new competition is added to the database and the user is redirected to the list of competitions.

    Returns:
        render_template: The rendered template for adding a competition (GET) or displaying an error (POST).
        redirect: Redirects to the list of competitions upon successful addition of a competition.
    """

    if request.method == "GET":
        weight_categories = WeightCategory.query.all()
        return render_template("add-competition.html", pageIs='competitions', weight_categories=weight_categories)

    name = request.form.get("name", None)
    date = request.form.get("date", None)
    weight_category = request.form.get("weight_category", None)
    entry_fee = request.form.get("entry_fee", None)

    if not date or not is_second_saturday(date):
        return render_template("add-competition.html", pageIs='competitions',
                               error="Competition date must be on the second Saturday of the month.")

    competition = Competition(
        name=name,
        date=date,
        weight_category=weight_category,
        entry_fee=entry_fee
    )
    db.session.add(competition)
    db.session.commit()

    return redirect(url_for("list_competitions"))


@app.route("/list-competitions", methods=["GET"])
@login_required
def list_competitions():
    """
    Retrieves a list of competitions from the database and renders them in a template.

    This route handler connects to the database and executes a query to retrieve details of all competitions,
    including the competition name, date, entry fee, number of participants, and weight category. The results
    are then passed to the "list-competitions.html" template for rendering.

    Returns:
        render_template: The rendered template containing the list of competitions.
    """

    query = """
    select c.id, c.name as competition_name, c.date, c.entry_fee,
        count(cr.id) as participants_count, concat(wc.name, ' (', wc.max_weight, ' kg)' ) as weight_category
        from competitions as c
        left join competition_registrations as cr on c.id = cr.competition_id
        join weight_categories as wc on c.weight_category = wc.id
        group by c.name
        """

    with db.engine.connect() as conn:
        result = conn.execute(text(query))
        competitions = result.fetchall()

    return render_template("list-competitions.html", pageIs='competitions', competitions=competitions)


@app.route("/view-competition/<int:competition_id>", methods=["GET"])
@login_required
def view_competition(competition_id):
    """
    Retrieves detailed information about a specific competition and its participants, then renders them in a template.

    This route handler executes two queries:
    1. Retrieves the competition details, including its name, date, and weight category.
    2. Retrieves the list of participants registered for the competition, including their names and weights.

    The results of these queries are then passed to the "view-competition.html" template for rendering.

    Args:
        competition_id (int): The unique identifier of the competition to be viewed.

    Returns:
        render_template: The rendered template containing the competition details and list of participants.
    """

    with db.engine.connect() as conn:
        query = """
        select c.id, c.name, c.date, concat(wc.name, ' (', wc.max_weight, ' kg)' ) as 'weight', wc.id as 'weight_id' 
            from competitions as c 
            join weight_categories as wc on c.weight_category = wc.id
            where c.id = %d
        """ % competition_id
        result = conn.execute(text(query))
        competition = result.fetchone()

    with db.engine.connect() as conn:
        query = """
        select cr.id, a.fullname, a.weight
            from competition_registrations as cr
            join athletes as a on cr.athlete_id = a.id
            where cr.competition_id = %d
        """ % competition_id
        result = conn.execute(text(query))
        participants = result.fetchall()

    return render_template("view-competition.html", pageIs='competitions', competition=competition, participants=participants)


@app.route("/add-competition-participant/<int:competition_id>/<int:weight_cat>", methods=["GET", "POST"])
@login_required
def add_competition_participant(competition_id, weight_cat):
    """
    Handles the addition of an athlete to a specific competition.

    GET:
        Renders a form to add a new participant to the competition. The form includes a list of eligible athletes
        based on their weight category and training plan.

    POST:
        Processes the form submission to add a new participant to the competition. Validates the input data and
        ensures the athlete meets the criteria for the competition. If validation fails, an error message is displayed.
        If successful, the new participant is added to the competition and the user is redirected to the competition details page.

    Args:
        competition_id (int): The unique identifier of the competition.
        weight_cat (int): The weight category ID to filter eligible athletes.

    Returns:
        render_template: The rendered template for adding a competition participant (GET) or displaying an error (POST).
        redirect: Redirects to the competition details page upon successful addition of a participant.
    """

    if request.method == "GET":

        query = """
        select at.id, at.fullname, at.weight from training_plans as tp 
            left join athletes as at on tp.id = at.training_plan 
		    join weight_categories as wc on wc.id = %d
		    where tp.can_attend_competitions = 1
		    and at.weight between wc.min_weight and wc.max_weight
        """ % weight_cat

        with db.engine.connect() as conn:
            result = conn.execute(text(query))
            athletes = result.fetchall()

        if len(athletes) == 0:
            return render_template("add-competition-participant.html",
                                   pageIs='competitions',
                                   competition_id=competition_id,
                                   error="No athletes found eligible for the selected weight category.")

        return render_template("add-competition-participant.html",
                               pageIs='competitions',
                               competition_id=competition_id,
                               weight_id=weight_cat,
                               athletes=athletes)

    athlete_id = request.form["athlete_id"]
    registration = CompetitionRegistration(
        competition_id=competition_id,
        athlete_id=athlete_id
    )
    db.session.add(registration)
    db.session.commit()

    return redirect(url_for("view_competition", competition_id=competition_id))


@app.route("/list-private-coaching", methods=["GET"])
@login_required
def list_private_coaching():
    """
    Retrieves a list of private coaching sessions from the database and renders them in a template.

    This route handler connects to the database and executes a query to retrieve the count of private coaching sessions
    for each athlete. The results are then passed to the "list-coaching-sessions.html" template for rendering.

    Returns:
        render_template: The rendered template containing the list of private coaching sessions.
    """

    with db.engine.connect() as conn:
        query = """
        select a.id, fullname, count(*) as 'sessions' 
            from coaching_sessions as c 
            join athletes as a on c.athlete_id = a.id 
            group by athlete_id
        """
        res = conn.execute(text(query))
        coaching_sessions = res.all()
    return render_template("list-coaching-sessions.html", pageIs='coaching', coaching_sessions=coaching_sessions)


@app.route("/log-coaching-session", methods=["GET", "POST"])
@login_required
def log_private_coaching():
    """
    Handles the logging of a new private coaching session for an athlete.

    GET:
        Renders a form to log a new private coaching session. The form includes a list of all athletes.

    POST:
        Processes the form submission to log a new private coaching session. Validates if the athlete can register
        a new session for the given date. If validation fails, an error message is displayed. If successful,
        the new private coaching session is added to the database and the user is redirected to the list of private coaching sessions.

    Returns:
        render_template: The rendered template for logging a private coaching session (GET) or displaying an error (POST).
        redirect: Redirects to the list of private coaching sessions upon successful logging of a session.
    """

    if request.method == "GET":
        athletes = Athlete.query.all()
        return render_template("log-coaching-session.html", pageIs='coaching', athletes=athletes)

    athlete_id = request.form["athlete_id"]
    session_dt = request.form["session_dt"]
    tuition_fees = request.form["tuition_fees"]

    if not can_athlete_register_coaching_session(athlete_id, session_dt):
        return render_template("log-coaching-session.html", pageIs='coaching',
                               error="Athlete has reached the maximum number of private coaching sessions for the week.")

    coaching_session = CoachingSession(
        athlete_id=athlete_id,
        date=datetime.strptime(session_dt, "%Y-%m-%d"),
        tuition_fees=tuition_fees
    )

    db.session.add(coaching_session)
    db.session.commit()

    return redirect(url_for("list_private_coaching"))


if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')
