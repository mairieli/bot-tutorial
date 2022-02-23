import os
from flask import Flask, request
from github import Github, GithubIntegration

app = Flask(__name__)

app_id = '<your_app_number_here>'

# Read the bot certificate
with open(
        os.path.normpath(os.path.expanduser('bot_key.pem')),
        'r'
) as cert_file:
    app_key = cert_file.read()
    
# Create an GitHub integration instance
git_integration = GithubIntegration(
    app_id,
    app_key,
)

@app.route("/", methods=['POST'])
def bot():
    payload = request.json

    owner = payload['repository']['owner']['login']
    repo_name = payload['repository']['name']

    git_connection = Github(
        login_or_token=git_integration.get_access_token(
            git_integration.get_installation(owner, repo_name).id
        ).token
    )
    repo = git_connection.get_repo(f"{owner}/{repo_name}")

    # Check if the event is a GitHub pull request creation event
    if all(k in payload.keys() for k in ['action', 'pull_request']) and payload['action'] == 'opened':
        # TODO: implement the feature to greet first-time developers

    return "", 204

if __name__ == "__main__":
    app.run(debug=True, port=5000)
