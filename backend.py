from flask import Flask, request, render_template_string
import pandas as pd
import random

app = Flask(__name__)

# Load employee data
df = pd.read_csv("employee_dataset.csv")


# Add simulated experience data
def simulate_experience(row):
    overall_exp = random.randint(3, 15)  # Overall experience in years
    skill_exp = {}
    for skill in row['skills'].split(', '):
        skill_exp[skill.lower()] = random.randint(1, min(overall_exp, 10))  # Skill-specific experience
    return overall_exp, skill_exp

df['overall_experience'], df['skill_experience'] = zip(*df.apply(simulate_experience, axis=1))

# HTML template with enhanced styling
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Employee Assistance Chat</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #74ebd5, #ACB6E5);
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            color: #333;
        }
        .container {
            background-color: #fff;
            border-radius: 10px;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
            padding: 25px;
            max-width: 800px;
            width: 100%;
            text-align: center;
        }
        h1 {
            color: #4a90e2;
        }
        label {
            font-size: 1.2em;
            color: #666;
        }
        input[type="text"] {
            width: 100%;
            padding: 12px;
            margin-top: 10px;
            border-radius: 5px;
            border: 1px solid #ddd;
            font-size: 1em;
        }
        input[type="submit"], button {
            background-color: #4a90e2;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1em;
            margin-top: 15px;
        }
        input[type="submit"]:hover, button:hover {
            background-color: #357ABD;
        }
        .results {
            text-align: left;
            margin-top: 20px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        table, th, td {
            border: 1px solid #ddd;
        }
        th, td {
            padding: 10px;
            text-align: left;
        }
        th {
            background-color: #f4f4f4;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Employee Assistance Chat</h1>
        <form action="/search" method="get">
            <label for="query">Enter a skill or task:</label><br><br>
            <input type="text" id="query" name="query" required placeholder="e.g., Python, DevOps">
            <input type="submit" value="Search">
        </form>
        <button onclick="window.location.href='/'">Refresh</button>
        <div class="results">
            {% if employees %}
                <h2>Results:</h2>
                <table>
                    <tr>
                        <th>Name</th>
                        <th>Skills</th>
                        <th>Overall Experience</th>
                        <th>Experience in '{{ query }}'</th>
                    </tr>
                    {% for employee in employees %}
                    <tr>
                        <td>{{ employee.name }}</td>
                        <td>{{ employee.skills }}</td>
                        <td>{{ employee.overall_experience }} years</td>
                        <td>{{ employee.skill_experience }} years</td>
                    </tr>
                    {% endfor %}
                </table>
            {% elif employees is not none %}
                <p>No employees found with expertise in the specified area.</p>
            {% endif %}
        </div>
    </div>
</body>
</html>
"""

# Route to render the search form
@app.route('/')
def index():
    return render_template_string(html_template, employees=None, query=None)

# Route to handle the search and display results
@app.route('/search', methods=['GET'])
def search_employees():
    query = request.args.get('query', '').lower()
    if not query:
        return render_template_string(html_template, employees=None, query=None)

    # Filter rows where 'skills' or 'tasks' contain the query
    results = df[
        df['skills'].str.lower().str.contains(query) |
        df['tasks'].str.lower().str.contains(query)
    ]
    
    employees = []
    for _, row in results.iterrows():
        skill_experience = row['skill_experience'].get(query, "N/A")
        employees.append({
            'name': row['name'],
            'skills': row['skills'],
            'overall_experience': row['overall_experience'],
            'skill_experience': skill_experience
        })

    return render_template_string(html_template, employees=employees, query=query)

if __name__ == '__main__':
    app.run(debug=True)
