
# Geocodificação e Mapeamento de Endereços com Python e Folium

Este projeto Python utiliza bibliotecas como Pandas, Geopy e Folium para geocodificar uma lista de endereços a partir de um arquivo CSV e visualizá-los em um mapa interativo.

## Pré-requisitos

Certifique-se de ter o Python instalado em seu sistema. Clone este repositório e instale as dependências usando pip:

    git clone https://github.com/brunodealmeida17/maping-geolocation
    cd maping-geolocation
    pip install -r requirements.txt

O arquivo `requirements.txt` contém as dependências necessárias para este projeto.

## Configuração do Ambiente

Antes de executar o script, certifique-se de ter um arquivo CSV válido com os endereços a serem geocodificados. O arquivo deve ter as seguintes colunas:

- `LOGRADOURO`
- `NOME`
- `NOME_CIDADE`
- `NOME_ESTADO`

Os endereços completos serão formados pela concatenação dessas colunas, adicionando ", Brasil" ao final.

## Como Rodar

Para executar o script e gerar o mapa de endereços geocodificados:

    python main.py


Isso iniciará o processo de leitura do arquivo CSV, limpeza dos dados, geocodificação assíncrona dos endereços e criação de um mapa interativo.

## Detalhes do Script

### Funções Principais

- `safe_geocode(address)`: Função para geocodificar um endereço com tratamento de exceções usando Geopy.
- `geocode_async(df, mapa)`: Função que geocodifica os endereços de forma assíncrona usando threads.
- `main()`: Função principal que carrega o arquivo CSV, limpa os dados, prepara os endereços e inicia o processo de geocodificação e mapeamento.

### Modificações nos Dados

- Os dados são lidos do arquivo CSV especificado e são limpos para remover duplicatas e espaços extras nos campos de texto.
- A coluna `LOGRADOURO` é ajustada para substituir abreviações comuns por seus equivalentes completos.

### Mapa Interativo

- Um mapa inicial é criado usando Folium, centrado em coordenadas específicas (por exemplo, Brasília).
- Os marcadores dos endereços geocodificados são adicionados dinamicamente ao mapa à medida que são processados.


