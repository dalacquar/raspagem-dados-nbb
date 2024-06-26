import os
import csv
import mysql.connector

# Função para obter os nomes das equipes a partir dos arquivos CSV em uma única pasta
def get_teams_from_csv(folder_path):
    teams = set()
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Pula a primeira linha (cabeçalho)
                for row in reader:
                    teams.add(row[0])  # Adiciona a equipe (primeira coluna)
    return teams

# Função para obter os nomes das equipes a partir de múltiplas pastas
def get_teams_from_multiple_folders(folder_paths):
    all_teams = set()
    for folder_path in folder_paths:
        teams = get_teams_from_csv(folder_path)
        all_teams.update(teams)
    return all_teams

# Função para inserir equipes no banco de dados
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

# Configurações de conexão ao banco de dados MySQL
db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'mydb',
    'raise_on_warnings': True
}

# Lista de caminhos para as pastas que contêm os arquivos CSV
folder_paths = [
    './dados/estatisticas/2021-2022',
]

# Obtém os nomes das equipes a partir de múltiplas pastas e insere no banco de dados
teams = get_teams_from_multiple_folders(folder_paths)
insert_teams_to_db(teams, db_config)

print("Equipes inseridas com sucesso.")
