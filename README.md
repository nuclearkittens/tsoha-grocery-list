# Grocery List Web App – Database Application Project, University of Helsinki (Summer 2023)
This web-based app is coursework for the University of Helsinki Database Application Project course. The aim is to create a web-based application to make a life just a bit easier by streamlining one of the most tedious parts of your weekly shop – i.e. compiling a shopping list.

## Project overview
### Main functionalities:
+ The user can register/log in
+ The user can create/save shopping lists
+ The user can view their previous shopping lists
+ The shopping list items are put categorised (fruit & veg, chilled food, frozen food, household items, etc.) for easier shopping
+ The user can edit an existing shopping list
+ The user can delete old shopping lists
+ The user can share a shopping list (kind of – this is fairly pointless when the application is run locally)
+ The user can delete their account

If I decide to come back to this project at a later date, the following could be implemented:

+ The user can add recipes (at least manually) from which the ingredients are imported to a shopping list
+ Unit of measurement conversion

### Known issues (*updated 02/07/23*):
+ When creating a new list, pressing `return` submits the last (can only use `tab` to navigate between fields)
+ When adding a new item to a list (either in creating a new list or editing an existing one), the new row has to be filled
+ The layout is a mess

For my own convenience, I have created a [spreadsheet](https://docs.google.com/spreadsheets/d/17Hk51ZoDV1AqUWWAYf6MvK6ZVflhoNZ81wzrthbtHzs/) to track the project progress. It includes a roadmap/backlog of sorts, checklists for deadlines, and I will probably use it for general planning/time keeping as well.

## Project progress

### *update 04/06/23*

The project is still very much a work in progress – only the log in/log out/register functionalities are (more or less) fully working. Lazy, me? You got it. Slowly getting into this.

On the database side of things, well, nothing is really implemented in the actual project yet. Been re-familiarising myself with SQL queries and playing around before diving into the implementation, so that I have an actual idea of what I'm doing.

The backlog spreadsheet has been updated, too, and I will keep using it, possibly add some more user stories if my time management allows it. The list of main functionalities (above) has been updated as well per the feedback I got on Labtool.

***

### *update 18/06/23*

Guess who got Just Dance 2022 a week ago and has been playing that instead of studying? Yes, that's me. Thanks to my awesome procrastination skills, I am somewhat behind with this project. However, below are new implemented functions and other updates:

+ The database schema has been updated to support current functionalities better
+ The user can create new grocery lists, as well as delete existing ones
+ The user page lists all of the users grocery lists
+ Error handling has been improved
+ The routes follow the PRG model better than previously, as per Labtool feedback
+ The grocery lists have a maximum item limit (currently 64 because why not)
+ The grocery lists can contain multiple items of the same name if the categories or units are different (duplicates should not be possible)
+ The spreadsheet has been updated

There is still a long way to go before the project is finished. I aim to add list editing next (some backend stuff for that is already in progress), plus the last week before final deadline will be dedicated for making the application presentable and testing.

***

### *update 02/07/2023*

As per usual, I had grand plans for my coursework. And again, I did not quite manage to meet all my expectations. I still need to learn to keep it simple. However, all the main functionalities I set out to do are implemented, the database has slightly grown during the project, and everything seems to work. During the last two weeks the project has seen these additions:

+ Editing of existing lists is now possible, including deleting items, updating the quantity, and adding new items
+ There is functionality to share the URL for a list – obviously fairly pointless if the application is only run locally and not in production, but hey ho
+ Both in the code review and Labtool feedback I was notified of the application displaying a wrong message when a list was successfully deleted – this has been fixed
+ Users can delete their accounts
+ The application has actual styling and a layout

Slightly disappointed I did not leave more time for the layout design, as I generally enjoy it. I am well aware the checkbox buttons do not align with text, and accessibility might be a problem as I simply did not have time to refactor all my templates to be more screenreader or text-based browser friendly.

I also apologise for not including any test data – I very much planned to do this, but only remembered it 15 minutes before the final deadline.

***

**There are absolutely no automated tests, so no guarantees of anything working. Code is fairly clean and documented, and linting is done using pylint (currently 9.51/10). The templates and stylesheet are a bit of a mess, been ages since I've written any HTML/CSS, sorry.**

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
