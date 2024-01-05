# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
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
                dispatcher.utter_message(text=f"""Error occured. Althought your number {mn_value} was recognized,
                                                    rasa encountered problem with the server
                                                    More: {e}""")
                return []
        else:
            print(mn_value)
            return []


class ActionReturnFAQ(Action):

    def name(self) -> Text:
        return "return_faq"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
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
        except requests.exceptions.RequestException as e:
            dispatcher.utter_message(text=f"""Error occured. Althought your request to get FAQ was recognized,
                                                    rasa encountered problem with the server
                                                    More: {e}""")
            return []


class ActionRememberLL(Action):

    def name(self) -> Text:
        return "remember_level_language"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        ll_value = tracker.get_slot("language_lvl")

        if ll_value:
            try:
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

                message = f"You can choose from several options:\n" + \
                    "\n".join([elective["elective_name"]
                              for elective in response.json()])

                # select * from electives where lower(elective_name) like "%a1%";
                # message = f"Okay, your german level is {ll_value}"

                dispatcher.utter_message(text=message)
                return []
            except requests.exceptions.RequestException as e:
                dispatcher.utter_message(text=f"""Error occured. Althought your language level {ll_value} was recognized,
                                                    rasa encountered problem with the server
                                                    More: {e}""")
                return []
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

        try:
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
        except requests.exceptions.RequestException as e:
            dispatcher.utter_message(text=f"""Error occured. Althought your wish to take {exam} was recognized,
                                                    rasa encountered problem with the server
                                                    More: {e}""")
            return []




class ValidateQuestionnaireForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_questionnaire_form"

    def __init__(self):
        self.data_to_insert = []  # Initialize an empty list to accumulate data

    def validate_reason_to_study_in_germany(self, 
                                            slot_value: Any,
                                            dispatcher: CollectingDispatcher,
                                            tracker: Tracker,
                                            domain: DomainDict,
                                            ) -> Dict[Text, Any]:
        dispatcher.utter_message(text=f"OK! You study here because {slot_value}")
        self.add_to_data("Reason", slot_value)
        return {"reason_to_study_in_germany": slot_value}

    def validate_language_about_question(self, 
                                        slot_value: Any,
                                        dispatcher: CollectingDispatcher,
                                        tracker: Tracker,
                                        domain: DomainDict,
                                        ) -> Dict[Text, Any]:
        dispatcher.utter_message(text=f"OK! You think about the German language that: {slot_value}")
        self.add_to_data("Language_question", slot_value)
        return {"language_about_question": slot_value}

    def validate_mother_country(self, 
                                slot_value: Any,
                                dispatcher: CollectingDispatcher,
                                tracker: Tracker,
                                domain: DomainDict,
                                ) -> Dict[Text, Any]:
        dispatcher.utter_message(text=f"OK! You are from: {slot_value}")
        self.add_to_data("mother_country", slot_value)
        print(self.data_to_insert)
        self.insert_into_database()
        return {"mother_country": slot_value}

    def add_to_data(self, column_name: str, value: Any):
        self.data_to_insert.append({"column_name": column_name, "value": value})

    def insert_into_database(self):
        url = "http://127.0.0.1:3000/insert_data"

        try:
            response = requests.post(url, json=self.data_to_insert)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error inserting data into the database: {e}")

        # Clear the accumulated data after inserting
        self.data_to_insert = []




