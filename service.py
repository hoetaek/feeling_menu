from random import choice
from data import feeling_data
import json


def recommend_menu(feeling: str):
    full_message = f'{feeling_to_message(feeling)}\n오늘 메뉴로 {feeling_to_menu(feeling)}은 어떨까요?'
    return full_message


def feeling_to_message(feeling: str):
    message = feeling_data[feeling]['message']
    return message


def feeling_to_menu(feeling: str):
    menu = choice(feeling_data[feeling]['menu'])
    return menu


def get_api_key():
    with open("secret.json", "r") as json_file:
        secret_data = json.load(json_file)
    key = secret_data['api']
    return key


def get_bot_token():
    with open("secret.json", "r") as json_file:
        secret_data = json.load(json_file)
    token = secret_data['token']
    return token
