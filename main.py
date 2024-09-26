from flask import Flask
from bet import bet
import webbrowser

app = Flask(__name__)
app.register_blueprint(bet)  # No need for a URL prefix here

if __name__ == "__main__":
    # Automatically open the app in the browser
    webbrowser.open("http://127.0.0.1:4000/")
    
    # Run the Flask app
    app.run('127.0.0.1', 4000, debug=True)