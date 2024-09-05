import calendar
from datetime import datetime, timedelta
from sqlalchemy import text
from models import *
from fixtures import *


def create_database_schema():
    """
    Creates the database schema and populates it with initial data.

    This function initializes the database by creating all tables defined in the models.
    It then populates the database with initial data for training plans and weight categories
    using predefined fixtures. Each training plan and weight category is added to the database
    and committed in a single transaction.

    The initial data includes:
        - Training plans with details such as name, price, number of sessions, and permissions.
        - Weight categories with details such as name, minimum weight, and maximum weight.

    Returns:
        None
    """

    db.create_all()
    for plan, details in training_plans.items():
        training_plan = TrainingPlan(
            name=plan,
            price=details["price"],
            num_of_sessions=details["num_of_sessions"],
            can_attend_competitions=details["can_attend_competitions"],
            can_attend_private_coaching=details["can_attend_private_coaching"],
            private_coaching_max_sessions=details["private_coaching_max_sessions"],
        )
        db.session.add(training_plan)

    for category, weight in weight_categories.items():
        weight_category = WeightCategory(
            name=category, min_weight=weight["min"], max_weight=weight["max"])
        db.session.add(weight_category)

    db.session.commit()


def get_week_start_end_dates(dt=None):
    """
    Calculates the start and end dates of the week containing the given date.

    This function determines the start and end dates of the week for the provided date.
    If no date is provided, it defaults to the current date. The week is assumed to start
    on Monday and end on Sunday.

    Parameters:
        dt (datetime.date, optional): The date for which to calculate the week start and end dates. Defaults to the current date.

    Returns:
        tuple: A tuple containing two datetime.date objects:
            - week_start (datetime.date): The start date of the week (Monday).
            - week_end (datetime.date): The end date of the week (Sunday).
    """

    if not dt:
        today = datetime.today().date()
    else:
        today = datetime.strptime(dt, '%Y-%m-%d').date()

    start = today - timedelta(days=today.weekday())
    end = start + timedelta(days=6)
    start = start.strftime('%Y-%m-%d')
    end = end.strftime('%Y-%m-%d')
    return start, end


def get_athelete_training_plan(athlete_id):
    """
    Retrieves the details of a specific training plan.

    This function queries the database to find the training plan associated with the given training plan ID.
    It returns the training plan object containing all the details of the training plan.

    Parameters:
        training_plan_id (int): The ID of the training plan.

    Returns:
        TrainingPlan: The training plan object containing the details of the training plan.
    """

    athlete_plan = Athlete.query.filter_by(
        id=athlete_id).first().training_plan
    return athlete_plan


def get_training_plan(training_plan_id):
    """
    Retrieves the training plan ID for a given athlete.

    This function queries the database to find the training plan associated with the specified athlete.
    It returns the training plan ID of the athlete.

    Parameters:
        athlete_id (int): The ID of the athlete.

    Returns:
        int: The ID of the training plan associated with the athlete.
    """

    training_plan = TrainingPlan.query.filter_by(
        id=training_plan_id).first()

    return training_plan


# def athlete_training_sessions_this_week(athlete_id):
#     """
#     Returns the number of training sessions for a given athlete in the current week.

#     Parameters:
#     athlete_id (int): The ID of the athlete.

#     Returns:
#     int: The number of training sessions for the athlete in the current week.
#     """

#     week_start, week_end = get_week_start_end_dates()

#     sessions = TrainingSession.query.filter_by(
#         athlete_id=athlete_id).filter(TrainingSession.date.between(week_start, week_end)).all()

#     return len(sessions)


def can_athlete_register_training_session(athlete_id, dt=None):
    """
    Checks if an athlete can register for a training session within a given week.

    This function verifies if the athlete's training plan allows for additional training sessions
    by checking the number of sessions the athlete has already registered for in the specified week.
    It retrieves the athlete's training plan, calculates the start and end dates of the week containing
    the provided date, and counts the number of training sessions the athlete has in that week.

    Parameters:
        athlete_id (int): The ID of the athlete.
        dt (datetime.date, optional): The date for which to check the registration eligibility. Defaults to the current date.

    Returns:
        bool: True if the athlete can register for the training session, False otherwise.
    """

    athlete_plan = get_athelete_training_plan(athlete_id)
    training_plan = get_training_plan(athlete_plan)

    week_start, week_end = get_week_start_end_dates(dt)

    sessions = TrainingSession.query.filter_by(
        athlete_id=athlete_id).filter(TrainingSession.date.between(week_start, week_end)).all()

    return len(sessions) < training_plan.num_of_sessions


def can_athlete_register_coaching_session(athlete_id, dt=None):
    """
    Determines if an athlete can register for a private coaching session within a given week.

    This function checks if the athlete's training plan allows for private coaching sessions and
    whether the athlete has reached the maximum number of allowed private coaching sessions for the week.
    It retrieves the athlete's training plan, calculates the start and end dates of the week containing
    the provided date, and counts the number of private coaching sessions the athlete has in that week.

    Parameters:
        athlete_id (int): The ID of the athlete.
        dt (datetime.date, optional): The date for which to check the registration eligibility. Defaults to the current date.

    Returns:
        bool: True if the athlete can register for a private coaching session, False otherwise.
    """

    athlete_plan = get_athelete_training_plan(athlete_id)
    training_plan = get_training_plan(athlete_plan)

    week_start, week_end = get_week_start_end_dates(dt)

    sessions = CoachingSession.query.filter_by(
        athlete_id=athlete_id).filter(CoachingSession.date.between(week_start, week_end)).all()

    if training_plan.can_attend_private_coaching:
        return len(sessions) < training_plan.private_coaching_max_sessions
    else:
        return False


def is_second_saturday(date):
    """
    Check if a given date falls on the second Saturday of the month.

    Parameters:
    - date (str): The date to be checked in the format "YYYY-MM-DD".

    Returns:
    - bool: True if the date falls on the second Saturday of the month, False otherwise.
    """

    dt = datetime.strptime(date, "%Y-%m-%d")
    cal = calendar.monthcalendar(dt.year, dt.month)

    if cal[0][calendar.SATURDAY]:
        second_saturday = cal[1][calendar.SATURDAY]
    else:
        second_saturday = cal[2][calendar.SATURDAY]

    return dt.day == second_saturday


def get_competitions_summary(athlete_id):
    """
    Retrieves a summary of all competitions, including the number of participants for each competition.

    This function queries the database to fetch details of all competitions, such as the competition name,
    date, entry fee, weight category, and the number of participants registered for each competition.
    The results are returned as a list of dictionaries, each representing a competition and its summary details.

    Returns:
        list: A list of dictionaries, each containing the following keys:
            - id (int): The unique identifier of the competition.
            - name (str): The name of the competition.
            - date (datetime.date): The date of the competition.
            - entry_fee (float): The entry fee for the competition.
            - weight_category (str): The weight category of the competition.
            - participants_count (int): The number of participants registered for the competition.
    """

    with db.engine.connect() as conn:
        query = """
            select cp.name, cp.date, cp.entry_fee from competition_registrations as cr
                join competitions as cp on cp.id = cr.competition_id
                where cr.athlete_id = %d
            """ % athlete_id

        raw = conn.execute(text(query))
        competitions = raw.fetchall()

    return competitions


def calculate_competition_fees(athlete_id):
    """
    Calculates the total competition fees for an athlete within a specified date range.

    This function queries the database to sum up the entry fees for all competitions
    the athlete has participated in between the given start and end dates.

    Parameters:
        athlete_id (int): The ID of the athlete.
        start_date (datetime.date): The start date of the period for which to calculate the fees.
        end_date (datetime.date): The end date of the period for which to calculate the fees.

    Returns:
        float: The total competition fees for the athlete within the specified date range.
    """

    with db.engine.connect() as conn:
        query = """
        select sum(cp.entry_fee) from competition_registrations as cr
	        join competitions as cp on cp.id = cr.competition_id
	        where cr.athlete_id = %d
        """ % athlete_id

        raw = conn.execute(text(query))
        competitions = raw.fetchall()

    return competitions[0][0] if competitions[0][0] else 0


def training_sessions_per_week(athlete_id):
    """
    Retrieves the number of training sessions an athlete has attended per week.

    This function queries the database to count the number of training sessions
    attended by a specific athlete, grouped by week. It returns a list of records,
    each containing the week number, start date, end date, and the number of sessions
    attended in that week.

    Parameters:
        athlete_id (int): The ID of the athlete.

    Returns:
        list: A list of tuples, each containing the week number, week start date, week end date,
              and the number of training sessions attended in that week.
    """

    with db.engine.connect() as conn:
        query = """
        select strftime('%%W', date) WeekNumber,
            max(date(date, 'weekday 0', '-7 day')) WeekStart, max(date(date, 'weekday 0', '-1 day')) WeekEnd,
            count(*) as NumSessions
            from training_sessions
            where athlete_id = %d group by WeekNumber
        """ % athlete_id

        raw = conn.execute(text(query))
        training_sessions = raw.fetchall()

        return training_sessions


def calculate_training_fees(athlete_id):
    """
    Calculates the total training fees for an athlete within a specified date range.

    This function queries the database to sum up the fees for all training sessions
    and private coaching sessions attended by the athlete between the given start and end dates.

    Parameters:
        athlete_id (int): The ID of the athlete.
        start_date (datetime.date): The start date of the period for which to calculate the fees.
        end_date (datetime.date): The end date of the period for which to calculate the fees.

    Returns:
        float: The total training fees for the athlete within the specified date range.
    """
    training_sessions = training_sessions_per_week(athlete_id)
    num_of_weeks = len(training_sessions)
    athlete_plan_fee = get_training_plan(
        get_athelete_training_plan(athlete_id)).price
    total_fee = num_of_weeks * athlete_plan_fee

    return total_fee


def coaching_sessions_per_week(athlete_id):
    """
    Retrieves the number of private coaching sessions an athlete has in a given week.

    This function queries the database to count the number of private coaching sessions
    for a specific athlete within the week starting from the provided date.

    Parameters:
        athlete_id (int): The ID of the athlete.
        week_start_date (datetime.date): The start date of the week for which to count the sessions.

    Returns:
        int: The number of private coaching sessions the athlete has in the specified week.
    """

    with db.engine.connect() as conn:
        query = """
        select strftime('%%W', date) WeekNumber,
            max(date(date, 'weekday 0', '-7 day')) WeekStart, max(date(date, 'weekday 0', '-1 day')) WeekEnd,
            count(*) as NumSessions, sum(tuition_fees) as 'total_fees'
            from coaching_sessions
            where athlete_id = %d group by WeekNumber
        """ % athlete_id

        raw = conn.execute(text(query))
        coaching_sessions = raw.fetchall()

        return coaching_sessions
