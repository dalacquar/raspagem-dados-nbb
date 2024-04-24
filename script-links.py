import json

# Carregar os links base do arquivo JSON
with open('./links/links-base/2012-2013-links-base.json', 'r') as file:
    data = json.load(file)

new_data = {}

# Iterar sobre as rodadas
cont_rodada = 1
for stage in range(1, 3):
    for rodada in range(1, 16):
        rodada_key = f"rodada-{str(cont_rodada).zfill(2)}"
        rodada_data = {}

        for key, value in data.items():
            modified_link = value.replace("stage%5B%5D=1&round%5B%5D=1", f"stage%5B%5D={stage}&round%5B%5D={(rodada)}")
            rodada_data[key] = modified_link

            new_data[rodada_key] = rodada_data
        cont_rodada += 1

# Salvar os novos links no arquivo JSON
with open('./links/links-prontos/2012-2013-links.json', 'w') as file:
    json.dump(new_data, file, indent=2)
