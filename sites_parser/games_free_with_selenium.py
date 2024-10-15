import time
from selenium import webdriver

def free_games(mesg, bot, message):
    try:
        browser = webdriver.Chrome()
        browser.get('https://store.epicgames.com/ru/free-games')
        time.sleep(5)
        free_game_url = browser.find_element('css selector','#dieselReactWrapper > div > div > div.css-1vplx76 > main > div.css-1dnikhe > div > div > div > div > div:nth-child(3) > span > div > div > section > div > div:nth-child(1) > div > div > div > a')
        url_first_free_game = free_game_url.get_attribute('href')
        list1 = free_game_url.get_attribute('aria-label').split()
        index11 = list1.index('бесплатно,')
        index12 = list1.index('Бесплатно')
        name1 = ' '.join(list1[index11 + 1:index12])
        date1 = ' '.join(list1[index12 + 3:index12 + 5])
        time.sleep(5)
        bot.send_message(message.chat.id, f'{url_first_free_game}\n'
                                               f'<b>{name1[:-1]}</b>, забрать бесплатно <b>до {date1[:-1]}</b> в Epic Games Store', parse_mode= "html")
    except:
        bot.send_message(message.chat.id,'Не найдено')

    bot.delete_message(message.chat.id, mesg.id)
    meseg = bot.send_message(message.chat.id, 'Запрос выполняется...(1/2)\nПожалуйста, ожидайте ~10 секунд')

    try:
        browser = webdriver.Chrome()
        browser.get('https://store.epicgames.com/ru/free-games')
        time.sleep(5)
        free_game_url_soon = browser.find_element('css selector', '#dieselReactWrapper > div > div > div.css-1vplx76 > main > div.css-1dnikhe > div > div > div > div > div:nth-child(3) > span > div > div > section > div > div:nth-child(2) > div > div > div > a')
        url_second_free_game = free_game_url_soon.get_attribute('href')
        list2 = free_game_url_soon.get_attribute('aria-label').split()
        index21 = list2.index('Скоро,')
        index22 = list2.index('Бесплатно')
        name2 = ' '.join(list2[index21 + 1:index22])
        date2 = ' '.join(list2[index22 + 2:index22 + 4])
        date3 = ' '.join(list2[index22 + 5:index22 + 7])
        bot.send_message(message.chat.id,f'{url_second_free_game}\n'
                                              f'<b>{name2[:-1]}</b>, можно будет забрать бесплатно <b>с {date2} по {date3}</b> в Epic Games Store', parse_mode= "html")
    except:
        bot.send_message(message.chat.id,'Не найдено')

    # Удалить сообщение meseg
    bot.delete_message(message.chat.id, meseg.id)