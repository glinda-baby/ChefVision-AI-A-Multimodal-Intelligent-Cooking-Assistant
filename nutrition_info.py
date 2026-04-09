import pandas as pd

# Load nutrition dataset
nutrition = pd.read_csv(
    "dataset/nutrition_dataset/nutrition.tsv",
    sep="\t",
    low_memory=False
)

# convert column names to lowercase
nutrition.columns = nutrition.columns.str.lower()

def get_nutrition(dish):

    result = nutrition[
        nutrition["product_name"].str.lower().str.contains(dish.lower(), na=False)
    ]

    if result.empty:
        return None

    item = result.iloc[0]

    return {
        "calories": item["energy_100g"],
        "protein": item["proteins_100g"],
        "carbs": item["carbohydrates_100g"],
        "fat": item["fat_100g"]
    }