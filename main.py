from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for development (optional)

# Route to serve the HTML file
@app.route('/')
def index():
    return render_template('index.html')

# Chatbot API
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '').lower()

    # Simple chatbot logic
    if user_message == 'hello':
        bot_reply = 'Hi there! How can I assist you today?'
    elif user_message == 'bye':
        bot_reply = 'Goodbye! Have a great day!'
    else:
        bot_reply = "I'm sorry, I didn't understand that. Can you try again?"

    return jsonify({'reply': bot_reply})

if __name__ == '__main__':
    app.run(debug=True)
