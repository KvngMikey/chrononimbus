from flask import Flask, request, jsonify, render_template
from agent import root_agent, get_weather, get_current_time

app = Flask(__name__, template_folder="templates")

# Wrapper function
def run_agent(city: str) -> str:
    weather = get_weather(city)
    time_info = get_current_time(city)

    if weather["status"] == "success" and time_info["status"] == "success":
        combined = f"{weather['report']}\n{time_info['report']}"
    else:
        combined = weather.get("error_message", "") + " " + time_info.get("error_message", "")
    return combined

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/query", methods=["GET"])
def query():
    city = request.args.get("city")
    if not city:
        return jsonify({"error": "Please provide a city parameter"}), 400
    response = run_agent(city)
    return jsonify({"response": response})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)
