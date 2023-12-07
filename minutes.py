# from excel_export import pass_to_excel
import requests
from bs4 import BeautifulSoup

url = 'https://egol.fcf.com.br/SISGOL/WDER0700_Sumula.asp?SelStart1=2023&SelStop1=2023&SelStart2=505&SelStop2=505&SelStart3=70&SelStop3=70&Index=1&RunReport=Run+Report'
response = requests.get(url)
targetURL = BeautifulSoup(response.text, 'html.parser')

# Read minutes information from inital line-up
initial_lineup_locator = targetURL.find(name="td",string="3.0 - RELAÇÃO DE JOGADORES")#.find_next(string="FIGUEIRENSE")
initial_lineup_locator = initial_lineup_locator.find_next(name="td")

# Read substitutions and make adding and subtractions

# Store all in variables

# Pass information to excel

print(initial_lineup_locator)