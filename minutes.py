# from excel_export import pass_to_excel
import requests
from bs4 import BeautifulSoup

url = 'https://egol.fcf.com.br/SISGOL/WDER0700_Sumula.asp?SelStart1=2023&SelStop1=2023&SelStart2=505&SelStop2=505&SelStart3=85&SelStop3=85&Index=1&RunReport=Run+Report'
response = requests.get(url)
targetURL = BeautifulSoup(response.text, 'html.parser')

home = 'Fora'

initial_lineup_locator = targetURL.find(name="td",string="3.0 - RELAÇÃO DE JOGADORES")#.find_next(string="FIGUEIRENSE")
initial_lineup_locator = initial_lineup_locator.find_next(name="td",string="BID").find_next(name="td",string="BID").find_next(name="td")
initial_lineup_end = initial_lineup_locator.find_next("p").get_text()
initial_lineup = []
while not initial_lineup_locator.get_text().startswith("Capitão:"):
    initial_lineup_locator = initial_lineup_locator.find_next(name="td")
    left_player_name = initial_lineup_locator.get_text()

    initial_lineup_locator = initial_lineup_locator.find_next(name="td")
    left_is_starter = initial_lineup_locator.get_text()

    initial_lineup_locator = initial_lineup_locator.find_next(name="td").find_next(name="td").find_next(name="td")
    right_player_name = initial_lineup_locator.get_text()

    initial_lineup_locator = initial_lineup_locator.find_next(name="td")
    right_is_starter = initial_lineup_locator.get_text()

    initial_lineup.append(left_player_name) if home =="Casa" and "T" in left_is_starter else None
    initial_lineup.append(right_player_name) if home =="Fora" and "T" in right_is_starter else None

    initial_lineup_locator = initial_lineup_locator.find_next(name="td").find_next(name="td")

initial_lineup = [name.rstrip() for name in initial_lineup]

# substitutions_locator = targetURL.find(name="td", string="12.0 - SUBSTITUIÇÕES")
# substitutions_locator = substitutions_locator.find_next(name="td",string="Saiu")
# substitutions_end = substitutions_locator.find_next(name="td",string="**1T = 1° Tempo | 2T = 2° Tempo | INT = Intervalo")
# subs = {}
# while substitutions_locator is not substitutions_end:
#     substitutions_locator = substitutions_locator.find_next(name="td")
#     minute_entered = substitutions_locator.get_text()

#     substitutions_locator = substitutions_locator.find_next(name="td")
#     which_half = substitutions_locator.get_text().split(" ")[0]

#     substitutions_locator = substitutions_locator.find_next(name="td")
#     team = substitutions_locator.get_text().split(" ")[0]

#     substitutions_locator = substitutions_locator.find_next(name="td")
#     entering_player_jersey = substitutions_locator.get_text().split(" - ")[0]
#     entering_player_name = substitutions_locator.get_text().split(" - ")[1]

#     substitutions_locator = substitutions_locator.find_next(name="td")
#     leaving_player_jersey = substitutions_locator.get_text().split(" - ")[0]
#     leaving_player_name = substitutions_locator.get_text().split(" - ")[1]



# Pass information to excel

# '''
#  Debugging with prints
print(initial_lineup)
# '''