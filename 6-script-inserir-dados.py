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

team_name_mapping = {
    'Oscar São José Basketball': 'Coop/São José Basketball',
    'Franca': 'Sesi Franca',
    'Bauru': 'Bauru Basket',
    'Basq. Cearense': 'Fortaleza B. C. / CFO',
    'Macaé': 'Macaé Basquete',
    'Caxias do Sul': 'Caxias do Sul Basquete',
    'Campo Mourão': 'VipTech CMB',
    'Vasco da Gama': 'R10 Score Vasco da Gama',
    'Fortaleza B. C.': 'Fortaleza B. C. / CFO',
    'Cerrado Basquete': 'Cerrado',
    'KTO/Caxias do Sul': 'Caxias do Sul Basquete',
    'Luvix/União Corinthians': 'União Corinthians',
    '123 Minas': 'Minas'
}

def convert_date(date_str):
    return datetime.strptime(date_str, '%d/%m/%Y')

def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def map_team_name(team_name):
    return team_name_mapping.get(team_name, team_name)

def insert_data(data, temporada):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    try:
        add_jogo = ("INSERT INTO jogos "
                    "(placar_casa, placar_visitante, data, round, stage, ano, equipe_casa, equipe_visitante, estatisticas_casa, estatisticas_visitantes) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        
        for i, jogo in enumerate(data, start=1):
            equipe_casa = map_team_name(jogo["Equipe_Casa"])
            equipe_visitante = map_team_name(jogo["Equipe_Visitante"])
            data_jogo = (
                jogo["Pontos_Casa"],
                jogo["Pontos_Visitante"],
                convert_date(jogo["Data"]),
                jogo["Rodada"],
                jogo["Etapa"],
                temporada,
                equipe_casa,
                equipe_visitante,
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

temporada = '2023-2024'
file_path = './dados/resultados/2023-2024-combined.json'

main(file_path, temporada)
