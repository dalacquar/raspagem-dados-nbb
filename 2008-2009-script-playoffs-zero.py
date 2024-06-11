import csv

# Caminho do arquivo CSV
input_file_path = './dados/jogos/2009-2010/2009-2010-partidas.csv'
output_file_path = './dados/jogos/2009-2010/2009-2010-partidas-atualizado.csv'

# Dicionário para manter o controle dos encontros das equipes por stage
match_count = {}

# Ler o arquivo CSV
with open(input_file_path, mode='r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    header = next(reader)  # Ler o cabeçalho
    
    # Preparar o conteúdo atualizado
    updated_rows = [header]
    
    current_stage = None
    
    for row in reader:
        date, home_team, home_points, away_points, away_team, round_number, stage = row
        
        # Converter stage para inteiro para comparação
        stage_number = int(stage)
        
        # Resetar o dicionário de contagem de encontros quando o stage muda
        if current_stage is None or stage_number != current_stage:
            current_stage = stage_number
            if current_stage >= 3:
                match_count = {}
        
        # Atualizar o valor da rodada apenas se o stage for 3 ou maior
        if current_stage >= 3:
            # Criar uma chave única para a combinação de equipes
            match_key = tuple(sorted([home_team, away_team]))
            
            # Incrementar o contador para esta combinação de equipes
            if match_key not in match_count:
                match_count[match_key] = 0
            match_count[match_key] += 1
            
            # Atualizar o valor da rodada
            round_number = match_count[match_key]
        
        # Adicionar a linha atualizada à lista de linhas
        updated_rows.append([date, home_team, home_points, away_points, away_team, round_number, stage])

# Salvar o conteúdo atualizado em um novo arquivo CSV
with open(output_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(updated_rows)

print("Arquivo atualizado salvo com sucesso.")
