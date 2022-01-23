# Steamy

This code powers a Discord bot that uses the Steam API to make requests for various game statistics and user data.

## Bot Setup 

### Windows Setup
#### Step 1) Install Git

You'll need to install git to preform git commands in the terminal and thus clone (and future update) this repository.  You can install it [here](https://gitforwindows.org/) and follow the installation keeping everything default. 

#### Step 2) Install Python

Next you'll need the latest version of Python from [here](https://www.python.org/downloads/windows/).  Make sure you check off `Add Python to PATH` at the bottom of the installer before proceeding :

![python_installer](https://user-images.githubusercontent.com/14614633/150685352-98169df6-29cf-40cc-90b7-b27d0b9ef3b6.png)

If at the end of the installation you see a `Disable path length limit`, you need click this! Otherwise `python` might not be set as an enviornment variable:

![unnamed (5)](https://user-images.githubusercontent.com/14614633/150688245-03c1f538-7e44-4c13-b5bf-ec8decde7b4b.png)


After installed type `python` in the command prompt to confirm proper setup.  It should show your current Python version:
![python_commandline](https://user-images.githubusercontent.com/14614633/150685563-a606ea25-f408-43a9-b67a-52a3cc566060.png)


*Note : If you have Microsoft Store version of Python installed this may cause issues running Poetry later on*

#### Step 3) Install Poetry

Now you'll need to install Poetry which is a dependency management and packaging tool for Python.  Poetry will be how you actually run the code for the Steamy bot.  There's documentation you could follow [here](https://python-poetry.org/docs/), or you can simply : 
* Download the script from [here](https://install.python-poetry.org) 
* Open the command prompt and change directories via `cd` to where the script was installed (usually `cd desktop`)
* Execute the file with `python install-poetry.py` ![install-poetry](https://user-images.githubusercontent.com/14614633/150686354-9391fd26-57ba-428c-aaaf-4af137a75818.png)
* As the installation print out on the terminal states, you'll need to add the Poetry directory as an environment variable in your PATH.  Go to `View advanced system settings` > `Environment Variables...` and find `Path` under `System variables`.  Edit `Path` > Click `New` > and paste the Poetry bin directory specified in the installation print out on your terminal:  ![poetry_to_PATH](https://user-images.githubusercontent.com/14614633/150686925-69936ee6-7fca-42fa-9b93-9427a208609b.jpg)

You can confirm success of these steps by **opening a new terminal** and typing `poetry --version`, which should show your Poetry version without any errors.  

#### Step 4) Clone the Steamy Repository

Now you're ready to clone the repository.  Type `git clone https://github.com/JDGiardino/Steamy.git` into the command prompt and you should see :

<img width="780" alt="Screen Shot 2021-12-30 at 12 25 46 PM" src="https://user-images.githubusercontent.com/14614633/147774473-667cc8dc-ac85-4b60-a6cf-c8bfdeb5d5e5.png">

Then just change directories to Steamy folder `cd steamy` and type `poetry update` to install the project dependencies in this Poetry enviornment.  

#### Step 5) Setup Steam API Key

In order to run this bot, you'll need to setup a personal Steam API key from https://steamcommunity.com/dev/apikey.  This is a sensitive secret key you should not share with anyone!  Once you've copied the key you'll want to create a new environment variable to assign it to, similar to editing the `Path` environment variable in step 3.  This newly created environment variable needs to be named `STEAM_API_KEY` and the value should be your Steam API key you copied. 

#### Step 6) Setup Discord Bot Token

Now you'll actually set up the bot user. Head to https://discordapp.com/developers and login. From there create a new application, set the name to `Steamy` and image to [the Steam icon](https://www.google.com/search?q=steam+icon&tbm=isch&source=iu&ictx=1&vet=1&fir=8hynYjVJFUF0dM%252CGb1T95sztjRmTM%252C_%253BAchSpA4DjH7QEM%252CnpkQdL8RtTSFyM%252C_%253B-zUyjeBm6ovCVM%252CXN0pmEHbiKS9OM%252C_%253B9hMXImxvW8jXlM%252CcONmuWK17pebeM%252C_%253B_kZqmSftoyURFM%252Ct6coTpJ2-ez1cM%252C_%253B_cU8gNUrJjwzUM%252CS4yjjc59yanu1M%252C_%253B2bCRaHhwcPxBVM%252CXN0pmEHbiKS9OM%252C_%253BNELS2oRXrI_PQM%252C7vZQI2uA8MoknM%252C_%253BEw3iklGCEwGyHM%252Cei_evZrmv3uADM%252C_%253BqOFth9jwk4ePEM%252Cyr-RlZ0T72YoXM%252C_%253BT-9GmSS8r4yDRM%252CtsFgddCOw6LEmM%252C_%253BSQPlt-acUToaEM%252CZWxpyNNPMivswM%252C_%253BH_Ou-2mQVJaNDM%252CXN0pmEHbiKS9OM%252C_%253B5iyGTYYk4B8HWM%252CG6XDcJvebhgsEM%252C_%253BiqIG3IrK38jYfM%252C1PK0z6m7vot2DM%252C_&usg=AI4_-kTteM0yhUUXpC9Li1GpkFvWedHycg&sa=X&ved=2ahUKEwj18PGvtMj1AhXhg-AKHXo5C8QQ9QF6BAgHEAE#imgrc=8hynYjVJFUF0dM), and then click the `Bot` tab on the left. Click `Add bot user` and once that's created, copy the token.  Similar to Step 5, create a new environment variable named 'DISCORD_BOT_TOKEN` and the value should be the token you copied. 

#### Step 7) Running the Bot
You are all setup and finally ready to run the Steamy bot!  

Simply open command prompt, `cd steamy` and `start /b poetry run start-steamy`.  This runs Steamy in the background, so long as you keep the command prompt open the Steamy bot will be online.  Likewise, closing the command prompt ends Steamy.  If you restart your computer you'll just need to enter the command again.







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


