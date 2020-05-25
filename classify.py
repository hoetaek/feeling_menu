import requests
from service import get_api_key


def classify_feeling(message: str):
    # This function will pass your text to the machine learning model
    # and return the top result with the highest confidence
    def classify(text):
        key = get_api_key()
        url = "https://machinelearningforkids.co.uk/api/scratch/" + key + "/classify"

        response = requests.get(url, params={"data": text})

        if response.ok:
            response_data = response.json()
            top_match = response_data[0]
            return top_match
        else:
            response.raise_for_status()

    # CHANGE THIS to something you want your machine learning model to classify
    demo = classify(message)

    label = demo["class_name"]
    confidence = demo["confidence"]

    # CHANGE THIS to do something different with the result
    return label
