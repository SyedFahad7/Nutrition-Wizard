from flask import Flask, render_template, request, jsonify
from chatbot_functions import format_recipe_info, get_recipe_info

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recipe', methods=['GET'])
def get_recipe():
    food_item = request.args.get('foodItem')

    # Call your chatbot script or API to get recipe information
    recipe_info = get_recipe_info(food_item)
    formatted_recipe_info = format_recipe_info(recipe_info)

    return jsonify({'message': formatted_recipe_info})


if __name__ == "__main__":
    app.run(debug=True)
