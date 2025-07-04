from flask import Flask, render_template, request, jsonify, send_file
from email_checker import generate_emails
import csv, os, uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check():
    data = request.get_json()
    first = data.get('first')
    last = data.get('last')
    domain = data.get('domain')
    results = generate_emails(first_name, last_name, domain)
    return jsonify(result)

@app.route('/bulk', methods=['POST'])
def bulk():
    file = request.files['csv']
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    output_filename = f"bulk_results_{uuid.uuid4().hex[:8]}.csv"
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)

    with open(filepath, newline='') as csvfile, open(output_path, 'w', newline='') as outfile:
        reader = csv.DictReader(csvfile)
        fieldnames = ['name', 'domain', 'pattern', 'status']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            first = row.get('first', '')
            last = row.get('last', '')
            domain = row.get('domain', '')
            result = check_email_permutations(first, last, domain)

            for email, status in result.items():
                writer.writerow({
                    'name': f"{first} {last}",
                    'domain': domain,
                    'pattern': email,
                    'status': status
                })

    os.remove(filepath)
    return send_file(output_path, as_attachment=True)
