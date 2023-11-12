from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

# Function to load response from a file in the responses folder
def load_response(file_name):
    file_path = os.path.join('responses', file_name)
    with open(file_path) as f:
        return json.load(f)

# Load routes from JSON and create them dynamically
def load_routes():
    with open('routes_config.json') as f:
        routes = json.load(f)

    # Clear existing rules (except for static and restart)
    for rule in list(app.url_map.iter_rules()):
        if rule.endpoint not in ['static', 'restart_server']:
            app.url_map._rules.remove(rule)

    # Create routes dynamically
    for route in routes:
        response = load_response(route['response_file'])
        endpoint = route['route'].replace('/', '_') + '_' + route['verb'].lower()

        if route['verb'].upper() == 'GET':
            app.route(route['route'], methods=['GET'], endpoint=endpoint)(lambda response=response: jsonify(response))
        elif route['verb'].upper() == 'POST':
            app.route(route['route'], methods=['POST'], endpoint=endpoint)(lambda response=response: jsonify(response))
        # Add other HTTP verbs as needed
def print_routes():
    print("😻😻😻😻😻     List of routes:     😻😻😻😻😻")
    for rule in app.url_map.iter_rules():
        methods = ','.join(rule.methods)
        print(f"🌎 {rule.endpoint}: {rule.rule} 🧩 [{methods}]")
def print_curl_commands():
    print("😻😻😻😻😻      Sample curl commands for testing endpoints:     😻😻😻😻😻")
    for rule in app.url_map.iter_rules():
        methods = ','.join(rule.methods - {'OPTIONS', 'HEAD'})  # Exclude OPTIONS and HEAD methods
        url = f"http://127.0.0.1:5000{rule.rule}"  # Adjust host and port as needed

        for method in methods.split(','):
            if method in ["GET", "DELETE"]:
                print(f"curl -X {method} '{url}'")
            elif method in ["POST", "PUT", "PATCH"]:
                print(f"curl -X {method} -H 'Content-Type: application/json' -d '{{}}' '{url}'")
                
# Route to restart and reload routes


# Initial load of routes
load_routes()
print_routes()
print_curl_commands()

if __name__ == "__main__":
    app.run(debug=True)
