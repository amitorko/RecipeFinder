import re
import html
import streamlit as st
from spoonacular_api import find_recipes_by_ingredients, get_recipe_details

st.set_page_config(
    page_title="Recipe Finder",
    page_icon="🍲",
    layout="wide"
)

# ---------- Helper functions ----------
def clean_html(raw_text):
    if not raw_text:
        return "No instructions available."
    clean_text = re.sub("<.*?>", "", raw_text)
    return html.unescape(clean_text)


# ---------- Custom CSS ----------
st.markdown(
    """
    <style>
    .main-title {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        color: #666;
        margin-bottom: 25px;
    }

    .recipe-card {
        border: 1px solid #e6e6e6;
        border-radius: 18px;
        padding: 18px;
        margin-bottom: 22px;
        background-color: #ffffff;
        box-shadow: 0 4px 14px rgba(0,0,0,0.06);
    }

    .recipe-title {
        font-size: 22px;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 999px;
        font-size: 14px;
        margin-right: 8px;
        margin-bottom: 8px;
        background-color: #f2f2f2;
    }

    .good-badge {
        background-color: #e7f8ec;
        color: #1f7a3f;
    }

    .bad-badge {
        background-color: #fff0f0;
        color: #b42318;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ---------- Header ----------
st.markdown('<div class="main-title">🍲 Recipe Finder</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Find recipes using ingredients you already have at home.</div>',
    unsafe_allow_html=True
)


# ---------- Sidebar ----------
with st.sidebar:
    st.header("Search Settings")
    number = st.slider("Number of recipes", 1, 10, 6)
    st.info("Tip: Try ingredients like chicken, rice, tomato or egg, cheese, bread.")


# ---------- Search Box ----------
with st.container():
    col1, col2 = st.columns([4, 1])

    with col1:
        ingredients = st.text_input(
            "Enter your ingredients",
            placeholder="Example: chicken, rice, tomato"
        )

    with col2:
        st.write("")
        st.write("")
        search_button = st.button("Find Recipes", use_container_width=True)


# ---------- Search Action ----------
if search_button:
    if not ingredients.strip():
        st.warning("Please enter at least one ingredient.")
    else:
        try:
            with st.spinner("Finding recipes..."):
                recipes = find_recipes_by_ingredients(ingredients, number)
                st.session_state["recipes"] = recipes

        except Exception as e:
            st.error(e)


# ---------- Results ----------
if "recipes" in st.session_state:
    recipes = st.session_state["recipes"]

    if not recipes:
        st.info("No recipes found. Try different ingredients.")
    else:
        st.markdown("## Recipe Results")

        for recipe in recipes:
            st.markdown('<div class="recipe-card">', unsafe_allow_html=True)

            left_col, right_col = st.columns([1.2, 2.8])

            with left_col:
                if recipe.get("image"):
                    st.image(recipe["image"], use_container_width=True)

            with right_col:
                st.markdown(
                    f'<div class="recipe-title">{recipe["title"]}</div>',
                    unsafe_allow_html=True
                )

                used_count = recipe.get("usedIngredientCount", 0)
                missed_count = recipe.get("missedIngredientCount", 0)

                st.markdown(
                    f"""
                    <span class="badge good-badge">✅ Used: {used_count}</span>
                    <span class="badge bad-badge">❌ Missing: {missed_count}</span>
                    """,
                    unsafe_allow_html=True
                )

                used = recipe.get("usedIngredients", [])
                missed = recipe.get("missedIngredients", [])

                if used:
                    st.markdown("**Ingredients you have:**")
                    st.write(", ".join([item["name"] for item in used]))

                if missed:
                    st.markdown("**Missing ingredients:**")
                    st.write(", ".join([item["name"] for item in missed]))

                with st.expander("View full recipe details"):
                    try:
                        details = get_recipe_details(recipe["id"])

                        st.write("⏱️ **Ready in:**", details.get("readyInMinutes", "N/A"), "minutes")
                        st.write("🍽️ **Servings:**", details.get("servings", "N/A"))

                        source_url = details.get("sourceUrl")
                        if source_url:
                            st.markdown(f"[Open original recipe]({source_url})")

                        st.markdown("### Instructions")
                        instructions = clean_html(details.get("instructions"))
                        st.write(instructions)

                    except Exception as e:
                        st.error(e)

            st.markdown("</div>", unsafe_allow_html=True)