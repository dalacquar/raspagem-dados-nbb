import json

def script_links (arq_base, arq_saida, hasStageTwo, resetRoundsInStageTwo, rounds_totais, round_virada=None):
    # Carregar os links base do arquivo JSON
    with open(arq_base, 'r') as file:
        data = json.load(file)

    new_data = {}

    # Iterar sobre as rodadas
    cont_rodada = 1
    for stage in range(1, 7):
        if (stage <= 2): #playin
            if hasStageTwo:
                if round_virada is None:
                    total_rounds = (rounds_totais // 2) + 1
                else:
                    if(stage == 1):
                        total_rounds = round_virada + 1
                    elif (stage == 2):
                        total_rounds = rounds_totais - round_virada + 1

            else:
                total_rounds = rounds_totais + 1
                
            for rodada in range(1, total_rounds):
                # rounds consecutivos 
                if(hasStageTwo):
                    rodada_key = f"rodada-{str(cont_rodada).zfill(2)}"
                    rodada_data = {}

                    for key, value in data.items():
                        if(resetRoundsInStageTwo):
                            modified_link = value.replace("stage%5B%5D=1&round%5B%5D=1", f"stage%5B%5D={stage}&round%5B%5D={(rodada)}")
                        else:
                            modified_link = value.replace("stage%5B%5D=1&round%5B%5D=1", f"stage%5B%5D={stage}&round%5B%5D={(cont_rodada)}")
                        rodada_data[key] = modified_link

                        new_data[rodada_key] = rodada_data
                    cont_rodada += 1
                else:
                    if(stage == 2):
                        continue
                    else :
                        rodada_key = f"rodada-{str(cont_rodada).zfill(2)}"
                        rodada_data = {}

                        for key, value in data.items():
                            modified_link = value.replace("stage%5B%5D=1&round%5B%5D=1", f"stage%5B%5D={stage}&round%5B%5D={(rodada)}")
                            rodada_data[key] = modified_link

                            new_data[rodada_key] = rodada_data
                        cont_rodada += 1
                    
        else : #playoffs
            cont_rodada = 1
            for rodada in range(1, 6):
                if stage == 3:
                    rodada_key = f"oitavas-{str(cont_rodada).zfill(2)}"
                elif stage == 4:
                    rodada_key = f"quartas-{str(cont_rodada).zfill(2)}"
                elif stage == 5:
                    rodada_key = f"semifinais-{str(cont_rodada).zfill(2)}"
                elif stage == 6:
                    rodada_key = f"finais-{str(cont_rodada).zfill(2)}"

                rodada_data = {}
                
                for key, value in data.items():
                    modified_link = value.replace("stage%5B%5D=1&round%5B%5D=1", f"stage%5B%5D={stage}&round%5B%5D={(rodada)}")
                    rodada_data[key] = modified_link

                    new_data[rodada_key] = rodada_data
                cont_rodada += 1

    # Salvar os novos links no arquivo JSON
    with open(arq_saida, 'w') as file:
        json.dump(new_data, file, indent=2)


links_base =    [       "./links/links-base/2008-2009-links-base.json",
                        "./links/links-base/2009-2010-links-base.json",
                        "./links/links-base/2010-2011-links-base.json",
                        "./links/links-base/2011-2012-links-base.json",
                        "./links/links-base/2012-2013-links-base.json",
                        "./links/links-base/2013-2014-links-base.json",
                        "./links/links-base/2014-2015-links-base.json",
                        "./links/links-base/2015-2016-links-base.json",
                        "./links/links-base/2016-2017-links-base.json",
                        "./links/links-base/2017-2018-links-base.json",
                        "./links/links-base/2018-2019-links-base.json",
                        "./links/links-base/2019-2020-links-base.json",
                        "./links/links-base/2020-2021-links-base.json",
                        "./links/links-base/2021-2022-links-base.json",
                        "./links/links-base/2022-2023-links-base.json",
                        "./links/links-base/2023-2024-links-base.json"
                    ]


links_prontos =    [    "./links/links-prontos/2008-2009-links.json",
                        "./links/links-prontos/2009-2010-links.json",
                        "./links/links-prontos/2010-2011-links.json",
                        "./links/links-prontos/2011-2012-links.json",
                        "./links/links-prontos/2012-2013-links.json",
                        "./links/links-prontos/2013-2014-links.json",
                        "./links/links-prontos/2014-2015-links.json",
                        "./links/links-prontos/2015-2016-links.json",
                        "./links/links-prontos/2016-2017-links.json",
                        "./links/links-prontos/2017-2018-links.json",
                        "./links/links-prontos/2018-2019-links.json",
                        "./links/links-prontos/2019-2020-links.json",
                        "./links/links-prontos/2020-2021-links.json",
                        "./links/links-prontos/2021-2022-links.json",
                        "./links/links-prontos/2022-2023-links.json",
                        "./links/links-prontos/2023-2024-links.json"
                    ]

script_links("./links/links-base/2022-2023-links-base.json", "./links/links-prontos/2022-2023-links.json", True, False, 22, 12)