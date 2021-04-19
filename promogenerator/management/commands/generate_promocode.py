import json
import os
import secrets
import string

from django.core.management import BaseCommand

group = input('Введите название группы: ')
amount = int(input('Введите количество промо-кодов для генерации: '))
promo_code_length = 10


class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group = group.lower()
        self.amount = amount
        self.promo_codes_dict = {}
        self.codes = []
        self.data = []
        self.list_for_checking_insistence = []
        self.promo_code_length = promo_code_length

    def promo_code_generator(self):
        """ Функция генерирующая один промо-код """
        code = ''.join(secrets.SystemRandom().choice(string.ascii_uppercase + string.digits)
                       for _ in range(self.promo_code_length))
        return code

    def check_repeating_promo_code(self):
        """ Функция, которая после чтения json файла создаёт список всех значений (промо-кодов) для проверки на
        повторение генерируемых кодов """
        for dicts in self.data:
            for value in dicts.values():
                for promo in value:
                    self.list_for_checking_insistence.append(promo)

    def create_new_group(self):
        """ Функция создания новой группы кодов и проверяющая коды из файла json и
        списка только что сгенерированных кодов на повторение """
        self.check_repeating_promo_code()
        i = 0
        while i != self.amount:
            code = self.promo_code_generator()
            if code in self.codes:
                continue
            elif code in self.list_for_checking_insistence:
                continue
            else:
                self.codes.append(code)
                i += 1
        self.promo_codes_dict[self.group] = self.codes
        self.data.append(self.promo_codes_dict)

    def check_group_insistence(self):
        """ Функция проверяющая существует ли введенная пользователем группа, если да,
        то дополняет список промо-кодов количеством указанным пользователем """
        self.check_repeating_promo_code()
        for dicts in self.data:
            for key, value in dicts.items():
                if key == self.group:
                    i = 0
                    while i != self.amount:
                        code = self.promo_code_generator()
                        if code in self.list_for_checking_insistence:
                            continue
                        elif code in value:
                            continue
                        else:
                            value.append(code)
                            i += 1
                    return True

    def save_json_file(self):
        """ Функция сохранения данных в json файл """
        with open("data_file.json", "w") as write_file:
            json.dump(self.data, write_file, indent=4)

    def handle(self, *args, **options):
        """ Основная функция """
        if os.path.exists(os.getcwd() + '/data_file.json'):
            with open('data_file.json') as file:
                self.data = json.load(file)
            if self.check_group_insistence():
                self.save_json_file()
            else:
                self.create_new_group()
                self.save_json_file()
        else:
            self.create_new_group()
            self.save_json_file()
