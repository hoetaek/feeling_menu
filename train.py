import requests
from service import get_api_key


def store_training(text: str, label: str):
    key = get_api_key()
    url = "https://machinelearningforkids.co.uk/api/scratch/" + key + "/train"

    response = requests.post(url, json={"data": text, "label": label})

    if not response.ok:
        # if something went wrong, display the error
        print(response.json())
    else:
        print(response)
