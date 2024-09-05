

training_plans = {
    "beginner": {
        "price": 250,
        "num_of_sessions": 2,
        "can_attend_competitions": False,
        "can_attend_private_coaching": True,
        "private_coaching_max_sessions": 5,
    },
    "intermediate": {
        "price": 300,
        "num_of_sessions": 3,
        "can_attend_competitions": True,
        "can_attend_private_coaching": True,
        "private_coaching_max_sessions": 5,
    },
    "elite": {
        "price": 350,
        "num_of_sessions": 5,
        "can_attend_competitions": True,
        "can_attend_private_coaching": True,
        "private_coaching_max_sessions": 5,
    },
}

weight_categories = {
    "flyweight": {
        "min": 15,
        "max": 66
    },
    "lightweight":
    {
        "min": 66,
        "max": 73
    },
    "light-middleweight": {
        "min": 73,
        "max": 80
    },
    "middleweight": {
        "min": 80,
        "max": 90
    },
    "light-heavyweight": {
        "min": 90,
        "max": 100
    },
    "heavyweight": {
        "min": 100,
        "max": 1000
    }
}
