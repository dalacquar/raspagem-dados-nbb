import pandas as pd
import os

team_name_mapping = {
    'São José': ['São José', 'Coop/São José Basketball'],
    'Franca': ['Franca', 'Sesi Franca'],
    'Bauru': ['Bauru', 'Bauru Basket'],
    'Basq. Cearense': ['Basq. Cearense', 'Fortaleza B. C. / CFO'],
    'Macaé': ['Macaé Basquete', 'Macaé'],
    'Caxias do Sul': ['Caxias do Sul Basquete', 'Caxias do Sul'],
    'Vasco da Gama': ['R10 Score Vasco da Gama', 'Vasco da Gama'],
    'Campo Mourão': [ 'VipTech CMB', 'Campo Mourão'],
    'Brasília': ['BRB/Brasília', 'Brasília'],
    'Fortaleza B. C.': ['Fortaleza B. C. / CFO', 'Fortaleza B. C.'],
    'Cerrado Basquete': ['Cerrado', 'Cerrado Basquete'],
    'KTO/Caxias do Sul': ['Caxias do Sul Basquete', 'KTO/Caxias do Sul']
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
                  "./dados/jogos/2012-2013/2012-2013-partidas.csv",
                  "./dados/jogos/2013-2014/2013-2014-partidas.csv",
                  "./dados/jogos/2014-2015/2014-2015-partidas.csv",
                  "./dados/jogos/2015-2016/2015-2016-partidas.csv",
                  "./dados/jogos/2016-2017/2016-2017-partidas.csv",
                  "./dados/jogos/2017-2018/2017-2018-partidas.csv",
                  "./dados/jogos/2018-2019/2018-2019-partidas.csv",
                  "./dados/jogos/2019-2020/2019-2020-partidas.csv",
                  "./dados/jogos/2020-2021/2020-2021-partidas.csv",
                  "./dados/jogos/2021-2022/2021-2022-partidas.csv",
                  "./dados/jogos/2022-2023/2022-2023-partidas.csv",
                  "./dados/jogos/2023-2024/2023-2024-partidas.csv"
                  ]

estatisticas_dirs = ["./dados/estatisticas/2008-2009",
                     "./dados/estatisticas/2009-2010",
                     "./dados/estatisticas/2010-2011",
                     "./dados/estatisticas/2011-2012",
                     "./dados/estatisticas/2012-2013",
                     "./dados/estatisticas/2013-2014",
                     "./dados/estatisticas/2014-2015",
                     "./dados/estatisticas/2015-2016",
                     "./dados/estatisticas/2016-2017",
                     "./dados/estatisticas/2017-2018",
                     "./dados/estatisticas/2018-2019",
                     "./dados/estatisticas/2019-2020",
                     "./dados/estatisticas/2020-2021",
                     "./dados/estatisticas/2021-2022",
                     "./dados/estatisticas/2022-2023",
                     "./dados/estatisticas/2023-2024"
                     ]

temporadas = ["2008-2009",
              "2009-2010",
              "2010-2011",
              "2011-2012",
              "2012-2013",
              "2013-2014",
              "2014-2015",
              "2015-2016",
              "2016-2017",
              "2017-2018",
              "2018-2019",
              "2019-2020",
              "2020-2021",
              "2021-2022",
              "2022-2023",
              "2023-2024"
              ]


output_paths = ['./dados/resultados/2008-2009-combined.json',
                './dados/resultados/2009-2010-combined.json',
                './dados/resultados/2010-2011-combined.json',
                './dados/resultados/2011-2012-combined.json',
                './dados/resultados/2012-2013-combined.json',
                './dados/resultados/2013-2014-combined.json',
                './dados/resultados/2014-2015-combined.json',
                './dados/resultados/2015-2016-combined.json',
                './dados/resultados/2016-2017-combined.json',
                './dados/resultados/2017-2018-combined.json',
                './dados/resultados/2018-2019-combined.json',
                './dados/resultados/2019-2020-combined.json',
                './dados/resultados/2020-2021-combined.json',
                './dados/resultados/2021-2022-combined.json',
                './dados/resultados/2022-2023-combined.json',
                './dados/resultados/2023-2024-combined.json'
                ]

i=12
main(partidas_paths[i], estatisticas_dirs[i], temporadas[i], output_paths[i])
