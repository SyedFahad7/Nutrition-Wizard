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
    formatted_info = {}
    if 'hits' in recipe_info and recipe_info['hits']:
        recipe = recipe_info['hits'][0]['recipe']
        formatted_info['label'] = recipe['label']
        formatted_info['source'] = recipe['source']
        formatted_info['url'] = recipe['url']
        formatted_info['calories'] = f"{recipe['calories']} kcal"
        formatted_info['ingredients'] = recipe['ingredientLines']
    return formatted_info

def main():
    print("Welcome to the Recipe Chatbot!")
    print("Ask me about recipes for any food item.")
    print("Type 'quit' to exit.")

    while True:
        user_input = input("You: ")

        if user_input.lower() == 'quit':
            print("Bot: Goodbye!")
            break

        recipe_info = get_recipe_info(user_input)

        if recipe_info:
            formatted_info = format_recipe_info(recipe_info)
            if formatted_info:
                print("Bot: Recipe Information:")
                print(f"  Recipe Label: {formatted_info['label']}")
                print(f"  Source: {formatted_info['source']}")
                print(f"  Calories: {formatted_info['calories']}")
                print("  Ingredients:")
                for ingredient in formatted_info['ingredients']:
                    print(f"    - {ingredient}")
                print(f"  URL: {formatted_info['url']}")
            else:
                print("Bot: No detailed recipe information found.")
        else:
            print("Bot: Sorry, I couldn't retrieve the recipe information at the moment.")

if __name__ == "__main__":
    main()
