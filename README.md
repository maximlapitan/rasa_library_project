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

Installation should be proceeded in python venv. Steps are done in linux OS, but can be adapted to windows as well.

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

## Architecture

Project consists of 3 parts: 

1. **Rasa Model**: yaml files describing domain and actions file to communicate with webserver
1. **Web Server** (built using rest-api approach) to facilitate responces from rasa model
1. **Database**, to which server can connect and execute select commands.

### Rasa model

### Web Server

### Database

Database has the following structure:

![](doc/electives_view.png)