import csv
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
wd = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)

# inserir aqui a página do tripadvisor do museu
driver.get("https://www.tripadvisor.co.uk/Attraction_Review-g187323-d617423-Reviews-The_Holocaust_Memorial_Memorial_to_the_Murdered_Jews_of_Europe-Berlin.html")

# verificar se existem botões na página
def check_exists_by_xpath(xpath):
	try:
		driver.find_element_by_xpath(xpath)
	except NoSuchElementException:
		return False
	return True

# verificar se existem botões na página (local)
def local_check_exists_by_xpath(local, xpath):
	try:
		local.find_element_by_xpath(xpath)
	except NoSuchElementException:
		return False
	return True

# abrir arquivo para salvar
with open("MMJE-Berlin/MMJE-Berlin_test.csv", 'a', encoding='utf-8') as f:
	c = csv.writer(f, delimiter=';')
	c.writerow(["Score", "Visit Date", "City", "Comment"])

	# aceitar os cookies
	if (check_exists_by_xpath("//*[@id='_evidon-accept-button']")):
		print(driver.find_element_by_xpath("//*[@id='_evidon-accept-button']").text)
		driver.find_element_by_xpath("//*[@id='_evidon-accept-button']").click()
		time.sleep(1)

	# selecionar reviews em todos os idiomas
	if (check_exists_by_xpath("//*[contains(text(), 'All languages')]")):
		print(driver.find_element_by_xpath("//*[contains(text(), 'All languages')]").text)
		driver.find_element_by_xpath("//*[contains(text(), 'All languages')]").click()
		time.sleep(2)

	# loop sobre todos os reviews, aumentar o range para obter mais reviews
	for i in range(0,36428):

		# expandir os comentários longos ("Ler Mais")
		if (check_exists_by_xpath("//span[@class='_3maEfNCR']")):
			print(driver.find_element_by_xpath("//span[@class='_3maEfNCR']").text)
			driver.find_element_by_xpath("//span[@class='_3maEfNCR']").click()
			time.sleep(5)

		# seleciona os reviews da página atual
		container = driver.find_elements_by_xpath("//div[@class='Dq9MAugU T870kzTX LnVzGwUB']")
		# numero de reviews na página atual
		num_page_items = len(container);
	 
	 	# loop sobre todos os reviews na página atual 
		#for j in range(num_page_items):
		for j in container:

			# salvar a nota do visitante e converter para escala 0-5
			string = j.find_element_by_xpath(".//span[contains(@class, 'ui_bubble_rating bubble_')]").get_attribute("class")
			data = string.split("_")
			score = int(data[3])/10
			score_str = str(score)

			# traduzir comentários em língua estrangeira
			if (local_check_exists_by_xpath(j, ".//button[@class='ui_button secondary small']")):
				j.find_element_by_xpath(".//button[@class='ui_button secondary small']").click()
				time.sleep(4)
				# salvar o comentário traduzido do visitante
				comment = driver.find_element_by_xpath(".//div[@class='entry']").text.replace("\n", "")
				#print('original em língua estrangeira')
				#print(comment)
				# fecha popup de tradução
				driver.find_element_by_xpath(".//div[@class='_2EFRp_bb _9Wi4Mpeb']").click()
			# salvar o comentário original do visitante
			else:
				comment = j.find_element_by_xpath(".//div[@class='_3hDPbqWO']").text.replace("\n", "")
						# remover rodapé do comentário
			comment_clean = comment.split("Read lessDate")
			comment_clean = comment_clean[0]

			# salvar localização do visitante
			if (local_check_exists_by_xpath(j, ".//span[@class='default _3J15flPT small']")):
				local = j.find_element_by_xpath(".//span[@class='default _3J15flPT small']").text.replace("\n", "")
			else:
				local = "Not informed"
			
			# salvar data da visita e remover cabeçalho
			if (local_check_exists_by_xpath(j, ".//span[@class='_34Xs-BQm']")):
				date = j.find_element_by_xpath(".//span[@class='_34Xs-BQm']").text
				date_clean = date.split(": ")
				date_clean = date_clean[1]
			else:
				date_clean = "Not informed"
			# salvar nota + data + comentário no arquivo CSV
			c.writerow([score_str, date_clean, local, comment_clean])

		# trocar para a próxima página (se houver)
		if (check_exists_by_xpath('//a[@class="ui_button nav next primary "]')):
			driver.find_element_by_xpath('//a[@class="ui_button nav next primary "]').click()
		time.sleep(5)

driver.close()
c.close()