from flask import Flask, request, jsonify

app = Flask(__name__)

RATES = {
    "USD": 90.0,
    "EUR": 100.0
}

@app.route("/rate")
def rate():
    try:
        currency = request.args.get("currency")

        if not currency or currency not in RATES:
            return jsonify({
                "message": "UNKNOWN CURRENCY"
            }), 400

        return jsonify({
            "rate": RATES[currency]
        }), 200

    except Exception as error:
        print("ERROR:", error)

        return jsonify({
            "message": "UNEXPECTED ERROR"
        }), 500


if __name__ == "__main__":
    app.run(port=5001, debug=True)