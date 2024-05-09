import json

links_base =    [       "./links/links-base/2008-2009-links-base.json",
                        "./links/links-base/2009-2010-links-base.json",
                        "./links/links-base/2010-2011-links-base.json",
                        "./links/links-base/2011-2012-links-base.json",
                        "./links/links-base/2012-2013-links-base.json"
                    ]


links_prontos =    [    "./links/links-prontos/2008-2009-links.json",
                        "./links/links-prontos/2009-2010-links.json",
                        "./links/links-prontos/2010-2011-links.json",
                        "./links/links-prontos/2011-2012-links.json",
                        "./links/links-prontos/2012-2013-links.json"
                    ]

def script_links (arq_base, arq_saida):
    # Carregar os links base do arquivo JSON
    with open(arq_base, 'r') as file:
        data = json.load(file)

    new_data = {}

    # Iterar sobre as rodadas
    cont_rodada = 1
    for stage in range(1, 7):
        if (stage <= 2):
            for rodada in range(1, 16):
                rodada_key = f"rodada-{str(cont_rodada).zfill(2)}"
                rodada_data = {}

                for key, value in data.items():
                    modified_link = value.replace("stage%5B%5D=1&round%5B%5D=1", f"stage%5B%5D={stage}&round%5B%5D={(rodada)}")
                    rodada_data[key] = modified_link

                    new_data[rodada_key] = rodada_data
                cont_rodada += 1
        else :
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

for i in range (5):
    script_links(links_base[i], links_prontos[i])