import streamlit as st
from spoonacular_api import find_recipes_by_ingredients, get_recipe_details

st.set_page_config(page_title="Recipe Finder", page_icon="🍲")

st.title("🍲 Recipe Finder")
st.write("Find recipes using ingredients you already have.")

ingredients = st.text_input(
    "Enter ingredients separated by commas:",
    placeholder="chicken, rice, tomato"
)

number = st.slider("How many recipes do you want?", 1, 10, 5)

if st.button("Find Recipes"):
    if not ingredients.strip():
        st.warning("Please enter at least one ingredient.")
    else:
        try:
            recipes = find_recipes_by_ingredients(ingredients, number)

            if not recipes:
                st.info("No recipes found. Try different ingredients.")
            else:
                st.session_state["recipes"] = recipes

        except Exception as e:
            st.error(e)


if "recipes" in st.session_state:
    st.subheader("Recipe Results")

    for recipe in st.session_state["recipes"]:
        st.divider()
        st.subheader(recipe["title"])

        if recipe.get("image"):
            st.image(recipe["image"], width=300)

        st.write("Used ingredients:", recipe.get("usedIngredientCount", 0))
        st.write("Missing ingredients:", recipe.get("missedIngredientCount", 0))

        used = recipe.get("usedIngredients", [])
        missed = recipe.get("missedIngredients", [])

        if used:
            st.write("✅ Ingredients you have:")
            for item in used:
                st.write("-", item["name"])

        if missed:
            st.write("❌ Missing ingredients:")
            for item in missed:
                st.write("-", item["name"])

        if st.button(f"View Details", key=recipe["id"]):
            try:
                details = get_recipe_details(recipe["id"])

                st.write("Ready in:", details.get("readyInMinutes"), "minutes")
                st.write("Servings:", details.get("servings"))

                instructions = details.get("instructions")

                if instructions:
                    st.markdown("### Instructions")
                    st.write(instructions)
                else:
                    st.info("No instructions available for this recipe.")

            except Exception as e:
                st.error(e)