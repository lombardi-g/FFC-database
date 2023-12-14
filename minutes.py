# from excel_export import pass_to_excel
import requests
from bs4 import BeautifulSoup

#Same from scraping, use import later after testing
url = 'https://egol.fcf.com.br/SISGOL/WDER0700_Sumula.asp?SelStart1=2023&SelStop1=2023&SelStart2=505&SelStop2=505&SelStart3=85&SelStop3=85&Index=1&RunReport=Run+Report'
response = requests.get(url)
targetURL = BeautifulSoup(response.text, 'html.parser')

# Read minutes information from inital line-up
initial_lineup_locator = targetURL.find(name="td",string="3.0 - RELAÇÃO DE JOGADORES")#.find_next(string="FIGUEIRENSE")
initial_lineup_locator = initial_lineup_locator.find_next(name="td")

# Read substitutions and make adding and subtractions
substitutions_locator = targetURL.find(name="td", string="12.0 - SUBSTITUIÇÕES")
substitutions_locator = substitutions_locator.find_next(name="td",string="Saiu")
substitutions_end = substitutions_locator.find_next(name="td",string="**1T = 1° Tempo | 2T = 2° Tempo | INT = Intervalo")
while substitutions_locator is not substitutions_end:
    substitutions_locator = substitutions_locator.find_next(name="td")
    minute_entered = substitutions_locator.get_text()

    substitutions_locator = substitutions_locator.find_next(name="td")
    which_half = substitutions_locator.get_text().split(" ")[0]

    substitutions_locator = substitutions_locator.find_next(name="td")
    team = substitutions_locator.get_text().split(" ")[0]

    substitutions_locator = substitutions_locator.find_next(name="td")
    entering_player_jersey = substitutions_locator.get_text().split(" - ")[0]
    entering_player_name = substitutions_locator.get_text().split(" - ")[1]

    substitutions_locator = substitutions_locator.find_next(name="td")
    leaving_player_jersey = substitutions_locator.get_text().split(" - ")[0]
    leaving_player_name = substitutions_locator.get_text().split(" - ")[1]

    substitutions_locator = substitutions_locator.find_next(name="td", string="8 - EZEQUIEL RIBEIRO DE SOUSA")
    substitutions_locator = substitutions_locator.find_next(name="td")

# Store all in variables

# Pass information to excel

'''
#  Debugging with prints
print(substitutions_locator)
print(minute_entered)
print(type(minute_entered))
print(which_half,"a")
print(team)
print(entering_player_jersey)
print(entering_player_name)
print(leaving_player_jersey)
print(leaving_player_name)
'''