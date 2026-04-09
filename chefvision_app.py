import streamlit as st
import pandas as pd
import ast

st.set_page_config(
    page_title="ChefVision AI",
    page_icon="🍳",
    layout="wide"
)

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>

.main {
background: linear-gradient(135deg,#ffecd2,#fcb69f);
}

h1 {
text-align:center;
color:#ff4b4b;
font-weight:800;
}

.recipe-card{
background:white;
padding:20px;
border-radius:15px;
box-shadow:0px 4px 15px rgba(0,0,0,0.15);
}

.stButton>button{
background:#ff4b4b;
color:white;
border-radius:10px;
height:45px;
width:200px;
font-size:16px;
font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# ---------- TITLE ----------
st.title("🍳 ChefVision AI")
st.caption("Your Smart Cooking Assistant")

# ---------- LOAD DATA ----------
data = pd.read_csv("dataset/recipes.csv")
data.columns = data.columns.str.lower()


# ---------- SEARCH FUNCTION ----------
def search_recipe(dish_name):
    result = data[data["title"].str.lower().str.contains(dish_name.lower(), na=False)]

    if not result.empty:
        return result.iloc[0]
    return None


# ---------- INGREDIENT MATCH ----------
def recommend_recipe(user_ing):

    user_ing = [i.strip().lower() for i in user_ing]

    best_recipe = None
    best_score = 0

    for _, row in data.iterrows():

        try:
            ingredients = ast.literal_eval(row["ingredients"])
        except:
            ingredients = []

        ingredients = [str(i).lower() for i in ingredients]

        score = 0

        for u in user_ing:
            for r in ingredients:
                if u in r:
                    score += 1
                    break

        if score > best_score:
            best_score = score
            best_recipe = row

    if best_recipe is not None and best_score >= 2:
        return best_recipe

    return None


# ---------- SIDEBAR ----------
st.sidebar.title("ChefVision Menu")

option = st.sidebar.selectbox(
    "Choose Feature",
    (
        "Home",
        "Image to Recipe",
        "Dish Search",
        "Ingredients to Recipe"
    )
)

# ---------- HOME ----------
if option == "Home":

    st.subheader("Welcome to ChefVision AI")

    col1, col2 = st.columns(2)

    with col1:
        st.image(
        "https://images.unsplash.com/photo-1498837167922-ddd27525d352",
        use_column_width=True
        )

    with col2:
        st.markdown("""
        ### Features

        📸 **Image to Recipe**  
        Upload food image and detect recipe.

        🍝 **Dish Search**  
        Search recipes instantly.

        🥕 **Ingredient Recommendation**  
        Find recipes using available ingredients.
        """)

# ---------- IMAGE MODULE ----------
elif option == "Image to Recipe":

    st.header("📸 Upload Food Image")

    img = st.file_uploader("Upload image", type=["jpg","png","jpeg"])

    if img:
        st.image(img, width=350)
        st.success("Image uploaded successfully!")

        st.info("Connect your computer vision model here.")


# ---------- DISH SEARCH ----------
elif option == "Dish Search":

    st.header("🍝 Search Recipe")

    dish = st.text_input("Enter dish name")

    if st.button("Find Recipe"):

        recipe = search_recipe(dish)

        if recipe is not None:

            st.markdown('<div class="recipe-card">', unsafe_allow_html=True)

            st.subheader(recipe["title"])

            st.markdown("### Ingredients")
            st.write(recipe["ingredients"])

            st.markdown("### Instructions")
            st.write(recipe["instructions"])

            st.markdown('</div>', unsafe_allow_html=True)

        else:

            st.error("Recipe not found")


# ---------- INGREDIENT SEARCH ----------
elif option == "Ingredients to Recipe":

    st.header("🥕 Find Recipe")

    ingredients = st.text_input(
        "Enter ingredients separated by comma",
        "egg, milk, bread"
    )

    if st.button("Recommend"):

        ing_list = ingredients.split(",")

        recipe = recommend_recipe(ing_list)

        if recipe is not None:

            st.markdown('<div class="recipe-card">', unsafe_allow_html=True)

            st.subheader(recipe["title"])

            st.markdown("### Ingredients")
            st.write(recipe["ingredients"])

            st.markdown("### Instructions")
            st.write(recipe["instructions"])

            st.markdown('</div>', unsafe_allow_html=True)

        else:

            st.error("No recipe found")