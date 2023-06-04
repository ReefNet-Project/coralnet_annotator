import requests
import json
from prepare_images import prepare_image_data
from dotenv import load_dotenv
import os
import time 

load_dotenv()
CORALNET_TOKEN = os.getenv('CORALNET_TOKEN')
CLASSIFIER_ID = os.getenv('CLASSIFIER_ID')

# function to request classifier deployment
def deploy_classifier(data):
    url = f"https://coralnet.ucsd.edu/api/classifier/{CLASSIFIER_ID}/deploy/"
    headers = {
        "Authorization": f"Token {CORALNET_TOKEN}",
        "Content-type": "application/vnd.api+json"
    }

    print("[INFO]: Sending request to deploy classifier and start classification process \n")
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(f"[INFO]: response.status_code = {response.status_code} \n")
    job_url = response.headers["Location"]

    # Check the status of the classifier deployment
    url = f"https://coralnet.ucsd.edu{job_url}"
    headers = {
        "Authorization": f"Token {CORALNET_TOKEN}"
    }

    print("[INFO]: Checking the status of the classifier deployment \n")
    response = requests.get(url, headers=headers)
    print(f"[INFO]: response.status_code = {response.status_code} \n")
    while response.status_code == 200:
        # wait 10 seconds before checking again
        time.sleep(10)
        # Keep checking until the job is finished
        response = requests.get(url, headers=headers)

    print(response.status_code)
    print(response.text)
    # Fetch the result of the finished classifier deployment
    result_url = response.headers["Location"]

    return result_url



def main():
    # prepare data 
    data = prepare_image_data()
    # Fetch the result of the finished classifier deployment
    result_url = deploy_classifier(data)
    url = f"https://coralnet.ucsd.edu{result_url}"
    headers = {
        "Authorization": f"Token {CORALNET_TOKEN}"
    }
    response = requests.get(url, headers=headers)
    classification_result = response.json()

    # Print the result
    print(classification_result)

    # save the json result into file 
    with open('classification_result.json', 'w') as f:
        json.dump(classification_result, f)

    return


if __name__ == "__main__":
    main()