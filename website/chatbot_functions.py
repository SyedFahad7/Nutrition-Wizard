import requests
def get_recipe_info(food_item):
    api_url = 'https://api.edamam.com/search'
    app_id = 'e291f673'  # Your Application ID
    app_key = 'a6ab020f175b668dc4a458d6a101204d'  # Your Application Key
    params = {
        'q': food_item,
        'app_id': app_id,
        'app_key': app_key,
        'to': 1  # Limit to 1 result
    }

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        return data
    except requests.RequestException as e:
        print('Error:', e)
        return None


def format_recipe_info(recipe_info):
    if 'hits' in recipe_info and recipe_info['hits']:
        recipe = recipe_info['hits'][0]['recipe']
        formatted_info = f"Recipe Label: {recipe['label']}\n"
        formatted_info += f"Source: {recipe['source']}\n"
        formatted_info += f"Calories: {recipe['calories']} kcal\n"
        formatted_info += "Ingredients:\n"
        formatted_info += "\n".join(recipe['ingredientLines'])
        return formatted_info
    else:
        return "No recipe information found."

