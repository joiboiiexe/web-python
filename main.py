import os
import firebase_admin
from firebase_admin import credentials, db
from flask import Flask, render_template, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# Initialize Firebase
cred = credentials.Certificate("firebase.json")  # Path to your firebase.json
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://joyboy-exe-default-rtdb.firebaseio.com'
})

# Firebase reference for chat messages
ref = db.reference('chat')

# Function to retrieve chat messages from Firebase
def get_chat_messages():
    messages = ref.get()
    if messages is None:
        return []  # Return an empty list if no messages are found
    return list(messages.values())  # Convert dict to list of messages

# Route for User I
@app.route("/useri")
def useri():
    messages = get_chat_messages()
    return render_template("useri.html", messages=messages)

# Route for User II
@app.route("/userii")
def userii():
    messages = get_chat_messages()
    return render_template("userii.html", messages=messages)

# API endpoint to fetch latest chat messages in JSON
@app.route("/get_messages", methods=["GET"])
def get_messages():
    messages = get_chat_messages()
    return jsonify(messages)

# API endpoint to send a message
@app.route("/send_message", methods=["POST"])
def send_message():
    message = request.form.get("message")
    user = request.form.get("user")

    if message and user:
        # Add message to Firebase
        ref.push({
            'user': user,
            'message': message
        })
        return jsonify({"status": "success"})
    return jsonify({"status": "error"}), 400

# Run Flask app
if __name__ == "__main__":
    app.run(debug=True)
