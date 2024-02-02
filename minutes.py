from bs4 import BeautifulSoup
from openpyxl import load_workbook
from datetime import datetime
from common_functions import caps_lock_ignore, minute_calculator

def scrape_minutes(imported_target_url, imported_home,imported_first_half_minutes, imported_second_half_minutes):
    targetURL = imported_target_url

    home = imported_home
    first_half_minutes = imported_first_half_minutes
    second_half_minutes = imported_second_half_minutes

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
        minute_entered = int(minute_entered.split("'")[0]) if minute_entered != "-" else int(0)

        substitutions_locator = substitutions_locator.find_next(name="td")
        which_half = substitutions_locator.get_text().split(" ")[0]

        substitutions_locator = substitutions_locator.find_next(name="td")
        team = substitutions_locator.get_text().split(" ")[0]

        substitutions_locator = substitutions_locator.find_next(name="td")
        # entering_player_jersey = substitutions_locator.get_text().split(" - ")[0]
        entering_player_name = substitutions_locator.get_text().split(" - ")[1]

        substitutions_locator = substitutions_locator.find_next(name="td")
        # leaving_player_jersey = substitutions_locator.get_text().split(" - ")[0]
        leaving_player_name = substitutions_locator.get_text().split(" - ")[1]

        subs.append({"half":which_half,
                    "minutes":minute_entered,
                    "name":entering_player_name,
                    "replacing":leaving_player_name}) if team == "FIGUEIRENSE" else None

        substitutions_locator = substitutions_locator.find_next(name="td")

    # Evaluating when the substitution happened
    for players in subs:
        match players["half"]:
            case "1":
                players["minutes"] = int(first_half_minutes) - players["minutes"] + int(second_half_minutes)            
            case "2":
                players["minutes"] = int(second_half_minutes) - players["minutes"]
            case "INTERVALO":
                players["minutes"] = int(second_half_minutes)

    # Final list. Subtract minutes of starters that left.
    summary_list = []
    for starter in initial_lineup:
        name:str = starter
        minutes_played:int = int(first_half_minutes) + int(second_half_minutes)
        
        for substitute in subs:
            if starter == substitute["replacing"]:
                summary_list.append(
                    {
                    "name":name,
                    "minutes_played": int(minutes_played) - substitute["minutes"]
                    })
                name = substitute["name"]
                minutes_played = substitute["minutes"]
            
        summary_list.append(
            {
            "name":name,
            "minutes_played":minutes_played
            })
    # If player was at the bench, entered and was substituted before the match ended, summary_list doesnt fetch.
    for player_entered in subs:
        for player_left in subs:
            if player_entered["name"] == player_left["replacing"]:
                match player_entered["half"]:
                    case "1":
                        minutes_played_benched = int(first_half_minutes) - player_entered["minutes"] + int(second_half_minutes)
                    case "2":
                        minutes_played_benched = int(second_half_minutes) - player_entered["minutes"]
                summary_list.append(
                    {
                    "name": player_left["name"],
                    "minutes_played": minutes_played_benched
                    })

    return summary_list

    # Debugging with prints
    # for each in summary_list:
    #     print(each)
    # print(len(summary_list))
    # print(date)
    # print(opponent)