from flask import Flask, render_template, request, jsonify
from email_checker import generate_emails

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check():
    try:
        # Get JSON data from request body (works with fetch JSON POST)
        data = request.get_json(force=True)
        first_name = data.get('first_name', '').strip()
        last_name = data.get('last_name', '').strip()
        domain = data.get('domain', '').strip()

        # Input validation
        if not first_name or not last_name or not domain:
            return jsonify({"error": "Please fill in all fields"}), 400

        # Generate and check email permutations
        results = generate_emails(first_name, last_name, domain)
        return jsonify(results)

    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
