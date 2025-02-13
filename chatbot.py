from flask import Flask, render_template, request, jsonify
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import json

app = Flask(__name__)

# Initialize chatbot
bot = ChatBot("WhaleX", read_only=False,
              logic_adapters=[
                  {
                      "import_path": "chatterbot.logic.BestMatch",
                      "default_response": "Sorry I don't have an answer!",
                      "maximum_similarity_threshold": 0.9
                  }
              ])

# Function to load JSON data
def load_chatbot_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            training_data = []
            for item in data:
                if 'question' in item and 'answer' in item:
                    training_data.append(item['question'])
                    training_data.append(item['answer'])
                else:
                    print(f"Invalid item structure: {item}")
            return training_data
    except Exception as e:
        print(f"Error loading JSON file: {str(e)}")
        raise

# Train the chatbot
try:
    # Train with custom JSON data
    list_trainer = ListTrainer(bot)
    custom_data = load_chatbot_data('chatbot_data.json')
    list_trainer.train(custom_data)
    
except Exception as e:
    print(f"Training error: {e}")

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    user_input = request.json["user_input"]
    bot_response = str(bot.get_response(user_input))
    return jsonify({"bot_response": bot_response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)