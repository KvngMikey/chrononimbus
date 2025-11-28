import os
from flask import Flask, request, jsonify
from agent import root_agent, get_weather, get_current_time

app = Flask(__name__)

# Wrapper function for your agent
def run_agent(city: str) -> dict:
    """Calls your root_agent tools and returns combined response."""
    weather = get_weather(city)
    time_info = get_current_time(city)

    # Combine responses if both succeeded
    if weather["status"] == "success" and time_info["status"] == "success":
        combined = f"{weather['report']}\n{time_info['report']}"
    else:
        combined = weather.get("error_message", "") + " " + time_info.get("error_message", "")

    return combined

@app.route("/query", methods=["GET"])
def query():
    city = request.args.get("city")
    if not city:
        return jsonify({"error": "Please provide a city parameter"}), 400
    response = run_agent(city)
    return jsonify({"response": response})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use Render's dynamic port
    app.run(host="0.0.0.0", port=port)
