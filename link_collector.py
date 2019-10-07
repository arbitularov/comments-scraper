from selenium import webdriver

import time
import csv
import socket


def is_connected():
    try:
        socket.create_connection(("www.google.com", 80))
        return False #True
    except OSError:
        pass
    return True #False

def csv_writer(data, path):

	with open(path, "w", newline='') as csv_file:
		writer = csv.writer(csv_file, delimiter='\n')
		writer.writerow(data)

def get_links(driver):
	links = []
	pathes = driver.find_elements_by_class_name('v1Nh3')

	for p in pathes:

		link = p.find_element_by_tag_name('a')
		links.append(link.get_attribute('href'))

	return links

def main():

	url = 'https://www.instagram.com/groznytv/'

	driver = webdriver.Chrome("/Users/arbi/Desktop/chromedriver")

	driver.get(url)

	SCROLL_PAUSE_TIME = 5
	URL_COUNTS = 25300

	last_height = driver.execute_script("return document.body.scrollHeight")

	links = []
	links.extend(get_links(driver))

	while True:

		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(SCROLL_PAUSE_TIME)

		new_height = driver.execute_script("return document.body.scrollHeight")
		time.sleep(SCROLL_PAUSE_TIME)
		if is_connected():
			internet = True
			while internet:
				time.sleep(SCROLL_PAUSE_TIME*2)
				internet = is_connected()
				print("Нет интернета!", time.ctime())
				driver.execute_script("window.scrollTo(0, -document.body.scrollHeight);")
			print("Интернет есть!", time.ctime())
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

			links.extend(get_links(driver))
			last_height = new_height

		else:
			links.extend(get_links(driver))
			last_height = new_height

		if len(set(links)) >= URL_COUNTS:
			break

	links = set(links)
	print(len(links))

	csv_writer(links, 'links.csv')
	driver.close()

if __name__ == '__main__':
	main()
