import json
import os

from promogenerator.management.commands.generate_promocode import group, amount
from promogenerator.management.commands.code_insistence import code_for_check_insistence

from django.core.management import call_command


def test_generate_promo_code_command():
    """ Функция проверяющая количество сгенерированных кодов.
    Созданная группа проверяется автоматически при сравнении 'if group == key:', т.к. key считывается уже в
    обновленном файле """
    if os.path.exists(os.getcwd() + '/data_file.json'):
        with open('data_file.json') as file:
            data_before = json.load(file)
        for dicts in data_before:
            for key, value in dicts.items():
                if key == group:
                    old_length_of_values = len(value)
                elif group not in dicts.keys():
                    old_length_of_values = 0
    else:
        old_length_of_values = 0

    args = []
    opts = {}
    call_command('generate_promocode', *args, **opts)

    with open('data_file.json') as file:
        data_after = json.load(file)
    for dicts in data_after:
        for key, value in dicts.items():
            if group == key:
                assert old_length_of_values + amount == len(value)


def test_code_insistence():
    """ Функция проверяет вывод команды, проверяющей наличие промокода в файле json """
    args = []
    opts = {}
    result = call_command('code_insistence', *args, **opts)

    with open('data_file.json') as file:
        data = json.load(file)
    for dicts in data:
        for key, value in dicts.items():
            if code_for_check_insistence in value:
                assert result == f'Код существует - группа "{key}"'
            else:
                assert result == 'Код не существует'
