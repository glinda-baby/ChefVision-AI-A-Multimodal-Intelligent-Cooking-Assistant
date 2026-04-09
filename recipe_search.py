import pandas as pd

data = pd.read_csv("dataset/recipes.csv")

# make all column names lowercase
data.columns = data.columns.str.lower()

def search_recipe(dish_name):

    result = data[
        data["title"].str.lower().str.contains(dish_name.lower(), na=False)
    ]

    if result.empty:
        return None

    recipe = result.iloc[0]

    return {
        "title": recipe["title"],
        "ingredients": recipe["ingredients"],
        "instructions": recipe["instructions"]
    }