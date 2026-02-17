# This project is deprecated

It is now prefered that you use the `poketwo` module in [persona](https://github.com/rodofdiscord/persona). 

## Catchtwo
A second generation **free** and open-source Pokétwo autocatcher, created with the goal of preventing people from wasting their money.

---

**For a version of this autocatcher that works easily with repl.it, please see the replit branch [here](https://github.com/devraza/catchtwo/tree/replit)**.

### Features
The bot has the following features:
- ⚙️ Easy Setup (simply run a script and enter the correct information, no 'coding' needed)
- ⬆️ Auto-levelling (Level up all your duel Pokémon to level 100 **overnight**!)
- ✨ Get notified when and if you've caught a Pokémon, and also if another event occurs
    - See when a Shiny/Legendary/Ultra Beast/Mythical Pokémon is caught, and which one it is!
- 💲 **Completely free** and open-source (you can see the code as it is currently)
- 💕 **Trustworthy**; this autocatcher is **completely** open-source (meaning you can see the latest code)
- 📜 Support for all Pokémon from generation I to generation VIII, including all Alolan and Galarian Pokémon
- 🏎️ Super fast; the autocatcher can even handle Incense!
- 🔍 Pokétwo-Resistant - the autocatcher sends a random series of numbers to enhance undetectability

### Requirements
Use **Python 3.10** for hosting deployments (recommended on Render).
Python 3.10 is the safest default for this project in hosted environments.

#### <b>Running the bot</b>
To start up the bot for the first time, please download the latest release from [here](https://github.com/devraza/catcher-one/releases/). <br>
Once you have done that, run the `setup.py` file using the command `python3 setup.py` and enter in the following fields when asked:

##### <b>user_token</b>:
Paste in your discord account's user token. You can find instructions on this [here](https://www.youtube.com/watch?v=3W9tAEsK7RM)

##### <b>channel_id</b>:
This will allow the bot to use your preferred channel to spam as well as catch Pokétwo spawns. Make sure you paste this carefully, as If you set it to the wrong channel it will spam and catch there. See [here](https://www.youtube.com/watch?v=6dqYctHmazc) for help on getting this.

After you've entered that in, the autocatcher should start successfully. (if not, check if you have entered in the right fields)

> Remember to cd into your autocatcher folder as well. If you need any help with something, feel free to open a Github Issue.


### Running on hosting providers
Many hosts (Railway, Render, Fly.io, etc.) are non-interactive, so `setup.py` may fail there.
Use environment variables instead:

- `USER_TOKEN`
- `SPAM_ID`
- `CATCH_ID`

Then start the app with:

```bash
pip install -r requirements.txt
python main.py
```

If those variables are set, `main.py` will use them and will not require `data/config.json`.


### KataBump / Pterodactyl-style panel fix (`EOFError: EOF when reading a line`)
If your console shows this error from `setup.py`:

```
EOFError: EOF when reading a line
```

it means your host is starting `setup.py` in a non-interactive environment, where `input()` prompts cannot be answered.

Use this instead:

- **Startup File / Start Command**: `python main.py`
- **Do NOT use**: `python setup.py`

Set these environment variables in the panel:

- `USER_TOKEN`
- `SPAM_ID`
- `CATCH_ID`

Also make sure dependencies are installed first:

```bash
pip install -r requirements.txt
```

### Render deployment fields (copy/paste)
Use a **Background Worker** on Render (not a Web Service), because this bot does not expose an HTTP port.

- **Environment**: `Python 3`
- **Python Version**: `3.10.13` (or latest available `3.10.x`)
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python main.py`
- **Auto-Deploy**: optional (`On Commit` recommended)
- **Plan**: any plan that supports always-on workers

Set these Render environment variables:

- `USER_TOKEN` = your Discord user token
- `SPAM_ID` = channel ID for spam messages
- `CATCH_ID` = channel ID where Pokétwo appears

If you accidentally create a Web Service, Render may fail health checks since no port is opened; switch it to a Background Worker.

### Auto-levelling
To enable auto-levelling, just put in the ID's of the Pokémon you want to be levelled up into the `level` file (inside the `data` folder).

---

## **DISCLAIMER**

Please note that self botting is against Discord's Terms of Service and being discovered using a self bot may result in your account being banned. To avoid this, keep knowledge of your self bot to a minimum and use a throwaway account. I am not responsible for any accounts lost due to the self bot. I also recommend checking the self bot channel's messages occasionally to see if Pokétwo has sent a captcha. **If it has, it would be a good idea to solve it.**

---
