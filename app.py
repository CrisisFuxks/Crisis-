from flask import Flask, request, render_template_string, redirect, url_for, flash
from instagrapi import Client
import os
import time

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "your_secret_key"

# Global variable for Instagram client session
ig_client = None

# HTML Template with shadow border and background wallpaper
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram Group Messaging</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background: url('https://i.ibb.co/fFqG2rr/Picsart-24-07-11-17-16-03-306.jpg') no-repeat center center;
            background-size: cover;
        }
        .container {
            background-color: rgba(255, 255, 255, 0.9);
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
            max-width: 400px;
            width: 100%;
        }
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 20px;
        }
        label {
            display: block;
            font-weight: bold;
            margin: 10px 0 5px;
        }
        input, select, button {
            width: 100%;
            padding: 10px;
            margin-bottom: 15px;
            border: 1px solid #ccc;
            border-radius: 5px;
            font-size: 16px;
        }
        input:focus, select:focus, button:focus {
            outline: none;
            border-color: #007bff;
            box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
        }
        button {
            background-color: #007bff;
            color: white;
            border: none;
            cursor: pointer;
            font-weight: bold;
        }
        button:hover {
            background-color: #0056b3;
        }
        .message {
            color: red;
            font-size: 14px;
            text-align: center;
        }
        .success {
            color: green;
            font-size: 14px;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Instagram Group Messaging</h1>
        <form action="/" method="POST" enctype="multipart/form-data">
            <label for="username">Instagram Username:</label>
            <input type="text" id="username" name="username" placeholder="Enter your username" required>

            <label for="password">Instagram Password:</label>
            <input type="password" id="password" name="password" placeholder="Enter your password" required>

            <label for="group_id">Group Chat ID:</label>
            <input type="text" id="group_id" name="group_id" placeholder="Enter group chat ID" required>

            <label for="message_file">Message File:</label>
            <input type="file" id="message_file" name="message_file" required>
            <p class="info">Upload a text file containing messages, one per line.</p>

            <label for="delay">Delay (seconds):</label>
            <input type="number" id="delay" name="delay" placeholder="Enter delay in seconds" required>

            <button type="submit">Send Messages</button>
        </form>
    </div>
</body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def home():
    global ig_client

    if request.method == "POST":
        try:
            # Collect form data
            username = request.form["username"]
            password = request.form["password"]
            group_id = request.form["group_id"]
            delay = int(request.form["delay"])
            message_file = request.files["message_file"]

            # Read messages from file
            messages = message_file.read().decode("utf-8").splitlines()
            if not messages:
                flash("Message file is empty!", "error")
                return redirect(url_for("home"))

            # Login to Instagram
            if not ig_client:
                ig_client = Client()
                ig_client.login(username, password)
                flash("Logged in successfully!", "success")

            # Send messages to group
            for message in messages:
                print(f"Sending message to group {group_id}: {message}")
                ig_client.direct_send(message, thread_ids=[group_id])
                time.sleep(delay)  # Delay between messages

            flash("All messages sent successfully!", "success")
        except Exception as e:
            flash(f"An error occurred: {e}", "error")

        return redirect(url_for("home"))

    return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
          
