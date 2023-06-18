# Grocery List Web App – Database Application Project, University of Helsinki (Summer 2023)
This web-based app is coursework for the University of Helsinki Database Application Project course. The aim is to create a web-based application to make a life just a bit easier by streamlining one of the most tedious parts of your weekly shop – i.e. compiling a shopping list.

## Project overview
Main functionalities:
+ The user can register/log in
+ The user can create/save shopping lists
+ The user can view their previous shopping lists
+ The shopping list items are put categorised (fruit & veg, chilled food, frozen food, household items, etc.) for easier shopping
+ The user can edit an existing shopping list
+ The user can delete old shopping lists

Super simple, right? Not to worry, if time is kind some of the following could be included:
+ The user can share a shopping list
+ The user can add recipes (at least manually) from which the ingredients are imported to a shopping list
+ The user can delete their account
+ Unit of measurement conversion

Known issues (*update 18/06/23*):
+ It ugly ':D' I will focus on the layout/CSS/making the application look nice after all the main functionalities are done
+ When creating a new list, pressing `return` submits the last (can only use `tab` to navigate between fields)

For my own convenience, I have created a [spreadsheet](https://docs.google.com/spreadsheets/d/17Hk51ZoDV1AqUWWAYf6MvK6ZVflhoNZ81wzrthbtHzs/) to track the project progress. It includes a roadmap/backlog of sorts, checklists for deadlines, and I will probably use it for general planning/time keeping as well.

## Project progress

### *update 18/06/23*
+ schema updated
+ creating new lists
+ error routing
+ spreadsheet
+ lists have max items 
+ shows list after creation
+ can create new shopping list
+ lists can be accessed from user's page
+ PRG
+ lists can have multiple items of the same name with different categories or units of measurement

***

### *update 04/06/23*

The project is still very much a work in progress – only the log in/log out/register functionalities are (more or less) fully working. Lazy, me? You got it. Slowly getting into this.

On the database side of things, well, nothing is really implemented in the actual project yet. Been re-familiarising myself with SQL queries and playing around before diving into the implementation, so that I have an actual idea of what I'm doing.

The backlog spreadsheet has been updated, too, and I will keep using it, possibly add some more user stories if my time management allows it. The list of main functionalities (above) has been updated as well per the feedback I got on Labtool.

***

**There are absolutely no automated tests, so no guarantees of anything working. Code is fairly clean and documented, and linting is done using pylint (8.76/10 last time I checked).**

## Installation & instructions

Start by cloning the repository (`git clone git@github.com:nuclearkittens/tsoha-grocery-list.git`) and create an `.env` file for the following environmental variables:

```
DATABASE_URL=local_path_to_the_database
SECRET_KEY=super_secret_key_wahoo
```
Create a virtual environment and install dependencies:
```
python3 -m venv venv
source venv/bin/activate
pip install -r ./requirements.txt
```
Assuming you've got PostgreSQL installed, you can define the database schema by `psql < schema.sql`. **The schema includes queries to drop existing tables**, so if you already have tables with the same names as defined in the schema, take this into account.

Within the virtual environment (you might need to navigate to the `src` directory for this to work, idk), run the application using the command `flask run`.
