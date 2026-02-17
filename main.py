import os
import re, asyncio, json, random, string
from discord.ext import commands
from discord.ext import tasks

version = 'v2.7.4'


def load_runtime_config():
    env_user_token = os.getenv('USER_TOKEN')
    env_spam_id = os.getenv('SPAM_ID')
    env_catch_id = os.getenv('CATCH_ID')

    if env_user_token and env_spam_id and env_catch_id:
        return env_user_token, env_spam_id, env_catch_id

    try:
        with open('data/config.json', 'r', encoding='utf8') as file:
            raw = file.read().strip()
            if not raw:
                raise ValueError('data/config.json is empty')
            info = json.loads(raw)
    except FileNotFoundError as error:
        raise RuntimeError(
            'Missing data/config.json. Run setup.py locally or set USER_TOKEN, SPAM_ID, and CATCH_ID environment variables.'
        ) from error
    except json.JSONDecodeError as error:
        raise RuntimeError(
            'data/config.json contains invalid JSON. Re-run setup.py or fix the file manually.'
        ) from error
    except ValueError as error:
        raise RuntimeError(
            'data/config.json is empty. Re-run setup.py or set USER_TOKEN, SPAM_ID, and CATCH_ID environment variables.'
        ) from error

    user_token = info.get('user_token')
    spam_id = info.get('spam_id')
    catch_id = info.get('catch_id')

    if not user_token or not spam_id or not catch_id:
        raise RuntimeError(
            'Missing required config fields. Ensure user_token, spam_id, and catch_id are set in data/config.json '
            'or via USER_TOKEN, SPAM_ID, and CATCH_ID environment variables.'
        )

    return user_token, spam_id, catch_id


user_token, spam_id, catch_id = load_runtime_config()

with open('data/pokemon', 'r', encoding='utf8') as file:
    pokemon_list = file.read()
with open('data/legendary', 'r', encoding='utf8') as file:
    legendary_list = file.read()
with open('data/mythical', 'r', encoding='utf8') as file:
    mythical_list = file.read()
with open('data/level', 'r', encoding='utf8') as file:
    to_level = file.readline().strip()

num_pokemon = 0
shiny = 0
legendary = 0
mythical = 0

poketwo = 716390085896962058
bot = commands.Bot(command_prefix='->', self_bot=True)
intervals = [1.5, 1.6, 1.7, 1.8, 1.9]


def solve(message):
    hint = []
    for i in range(15, len(message) - 1):
        if message[i] != '\\':
            hint.append(message[i])
    hint_string = ''.join(hint)
    hint_replaced = hint_string.replace('_', '.')
    solution = re.findall('^' + hint_replaced + '$', pokemon_list, re.MULTILINE)
    return solution


@tasks.loop(seconds=random.choice(intervals))
async def spam():
    channel = bot.get_channel(int(spam_id))
    if channel is not None:
        await channel.send(''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=random.randint(12, 24))))


@spam.before_loop
async def before_spam():
    await bot.wait_until_ready()


def start_spam_loop():
    if not spam.is_running():
        spam.start()


@bot.event
async def on_ready():
    print(f'Logged into account: {bot.user.name}')
    start_spam_loop()


@bot.event
async def on_message(message):
    channel = bot.get_channel(int(catch_id))
    if channel is None:
        return

    if message.channel.id == int(catch_id):
        if message.author.id == poketwo:
            if message.embeds:
                embed_title = message.embeds[0].title
                if embed_title and 'wild pokémon has appeared!' in embed_title:
                    if spam.is_running():
                        spam.cancel()
                    await asyncio.sleep(1)
                    await channel.send('p!h')
                elif embed_title and 'Congratulations' in embed_title:
                    embed_content = message.embeds[0].description
                    if embed_content and 'now level' in embed_content:
                        split = embed_content.split(' ')
                        a = embed_content.count(' ')
                        level = int(split[a].replace('!', ''))
                        if level == 100 and to_level:
                            await channel.send(f'p!s {to_level}')
                            with open('data/level', 'r', encoding='utf8') as fi:
                                data = fi.read().splitlines(True)
                            with open('data/level', 'w', encoding='utf8') as fo:
                                fo.writelines(data[1:])
            else:
                content = message.content
                if 'The pokémon is ' in content:
                    matches = solve(content)
                    if not len(matches):
                        print('Pokemon not found.')
                    else:
                        for i in matches:
                            await asyncio.sleep(1)
                            await channel.send(f'p!c {i}')
                    check = random.randint(1, 240)
                    if check == 1:
                        await asyncio.sleep(900)
                        start_spam_loop()
                    else:
                        await asyncio.sleep(1)
                        start_spam_loop()

                elif 'Congratulations' in content:
                    global shiny
                    global legendary
                    global num_pokemon
                    global mythical
                    num_pokemon += 1
                    split = content.split(' ')
                    pokemon = split[7].replace('!', '')
                    if 'seem unusual...' in content:
                        shiny += 1
                        print(f'Shiny Pokémon caught! Pokémon: {pokemon}')
                        print(f'Shiny: {shiny} | Legendary: {legendary} | Mythical: {mythical}')
                    elif re.findall('^' + pokemon + '$', legendary_list, re.MULTILINE):
                        legendary += 1
                        print(f'Legendary Pokémon caught! Pokémon: {pokemon}')
                        print(f'Shiny: {shiny} | Legendary: {legendary} | Mythical: {mythical}')
                    elif re.findall('^' + pokemon + '$', mythical_list, re.MULTILINE):
                        mythical += 1
                        print(f'Mythical Pokémon caught! Pokémon: {pokemon}')
                        print(f'Shiny: {shiny} | Legendary: {legendary} | Mythical: {mythical}')
                    else:
                        print(f'Total Pokémon Caught: {num_pokemon}')
                elif 'human' in content:
                    if spam.is_running():
                        spam.cancel()
                    print('Captcha detected; autocatcher paused. Press enter to restart, after solving captcha manually.')
                    input()
                    await channel.send('p!h')
    if not message.author.bot:
        await bot.process_commands(message)


print(f'Pokétwo Autocatcher {version}\nA second gen free and open-source Pokétwo autocatcher by devraza\nEvent Log:')
bot.run(f'{user_token}')
