from flask import Flask, jsonify, request
from flask_cors import CORS
from calculations import calculate_investment

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "app": "WealthLens",
        "status": "running"
    })

@app.route("/calculate", methods=["POST"])
def calculate():
    try:
        data = request.get_json(force=True)

        sip = calculate_investment(
            monthly_amount=float(data.get("monthly_amount", 0)),
            years=int(data.get("years", 0)),
            annual_return=float(data.get("expected_return", 0)),
            step_up_percent=float(data.get("step_up_percent", 0)),
            expense_ratio=float(data.get("expense_ratio", 0)),
            exit_load=float(data.get("exit_load", 0)),
            tax_percentage=float(data.get("tax_percentage", 0)),
            inflation_percentage=float(data.get("inflation_percentage", 0)),
            pause_months=int(data.get("pause_months", 0))
        )

        return jsonify({"sip": sip}), 200

    except Exception as e:
        # 🔥 THIS will stop silent failures
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000,)
