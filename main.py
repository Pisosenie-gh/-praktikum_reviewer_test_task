# Желательно импортировать только необходимые методы из модуля.
import datetime as dt


# Не хватает описания класса (docstring).
class Record:
    # Желательно добавлять аннотацию типов для лучшей читаемости кода.
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        """
            Тернарный оператор if лучше использовать для условий,
            которые можно записать в одну строку.
            Нужно проверять if date (убрать not)
            или заменить на простое условие .
        """
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


# Не хватает описания класса и методов (docstring).
class Calculator:
    # Желательно добавлять аннотацию типов для лучшей читаемости кода.
    # https://peps.python.org/pep-0484/
    # https://peps.python.org/pep-0483/
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        # Нужно изменить название переменной т.к Record - имя класса.
        # По PEP8 имя переменной должно начинаться с маленькой буквы.
        for Record in self.records:
            if Record.date == dt.datetime.now().date():
                # Лучше использовать +=
                # today_stats += Record.amount
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


# Не хватает описания класса и метода (docstring).
class CaloriesCalculator(Calculator):
    # При комментировании функции лучше использовать Docstring Conventions
    # https://peps.python.org/pep-0257/
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        # Название переменной должно иметь смысл.
        x = self.limit - self.get_today_stats()
        if x > 0:
            # Для переноса длинной строки можно использовать тройные кавычки.
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        else:
            # Скобки не нужны.
            return ('Хватит есть!')


class CashCalculator(Calculator):
    # Нужно убрать конвертацию типов или использовать типизацию.
    # USD_RATE: float = 60.0 или USD_RATE = 60.0
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        """
            Создание переменной currency_type лишнее, т.к в условиях
            можно использовать переменную currency
            либо везде используйте созданную currency_type.
        """
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        # Лишнее условие, т.к просто сравнили cash_remained c 1.00.
        elif currency_type == 'rub':
            cash_remained == 1.00
            currency_type = 'руб'
        if cash_remained > 0:
            # Для переноса длинной строки можно использовать тройные кавычки.
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        # Можно использовать f-строку вместо .format().
        # Можно убрать бэкслеш
        # и использовать f""" {'%0.2f'%cash_remained} """...
        # Убрать - , т.к cash_remained уже отрицатльное число
        elif cash_remained < 0:
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

    # Данный метод не нужно переопределять в дочернем классе,
    # т.к. никакой дополнительной логики в нем не выполняется
    def get_week_stats(self):
        super().get_week_stats()
