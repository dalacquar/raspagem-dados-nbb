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

def escrever_csv(dados, nome_arquivo):
    try:
        with open("./dados/"+nome_arquivo, 'w', newline='', encoding='utf-8') as file:
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

def main(arquivo_temporada, temporada):

    dados = []

    with open(arquivo_temporada, 'r') as links_json:
        dados_rodadas = json.load(links_json)

    for rodada, links in dados_rodadas.items():
        cont=0
        print(f"Rodada: {rodada}")
        for dado, link in links.items():
            print(f"Link: {link}")
            if(cont == 0):
                dados = realizar_scrap(link) 

            if(cont != 0):
                dados_aux = realizar_scrap(link)
                dados = concatenar_dados(dados, dados_aux)
                
                print("Printando dados concatenados: \n")
                printar_dados(dados)
                print("\n")

            cont+=1
            
        dados = remover_colunas_duplicadas(dados)
        print("Removendo dados duplicados:\n")
        printar_dados(dados)

        nome_arquivo = temporada + "-" + rodada + ".csv"
        escrever_csv(dados, nome_arquivo)
    
    return 0



arquivos_links =    [     "./links/links-prontos/2008-2009-links.json",
                        "./links/links-prontos/2009-2010-links.json",
                        "./links/links-prontos/2010-2011-links.json",
                        "./links/links-prontos/2011-2012-links.json",
                        "./links/links-prontos/2012-2013-links.json"
                    ]

nomes_arquivos =    [   "2008-2009",
                        "2009-2010",
                        "2010-2011",
                        "2011-2012",
                        "2012-2013"
                    ]

# nomes_arquivos = ["2008-2009"]
# arquivos_links = ["./links/links-prontos/2008-2009-links.json"]

for i in range (5):
    print(arquivos_links[i])
    main(arquivos_links[i], nomes_arquivos[i])



