import json

from django.core.management import BaseCommand

code_for_check_insistence = input('Введите код для поиска: ')


class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code_for_check_insistence = code_for_check_insistence

    def handle(self, *args, **options):
        with open('data_file.json') as file:
            data = json.load(file)
        for dicts in data:
            for key, value in dicts.items():
                if self.code_for_check_insistence in value:
                    return f'Код существует - группа "{key}"'
        return 'Код не существует'
