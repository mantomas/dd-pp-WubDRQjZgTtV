# TODO in Flask
**WORK IN PROGRESS**  
Skeleton of simple ToDo app. Written in Python (3.9+) using Flask and Bootstrap. It can be used as a starting point to create something more advanced.  

![Preview](todo.png)  
## Features overview
- user registration (can be deactivated in the configuration)
- login to user account (with *remember me* option)
- add new task
    - title
    - description (optional)
    - one file attachment (optional)
    - deadline (optional)
- curent tasks overview
    - number of active tasks
    - 4 colors according to the task state
    - link to task detail
    - time difference with respect to the deadline (if set)
    - link to mark the task as completed
- finished tasks overview
    - number of finished tasks
    - tasks completion time
- task detail
    - editable
    - with time of creation
    - link to attachment (if any)
    - the ability to permanently delete a task
## Application structure - only necessary
```
todo
│   run.py   
│   config.py
│   .flaskenv
│
└───app
│   │   __init__.py
│   │   models.py
│   │       
│   └───auth
│   │       __init__.py
│   │       routes.py
│   │       forms.py
│   │
│   └───main
│   │       __init__.py
│   │       routes.py
│   │       forms.py
│   │
│   └───errors
│   │       __init__.py
│   │       handlers.py
│   │
│   └───templates
│   │        layout.html
│   │        ... 
│   └───tests
│            conftest.py
|            ...
│
└───migrations
    │   ... 
```
**run.py** - app entry point, creates main app - set in *.flaskenv*  
**config.py** - Flask configuration and app basic settings: DB path, upload path, max filesize, file extensions allowed  
**.flaskenv** * set environment variables, development/production switch  
**app/__init__.py** - joining all parts together  
**app/models.py** - SQAlchemy DB models and their methods  
**app/auth/__init__.py** - blueprint for authentication parts  
**app/auth/routes.py** - mapping of URL pathes to function calls for authentication  
**app/auth/forms.py** - forms used in auth templates and their validation  
**app/main/__init__.py** - blueprint for main app  
**app/main/routes.py** - mapping of URL pathes to main function calls  
**app/main/forms.py** - forms used in templates and their validation  
**app/errors/__init__.py** - blueprint for error handling  
**app/errors/handlers.py** - routing for error pages  
**templates** - Jinja templates in html  
**migrations** - keeping track of DB changes and their migrations, used for DB upgrade - auto-generated  
**tests** - tests folder, use Pytest  
**tests/conftest.py** - test fixtures  

## Installation and running (development)
1. clone repository
2. create and activate Python virtual environment (tested on python 3.9.+ but should work in 3.7.+)
3. install dependencies `pip install -r requirements.txt`
4. create local DB `flask db upgrade` (creates *todo.db*, SQLite, in the root folder of the application , with the tables created)
5. run the app `flask run`

## Testing
All tests are in a subfolder `tests` and configured to use **Pytest** suite, which is a part of dependencies. To run all tests, activate virtual environment and execute `pytest` in application root folder.
## Possible next steps (ToDo)
- [ ] **tests**
- [ ] **more advanced user account:** email, editable profile page, password recovery, statistics, export to various file formats, deleting an account
- [ ] **search function:** titles, body
- [ ] **date-time picker in JS**
- [ ] **tasks filtering**
- [ ] **optional email notification**
- [ ] **supervisor account**
