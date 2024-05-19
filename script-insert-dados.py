import pandas as pd
import os


def ler_estatisticas(estatisticas_file, equipe):
    if os.path.isfile(estatisticas_file):
        estatisticas_df = pd.read_csv(estatisticas_file)
        
        # Encontrar as estatísticas da equipe especificada
        equipe_stats = estatisticas_df[estatisticas_df['Equipe'] == equipe]
        
        if not equipe_stats.empty:
            # Converter a linha para um dicionário e retornar
            stats_dict = equipe_stats.iloc[0].to_dict()
            # Remover a chave 'Equipe' do dicionário
            stats_dict.pop('Equipe', None)
            return stats_dict
        else:
            print(f"Estatísticas não encontradas para a equipe {equipe} no arquivo {estatisticas_file}")
            return None
    else:
        print(f"Arquivo de estatísticas não encontrado: {estatisticas_file}")
        return None

def ler_dados(partidas_path, estatisticas_dir, temporada):
    partidas_df = pd.read_csv(partidas_path)

    combined_rows = []

    # Iterar sobre cada linha do arquivo de partidas
    for index, partida in partidas_df.iterrows():
        data = partida['Data']
        equipe_casa = partida['Equipe_Casa']
        pontos_casa = partida['Pontos_Casa']
        pontos_visitante = partida['Pontos_Visitante']
        equipe_visitante = partida['Equipe_Visitante']
        rodada = partida['Rodada']
        etapa = partida['Etapa']

        # Construir o nome do arquivo de estatísticas
        estatisticas_file = f"{estatisticas_dir}/{temporada}-{etapa:02d}-{rodada:02d}.csv"
        
        # Ler estatísticas para equipe da casa
        casa_stats = ler_estatisticas(estatisticas_file, equipe_casa)
        
        # Ler estatísticas para equipe visitante
        visitante_stats = ler_estatisticas(estatisticas_file, equipe_visitante)

        if casa_stats is not None and visitante_stats is not None:
            partida_dict = partida.to_dict()
            
            partida_dict['casa_estatisticas'] = casa_stats
            partida_dict['visitante_estatisticas'] = visitante_stats
            
            combined_rows.append(partida_dict)

    return combined_rows

def main (partidas_path, estatisticas_dir, temporada):
    dados_combinados = ler_dados(partidas_path, estatisticas_dir, temporada)
    df_combinado = pd.DataFrame(dados_combinados)

    output_path = './dados/resultados/2008-2009-combined.json'

    def salvar_em_json(df, output_path):
        df.to_json(output_path, orient='records', indent=4)

    salvar_em_json(df_combinado, output_path)

partidas_path = './dados/jogos/2009-2010/2009-2010-partidas.csv'
estatisticas_dir = './dados/estatisticas/2008-2009'
temporada = '2008-2009'

main(partidas_path, estatisticas_dir, temporada)

