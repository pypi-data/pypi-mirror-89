import shutil
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os

# Нужна для названия картинок
name_count = 0


def img_save(sub, themes, counts, path_to_save):  # Функция сохранения изображения по src
    root = path_to_save + '/' + 'data'
    midFolders = ['training', 'testing', 'validation']
    print(themes)
    try:
        os.mkdir(root)
    except FileExistsError:
        pass
    try:
        for midFolder in midFolders:
            os.makedirs(os.path.join(root, midFolder, themes))
    except FileExistsError:
        pass

    for midFolder in midFolders:
        path_s = os.path.join(root, midFolder, themes)
        print(path_s)
        #os.mkdir(path_s + '/' + 'ex')

        count = 0
        for i in sub:
            if count < counts:
                src = i.get_attribute('src')
                try:
                    if src != None:
                        src = str(src)
                        print(count, "/", counts)
                        global name_count
                        name_count += 1
                        count += 1
                        urllib.request.urlretrieve(src, os.path.join(path_s, 'image' + str(name_count) + '.jpg'))
                    else:
                        raise TypeError
                except TypeError:
                    print('fail')
            else:
                break



def separation(path, one, two):  # Функция деленя по пропорциям
    path_separation = path
    images_count = os.listdir(path_separation)
    n_files = len(images_count)
    #
    split_index = int(n_files - (n_files/100 * one))
    #
    list_one = images_count[0:split_index]
    #
    list_two = images_count[split_index:]
    #
    try:
        os.mkdir(path_separation + "/" + str(one))
        os.mkdir(path_separation + "/" + str(two))
    except FileExistsError:
        pass
    destination_one = path_separation + "/" + str(one)
    destination_two = path_separation + "/" + str(two)
    for file in images_count:
        if file in list_one:
            name = os.path.join(path_separation, file)
            if os.path.isfile(name):
                shutil.copy(name, destination_one)
            else:
                print('file does not exist', name)
        if file in list_two:
            name = os.path.join(path_separation, file)
            if os.path.isfile(name):
                shutil.copy(name, destination_two)
            else:
                print('file does not exist', name)


def find_element_in_browser(theme, counts, path_to_save):  # Функция поиска в браузере картинок
    if( (type(theme) == str) and (type(counts) == int) and (type(path_to_save) == str) ):
        theme = theme
        path = r"chromedriver.exe"
        driver = webdriver.Chrome(executable_path=path)
        driver.get('https://google.com')
        search_box_dogs = driver.find_element_by_css_selector('input.gLFyf')  # нашли поисковую строку
        search_box_dogs.send_keys(theme)  # вводим поисковый запрос
        search_box_dogs.send_keys(Keys.ENTER)
        driver.find_element_by_partial_link_text('Картинки').click()
        # код предназначен для прокрутки страницы вниз для загрузки всех изображений
        value = 0
        count = 16  # равен 300 картинкам
        # для нажатия кнопки подгрузки фото
        a = 0
        add_list_image = 0
        if counts > 300:
            count = round(counts / 16) + 3
            # один range равен 16 картинкам
            for i in range(count):
                driver.execute_script("scrollBy(" + str(value) + ", +1000); ")
                value += 1000
                time.sleep(5)
                if (value == 26000):
                    python_button = driver.find_elements_by_xpath("// input [@ class = 'mye4qd' and @ value = 'Ещё результаты']")[0]
                    python_button.click()
        else:
            count = counts
            for i in range(count // 10):
                driver.execute_script("scrollBy(" + str(value) + ", +1000); ")
                value += 1000
                time.sleep(5)
        elem1 = driver.find_element_by_id('islmp')  # Получить элемент по идентификатору со значением islmp.
        sub = elem1.find_elements_by_tag_name("img")
        img_save(sub, theme, counts, path_to_save)
        driver.close()
    return "Error data"


def find_and_separate(theme, quantity, path):  # Главная функция
    try:
        os.mkdir(path + "/" + "SeparateFolder")
    except FileExistsError:
        pass
    # Делаем запрос
    themes = theme.split(',')
    # destination_one = path + "/" + "SeparateFolder"
    if(len(themes) == 2):
        for element in themes:
            # Ищем элементы в интернете и скачиваем их
            find_element_in_browser(element, quantity, path)
            # Сохраняем все элементы поиска в одну папку
            images_count = os.listdir(path)

            '''
            for file in images_count:
                name = os.path.join(path + '/' + element, file)
                if os.path.isfile(name):
                    shutil.copy(name, destination_one)
                else:
                    print("Error file")
                '''
    # Выполняем деление по пропорциям
    #separation(destination_one, separation_one, separation_two)



if __name__ == '__main__':
    find_and_separate("red car,blue car", 1000, "C:\\Users\\Red_Fox\\Pictures")
