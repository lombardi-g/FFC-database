# from excel_export import pass_to_excel
import requests
from bs4 import BeautifulSoup

#Same from scraping, use import later after testing
url = 'https://egol.fcf.com.br/SISGOL/WDER0700_Sumula.asp?SelStart1=2023&SelStop1=2023&SelStart2=557&SelStop2=557&SelStart3=67&SelStop3=67&Index=1&RunReport=Run+Report'
response = requests.get(url)
targetURL = BeautifulSoup(response.text, 'html.parser')

# Read minutes information from inital line-up
initial_lineup_locator = targetURL.find(name="td",string="3.0 - RELAÇÃO DE JOGADORES")#.find_next(string="FIGUEIRENSE")
initial_lineup_locator = initial_lineup_locator.find_next(name="td")

# Read substitutions and make adding and subtractions
substitutions_begin = targetURL.find(name="td", string="12.0 - SUBSTITUIÇÕES")
substitutions_begin = substitutions_begin.find_next(name="td",string="Saiu").find_next(name="td")
substitutions_end = substitutions_begin.find_next(name="td",string="**1T = 1° Tempo | 2T = 2° Tempo | INT = Intervalo")

# Store all in variables

# Pass information to excel
