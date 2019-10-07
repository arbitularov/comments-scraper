from selenium import webdriver
from tqdm import tqdm

import pandas as pd

import json
import time
import sys
import os
import socket

def is_connected():
    try:
        socket.create_connection(("www.google.com", 80))
        return False #True
    except OSError:
        pass
    return True #False

def get_comment(driver, path_to_post):
    user_comments = []

    driver.get(path_to_post)
    try:
        close_button = driver.find_element_by_class_name('xqRnw')
        close_button.click()
    except:
        pass


    try:
        load_more_comment = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[2]/div[1]/ul/li[2]/button')
        i = 0
        while load_more_comment.is_displayed():
            load_more_comment.click()
            i += 1
            time.sleep(3)
    except:
        pass


    description = driver.find_element_by_class_name('C4VMK')
    description = description.find_elements_by_tag_name('span')[1].text

    comment = driver.find_elements_by_class_name('gElp9 ')
    for c in comment:
        container = c.find_element_by_class_name('C4VMK')
        content = container.find_element_by_tag_name('span').text
        content = content.replace('\n', ' ').strip().rstrip()
        user_comments.append(content)

    user_comments.pop(0)

    return description, user_comments


def main():

    driver = webdriver.Chrome("/Users/arbi/Desktop/chromedriver")

    descriptions = 0
    comment_count = 0
    zero_comment_descriptions = 0
    loss = 0
    restart_driver_step = 500



    links = pd.read_csv('links.csv',header=None)

    with open('comments.json','w', encoding='utf-8') as f_json:
        f_json.write('[\n')
        with tqdm(total=25300) as progbar:
            for idx, link in links.iterrows():

                if idx % restart_driver_step == 0:
                    driver.close()
                    print("Перезагрузка driver, в течении 20 секунд...")
                    time.sleep(10)
                    driver = webdriver.Chrome("/Users/arbi/Desktop/chromedriver")
                    time.sleep(10)

                if is_connected():
                    internet = True
                    while internet:
                        time.sleep(10)
                        internet = is_connected()
                        print("Нет интернета!", time.ctime())
                    print("Интернет есть!", time.ctime())

                try:
                    description, comments = get_comment(driver, link[0])
                    descriptions += 1
                    len_comments = len(comments)
                    comment_count += len_comments
                    if len_comments == 0:
                        zero_comment_descriptions += 1
                    #print("description ", len(description), description, "comments", len(comments), comments)
                    data = {'описание': description, 'комменты': comments}
                    out = json.dumps(data, ensure_ascii=False)
                    print(f'\t{out},', file=f_json)
                except:
                    loss += 1
                    print("Не загрузил пост: ", link[0])

                progbar.set_postfix(description='{}'.format(descriptions),
                                    comment='{}'.format(comment_count),
                                    loss='{}'.format(loss),
                                    zero='{}'.format(zero_comment_descriptions))

                progbar.update()

        f_json.seek(0, os.SEEK_END)
        f_json.seek(f_json.tell() - 3, os.SEEK_SET)
        f_json.write('\n]')

    driver.close()

if __name__ == '__main__':
    main()
