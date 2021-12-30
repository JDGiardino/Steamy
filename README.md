# Steamy

This code powers a Discord bot that uses the Steam API to make requests for various game statistics and user data.

## Bot Setup 

### Windows Setup
Step 1) You'll need to install git to preform git commands in the terminal and thus clone this repository.  You can install it [here](https://gitforwindows.org/) and follow the installation keeping everything default. 

Step 2) Next you'll need the latest version of Python.  First, I downloaded and installed from https://www.python.org/.  I also needed to install Python from the Microsoft store which can be accessed simply by typing `python` into the Command Prompt.  This lands you on the following page: 
![unnamed (1)](https://user-images.githubusercontent.com/14614633/147771455-14ce98fb-5988-438d-bc5d-fd41ca062816.png)
After installed typing `python` in the command line should show your current Python version
![unnamed (3)](https://user-images.githubusercontent.com/14614633/147776334-6d6ef956-3dbd-4054-87ef-04973e6cb65c.png)


Step 3) Finally you'll need to install pip which can be done by typing `curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py` into the command line.

Step 4) Now you're ready to clone the repository.  Type `git clone https://github.com/JDGiardino/Steamy.git` into the command line and you should see :

<img width="780" alt="Screen Shot 2021-12-30 at 12 25 46 PM" src="https://user-images.githubusercontent.com/14614633/147774473-667cc8dc-ac85-4b60-a6cf-c8bfdeb5d5e5.png">





## Bot Commands
The following lists all the commands Steamy bot can preform and examples of their output:

`$help` - This command sends a direct message to user who called it, with a list of all commands Steamy can preform.

<img width="602" alt="Screen Shot 2021-12-21 at 10 22 59 PM" src="https://user-images.githubusercontent.com/14614633/147030248-b1fefcd2-7f55-477a-8b73-4ce7b129e62a.png">
<img width="747" alt="Screen Shot 2021-12-21 at 10 23 24 PM" src="https://user-images.githubusercontent.com/14614633/147030266-0cd25832-091f-46c5-a574-b9f38cac90df.png">

`$achievement GAME_NAME` - This command posts to the server the rarest achievement for the given game name.

<img width="664" alt="Screen Shot 2021-12-21 at 10 26 21 PM" src="https://user-images.githubusercontent.com/14614633/147030640-25e85b2d-a7f1-478e-b4d4-2c2a386031b1.png">

`$user USER_NAME` - This command posts to the server the total played hours on Steam for the given Steam user name.

<img width="605" alt="Screen Shot 2021-12-21 at 10 31 13 PM" src="https://user-images.githubusercontent.com/14614633/147030910-6344f0f4-d4e9-49be-aa50-58f84c1b7184.png">

`$game GAME_NAME` - This command posts to the server the player count and rank in top played games for the given game name. 

<img width="641" alt="Screen Shot 2021-12-21 at 10 33 06 PM" src="https://user-images.githubusercontent.com/14614633/147031190-9c937f96-dc38-4b6e-9e9d-f9b1967b625a.png">

`$top NUMBER` - This command posts to the server the top played games by player count up to the given number(No higher than 100).

<img width="635" alt="Screen Shot 2021-12-21 at 10 39 08 PM" src="https://user-images.githubusercontent.com/14614633/147031705-477465be-4a55-44c1-92f1-eb69e0810b31.png">

`$users_game "USERS_NAME" "GAME_NAME"` - This command posts to the server a given user's played hours and unlocked achievements for a given game.

<img width="657" alt="Scre![Uploading Screen Shot 2021-12-21 at 11.04.23 PM.png…]() en Shot 2021-12-21 at 10 43 33 PM" src="https://user-images.githubusercontent.com/14614633/147032049-9af3ef78-a000-4675-b21d-34d55205e9d6.png">

`$game_id GAME_NAME` - This command posts to the server the ID for a given game name. 

<img width="414" alt="Screen Shot 2021-12-21 at 11 04 23 PM" src="https://user-images.githubusercontent.com/14614633/147037953-9ec74d3c-8788-40d4-9d97-dafe491466e0.png">

`$user_id` USER_NAME - This command posts to the server the ID for a given Steam user name.

<img width="523" alt="Screen Shot 2021-12-21 at 11 57 38 PM" src="https://user-images.githubusercontent.com/14614633/147038061-df0c57e4-d5aa-4957-95e9-db636cf1ae95.png">


