import os

from flask import Flask, request, send_file
import requests
from dotenv import load_dotenv
import base64

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

DOMAIN = os.getenv("DOMAIN")

token = ""


@app.route('/api/v1/user/<str:username>', methods=['GET'])
def process(username):
    global token
    # Step 2: Send a request to a given URL with the `id`
    url = f'{DOMAIN}/api/user/{username}'
    response = requests.get(url, headers={"Authorization": f"Bearer {token}"})

    if response.status_code != 200:
        print(response.json())
        return

    # Step 3: Perform some actions with the response
    data = response.json()
    processed_data = process_data(data)

    # Step 4: Write the result to a file
    filename = f'output_{username}.txt'
    with open(filename, 'w') as f:
        f.write(processed_data)

    # Step 5: Serve the file
    return send_file(filename, as_attachment=True)


def process_data(user):
    text = ""
    for link in user["links"]:
        link = link.split("#")
        text += link[0] + "&allowInsecure=1#" + link[1] + "\n"
    text = base64.b64encode(text.encode()).decode()
    return text


def sign_up():
    username = os.getenv("username")
    password = os.getenv("password")
    global token

    res = requests.post(DOMAIN + "/api/admin/token", data={"username": username, "password": password})
    if res.status_code == 200:
        token = res.json().get("access_token")
    else:
        print(res)


if __name__ == '__main__':
    sign_up()
    app.run(host="", port=5000)
