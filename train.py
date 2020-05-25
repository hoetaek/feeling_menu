import requests


def store_training(text, label):
    key = "03cc2510-9844-11ea-aa7a-c3c2b08ff20fbfa2dc82-0846-43bf-aa70-6d34390bb241"
    url = "https://machinelearningforkids.co.uk/api/scratch/" + key + "/train"

    response = requests.post(url, json={"data": text, "label": label})

    if not response.ok:
        # if something went wrong, display the error
        print(response.json())
    else:
        print(response)
