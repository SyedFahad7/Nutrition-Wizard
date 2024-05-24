from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recipe', methods=['GET'])
def get_recipe():
    food_item = request.args.get('foodItem')
    recipe_info = get_recipe_info(food_item)
    return jsonify({'message': recipe_info})

@app.route('/voice_input', methods=['POST'])
def voice_input():
    audio_file = request.files['audio']
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio_data)
        return jsonify({'text': text})
    except sr.UnknownValueError:
        return jsonify({'text': 'Could not understand audio'})
    except sr.RequestError as e:
        return jsonify({'text': f"Error: {e}"})

def get_recipe_info(food_item):
    api_url = 'https://api.edamam.com/search'
    app_id = 'e291f673'
    app_key = 'a6ab020f175b668dc4a458d6a101204d'
    params = {
        'q': food_item,
        'app_id': app_id,
        'app_key': app_key,
        'to': 1
    }
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()
        return format_recipe_info(data)
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

if __name__ == "__main__":
    app.run(debug=True)
