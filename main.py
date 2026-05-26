import os
import shutil
from collections import Counter
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt

import pandas as pd
from fpdf import FPDF

from Player import Player
from Team import Team

NOME_FILE = 'incampo-iscritti-al-torneo'

L_CEL = 45
H_CEL_INT = 10
H_CEL = 15
H_CEL_PL = 5

# Statistiche su luogo di nascita
def luogo_nascita_stats(teams):
    luogo_counter = Counter()
    for team in teams:
        for player in team.players:
            luogo_counter[player.place] += 1
    return luogo_counter

# Statistiche su anno di nascita
def anno_nascita_stats(teams):
    anno_counter = Counter()
    for team in teams:
        for player in team.players:
            anno_nascita = int(player.date.split('-')[0])  # Supponendo formato 'YYYY-MM-DD'
            anno_counter[anno_nascita] += 1
    return anno_counter

# Statistiche sulle taglie
def taglia_stats(teams):
    taglia_counter = Counter()
    for team in teams:
        for player in team.players:
            taglia_counter[player.shirt_size] += 1
    return taglia_counter

# Statistiche sulle categorie
def categoria_stats(teams):
    categoria_counter = Counter()
    for team in teams:
        for player in team.players:
            categoria_counter[player.cat] += 1
    return categoria_counter


def somma_taglie(squadre):
    conteggio_totale = {'S': 0, 'M': 0, 'L': 0, 'XL': 0}

    for squadra in squadre:
        for taglia, conteggio in squadra.conteggioTaglie.items():
            conteggio_totale[taglia] += conteggio

    return conteggio_totale


def create_resp_pdf(tounament, list_teams, file_name):
    path_folder = '/Users/francescobruno/Library/CloudStorage/GoogleDrive-francesco.bruno@vbcvallestura.it/Il mio Drive/VBC_Valle_Stura/StraValEsturo/2025_StraValEsturo/Squadre'

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
    pdf.cell(L_CEL * 2, H_CEL_PL, txt="Email", border=1)
    pdf.cell(L_CEL / 2, H_CEL_PL, txt="C.I", border=1)
    pdf.cell(L_CEL / 2, H_CEL_PL, txt="Mod.Min.", border=1)
    pdf.cell(0, H_CEL_PL, txt="", ln=1)

    pdf.set_line_width(0.1)

    for t in list_teams:
        pdf.cell(L_CEL, H_CEL_PL, txt=f"{t.team_name}", border=1)
        pdf.cell(L_CEL, H_CEL_PL, txt=f"{t.resp_name}", border=1)
        pdf.cell(L_CEL, H_CEL_PL, txt=f"{t.tel}", border=1)
        pdf.cell(L_CEL * 2, H_CEL_PL, txt=f"{t.mail}", border=1)
        pdf.cell(L_CEL / 2, H_CEL_PL, txt=f" ", border=1)
        pdf.cell(L_CEL / 2, H_CEL_PL, txt=f" ", border=1)
        pdf.cell(0, H_CEL_PL, txt="", ln=1)

    pdf.add_page()
    pdf.cell(0, H_CEL_INT, txt=f"RIEPILOGO TAGLIE", ln=1)
    conteggio_totale = somma_taglie(list_teams)

    pdf.set_font("Times", style="B", size=9)
    pdf.set_line_width(0.3)
    headers = ["S", "M", "L", "XL"]

    for header in headers:
        pdf.cell(15, 10, txt=header, border='B')
    pdf.cell(0, 10, ln=1)

    pdf.set_font("Times", size=8)
    pdf.cell(15, H_CEL_PL, txt=str(conteggio_totale['S']), border='B')
    pdf.cell(15, H_CEL_PL, txt=str(conteggio_totale['M']), border='B')
    pdf.cell(15, H_CEL_PL, txt=str(conteggio_totale['L']), border='B')
    pdf.cell(15, H_CEL_PL, txt=str(conteggio_totale['XL']), border='B')
    pdf.cell(0, H_CEL_PL, ln=1)

    pdf.output(f"{path_folder}/{tounament}/{file_name}.pdf")


def read_team(tournament_team):
    list_teams = []
    for index, row in tournament_team.iterrows():
        #print(f"Riga {index}:")
        # Itera sulle colonne per leggere cella per cella
        team = Team(row['Nome squadra'], f"{row['Nome']} {row['Cognome']}", row['Telefono'], row['E-mail'])

        num_giocatori = int(row['Numero giocatori'].split(' ')[0])

        for i in range(1, num_giocatori + 1):
            player_key = f"Giocatore {i}"
            if player_key in row:
                player_info = row[player_key]
                player = parse_player_info(player_info)
                team.add_player(player)

        ############################
        ### Modifiche AC picchia ###
        if row['Nome squadra'] == 'AC picchia':
            team.add_player(Player('Francesco', 'Ferraiuolo', '2001-09-05', 'Cuneo', 'CA10580JP', None, 'L'))
            team.add_player(Player('Marco Claudio', 'Lerda', '2003-08-23', 'Torino', 'CA83430RA', None, 'L'))
        ### -------------------- ###
        ############################

        ############################
        ### Modifiche Miramonti Live ###
        if row['Nome squadra'] == 'Miramonti Live':
            team.add_player(Player('Luca', 'Peano', '1997-02-04', 'Cuneo', 'AY9594302', 'Pedona promozione', 'L'))
            team.add_player(Player('Stefano', 'Quaranta', '1995-06-12', 'Beinette', 'CA47216MB', 'Terza Categoria', 'M'))
        ### -------------------- ###
        ############################

        ############################
        ### Modifiche Mongardino ###
        if row['Nome squadra'] == 'Mongardino':
            team.add_player(Player('Donato', 'Ciola', '1991-06-24', 'ASTI', '4375815AA', None, 'L'))
        ### -------------------- ###
        ############################

        ############################
        ### Modifiche Suli Cudati ###
        if row['Nome squadra'] == 'Suli Cudati':
            team.add_player(Player('Andrea', 'Camia', '2006-11-29', 'Cuneo', 'CA47981NP', 'Prima Divisione', 'M'))
        ### -------------------- ###
        ############################

        ############################
        ### Modifiche I desperados ###
        if row['Nome squadra'] == 'I desperados':
            team.add_player(Player('Christian', 'Dobrev', '2007-09-29', 'Cuneo', 'CA08934HS', 'Serie D', 'L'))
        ### -------------------- ###
        ############################

        ############################
        ### Modifiche Gnun Sens ###
        if row['Nome squadra'] == 'Gnun Sens':
            team.add_player(Player('Tommaso', 'Viglietti', '2005-06-02', 'Cuneo', 'CA19669LS', 'Promozione', 'L'))
            team.add_player(Player('Pietro', 'Costa', '2005-11-07', 'Cuneo', 'CA62771NI', 'Promozione', 'M'))
        ### -------------------- ###
        ############################

        ############################
        ### Modifiche La Curva del T ###
        if row['Nome squadra'] == 'La Curva del T':
            team.add_player(Player('Cesar Augusto', 'Otazu Silva', '1996-05-18', 'Paraguay', 'P485689', None, 'L'))
        ### -------------------- ###
        ############################

        ############################
        ### Modifiche Ac Donatello ###
        if row['Nome squadra'] == 'Ac Donatello':
            team.add_player(Player('Francesco', 'Borreale', '2003-09-04', 'Cuneo', 'CA02534TL', 'Terza Categoria', 'M'))
        ### -------------------- ###
        ############################

        list_teams.append(team)

    return list_teams


def create_teams_folders(tournament, list_teams):
    for t in list_teams:
        # t.to_string()
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

    ############################
    ### Modifiche AC picchia ###
    if name == 'El': name = 'Amine'
    if surname == 'Baharaoui Amine': surname = 'El Bahraoui'
    if name == 'De': name = 'Ciro'
    if surname == 'Gregorio Ciro': surname = 'De Gregorio'
    ### -------------------- ###
    ############################

    ############################
    ### Modifiche Miramonti Live ###
    if name == 'Giorgio' and surname == 'Oliva': name = 'Giorgia'
    ### -------------------- ###
    ############################

    date = player_data['Data di nascita']
    place = player_data['Luogo di nascita']
    ci = player_data['Numero carta identità']
    cat = player_data.get('Se tesserato, categoria di riferimento', None)
    shirt_size = player_data['Taglia maglietta']

    ############################
    ### Modifiche Gnun Sens ###
    if name == 'Federico' and surname == 'Favole': shirt_size = 'XL'
    if name == 'Matteo' and surname == 'Castellino': shirt_size = 'M'
    if name == 'Samuele' and surname == 'Rosso': shirt_size = 'M'
    ### -------------------- ###
    ############################

    return Player(name, surname, date, place, ci, cat, shirt_size)

def normalize_category(cat):
    if not cat:  # Controlla se cat è None, vuoto, o NaN
        return "No"
    cat = cat.lower()  # Converti tutto in minuscolo
    # Normalizzazione delle categorie
    if "serie c" in cat or cat == "c":
        return "Serie C"
    if "serie d" in cat or cat == "d":
        return "Serie D"
    if "serie b" in cat or "b1" in cat or "b2" in cat or cat == "b":
        return "Serie B"
    if "serie d c5" in cat or "calcio a 5" in cat or "c5" in cat:
        return "Serie D Calcio a 5"
    if "figc" in cat:
        return "FIGC"
    if "no" in cat:
        return "No"
    return cat.capitalize()  # Ritorna con iniziale maiuscola per uniformità


def build_df(teams):
    data = []
    for team in teams:
        for p in team.players:
            anno = int(p.date.split('-')[0])
            data.append({
                'place': p.place,
                'year': anno,
                'size': p.shirt_size,
                'cat': p.cat
            })
    return pd.DataFrame(data)

def stats(list_teams, torneo):
    df = build_df(list_teams)
    sns.set_theme(style="darkgrid")

    df['cat'] = df['cat'].apply(normalize_category)

    # Conteggio luogo di nascita
    plt.figure(figsize=(10, 6))
    sns.countplot(y='place', data=df, order=df['place'].value_counts().index)
    plt.title(f"Numero di giocatori per luogo di nascita - {torneo}")
    plt.xlabel("Conteggio")
    plt.ylabel("Luogo")
    plt.show()

    # Grafico per la distribuzione delle taglie
    plt.figure(figsize=(10, 6))
    sns.countplot(x='size', data=df, order=['S', 'M', 'L', 'XL'], palette="viridis")
    plt.title(f"Distribuzione delle taglie  - {torneo}")
    plt.xlabel("Taglia")
    plt.ylabel("Numero di giocatori")
    plt.show()

    # Grafico per la distribuzione delle categorie
    plt.figure(figsize=(10, 6))
    sns.countplot(x='cat', data=df, palette="muted")
    plt.title(f"Distribuzione delle categorie  - {torneo}")
    plt.xlabel("Categoria")
    plt.ylabel("Numero di giocatori")
    plt.show()

    # anno di nascita
    plt.figure(figsize=(10, 5))
    sns.histplot(df['year'], bins=10, kde=True, color='skyblue')
    plt.title(f"Distribuzione anni di nascita  - {torneo}")
    plt.xlabel("Anno")
    plt.ylabel("Numero giocatori")
    plt.show()

    # luogo vs categorie
    plt.figure(figsize=(12, 7))
    sns.countplot(y='place', hue='cat', data=df)
    plt.title(f"Categorie per luogo di nascita - {torneo}")
    plt.xlabel("Conteggio")
    plt.ylabel("Luogo")
    plt.legend(title="Categoria")
    plt.show()


def main():
    path_folder = '/Users/francescobruno/Library/CloudStorage/GoogleDrive-francesco.bruno@vbcvallestura.it/Il mio Drive/VBC_Valle_Stura/StraValEsturo/2025_StraValEsturo/Squadre'

    ### Pallavolo ###
    print('Torneo di pallavolo')
    try:
        shutil.rmtree(f"{path_folder}/Pallavolo")
    except:
        print("Niente da cancellare")

    file_name_referenti = 'ReferentiTorneoPallavolo'
    tournament_team = pd.read_excel(f"{NOME_FILE}-pallavolo.xlsx")
    tournament = 'Pallavolo'

    os.mkdir(f"{path_folder}/{tournament}")
    list_teams_pallavolo = read_team(tournament_team)
    create_teams_folders(tournament, list_teams_pallavolo)
    create_resp_pdf(tournament, list_teams_pallavolo, file_name_referenti)

    luoghi = luogo_nascita_stats(list_teams_pallavolo)
    anni = anno_nascita_stats(list_teams_pallavolo)
    taglie = taglia_stats(list_teams_pallavolo)
    categorie = categoria_stats(list_teams_pallavolo)

    # Visualizza i risultati
    print("Distribuzione per luogo di nascita:", luoghi)
    print("Distribuzione per anno di nascita:", anni)
    print("Distribuzione per taglia:", taglie)
    print("Distribuzione per categoria:", categorie)

    #stats(list_teams_pallavolo, 'pallavolo')




    ### Calcio a 5 ###
    print('Torneo di Calcio a 5')
    try:
        shutil.rmtree(f"{path_folder}/Calcetto")
    except:
        print("Niente da cancellare")
    file_name_referenti = 'ReferentiTorneoCalcetto'
    tournament_team = pd.read_excel(f"{NOME_FILE}-calcetto.xlsx")
    tournament = 'Calcetto'

    os.mkdir(f"{path_folder}/{tournament}")
    list_teams_calcio = read_team(tournament_team)
    create_teams_folders(tournament, list_teams_calcio)
    create_resp_pdf(tournament, list_teams_calcio, file_name_referenti)

    luoghi = luogo_nascita_stats(list_teams_calcio)
    anni = anno_nascita_stats(list_teams_calcio)
    taglie = taglia_stats(list_teams_calcio)
    categorie = categoria_stats(list_teams_calcio)

    # Visualizza i risultati
    print("Distribuzione per luogo di nascita:", luoghi)
    print("Distribuzione per anno di nascita:", anni)
    print("Distribuzione per taglia:", taglie)
    print("Distribuzione per categoria:", categorie)

    #stats(list_teams_calcio, 'calcio a 5')



if __name__ == '__main__':
    main()
