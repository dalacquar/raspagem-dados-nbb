# Raspagem de dados Novo Basquete Brasil

Nesse repositório está disponível os scripts utilizados para realizar a extração dos dados das partidas da NBB.
Cada script tem um papel crucial para criação final do arquivo da database.

Os scripts não foram feitos para executar de forma dinâmica, do modo de que para extrair as estátisticas de temporada se deva fazer a execução dos algoritmos mudando os parametros de forma manual.

## Dados
O conjunto de dados está disponível no arquivo `./database/data-set.sql`. Esse arquivo tem um backup da base de dados em MySql. Na pasta `./dados/` estão disponiveis os dados separados.

## Pós-conclusão
Após a conclusão da raspagem, a fins de organização, os arquivos de script que estavam na raiz do projeto foram movidos para dentro da pasta script. Como os scripts usam a estrutura de pastas será necessário alterar os caminhos dos arquivos para o funcionamento correto da execução e teste ou mover os arquivos scripts de volta para a pasta raiz.

## Autor: Rafael Dalacqua
Contato: dalacquar@gmail.com

Este repositório está licenciado sob a Licença MIT. Isso significa que você é livre para usar, copiar, modificar, mesclar, publicar, distribuir, sublicenciar e/ou vender cópias deste software, desde que inclua uma cópia da licença junto com o software. Este repositório é fornecido "como está", sem garantias de qualquer tipo, expressas ou implícitas, incluindo, mas não se limitando a, garantias de comercialização, adequação a um propósito específico ou não violação. Para mais detalhes, consulte o arquivo LICENSE no repositório.
