import json
import subprocess
import sys
from pathlib import Path


CONFIG_PATH = Path('data/config.json')


def install_requirements() -> None:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])


def write_config(auth_token: str, spam_id: str, catch_id: str) -> None:
    payload = {
        'user_token': auth_token.strip(),
        'spam_id': spam_id.strip(),
        'catch_id': catch_id.strip(),
    }
    CONFIG_PATH.write_text(json.dumps(payload, indent=2), encoding='utf8')


def main() -> None:
    install_requirements()
    print('\nInput your discord authorization token:')
    auth_token = input().strip()
    print('Now, input the Channel ID of the channel for spamming:')
    spam_id = input().strip()
    print('Now, input the Channel ID of the channel for catching:')
    catch_id = input().strip()

    write_config(auth_token, spam_id, catch_id)
    print('Configuration saved to data/config.json. Run `python main.py` to start the bot.')


if __name__ == '__main__':
    main()
