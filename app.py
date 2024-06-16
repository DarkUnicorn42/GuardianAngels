from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def home():
    # Assuming you have set the GOOGLE_MAPS_API_KEY in your environment variables
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    return render_template('home.html', api_key=api_key)

if __name__ == '__main__':
    app.run(debug=True)