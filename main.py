from flask import Flask, render_template, request, jsonify
import firebase_admin
from firebase_admin import credentials, db

# Initialize Flask app
app = Flask(__name__)

# Firebase initialization
cred = credentials.Certificate('firebase.json')  # Path to your Firebase service account key
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://joyboy-exe-default-rtdb.firebaseio.com/'
})

@app.route('/')
def index():
    """
    Render the chat interface.
    """
    return render_template('index.html')

@app.route('/send-message', methods=['POST'])
def send_message():
    """
    Handle user's message and insert both user and bot responses into Firebase.
    """
    data = request.json
    user_message = data.get('message')

    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    # Generate bot reply instantly
    bot_reply = f"Bot says: I received your message: '{user_message}'"

    # Return bot reply immediately
    response = {
        'status': 'success',
        'bot_reply': bot_reply
    }

    # Insert user and bot messages into Firebase in the background
    user_ref = db.reference('messages').push()
    user_ref.set({
        'message': user_message,
        'from': 'user'
    })

    bot_ref = db.reference('messages').push()
    bot_ref.set({
        'message': bot_reply,
        'from': 'bot'
    })

    return jsonify(response), 200

@app.route('/get-messages', methods=['GET'])
def get_messages():
    """
    Fetch all messages from Firebase to display on page load.
    """
    messages = db.reference('messages').order_by_key().get()
    return jsonify(messages)

if __name__ == '__main__':
    app.run(debug=True)
