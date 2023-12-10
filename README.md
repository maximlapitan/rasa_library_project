# Rasa Chatbot "German Language Electives Assistant - Schoschka"

## Authors

Maxim Lapitan 22200839

Maxim Zotov 22200849

[Link to MyGit repo](https://mygit.th-deg.de/mz20849/mm-sas)

## Project description

This Rasa chatbot can help international students to learn German language. One can:
- ask general questions, 
- ask how to register to exams (one-site and exams like goethe)
- get additional information regarding rules

You can get more information about chatbot's scope in [respective wiki page](https://mygit.th-deg.de/mz20849/mm-sas/-/wikis/user-journeys)

Internal structure is covered in [here](#architecture)

## Installation

Installation should be proceeded in python venv. Steps are done in linux OS, but can be adapted to windows as well. Basically just git clone, create and activate venv (in console or in ide) and install required packages.

```bash
git clone https://mygit.th-deg.de/mz20849/mm-sas
cd mm-sas/
python3.10 -m venv sas-venv
source sas-venv/bin/activate
pip install -r requirements.txt
```

Eventually you may need [sqlite3](https://www.sqlite.org/index.html) installed, although it comes out of the box in linux.

## Basic usage
Usage consists of 4 parts (You may need several terminal windows for that):

1. Training rasa
1. Starting flask server
1. Running rasa actions
1. Activating rasa shell and working with trained model

Let's do it step by step.

1. Let's train model **(Window 1)**
    ```bash
    cd system
    rasa train
    ```
1. While rasa is doing it's training, let's start our **flask** webserver. There are 2 equal options **(Window 2)**

    1. ```bash
        cd mm-sas/
        flask run -p 3000
        ```
    2. ```bash
        cd mm-sas/webserver
        python3 server.py
        ```

1. Now let's activate rasa actions by running **(Window 3)**

    ```
    cd mm-sas/system
    rasa run actions
    ```

1. After model is trained, we can start rasa shell and input something in it. For this run **(Window 1)**

    ```bash
    rasa shell
    ```

Your setup may look like this

![](doc/3_windows.png)

## Implementation of the Requests

There are several rasa requests, which have to have some sort of processing to them. Therefore we have 6 slots and 6 entities together with 6 custom actions to produce user-tailored responces.

There are 5 custom actions:

- [trigger_test_responce](#trigger_test_responce) - `ActionHelloWorld`, triggers test responce from REST server
- [remember_mn](#remember_mn) - `ActionRememberMN`, accesses the server and returns student (if he is available). Additionally sets slots `name`, `surname` and `gpa` using `return [SlotSet(key, value) for key, value in person.items() if key != "student_mn"]`
- [return_faq](#return_faq) - `ActionReturnFAQ`, returns link to faq, if user asks for frequent questions
- [remember_level_language](#remember_level_language) - `ActionRememberLL`, gets user's level of german and provides him with possible courses
- [exam_reg_procedure](#exam_reg_procedure) - `ActionExamRegistration`, returns instructions to register to goethe, telc and similar exams
- [action_default_fallback](#action_default_fallback) - `ActionDefaultFallback`, returns nothing, was added to prevent answering randomly to empty string inputs

### trigger_test_responce

Part of the story

```yaml
- story: test_ping
    steps:
      - intent: trigger_test
      - action: trigger_test_responce
      - intent: goodbye
      - action: utter_goodbye
```

Will return *Success, the server is up and running, rasa is requesting as expected* if everything is fine. Else it will print "Error" and error message

Example:

> **Your input** -> test              

> Success, the server is up and running, rasa is requesting as expected

### remember_mn

Returns your matriculation number, GPA and name with surname (if exists), otherwise you will get some sort of error. Part of the story

```yaml
- story: identify student
    steps:
        - intent: greet
        - action: utter_ask_for_id
        - intent: say_matriculation
        - action: remember_mn
```

It also uses several slots (`student_mn`) is used to get information from database and others are "remembered" after request is completed.

```yaml
slots:
    student_mn:
        type: text
        mappings:
        - type: from_entity
            entity: matriculation_number
    name:
        type: text
        mappings:
        - type: custom
            action: remember_mn

    surname:
        type: text
        mappings:
        - type: custom
            action: remember_mn

    gpa:
        type: float
        mappings:
        - type: custom
            action: remember_mn
```

Example: 

> **Your input** ->  hi

> Hi, can I have you id number please?

> **Your input** ->  22200849

> Hello Maxim Zotov, your id is 22200849 and gpa is 1

### return_faq

when user wants to get access to all FAQ at once, he can request it.

```yaml
- story: get faq
    steps:
        - intent: get_faq
        - action: return_faq
```
`return_faq` will contact server to get link to most recent faq

Example: 

> **Your input** -> faq

> https://www.th-deg.de/Studierende/AWP-Sprachkurse/FAQ_EN.pdf

### remember_level_language

Part of story

```yaml
- story: identify student's level of language
    steps:
      - intent: want_learn_german
      - action: utter_ask_for_level_language
      - intent: say_level_language
      - action: remember_level_language
      - intent: ask_register_procedure
      - action: utter_register_procedure
```
When user wants to learn german, user gets asked about his level and then gets possible courses to attend. After that one can request registration instructions.

Example:

> **Your input** ->  I want to start lerning german

> Can I know your level of knowledge of german language?

> **Your input** ->  i have a1

> You can choose from several options:
>
> German A1/ part 1 + 2
>
> German A1/ part 3 + 4
>
> German A1/ Grammar and Vocabulary

> **Your input** ->  how to register

> Check your email. It should be an email from julia.vollbrecht@th-deg.de. Inside this email you will be able to find instructions of registration. Good luck!

### exam_reg_procedure

Part of the story

```yaml
- story: german exam registration
    steps:
      - intent: want_german_exam
      - action: utter_which_exam
      - intent: say_german_exam
      - action: exam_reg_procedure
```

When one wants to pass german exam, system asks about type of the exam and then returns options how to register.

Example: 

> **Your input** ->  How do I register for a German exam?

> Which one exam do you like do pass? Say me its name.

> **Your input** ->  goethe

> You selected goethe
>
> You can find additional information at https://www.goethe.de/de/spr/kup/prf/prf.html
>
> Note, that self registration without participation of DIT university

### action_default_fallback

This was added primarily to stop model from responding to empty promts

Example: 

> **Your input** -> 

> I'm sorry, I didn't understand that. Can you please provide more information?

## Architecture

Project consists of 3 parts: 

1. **Rasa Model**: yaml files describing domain and actions file to communicate with webserver
1. **Web Server** (built using rest-api approach) to facilitate responces from rasa model
1. **Database**, to which server can connect and execute select commands.

### Rasa model

Simple rasa model, built with 3 entities, 6 slots, 6 custom actions, more than 20 stories, almost 50 intents and 6 rules. 

### Web Server

REST-API python server, built using flask. Has several REST addresses, to issue GET requests (by now only GET is supported).

- `/test` - check if server is working and rasa actions functional
- `/languages/faq` - return link to frequently asked questions about the selection of language courses and electives (AWPs)
- `/student/<int:student_id>` - return student from a database. Print his gpa, name, surname and MN (if student is present)
- `/languages/levels/<ll_value>` - return available courses for each level (A1-C1)
- `/exams/<exam>` - get information about exams (goethe, telc, etc.)

### Database

Database has the following structure:

![](doc/electives_view.png)

Database can be used in variety of scenarios. It can be filled with students, their matriculation number, name, surname and GPA.

```sql
select * from student;
student_mn	name	surname	gpa
10817623	Jack	Perez	2.7
12399158	Yvonne	Johnson	2.9
```
Table is also filled with all faculties and programmes, which were at DIT website.

```sql
select * from faculty JOIN program LIMIT 2;
faculty_id	faculty_name	program_id	program_name	faculty_id	program_type
1	Civil and Construction Engineering	1	Civil and Construction Engineering 	1	Bachelor
1	Civil and Construction Engineering	2	Construction Management 	1	Bachelor
```

There is a table `programm_type`, which is responsible for holding programm types (Bachelor or Master).

Table `courses_status` holds values, which can be attached to `student_course_status` to control which student has which courses.

```sql
select * from courses_status;
name
attending
completed
retake
must_be_taken
```

`course_prerequisite` is used to specify which courses should be taken prior to attempting new one.

Table `side_exam` used to get information regarding german language exams (goethe, telc etc.).

## Work done

Work was always carried out together without exceptions. We either sat together, or communicated via video chat and were implementing every task using 2 brains at the same time, thus reducing amount of human errors, because two eyes were looking at the project at the same time.