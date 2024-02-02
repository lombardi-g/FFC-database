from excel_export import pass_to_excel, excel_file
from minutes import scrape_minutes
import requests
from datetime import datetime
from common_functions import minute_calculator, caps_lock_ignore
from bs4 import BeautifulSoup              

def scrape_match_summary(URL_from_interface):
    url = URL_from_interface
    response = requests.get(url)
    targetURL = BeautifulSoup(response.text, 'html.parser')

    # Determine opponent
    match = targetURL.find(string=caps_lock_ignore('figueirense'))
    teams = match.split(' x ')
    opponent = [team for team in teams if team.upper() != 'FIGUEIRENSE'][0].title()

    # Final score
    final_score = match.find_next('p').find_next()
    final_score = final_score.get_text().split(' x ')
    if teams[0] == "FIGUEIRENSE":
        home = "Casa"
        figueira_final_score = int(final_score[0])
        opponent_final_score = int(final_score[1])
    else:
        home = "Fora"
        figueira_final_score = int(final_score[1])
        opponent_final_score = int(final_score[0])


    # Find category
    # Supports only 2 tornaments from FCF
    full_tournament = targetURL.find(string=caps_lock_ignore('sub-'))
    category = "Sub"+full_tournament[full_tournament.upper().find("SUB-")+4:full_tournament.upper().find("SUB-")+6]
    if full_tournament.get_text().startswith("CAMPEONATO CATARINENSE"):
        tournament = "Campeonato Catarinense"
    elif full_tournament.get_text().startswith("COPA SC"):
        tournament = "Copa SC"
    else:
        tournament = ""

    # Which round
    # round_number = full_tournament.find_next(string='Rodada:').find_next()
    # round_number = round_number.get_text()

    # Find date
    date_locator = targetURL.find(string="Data:")
    date = date_locator.find_next(string=caps_lock_ignore('/202'))
    time_locator = date.find_next(string='Horário:')
    # time = time_locator.find_next().get_text()

    # Find place
    place_locator = time_locator.find_next(string="Local:").find_next()
    place = place_locator.get_text().split(' / ')
    city = place[1]
    place = place[0]

    # Find minutes played        
    first_half_locator = targetURL.find(name="td",string="Início 1° Tempo:").find_next()
    first_half_started = first_half_locator.get_text()
    first_half_finished = targetURL.find(name="td",string="Término do 1º Tempo:").find_next()
    first_half_finished = first_half_finished.get_text()
    first_half_minutes = datetime.strftime(minute_calculator(first_half_started, first_half_finished),'%M')
    second_half_locator = targetURL.find(name="td",string="Início 2° Tempo:").find_next()
    second_half_started = second_half_locator.get_text()
    second_half_finished = targetURL.find(name="td", string="Término do 2º Tempo:").find_next()
    second_half_finished = second_half_finished.get_text()
    second_half_minutes = datetime.strftime(minute_calculator(second_half_started,second_half_finished),'%M')

    #Scoring information
    score_locator_beginning = targetURL.find(string=caps_lock_ignore("5.0 - GOLS"))
    score_locator_end = targetURL.find(name="td",string=caps_lock_ignore("6.0 - "))
    goal_reader = score_locator_beginning.findNext(name="td",string="Equipe")
    goal_minute_locator = goal_reader
    goals_info=[]
    total_goals=0
    if figueira_final_score or opponent_final_score != 0:
        while goal_minute_locator is not score_locator_end:
            goal_minute_locator = goal_reader.find_next(name="td")
            goal_minute = goal_minute_locator.get_text().replace("'","")
            goal_minute = int(goal_minute)
            goal_half_locator = goal_minute_locator.find_next(name="td")
            goal_half = goal_half_locator.get_text()
            own_goal_locator = goal_half_locator.find_next(name="td").find_next(name="td")
            own_goal = "CONTRA" in own_goal_locator.get_text().upper()
            goal_team_locator = goal_half_locator.find_next(name="td").find_next(name="td").find_next(name="td").find_next(name="td")
            goal_team = goal_team_locator.get_text().capitalize()
            goal_info = {
                "minute":goal_minute,
                "half":goal_half,
                "OG":own_goal,
                "team":goal_team
            }
            goals_info.append(goal_info)
            total_goals+=1
            goal_reader = goal_team_locator
            goal_minute_locator = goal_reader.find_next(name="td")
        first_goal = goals_info[0]
        for goalinfo in goals_info:
            if goalinfo["half"] == "1T" and first_goal["half"] == "2T":
                first_goal = goalinfo
        for goalinfo in goals_info:
            if goalinfo["minute"] < first_goal["minute"] and goalinfo["half"] == first_goal["half"]:
                first_goal = goalinfo
        figueira_first = True if first_goal["team"] == "Figueirense" and first_goal["OG"] == False else False 
    else:
        figueira_first= "Empate"

    scored_list=[0,0,0,0,0,0]
    conceded_list=[0,0,0,0,0,0]

    for goals in goals_info:
        match (goals["half"],goals["team"],goals["OG"]):
            # Separating goals scored per third, or own goals from opponent
            case ("1T","Figueirense",False) if goals['minute'] < float(first_half_minutes)/3:
                scored_list[0] += 1
            case ("1T","Figueirense",False) if goals['minute'] <= float(first_half_minutes)*2/3 and goals["minute"] > float(first_half_minutes)/3:
                scored_list[1] += 1
            case ("1T","Figueirense",False) if goals['minute'] >= float(first_half_minutes)*2/3:
                scored_list[2] += 1
            case ("2T","Figueirense",False) if goals['minute'] < float(second_half_minutes)/3:
                scored_list[3] += 1
            case ("2T","Figueirense",False) if goals['minute'] <= float(second_half_minutes)*2/3 and goals["minute"] > float(second_half_minutes)/3:
                scored_list[4] += 1
            case ("2T","Figueirense",False) if goals['minute'] >= float(second_half_minutes)*2/3:
                scored_list[5] += 1
            case ("1T",_,True) if goals['minute'] < float(first_half_minutes)/3:
                scored_list[0] += 1
            case ("1T",_,True) if goals['minute'] <= float(first_half_minutes)*2/3 and goals["minute"] > float(first_half_minutes)/3:
                scored_list[1] += 1
            case ("1T",_,True) if goals['minute'] >= float(first_half_minutes)*2/3:
                scored_list[2] += 1
            case ("2T",_,True) if goals['minute'] < float(second_half_minutes)/3:
                scored_list[3] += 1
            case ("2T",_,True) if goals['minute'] <= float(second_half_minutes)*2/3 and goals["minute"] > float(second_half_minutes)/3:
                scored_list[4] += 1
            case ("2T",_,True) if goals['minute'] >= float(second_half_minutes)*2/3:
                scored_list[5] += 1

            # Separating goals conceded per third, or our own goals
            case ("1T",_,False) if goals['minute'] < float(first_half_minutes)/3:
                conceded_list[0] += 1
            case ("1T",_,False) if goals['minute'] <= float(first_half_minutes)*2/3 and goals["minute"] > float(first_half_minutes)/3:
                conceded_list[1] += 1
            case ("1T",_,False) if goals['minute'] >= float(first_half_minutes)*2/3:
                conceded_list[2] += 1
            case ("2T",_,False) if goals['minute'] < float(second_half_minutes)/3:
                conceded_list[3] += 1
            case ("2T",_,False) if goals['minute'] <= float(second_half_minutes)*2/3 and goals["minute"] > float(second_half_minutes)/3:
                conceded_list[4] += 1
            case ("2T",_,False) if goals['minute'] >= float(second_half_minutes)*2/3:
                conceded_list[5] += 1
            case ("1T","Figueirense",True) if goals['minute'] < float(first_half_minutes)/3:
                conceded_list[0] += 1
            case ("1T","Figueirense",True) if goals['minute'] <= float(first_half_minutes)*2/3 and goals["minute"] > float(first_half_minutes)/3:
                conceded_list[1] += 1
            case ("1T","Figueirense",True) if goals['minute'] >= float(first_half_minutes)*2/3:
                conceded_list[2] += 1
            case ("2T","Figueirense",True) if goals['minute'] < float(second_half_minutes)/3:
                conceded_list[3] += 1
            case ("2T","Figueirense",True) if goals['minute'] <= float(second_half_minutes)*2/3 and goals["minute"] > float(second_half_minutes)/3:
                conceded_list[4] += 1
            case ("2T","Figueirense",True) if goals['minute'] >= float(second_half_minutes)*2/3:
                conceded_list[5] += 1
            
    minutes_played_list = scrape_minutes(targetURL, home, first_half_minutes, second_half_minutes)
    pass_to_excel(date,category,tournament,figueira_final_score,opponent_final_score,opponent,home,place,city,first_half_minutes,second_half_minutes,figueira_first,scored_list,conceded_list,minutes_played_list)