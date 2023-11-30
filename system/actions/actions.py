# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, slots
from rasa_sdk.executor import CollectingDispatcher
import requests


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "trigger_test_responce"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        url = 'http://127.0.0.1:3000/test'
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Print the response content
            print(response.text)
        else:
            # Print an error message if the request was not successful
            print(f"Error: {response.status_code}")

        dispatcher.utter_message(text=response.text)

        return []


class ActionReturnMN(Action):
    def name(self) -> Text:
        return "return_mn"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Extract the MN value from the tracker
        mn_value = tracker.get_slot("MN")

        if mn_value:
            message = f"Okay, your MN is {mn_value}"

            url = f'http://127.0.0.1:3000/student/{mn_value}'
            response = requests.get(url)
            if response.status_code == 200:
                # Print the content of the response (usually JSON or HTML)
                name = response.json()["name"]
                message = f"Your name is {name}"
                
            else:
                message = f"Error: {response.status_code}"
            
        else:
            message = "I couldn't extract the MN value from your message."

        dispatcher.utter_message(text=message)

        return []
