import pandas as pd
import os

team_name_mapping = {
    'São José': ['São José', 'Coop/São José Basketball'],
    'Franca': ['Franca', 'Sesi Franca'],
    'Bauru': ['Bauru', 'Bauru Basket'],
}


def ler_estatisticas(estatisticas_file, equipe):
    if os.path.isfile(estatisticas_file):
        estatisticas_df = pd.read_csv(estatisticas_file)
        
        possible_names = team_name_mapping.get(equipe, [equipe])
        for name in possible_names:
            equipe_stats = estatisticas_df[estatisticas_df['Equipe'] == name]
            if not equipe_stats.empty:
                stats_dict = equipe_stats.iloc[0].to_dict()
                stats_dict.pop('Equipe', None)
                return stats_dict
        
        print(f"Estatísticas não encontradas para a equipe {equipe} no arquivo {estatisticas_file}")
        return None
    else:
        print(f"Arquivo de estatísticas não encontrado: {estatisticas_file}")
        return None

def ler_dados(partidas_path, estatisticas_dir, temporada):
    partidas_df = pd.read_csv(partidas_path)

    combined_rows = []

    for index, partida in partidas_df.iterrows():
        data = partida['Data']
        equipe_casa = partida['Equipe_Casa']
        pontos_casa = partida['Pontos_Casa']
        pontos_visitante = partida['Pontos_Visitante']
        equipe_visitante = partida['Equipe_Visitante']
        rodada = partida['Rodada']
        etapa = partida['Etapa']
    
        estatisticas_file = f"{estatisticas_dir}/{temporada}-{etapa:02d}-{rodada:02d}.csv"

        casa_stats = ler_estatisticas(estatisticas_file, equipe_casa)
        visitante_stats = ler_estatisticas(estatisticas_file, equipe_visitante)

        if casa_stats is not None and visitante_stats is not None:
            partida_dict = partida.to_dict()
            
            partida_dict['casa_estatisticas'] = casa_stats
            partida_dict['visitante_estatisticas'] = visitante_stats
            
            combined_rows.append(partida_dict)

    return combined_rows

def salvar_em_json(df, output_path):
    df.to_json(output_path, orient='records', indent=4, force_ascii=False)

def main (partidas_path, estatisticas_dir, temporada, output_path):
    dados_combinados = ler_dados(partidas_path, estatisticas_dir, temporada)
    df_combinado = pd.DataFrame(dados_combinados)

    salvar_em_json(df_combinado, output_path)

partidas_paths = ["./dados/jogos/2008-2009/2008-2009-partidas.csv",
                  "./dados/jogos/2009-2010/2009-2010-partidas-atualizado.csv",
                  "./dados/jogos/2010-2011/2010-2011-partidas.csv",
                  "./dados/jogos/2011-2012/2011-2012-partidas.csv",
                  "./dados/jogos/2012-2013/2012-2013-partidas.csv"]

estatisticas_dirs = ["./dados/estatisticas/2008-2009",
                     "./dados/estatisticas/2009-2010",
                     "./dados/estatisticas/2010-2011",
                     "./dados/estatisticas/2011-2012",
                     "./dados/estatisticas/2012-2013",]

temporadas = ["2008-2009",
              "2009-2010",
              "2010-2011",
              "2011-2012",
              "2012-2013"]

output_paths = ['./dados/resultados/2008-2009-combined.json',
                './dados/resultados/2009-2010-combined.json',
                './dados/resultados/2010-2011-combined.json',
                './dados/resultados/2011-2012-combined.json',
                './dados/resultados/2012-2013-combined.json'
                ]

#for i in range (2):
main(partidas_paths[3], estatisticas_dirs[3], temporadas[3], output_paths[3])

