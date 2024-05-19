import json
import mysql.connector
from datetime import datetime

db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'mydb',
    'raise_on_warnings': True
}

def convert_date(date_str):
    return datetime.strptime(date_str, '%d/%m/%Y')

def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def insert_teams_to_db(teams, db_config):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    for team in teams:
        try:
            cursor.execute("INSERT INTO equipe (equipe) VALUES (%s)", (team,))
        except mysql.connector.Error as err:
            print(f"Error: {err}")
    connection.commit()
    cursor.close()
    connection.close()

def insert_data(data, temporada):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    try:
        add_jogo = ("INSERT INTO jogos "
                    "(placar_casa, placar_visitante, data, round, stage, ano, equipe_casa, equipe_visitante, estatisticas_casa, estatisticas_visitantes) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        
        for i, jogo in enumerate(data, start=1):
            data_jogo = (
                jogo["Pontos_Casa"],
                jogo["Pontos_Visitante"],
                convert_date(jogo["Data"]),
                jogo["Rodada"],
                jogo["Etapa"],
                temporada,
                jogo["Equipe_Casa"],
                jogo["Equipe_Visitante"],
                json.dumps(jogo["casa_estatisticas"]),
                json.dumps(jogo["visitante_estatisticas"])
            )
            cursor.execute(add_jogo, data_jogo)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        
    connection.commit()
    cursor.close()
    connection.close()

def main(file_path, temporada):
    data = read_json(file_path)
    insert_data(data, temporada)

temporada = '2008-2009'
file_path = './dados/resultados/2008-2009-combined.json'

main(file_path, temporada)
