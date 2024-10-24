"""Модуль для вывода до 5 самых дешевых цен игр с ссылкой и названием"""
import telebot


def print_result(
        sorted_prices: list, bot: telebot.TeleBot,
        message: telebot.types.Message) -> telebot.types.Message:
    """Выводит до 5 самых дешевых цен игр с ссылкой и названием

    :param sorted_prices: Список с ценами игр по возрастанию, ссылкой и
    названием
    :type sorted_prices: List
    """
    len_pricelist = len(sorted_prices)

    try:
        if len_pricelist >= 5:
            return bot.send_message(
                message.chat.id,
                f'<b>{sorted_prices[0][0]} руб.</b> - '
                f'{sorted_prices[0][1][0]}\n'
                f'{sorted_prices[0][1][1]}\n'
                f'\n'
                f'<b>{sorted_prices[1][0]} руб.</b> - '
                f'{sorted_prices[1][1][0]}\n'
                f'{sorted_prices[1][1][1]}\n'
                f'\n'
                f'<b>{sorted_prices[2][0]} руб.</b> - '
                f'{sorted_prices[2][1][0]}\n'
                f'{sorted_prices[2][1][1]}\n'
                f'\n'
                f'<b>{sorted_prices[3][0]} руб.</b> - '
                f'{sorted_prices[3][1][0]}\n'
                f'{sorted_prices[3][1][1]}\n'
                f'\n'
                f'<b>{sorted_prices[4][0]} руб.</b> - '
                f'{sorted_prices[4][1][0]}\n'
                f'{sorted_prices[4][1][1]}', parse_mode="html"
            )

        elif len_pricelist == 4:
            return bot.send_message(
                message.chat.id,
                f'<b>{sorted_prices[0][0]} руб.</b> - '
                f'{sorted_prices[0][1][0]}\n'
                f'{sorted_prices[0][1][1]}\n'
                f'\n'
                f'<b>{sorted_prices[1][0]} руб.</b> - '
                f'{sorted_prices[1][1][0]}\n'
                f'{sorted_prices[1][1][1]}\n'
                f'\n'
                f'<b>{sorted_prices[2][0]} руб.</b> - '
                f'{sorted_prices[2][1][0]}\n'
                f'{sorted_prices[2][1][1]}\n'
                f'\n'
                f'<b>{sorted_prices[3][0]} руб.</b> - '
                f'{sorted_prices[3][1][0]}\n'
                f'{sorted_prices[3][1][1]}', parse_mode="html"
            )

        elif len_pricelist == 3:
            return bot.send_message(
                message.chat.id,
                f'<b>{sorted_prices[0][0]} руб.</b> - '
                f'{sorted_prices[0][1][0]}\n'
                f'{sorted_prices[0][1][1]}\n'
                f'\n'
                f'<b>{sorted_prices[1][0]} руб.</b> - '
                f'{sorted_prices[1][1][0]}\n'
                f'{sorted_prices[1][1][1]}\n'
                f'\n'
                f'<b>{sorted_prices[2][0]} руб.</b> - '
                f'{sorted_prices[2][1][0]}\n'
                f'{sorted_prices[2][1][1]}', parse_mode="html"
            )

        elif len_pricelist == 2:
            return bot.send_message(
                message.chat.id,
                f'<b>{sorted_prices[0][0]} руб.</b> - '
                f'{sorted_prices[0][1][0]}\n'
                f'{sorted_prices[0][1][1]}\n'
                f'\n'
                f'<b>{sorted_prices[1][0]} руб.</b> - '
                f'{sorted_prices[1][1][0]}\n'
                f'{sorted_prices[1][1][1]}', parse_mode="html"
            )

        elif len_pricelist == 1:
            return bot.send_message(
                message.chat.id,
                f'<b>{sorted_prices[0][0]} руб.</b> - '
                f'{sorted_prices[0][1][0]}\n'
                f'{sorted_prices[0][1][1]}', parse_mode="html"
            )

        else:
            return bot.send_message(
                message.chat.id,
                'Ключи не найдены.\n'
                'Пожалуйста, проверьте точное написание названия игры.\n'
                'Попробуйте заменить цифры на римские (например, Mafia II, '
                'The Elder Scrolls V: Skyrim)'
            )

    except Exception:
        return bot.send_message(
            message.chat.id,
            'Ключи не найдены.\n'
            'Пожалуйста, проверьте точное написание названия игры.\n'
            'Попробуйте заменить цифры на римские (например, Mafia II, '
            'The Elder Scrolls V: Skyrim)'
        )


if __name__ == '__main__':

    sorted_prices = (
        (3259, ('https://plati.market/itm/3901794',
                'STARFIELD (STEAM/RU) 0% КАРТОЙ + ПОДАРОК')),
        (3399, ('https://plati.market/itm/3898631',
                'Starfield (Steam)  🔵 РФ-СНГ')),
        (5299, ('https://plati.market/itm/3898632',
                'Starfield Premium Edition (Steam)🔵 РФ-СНГ')),
        (5690, ('https://plati.market/itm/3782364',
                'STARFIELD * RU/KZ/СНГ/TR/AR * STEAM АВТОДОСТАВКА')),
        (5934, ('https://plati.market/itm/3782302',
                'STARFIELD STANDARD/PREMIUM STEAM ⚡️АВТО RU+TR+KZ')),
        (6990, ('https://plati.market/itm/3782532',
                '🌌🌟STARFIELD STEAM GIFT🌟🌌 ☑️РФ/МИР☑️')),
        (7990, ('https://plati.market/itm/3782367',
                'STARFIELD DIGITAL PREMIUM EDITION RU/KZ/СНГ/TR/AR')),
    )

    print(
        f'<b>{sorted_prices[0][0]} руб.</b> - {sorted_prices[0][1][0]}\n'
        f'{sorted_prices[0][1][1]}\n'
        f'\n'
        f'<b>{sorted_prices[1][0]} руб.</b> - {sorted_prices[1][1][0]}\n'
        f'{sorted_prices[1][1][1]}\n'
        f'\n'
        f'<b>{sorted_prices[2][0]} руб.</b> - {sorted_prices[2][1][0]}\n'
        f'{sorted_prices[2][1][1]}\n'
        f'\n'
        f'<b>{sorted_prices[3][0]} руб.</b> - {sorted_prices[3][1][0]}\n'
        f'{sorted_prices[3][1][1]}\n'
        f'\n'
        f'<b>{sorted_prices[4][0]} руб.</b> - {sorted_prices[4][1][0]}\n'
        f'{sorted_prices[4][1][1]}'
    )
