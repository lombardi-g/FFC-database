from excel_export import pass_to_excel
import requests
import re
from datetime import datetime
# import os
# import tkinter as tk
# from tkinter import messagebox
from bs4 import BeautifulSoup

def caps_lock_ignore(text):
    return re.compile(text,re.I)                    

def scrape_match_summary():
    url = 'https://egol.fcf.com.br/SISGOL/WDER0700_Sumula.asp?SelStart1=2023&SelStop1=2023&SelStart2=557&SelStop2=557&SelStart3=70&SelStop3=70&Index=1&RunReport=Run+Report'
    response = requests.get(url)
    targetURL = BeautifulSoup(response.text, 'html.parser')

    # Determine opponent
    match = targetURL.find(string=caps_lock_ignore('figueirense'))
    teams = match.split(' x ')
    opponent = [team for team in teams if team.upper() != 'FIGUEIRENSE'][0]

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
    full_tournament = targetURL.find(string=caps_lock_ignore('sub-'))
    category = "Sub"+full_tournament[full_tournament.upper().find("SUB-")+4:full_tournament.upper().find("SUB-")+6]
    tournament = "Campeonato Catarinense"

    # Which round
    round_number = full_tournament.find_next(string='Rodada:').find_next()
    round_number = round_number.get_text()

    # Find date
    date_locator = targetURL.find(string="Data:")
    date = date_locator.find_next(string=caps_lock_ignore('/202'))
    time_locator = date.find_next(string='Horário:')
    time = time_locator.find_next().get_text()

    # Find place
    place_locator = time_locator.find_next(string="Local:").find_next()
    place = place_locator.get_text().split(' / ')
    city = place[1]
    place = place[0]

    # Find minutes played
    def minute_calculator(start: str, end: str, added: str):
        format = '%H:%M'
        match_start = datetime.strptime(start,format)
        match_end = datetime.strptime(end,format)
        added_time = datetime.strptime(added,format)
        return match_end - match_start + added_time
        
    first_half_locator = targetURL.find(name="td",string="Início 1° Tempo:").find_next()
    first_half_started = first_half_locator.get_text()
    first_half_finished = targetURL.find(name="td",string="Término do 1º Tempo:").find_next()
    first_half_added_time = first_half_finished.find_next(name="td",string="Acréscimo:").find_next().get_text()
    first_half_finished = first_half_finished.get_text()
    first_half_minutes = datetime.strftime(minute_calculator(first_half_started, first_half_finished, first_half_added_time),'%M')
    second_half_locator = targetURL.find(name="td",string="Início 2° Tempo:").find_next()
    second_half_started = second_half_locator.get_text()
    second_half_finished = targetURL.find(name="td", string="Término do 2º Tempo:").find_next()
    second_half_added_time = second_half_finished.find_next(name="td",string="Acréscimo:").find_next().find_next().get_text()
    second_half_finished = second_half_finished.get_text()
    second_half_minutes = datetime.strftime(minute_calculator(second_half_started,second_half_finished, second_half_added_time),'%M')

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
            goal_minute = goal_minute_locator.get_text()
            goal_half_locator = goal_minute_locator.find_next(name="td")
            goal_half = goal_half_locator.get_text()
            goal_team_locator = goal_half_locator.find_next(name="td").find_next(name="td").find_next(name="td").find_next(name="td")
            goal_team = goal_team_locator.get_text().capitalize()
            if total_goals==0:
                figueira_first = True if goal_team == "Figueirense" else False
            goal_info = {
                "minute":goal_minute,
                "half":goal_half,
                "team":goal_team
            }
            goals_info.append(goal_info)
            total_goals+=1
            goal_reader = goal_team_locator
            goal_minute_locator = goal_reader.find_next(name="td")
    else:
        figueira_first=False

    if __name__ == "__main__":
        pass_to_excel()