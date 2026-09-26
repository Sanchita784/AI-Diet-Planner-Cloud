def generate_diet_plan(age, goal):

    if goal == "weight_loss":

        plan = {
            "Breakfast": "Oats with fruits and milk",
            "Lunch": "2 chapati, dal, vegetables and salad",
            "Evening Snack": "Fruit or roasted chana",
            "Dinner": "2 chapati, vegetables and dal"
        }

    elif goal == "weight_gain":

        plan = {
            "Breakfast": "Oats, banana and milk",
            "Lunch": "Rice, dal, vegetables and curd",
            "Evening Snack": "Banana shake and nuts",
            "Dinner": "Chapati, vegetables, dal and paneer"
        }

    else:

        plan = {
            "Breakfast": "Oats with fruits and milk",
            "Lunch": "Chapati, dal, vegetables and salad",
            "Evening Snack": "Fruit or roasted chana",
            "Dinner": "Chapati, vegetables and dal"
        }

    return plan