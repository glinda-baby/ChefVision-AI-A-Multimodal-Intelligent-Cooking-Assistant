import pandas as pd
import ast

# load dataset
data = pd.read_csv("dataset/recipes.csv")

# convert column names to lowercase
data.columns = data.columns.str.lower()


def recommend_recipe(user_ingredients):

    user_ingredients = [i.strip().lower() for i in user_ingredients]

    best_recipe = None
    best_score = 0

    for _, row in data.iterrows():

        try:
            recipe_ingredients = ast.literal_eval(row["ingredients"])
        except:
            recipe_ingredients = []

        recipe_ingredients = [str(i).lower() for i in recipe_ingredients]

        score = 0

        for user_ing in user_ingredients:
            for rec_ing in recipe_ingredients:
                if user_ing in rec_ing:
                    score += 1
                    break

        # update best recipe
        if score > best_score:
            best_score = score
            best_recipe = row

    # require at least 2 ingredient matches
    if best_recipe is not None and best_score >= 3:
        return {
            "title": best_recipe["title"],
            "ingredients": best_recipe["ingredients"],
            "instructions": best_recipe["instructions"],
        }

    return None