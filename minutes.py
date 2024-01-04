import requests
from bs4 import BeautifulSoup

# Hard coding for tests. Use scraping.py variables
url = 'https://egol.fcf.com.br/SISGOL/WDER0700_Sumula.asp?SelStart1=2023&SelStop1=2023&SelStart2=505&SelStop2=505&SelStart3=85&SelStop3=85&Index=1&RunReport=Run+Report'
response = requests.get(url)
targetURL = BeautifulSoup(response.text, 'html.parser')

home = 'Fora'
first_half_minutes = 47
second_half_minutes = 61
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

# Return list to use pass_to_excel function

    workbook = load_workbook(excel_file)
    sheet = workbook['Minutagem']
    # Hard-coded labels from sheet. Read them and dynamically make the dict?
    column_labels = {
        "CÓDIGO JOGO":1,
        "DATA JOGO":2,
        "TREINADOR":3,
        "CATEGORIA":4,
        "COMPETIÇÃO":5,
        "FIGUEIRENSE":6,
        "G.F.":7,
        "G.A.":8,
        "ADVERSÁRIO":9,
        "MANDO":10,
        "LOCAL":11,
        "Cidade":12,
        "UF":13,
        "JOGOS":14,
        "VITÓRIA":15,
        "EMPATE":16,
        "DERROTA":17,
        "MINUTOS JOGADOS":18,
        "1º A MARCAR FIGUEIRENSE":19,
        "1º A MARCAR ADVERSÁRIO":20,
        "GOLS MARCADOS 1ºT - 0'-15'":21,
        "GOLS MARCADOS 1ºT - 15'-30'":22,
        "GOLS MARCADOS 1ºT - 30'-45'":23,
        "GOLS MARCADOS 2ºT - 0'-15'":24,
        "GOLS MARCADOS 2ºT - 15'-30'":25,
        "GOLS MARCADOS 2ºT - 30'-45'":26,
        "GOLS SOFRIDOS 1ºT - 0'-15'":27,
        "GOLS SOFRIDOS 1ºT - 15'-30'":28,
        "GOLS SOFRIDOS 1ºT - 30'-45'":29,
        "GOLS SOFRIDOS 2ºT - 0'-15'":30,
        "GOLS SOFRIDOS 2ºT - 15'-30'":31,
        "GOLS SOFRIDOS 2ºT - 30'-45'":32
    }
    staff = {
        "Sub14":"Guilherme Pereira",
        "Sub15":"Guilherme Pereira",
        "Sub17":"Lucas Ligio",
        "Sub20":"Jhonatas Reis",
        "Sub21":"Jhonatas Reis"
    }

    last_row = sheet.max_row
    last_row_value = 2
    while last_row > 1:
        last_row_value = sheet.cell(row=last_row,column=1).value
        if last_row_value is not None:
            break
        last_row -= 1
        
    last_row_value = sheet.cell(row=last_row, column=column_labels['CÓDIGO JOGO']).value
    
    new_row = last_row + 1
    sheet.cell(row=new_row, column=column_labels['CÓDIGO JOGO'],value=last_row_value+1)
    sheet.cell(row=new_row, column=column_labels['DATA JOGO'],value=date)
    sheet.cell(row=new_row, column=column_labels['TREINADOR'],value=staff[category])
    sheet.cell(row=new_row, column=column_labels['CATEGORIA'],value=category)
    sheet.cell(row=new_row, column=column_labels['COMPETIÇÃO'],value=tournament)
    sheet.cell(row=new_row, column=column_labels['FIGUEIRENSE'],value="Figueirense")
    sheet.cell(row=new_row, column=column_labels['G.F.'],value=figueira_final_score)
    sheet.cell(row=new_row, column=column_labels['G.A.'],value=opponent_final_score)
    sheet.cell(row=new_row, column=column_labels['ADVERSÁRIO'],value=opponent)
    sheet.cell(row=new_row, column=column_labels['MANDO'],value=home)
    sheet.cell(row=new_row, column=column_labels['LOCAL'],value=place)
    sheet.cell(row=new_row, column=column_labels['Cidade'],value=city)
    sheet.cell(row=new_row, column=column_labels['UF'],value="SC")
    sheet.cell(row=new_row, column=column_labels['JOGOS'],value=1)
    sheet.cell(row=new_row, column=column_labels['VITÓRIA'],value=1 if figueira_final_score > opponent_final_score else 0)
    sheet.cell(row=new_row, column=column_labels['EMPATE'],value=1 if figueira_final_score == opponent_final_score else 0)
    sheet.cell(row=new_row, column=column_labels['DERROTA'],value=1 if figueira_final_score < opponent_final_score else 0)
    sheet.cell(row=new_row, column=column_labels['MINUTOS JOGADOS'],value = int(first_half_minutes) + int(second_half_minutes))
    sheet.cell(row=new_row, column=column_labels['1º A MARCAR FIGUEIRENSE'],value=1 if figueira_first == True else 0)
    sheet.cell(row=new_row, column=column_labels['1º A MARCAR ADVERSÁRIO'],value=1 if figueira_first == False else 0)
    sheet.cell(row=new_row, column=column_labels['GOLS MARCADOS 1ºT - 0\'-15\''], value= scored_list[0])
    sheet.cell(row=new_row, column=column_labels['GOLS MARCADOS 1ºT - 15\'-30\''],value= scored_list[1])
    sheet.cell(row=new_row, column=column_labels['GOLS MARCADOS 1ºT - 30\'-45\''],value= scored_list[2])
    sheet.cell(row=new_row, column=column_labels['GOLS MARCADOS 2ºT - 0\'-15\''], value= scored_list[3])
    sheet.cell(row=new_row, column=column_labels['GOLS MARCADOS 2ºT - 15\'-30\''],value= scored_list[4])
    sheet.cell(row=new_row, column=column_labels['GOLS MARCADOS 2ºT - 30\'-45\''],value= scored_list[5])
    sheet.cell(row=new_row, column=column_labels['GOLS SOFRIDOS 1ºT - 0\'-15\''], value= conceded_list[0])
    sheet.cell(row=new_row, column=column_labels['GOLS SOFRIDOS 1ºT - 15\'-30\''],value= conceded_list[1])
    sheet.cell(row=new_row, column=column_labels['GOLS SOFRIDOS 1ºT - 30\'-45\''],value= conceded_list[2])
    sheet.cell(row=new_row, column=column_labels['GOLS SOFRIDOS 2ºT - 0\'-15\''], value= conceded_list[3])
    sheet.cell(row=new_row, column=column_labels['GOLS SOFRIDOS 2ºT - 15\'-30\''],value= conceded_list[4])
    sheet.cell(row=new_row, column=column_labels['GOLS SOFRIDOS 2ºT - 30\'-45\''],value= conceded_list[5])

    workbook.save("Banco de Dados Figueirense Base.xlsx")


# Debugging with prints
print(initial_lineup)
print(len(subs))
print(subs)