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
    table = soup.find("table", {"class": "tablesorter stats-table-catch"})

    dados = []

    for row in table.find_all("tr"):
        cells = row.find_all(["th", "td"])
        
        row_data = [cell.text.strip() for cell in cells[1:]]
    
        if row_data:
            dados.append(row_data)

    return dados

def printar_dados(dados):
    if dados is None:
        print("Nenhum dado para imprimir.")
        return

    for row in dados:
        print(row)

def escrever_csv(dados, nome_arquivo, temporada):
    try:
        with open("./dados/estatisticas/" + temporada + "/" + nome_arquivo, 'w', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            for row in dados:
                writer.writerow(row)
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

def main(arquivo_temporada, temporada, isTesting, rounds_totais):
    dados = []

    flag_classificacao = 0

    with open(arquivo_temporada, 'r') as links_json:
        dados_rodadas = json.load(links_json)

    for rodada, links in dados_rodadas.items():
        cont = 0
        print(f"Rodada: {rodada}")
        for dado, link in links.items():
            print(f"Link: {link}")
            if cont == 0:
                if(isTesting):
                    dados = [['Equipe', 'JO', 'Min', 'Pts', '3P', '2P', 'LL']]
                else:
                    dados = realizar_scrap(link) 
            if cont != 0:
                if(isTesting):
                    dados_aux = [['Equipe', 'JO', 'Min', 'Pts', '3P', '2P', 'LL']]
                else:
                    dados_aux = realizar_scrap(link)
                dados = concatenar_dados(dados, dados_aux)
                print("Printando dados concatenados: \n")
                printar_dados(dados)
                print("\n")
            cont += 1
            
        dados = remover_colunas_duplicadas(dados)
        print("Removendo dados duplicados:\n")
        printar_dados(dados)

        rodada_num = int(rodada.split('-')[-1])
        if ( 1 <= rodada_num <= rounds_totais // 2 ) and (flag_classificacao == 0):
            etapa = 1
        elif 19 <= rodada_num <= rounds_totais:
            etapa = 2
            rodada_num -= rounds_totais // 2
            flag_classificacao = 1
        else:
            fase_map = {
                "oitavas": 3,
                "quartas": 4,
                "semifinais": 5,
                "finais": 6
            }
            etapa = fase_map.get(rodada.split('-')[0], "N/A")
            rodada_num = int(rodada.split('-')[1])

        nome_arquivo = f"{temporada}-{etapa:02d}-{rodada_num:02d}.csv"
        escrever_csv(dados, nome_arquivo, temporada)
    
    return 0

arquivos_links = [
    "./links/links-prontos/2009-2010-links.json",
    "./links/links-prontos/2008-2009-links.json",
    "./links/links-prontos/2010-2011-links.json",
    "./links/links-prontos/2011-2012-links.json",
    "./links/links-prontos/2012-2013-links.json",
    "./links/links-prontos/2013-2014-links.json"
]

nomes_arquivos = [
    "2009-2010",
    "2008-2009",
    "2010-2011",
    "2011-2012",
    "2012-2013",
    "2013-2014"
]

i=5
isTesting = False
print(arquivos_links[i])
main(arquivos_links[i], nomes_arquivos[i], isTesting, 36)
