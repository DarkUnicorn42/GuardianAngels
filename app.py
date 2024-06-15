from flask import Flask, render_template, jsonify
import ewaste
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)

@app.route('/')
def home():
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    return render_template('home.html', api_key=api_key)

@app.route('/find-disposal')
def find_disposal():
    try:
        current_location = ewaste.get_current_location()
        disposal_locations = ewaste.get_disposal_locations()
        closest_disposal = ewaste.find_closest_disposal(current_location, disposal_locations)
        
        distance, duration, steps = ewaste.get_shortest_route(current_location, closest_disposal['location'])
        
        result = {
            "current_location": current_location,
            "closest_disposal": closest_disposal,
            "distance": distance,
            "duration": duration,
            "steps": steps
        }
        
        # Log the result for debugging
        app.logger.info(f"Disposal data: {result}")
        
        return jsonify(result)
    except Exception as e:
        # Log the error to the console for debugging
        app.logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
