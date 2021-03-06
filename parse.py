import requests
from bs4 import BeautifulSoup
import csv
import subprocess
import os
from datetime import datetime


def __clear_data():
	subprocess.call(['spark-submit', 'clear_data.py'])


def __append_row(path, row):
	with open(path, 'a', encoding='utf8') as file:
		writer = csv.writer(file)
		writer.writerow(row)




def __parse_page(url, mark, page_num):

	result = requests.get(url.format(mark, page_num))
	soup = BeautifulSoup(result.content, 'html.parser')
	resultCarsList = []
	carsList = soup.select('.ListingItem-module__container')
	if len(carsList) == 0:
		return -1


	for car in carsList:
		resultrow = []
		try:
			resultrow.append(car.select_one('.ListingItemTitle-module__link').text)

			for option in car.select('.ListingItemTechSummaryDesktop__cell'):
				resultrow.append(option.text)

			resultrow.append(car.select_one('.ListingItemPrice-module__content').text)
			resultrow.append(car.select_one('.ListingItem-module__year').text)
			resultrow.append(car.select_one('.ListingItem-module__kmAge').text)
			resultCarsList.append(resultrow)
		except Exception:
			pass

	return resultCarsList


def get_data(mark, filePath):

	url = 'https://auto.ru/moskva/cars/{}/all/?page={}&output_type=list'
	page_num = 30

	os.chdir('results')
	dirname = datetime.now().strftime("%Y_%m_%d__%H_%M_%S")
	os.mkdir(dirname)
	os.chdir(dirname)



	while True:

		result = __parse_page(url, mark, page_num)
		if result == -1:
			break
		else: 
			for row in result:
				__append_row(filePath, row)
		
		print(str(page_num) + '='*20)
		page_num += 1





if __name__ == '__main__':
	get_data('honda', 'result.csv')
	os.chdir('../../')
	__clear_data()
