# Лучше не импортировать всю библиотеку datetime а указать необходимые функции
# в формате "from datetime import ..." это позволит сэкономить память
# и скорость загрузки в дальнейшем
import datetime as dt


class Record:
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        # Если в условии можно описать поведение без "not" лучше это сделать
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        # Переменные в python называются с маленькой буквы
        for Record in self.records:
            # Значение dt.datetime.now().date() лучше вынести в переменную а
            # не вычислять её при каждом прохождении цикла
            if Record.date == dt.datetime.now().date():
                # нагляднее в виде "+="
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            # Будет нагляднее и меньше вычислений, если использовать сразу
            # два неравенства "0 < x < 1"
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        # Названия переменных должна указывать на её функцию, чтобы было
        # проще разобраться в коде, нельзя использовать однобуквенные
        # переменные
        x = self.limit - self.get_today_stats()
        if x > 0:
            # Не используем бэкслеш для переноса строк
            # В данном случае лучше заполнять строку через .format, как
            # это сделано ниже, а константные значения строк вынести в
            # константы класса
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        # если в предыдущем условии есть return - не нужен else
        # прочитай про Guard Block
        else:
            # Скобки лишние
            # константные значения строк лучше вынести в константы класса
            return('Хватит есть!')


class CashCalculator(Calculator):
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.
    # Константы класса можно получить внутри функций класса с помощью указания
    # класса: CashCalculator.USD_RATE

    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        # Лишняя операция, одна из переменных нам в дальнейшем не понадобится
        currency_type = currency
        # Название переменной cash_remained не соответсвтует её смыслу
        cash_remained = self.limit - self.get_today_stats()
        # Тут можно создать словарь значений, и в зависимости от значения
        # currency - ключа к этому словарю, будут подставляться type и rate
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            cash_remained == 1.00
            currency_type = 'руб'
        if cash_remained > 0:
            # В f-строки подставляются только переменные, без методов.
            # В данном случае лучше заполнять строку через .format, как
            # это сделано ниже, а константные значения строк вынести в
            # константы класса
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        # прочитай про Guard Block
        elif cash_remained == 0:
            return 'Денег нет, держись'
        # прочитай про Guard Block
        elif cash_remained < 0:
            # Не используем бэкслеш для переноса строк
            #
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)
    # В классе потомке и так будут работать все методы родительского класса.
    # Эта строка ничего не выполняет

    def get_week_stats(self):
        super().get_week_stats()

# Во всей работе лучше использовать type hints и Docstrings
