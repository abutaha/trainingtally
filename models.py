from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class TrainingPlan(db.Model):
    class TrainingPlan:
        """
        Represents a training plan for gym members.

        Attributes:
            id (int): The unique identifier of the training plan.
            name (str): The name of the training plan.
            price (float): The price of the training plan.
            num_of_sessions (int): The number of sessions included in the training plan.
            can_attend_competitions (bool): Indicates whether the member can attend competitions.
            can_attend_private_coaching (bool): Indicates whether the member can attend private coaching.
            private_coaching_max_sessions (int): The maximum number of private coaching sessions allowed for the member.
        """

    __tablename__ = "training_plans"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)
    num_of_sessions = db.Column(db.Integer)
    can_attend_competitions = db.Column(db.Boolean)
    can_attend_private_coaching = db.Column(db.Boolean)
    private_coaching_max_sessions = db.Column(db.Integer)


class WeightCategory(db.Model):
    """
    Represents a weight category in the gym app.

    Attributes:
        id (int): The unique identifier of the weight category.
        name (str): The name of the weight category.
        weight (int): The weight of the weight category.
        min_weight (float): The minimum weight allowed in the weight category.
        max_weight (float): The maximum weight allowed in the weight category.
    """

    __tablename__ = "weight_categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    weight = db.Column(db.Integer)
    min_weight = db.Column(db.Float)
    max_weight = db.Column(db.Float)


class Athlete(db.Model):
    """
    Represents an athlete in the gym app.

    Attributes:
        id (int): The unique identifier of the athlete.
        fullname (str): The full name of the athlete.
        gender (str): The gender of the athlete.
        age (int): The age of the athlete.
        weight (float): The weight of the athlete.
        training_plan (int): The ID of the training plan assigned to the athlete.
    """

    __tablename__ = "athletes"

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String)
    gender = db.Column(db.String)
    age = db.Column(db.Integer)
    weight = db.Column(db.Float)
    training_plan = db.Column(db.Integer)


class Competition(db.Model):
    """
    Represents a competition in the gym app.

    Attributes:
        id (int): The unique identifier of the competition.
        name (str): The name of the competition.
        date (str): The date of the competition.
        entry_fee (float): The entry fee for the competition.
        weight_category (int): The weight category for the competition.
    """

    __tablename__ = "competitions"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    date = db.Column(db.String)
    entry_fee = db.Column(db.Float)
    weight_category = db.Column(db.Integer)


class CompetitionRegistration(db.Model):
    """
    Represents athlete registration for a competition in the gym app.

    Attributes:
        id (int): The unique identifier of the registration.
        competition_id (int): The ID of the competition for which the registration is made.
        athlete_id (int): The ID of the athlete who is registering for the competition.
    """

    __tablename__ = "competition_registrations"

    id = db.Column(db.Integer, primary_key=True)
    competition_id = db.Column(db.Integer)
    athlete_id = db.Column(db.Integer)


class TrainingSession(db.Model):
    """
    Represents a training session.

    Attributes:
        id (int): The unique identifier of the training session.
        date (datetime.date): The date of the training session.
        athlete_id (int): The ID of the athlete associated with the training session.
    """

    __tablename__ = "training_sessions"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    athlete_id = db.Column(db.Integer)


class CoachingSession(db.Model):
    """
    Represents a private coaching session.

    Attributes:
        id (int): The unique identifier for the coaching session.
        date (date): The date of the coaching session.
        athlete_id (int): The ID of the athlete participating in the coaching session.
        tuition_fees (float): The tuition fees for the coaching session.
    """

    __tablename__ = "coaching_sessions"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    athlete_id = db.Column(db.Integer)
    tuition_fees = db.Column(db.Float)
