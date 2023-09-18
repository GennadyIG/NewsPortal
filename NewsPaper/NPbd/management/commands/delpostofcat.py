from django.core.management.base import BaseCommand, CommandError
from NPbd.models import Post, Category

class Command(BaseCommand):
    help = 'Удаление постов относящихся к заданной категории'

    # def add_arguments(self, parser):
    #     parser.add_argument('argument', )

    def handle(self, *args, **options):
        self.stdout.readable()
        cats = Category.objects.values_list("name", flat=True)
        self.stdout.write(f'Посты какой категории необходмо удалить? '
                          f'Введите значение из списка: {", ".join(cats)}')
        answer = input()
        if answer not in cats:
            raise CommandError('Такой категории нет')
        self.stdout.write(f'Вы уверены в удалении постов категории {answer}? да/нет')
        confirmation = input()
        if confirmation == 'да':
            Post.objects.filter(category__name=f'{answer}').delete()
            self.stdout.write(self.style.SUCCESS(f'Посты относящиеся к категории {answer} удалены.'))
            return

        self.stdout.write(self.style.ERROR('Удаление отменено.'))
