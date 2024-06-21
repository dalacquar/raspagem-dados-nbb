import requests
import time
import csv
import json

from bs4 import BeautifulSoup

def request_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print("Erro na solicitação HTTP:", e)
        return None

def extrair_dados(html_content):
    if html_content is None:
        return None

    soup = BeautifulSoup(html_content, "html.parser")
    table = soup.find("table", {"class": "table_matches_table"})

    dados = []

    if table:
        headers = ["Data", "Equipe_Casa", "Pontos_Casa", "Pontos_Visitante", "Equipe_Visitante", "Rodada", "Etapa"]
        dados.append(','.join(headers))

        for row in table.find_all("tr", {"class": "with-hotel"}):
            cells = row.find_all("td")

            date_elems = cells[1].find_all("span")
            date = date_elems[0].text.strip() if len(date_elems) > 1 else "N/A"
            home_team_elem = cells[3].find("span", {"class": "team-shortname"})
            home_team = home_team_elem.text.strip() if home_team_elem else "N/A"
            
            # Extrair placar
            home_score_elem = cells[5].find("span", {"class": "home"})
            home_score = home_score_elem.text.strip() if home_score_elem else "N/A"
            away_score_elem = cells[5].find("span", {"class": "away"})
            away_score = away_score_elem.text.strip() if away_score_elem else "N/A"
            
            away_team_elem = cells[7].find("span", {"class": "team-shortname"})
            away_team = away_team_elem.text.strip() if away_team_elem else "N/A"

            raw_round_number = cells[9].text.strip()
            round_number = ''.join(filter(str.isdigit, raw_round_number))
            round_number_int = int(round_number) if round_number.isdigit() else 0

            # Ajustar o número da rodada para rodadas a partir de 16
            if round_number_int >= 19:
                adjusted_round_number = str(round_number_int - 18)
            else:
                adjusted_round_number = round_number
            
            phase_text = cells[10].text.strip().lower()
            
            # Mapeamento das fases para números
            phase_map = {
                "1º turno": "1",
                "2º turno": "2",
                "oitavas": "3",
                "quartas": "4",
                "semi": "5",
                "final": "6"
            }
            
            phase = phase_map.get(phase_text, "N/A")

            # Criar uma string com os dados separados por vírgula
            dados_row = ','.join([
                date, home_team, home_score, away_score, away_team, adjusted_round_number, phase
            ])
            
            dados.append(dados_row)

    return dados

def printar_dados(dados):
    if dados is None:
        print("Nenhum dado para imprimir.")
        return

    for row in dados:
        print(row)

def escrever_csv(dados, nome_arquivo):
    try:
        with open("./dados/"+nome_arquivo, 'w', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            for row in dados:
                writer.writerow(row.split(','))  # Dividir a string por vírgulas e passar como lista de valores
        print(f"Dados salvos com sucesso em '{nome_arquivo}'.")
    except Exception as e:
        print(f"Erro ao escrever arquivo CSV: {e}")

def realizar_scrap(url):
    html_content = None
    while html_content is None:
        start_time = time.time()
        html_content = request_html(url)
        end_time = time.time()
        print("Tempo para fazer a requisição HTML:", end_time - start_time, "segundos\n")

        if html_content is None:
            print("Falha na requisição. Tentando novamente em 5 segundos...")
            time.sleep(5)
            
    start_time = time.time()
    dados_extraidos = extrair_dados(html_content)
    end_time = time.time()
    print("Tempo para extrair os dados:", end_time - start_time, "segundos\n")

    start_time = time.time()
    printar_dados(dados_extraidos)
    print("\n")
    
    end_time = time.time()
    print("Tempo para imprimir os dados:", end_time - start_time, "segundos\n")

    return dados_extraidos

def concatenar_dados(dados_inicio, dados_final):
    dados_concatenados = {}

    for dados in dados_inicio[1:]:
        equipe = dados[0]
        dados_concatenados[equipe] = dados[1:]

    for dados in dados_final[1:]:
        equipe = dados[0]
        if equipe in dados_concatenados:
            dados_concatenados[equipe].extend(dados[1:])
        else:
            dados_concatenados[equipe] = dados[1:]

    resultado_concatenado = [['Equipe'] + dados_inicio[0][1:] + dados_final[0][1:]]
    for equipe, dados in dados_concatenados.items():
        resultado_concatenado.append([equipe] + dados)

    return resultado_concatenado

def remover_colunas_duplicadas(dados):
    if not dados:
        return []
    
    colunas = {}
    for idx, coluna in enumerate(dados[0]):
        colunas.setdefault(coluna, []).append(idx)

    colunas_remover = set()
    for sigla, indices in colunas.items():
        if len(indices) > 1:
            colunas_remover.update(indices[1:])

    dados_sem_duplicatas = []
    for linha in dados:
        nova_linha = [valor for idx, valor in enumerate(linha) if idx not in colunas_remover]
        dados_sem_duplicatas.append(nova_linha)

    return dados_sem_duplicatas

def main(arquivo_temporada, temporada):

    dados = []

    with open(arquivo_temporada, 'r') as links_json:
        dados_rodadas = json.load(links_json)

    for rodada, links in dados_rodadas.items():
        for dado, link in links.items():
            print(f"Link: {link}")
            dados = realizar_scrap(link) 
            
            printar_dados(dados)
            print("\n")

        nome_arquivo = "jogos/" + temporada + "/" + temporada + "-partidas.csv"
        escrever_csv(dados, nome_arquivo)
    
    return 0

arquivos_links = ["./links/links-games/2008-2009-links-games.json",
                  "./links/links-games/2009-2010-links-games.json",
                  "./links/links-games/2010-2011-links-games.json",
                  "./links/links-games/2011-2012-links-games.json",
                  "./links/links-games/2012-2013-links-games.json",
                  "./links/links-games/2013-2014-links-games.json"
                  ]

nomes_arquivos =    [   "2008-2009",
                        "2009-2010",
                        "2010-2011",
                        "2011-2012",
                        "2012-2013",
                        "2013-2014"
                    ]

#for i in range (5):
main(arquivos_links[5], nomes_arquivos[5])
