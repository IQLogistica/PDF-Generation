import requests
import json
import uuid


def fetch_json(quote_number: str):

    # generate a v4 style guid
    x_request_id = str(uuid.uuid4())

    # set the custom headers
    headers = {
        "X-Request-ID": x_request_id,
        "X-User-ID": "0001"
    }

    # Call the API with the quote number
    response = requests.get(f"https://func-quotingservice-qa.azurewebsites.net/api/quote/{quote_number}/detail", headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Save the JSON data to a file
        content = response.content
        data = json.loads(content)
        return data
    else:
        return False

