import requests
from bs4 import BeautifulSoup
from openpyxl import load_workbook

# Hard coding for tests. Use scraping.py variables
url = 'https://egol.fcf.com.br/SISGOL/WDER0700_Sumula.asp?SelStart1=2023&SelStop1=2023&SelStart2=505&SelStop2=505&SelStart3=85&SelStop3=85&Index=1&RunReport=Run+Report'
response = requests.get(url)
targetURL = BeautifulSoup(response.text, 'html.parser')

home = 'Fora'
first_half_minutes = 47
second_half_minutes = 51
match = first_half_minutes+second_half_minutes

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

substitutions_locator = targetURL.find(name="td", string="12.0 - SUBSTITUIÇÕES")
substitutions_locator = substitutions_locator.find_next(name="td",string="Saiu").find_next(name="td")
substitutions_end = substitutions_locator.find_next(name="td",string="**1T = 1° Tempo | 2T = 2° Tempo | INT = Intervalo")
subs = []
while substitutions_locator is not substitutions_end:
    minute_entered = substitutions_locator.get_text()
    minute_entered = int(minute_entered.split("'")[0]) if minute_entered != "-" else None

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

    subs.append({"half":which_half,
                 "minutes":minute_entered,
                 "name":entering_player_name,
                 "replacing":leaving_player_name}) if team == "FIGUEIRENSE" else None

    substitutions_locator = substitutions_locator.find_next(name="td")

for players in subs:
    match players["half"]:
        case "1":
            players["minutes"] = int(first_half_minutes) - players["minutes"] + int(second_half_minutes)            
        case "2":
            players["minutes"] = int(second_half_minutes) - players["minutes"]

# Final list. Subtract minutes of starters that left.
summary_list = []
for starter in initial_lineup:
    name:str = starter
    minutes_played:int = first_half_minutes + second_half_minutes
    
    for substitute in subs:
        if starter == substitute["replacing"]:
            summary_list.append(
                {
                "name":name,
                "minutes_played": minutes_played - substitute["minutes"]
                })
            name = substitute["name"]
            minutes_played = substitute["minutes"]
        
    summary_list.append(
        {
        "name":name,
        "minutes_played":minutes_played
        })

excel_file = "MinutagemBase2023.xlsx"
workbook = load_workbook(excel_file)
sheet = workbook['Base23']

column_labels = {
    "Data":1,
    "Adversário":2,
    "Nome":3,
    "Minutos":4        
}

last_row = sheet.max_row
last_row_value = 2
while last_row > 1:
    last_row_value = sheet.cell(row=last_row,column=1).value
    if last_row_value is not None:
        break
    last_row -= 1
    
last_row_value = sheet.cell(row=last_row, column=column_labels['Data']).value

new_row = last_row + 1
sheet.cell(row=new_row, column=column_labels['Data'],value = ...)
sheet.cell(row=new_row, column=column_labels['Adversário'],value = ...)
sheet.cell(row=new_row, column=column_labels['Nome'],value = ...)
sheet.cell(row=new_row, column=column_labels['Minutos'],value = ...)

workbook.save("Banco de Dados Figueirense Base.xlsx")


# Debugging with prints
print(summary_list)