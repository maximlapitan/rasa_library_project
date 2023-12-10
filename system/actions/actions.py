# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import requests


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "trigger_test_responce"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        url = 'http://127.0.0.1:3000/test'
        try:
            response = requests.get(url)
            if response.status_code == 200:
                # Print the response content
                print(response.text)
                dispatcher.utter_message(text=response.text)
            else:
                # Print an error message if the request was not successful
                print(f"Error: {response.status_code}")
                dispatcher.utter_message(text=f"Error: {response.status_code}")
            
        except requests.exceptions.RequestException as e:
            print(f"Error {e}")
            dispatcher.utter_message(text=f"Error occured\n More: {e}")
            

        # Check if the request was successful (status code 200)
        

        return []


class ActionRememberMN(Action):

    def name(self) -> Text:
        return "remember_mn"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        mn_value = tracker.get_slot("student_mn")
        person = {
            "name": None,
            "surname": None,
            "gpa": None,
            "student_mn": mn_value
        }
        if mn_value:
            message = f"Okay, your student_mn is {mn_value}"

            try: 
                url = f'http://127.0.0.1:3000/student/{mn_value}'
                response = requests.get(url)
                if response.status_code == 200:
                    # Print the content of the response (usually JSON or HTML)
                    name = response.json()["name"]
                    gpa = response.json()["gpa"]
                    surname = response.json()["surname"]
                    number = response.json()["student_mn"]
                    if name is None:
                        message = f"Your number {mn_value} is not found in our database. Try to correct the typo"
                        dispatcher.utter_message(text=message)
                    else:
                        message = f"Hello {name} {surname}, your id is {number} and gpa is {gpa}"
                        person = response.json()
                        dispatcher.utter_message(text=message)
            
                        return [SlotSet(key, value) for key, value in person.items() if key != "student_mn"]
                else:
                    message = f"Error: {response.status_code}"
                    dispatcher.utter_message(text=message)
                    return []
            except requests.exceptions.RequestException as e:
                dispatcher.utter_message(text=f"""Error occured. Althought you number {mn_value} was recognized,
                                                    rasa encountered problem with the server
                                                    More: {e}""")
                return []
        else:
            print(mn_value)
            

class ActionReturnFAQ(Action):

    def name(self) -> Text:
        return "return_faq"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        url = 'http://127.0.0.1:3000//languages/faq'
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
    
    
class ActionRememberLL(Action):

    def name(self) -> Text:
        return "remember_level_language"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        ll_value = tracker.get_slot("language_lvl")

        if ll_value:
            
            url = f'http://127.0.0.1:3000/languages/levels/{ll_value}'
            print(url)
            response = requests.get(url)
            print(type(response.json()))
            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Print the response content
                print(response.json())
            else:
                # Print an error message if the request was not successful
                print(f"Error: {response.status_code}")
            
            message = f"You can choose from several options:\n" + "\n".join([elective["elective_name"] for elective in response.json()])
            
            # select * from electives where lower(elective_name) like "%a1%";
            # message = f"Okay, your german level is {ll_value}"
            
            dispatcher.utter_message(text=message)
            
        return []
    
class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_template("utter_default_fallback", tracker)
        return []
    
class ActionExamRegistration(Action):
    def name(self) -> Text:
        return "exam_reg_procedure"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        exam = tracker.get_slot("german_exam")
        
        url = f'http://127.0.0.1:3000/exams/{exam}'
        print(url)
        response = requests.get(url)
        print(type(response))
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Print the response content
            message = f"You selected {exam}\n"
            message += f'You can find additional information at {response.json()[0]["link"]}\n'
            message += f'Note, that {response.json()[0]["Notes"]}\n'
            
            print(response.json())
        else:
            # Print an error message if the request was not successful
            print(f"Error: {response.status_code}")
            message = f"Exam {exam} not found in our exam database"
        
        dispatcher.utter_message(text=message)
        
        return []
    
