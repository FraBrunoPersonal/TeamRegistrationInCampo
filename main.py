import os
import shutil

import pandas as pd
from fpdf import FPDF

from Player import Player
from Team import Team

NOME_FILE = 'incampo-iscritti-al-torneo'

L_CEL = 45
H_CEL_INT = 10
H_CEL = 15
H_CEL_PL = 5


def create_resp_pdf(tounament, list_teams, file_name):
    pdf = FPDF("L", "mm", "A4")
    pdf.add_page()
    pdf.set_font("Times", size=30)
    pdf.cell(0, H_CEL_PL, txt=f"Responsabili {tounament}", align='C')
    pdf.cell(0, H_CEL_PL * 3, txt="", ln=1)
    pdf.set_font("Times", size=10)

    pdf.set_line_width(0.3)

    pdf.cell(L_CEL, H_CEL_PL, txt="Squadra", border=1)
    pdf.cell(L_CEL, H_CEL_PL, txt="Referente", border=1)
    pdf.cell(L_CEL, H_CEL_PL, txt="Numero", border=1)
    pdf.cell(L_CEL*2, H_CEL_PL, txt="Email", border=1)
    pdf.cell(L_CEL/2, H_CEL_PL, txt="C.I", border=1)
    pdf.cell(L_CEL/2, H_CEL_PL, txt="Mod.Min.", border=1)
    pdf.cell(0, H_CEL_PL, txt="", ln=1)

    pdf.set_line_width(0.1)

    for t in list_teams:
        pdf.cell(L_CEL, H_CEL_PL, txt=f"{t.team_name}", border=1)
        pdf.cell(L_CEL, H_CEL_PL, txt=f"{t.resp_name}", border=1)
        pdf.cell(L_CEL, H_CEL_PL, txt=f"{t.tel}", border=1)
        pdf.cell(L_CEL*2, H_CEL_PL, txt=f"{t.mail}", border=1)
        pdf.cell(L_CEL/2, H_CEL_PL, txt=f" ", border=1)
        pdf.cell(L_CEL/2, H_CEL_PL, txt=f" ", border=1)
        pdf.cell(0, H_CEL_PL, txt="", ln=1)

    pdf.output(f"{tounament}/{file_name}.pdf")

def read_team(tournament_team):
    list_teams = []
    for index, row in tournament_team.iterrows():
        print(f"Riga {index}:")
        # Itera sulle colonne per leggere cella per cella
        team = Team(row['Nome squadra'], f"{row['Nome']} {row['Cognome']}", row['Telefono'], row['E-mail'])

        num_giocatori = int(row['Numero giocatori'].split(' ')[0])

        for i in range(1, num_giocatori + 1):
            player_key = f"Giocatore {i}"
            if player_key in row:
                player_info = row[player_key]
                player = parse_player_info(player_info)
                team.add_player(player)

        list_teams.append(team)


    return list_teams


def create_teams_folders(tournament, list_teams):
    for t in list_teams:
        #t.to_string()
        t.create_team_folder(tournament)

def parse_player_info(info):
    """
    Parses the player information string and returns a Player object.
    """
    parts = info.split('|')
    player_data = {}

    for part in parts:
        key, value = part.split(':', 1)
        key = key.strip()
        value = value.strip()
        player_data[key] = value

    # Extract individual details
    name, surname = player_data['Nome e cognome'].split(' ', 1)
    date = player_data['Data di nascita']
    place = player_data['Luogo di nascita']
    ci = player_data['Numero carta identità']
    cat = player_data.get('Se tesserato, categoria di riferimento', None)
    shirt_size = player_data['Taglia maglietta']

    return Player(name, surname, date, place, ci, cat, shirt_size)


def main():
    list_teams = []

    torneo = input("Inserire di quale torneo si vogliono scaricare i dati\n"
                   "\tPallavolo (p)\n"
                   "\tCalcio a 5 (c)\n-> ")
    if torneo == 'p':
        try:
            shutil.rmtree("Pallavolo")
        except:
            print("Niente da cancellare")
        file_name_referenti = 'ReferentiTorneoPallavolo'
        tournament_team = pd.read_excel(f"{NOME_FILE}-pallavolo.xlsx")
        tournament = 'Pallavolo'
    else:
        if torneo == 'c':
            try:
                shutil.rmtree("Calcetto")
            except:
                print("Niente da cancellare")
            file_name_referenti = 'ReferentiTorneoCalcetto'
            tournament_team = pd.read_excel(f"{NOME_FILE}-calcetto.xlsx")
            tournament = 'Calcetto'
        else:
            exit("Nessun torneo trovato")
    os.mkdir(tournament)
    list_teams = read_team(tournament_team)
    create_teams_folders(tournament, list_teams)
    create_resp_pdf(tournament, list_teams, file_name_referenti)


    #tournament_team = pd.read_excel(NOME_FILE)

    #print(tournament_team)









        #   for col_name, cell_value in row.items():
        #    print(f"  Colonna '{col_name}': {cell_value}")
        #    print(f"")
        #   list_teams.append(new Team(col_name['']))



if __name__ == '__main__':

    main()