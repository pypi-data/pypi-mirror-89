import argparse
import configparser
import os
import sys
import subprocess
import logging
from datetime import datetime

from telegram.bot import Bot


def send_result(arguments, start_time, end_time, return_code, text):
    config = configparser.ConfigParser()
    config.read('config.ini')

    title = 'Success' if return_code == 0 else "Error"
    command = ' '.join(arguments)
    execution_time = end_time - start_time

    message = f"**{title}**\n\n **{command} \n\n **Execution time: {execution_time} \n\n\n Log output:\n ```text```"

    bot = Bot(config['telegram']['token'])
    bot.send_message(config['telegram']['username'], message, parse_mode='Markdown')


def notify(arguments):
    return_code = 0
    text = ""

    start_time = datetime.today()
    try:
        result = subprocess.check_output(arguments, stderr=subprocess.STDOUT)
        text = result.decode('utf-8')

    except subprocess.CalledProcessError as error:
        return_code = error.returncode
        text = error.stdout.decode('utf-8')
    end_time = datetime.today()

    send_result(arguments, start_time, end_time, return_code, text)


def config(arguments):
    config = configparser.ConfigParser()
    config['telegram'] = {'username': arguments.username,
                          'token': arguments.token}

    with open('config.ini', 'w') as fout:
        config.write(fout)


def check_config():
    config = configparser.ConfigParser()

    if not os.path.isfile('config.ini'):
        return False

    config.read('config.ini')

    if 'telegram' not in config:
        return False

    telegram_config = config['telegram']
    if 'username' not in telegram_config or 'token' not in telegram_config:
        return False

    return True


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    config_parser = subparsers.add_parser('config')
    config_parser.add_argument('--username', help='Your telegram username.', required=True)
    config_parser.add_argument('--token', help='Token for your telegram bot.', required=True)
    config_parser.set_defaults(mode='config')

    notify_parser = subparsers.add_parser('notify')
    notify_parser.set_defaults(mode='notify')

    known, unknown = parser.parse_known_args()
    if known.mode == 'config':
        config(known)
    elif known.mode == 'notify':
        if check_config():
            notify(unknown)
        else:
            raise FileNotFoundError('You have not configured the tool.')
