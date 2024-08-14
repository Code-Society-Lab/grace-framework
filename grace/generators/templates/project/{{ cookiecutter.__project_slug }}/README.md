
# {{ cookiecutter.project_name }}
{{ cookiecutter.project_description }}

---

## Installation
Installing {{ cookiecutter.project_name }} is fairly simple. You can do it in three short step.

0. [Install Python and dependencies](#0-install-python-and-dependencies)
1. [Set up your app and token](#1-set-up-your-app-and-token)
2. [Start the bot](#2-start-the-bot)

### 0. Python and Dependencies
Install [Python](https://www.python.org/downloads/). Python 3.9 or higher is required.

> We highly recommend that you set up a virtual environment for development.
> https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/

In the `grace` directory, open a terminal (Linus/MacOS) or cmd (Windows) and execute `pip install -e .` 
(recommended for development) or `pip install .`. 

### 1. Set up your App and Token
If you did not already do it, [create](https://discord.com/developers/docs/getting-started#creating-an-app) your Discord 
bot. Then, create a file called `.env` in the project directory, open it and add 
`DISCORD_TOKEN=<Past your token here>`. (Replace < ... > by your discord token).

> Do not share that file nor the information inside with anyone.

### 2. Start the Bot
The last part is to execute the bot. Execute `grace start` to start Grace in development mode. The rest
of the installation should complete itself and start the bot.

> If the grace command is unrecognized, be sure that you installed the bot properly. 

## Script Usage
- **Bot Command(s)**:
  - `grace start` : Starts the bot (`ctrl+c` to stop the bot)
- **Database Command(s)**:
    - `grace db create` : Creates the database and the tables
    - `grace db drop`   : Deletes the tables and the database
    - `grace db seed`   : Seeds the tables (Initialize the default values)
    - `grace db reset`  : Drop, recreate and seeds the database.

All commands can take the optional `-e` argument with a string to define the environment.<br>
Available environment: (production, development [default], test)
