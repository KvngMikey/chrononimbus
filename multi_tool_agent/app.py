import os
from flask import Flask, request, jsonify
from agent import run_agent

app = Flask(__name__)

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
