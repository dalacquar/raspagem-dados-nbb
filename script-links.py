import json

with open('./links/links-base/2012-2013-links-base.json', 'r') as file:
    data = json.load(file)

new_data = {}
for rodada in range(1, 37):
    rodada_key = f"rodada-{str(rodada).zfill(2)}"
    rodada_data = {}
    for key, value in data.items():
        rodada_data[key] = value.replace("round%5B%5D=1", f"round%5B%5D={rodada}")
    new_data[rodada_key] = rodada_data

with open('./links/links-prontos/2012-2013-links.json', 'w') as file:
    json.dump(new_data, file, indent=2)

