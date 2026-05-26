import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("SPOONACULAR_API_KEY")
BASE_URL = "https://api.spoonacular.com"


def find_recipes_by_ingredients(ingredients, number=5):
    url = f"{BASE_URL}/recipes/findByIngredients"

    params = {
        "apiKey": API_KEY,
        "ingredients": ingredients,
        "number": number,
        "ranking": 1,
        "ignorePantry": True
    }

    response = requests.get(url, params=params)

    # Helps you see the exact URL being called, but hides your key
    safe_url = response.url.replace(API_KEY, "HIDDEN_API_KEY") if API_KEY else response.url
    print("Calling:", safe_url)

    if response.status_code != 200:
        raise Exception(f"API error: {response.status_code} - {response.text}")

    return response.json()


def get_recipe_details(recipe_id):
    url = f"{BASE_URL}/recipes/{recipe_id}/information"

    params = {
        "apiKey": API_KEY,
        "includeNutrition": False
    }

    response = requests.get(url, params=params)

    safe_url = response.url.replace(API_KEY, "HIDDEN_API_KEY") if API_KEY else response.url
    print("Calling:", safe_url)

    if response.status_code != 200:
        raise Exception(f"API error: {response.status_code} - {response.text}")

    return response.json()