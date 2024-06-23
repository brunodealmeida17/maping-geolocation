import pandas as pd
from geopy.geocoders import Nominatim
import folium
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue

# Configuração do geolocalizador com o agente do usuário e o timeout
user_agent = "my-cool-application"
geolocator = Nominatim(user_agent=user_agent, timeout=10)

def safe_geocode(address):
    """
    Função para geocodificar um endereço com tratamento de exceções.
    """
    print(address)
    print(geolocator.geocode(address))
    try:
        location = geolocator.geocode(address)
        return location
    except Exception as e:
        print(f"Erro ao geocodificar {address}: {e}")
        return None

def geocode_async(df, mapa):
    """
    Função para geocodificar endereços de forma assíncrona utilizando threads.
    """
    queue = Queue()
    results = []

    # Preencher a fila com os endereços a serem geocodificados
    for idx, address in df['ENDERECO_COMPLETO'].items():
        queue.put((idx, address))

    def worker():
        nonlocal mapa
        while not queue.empty():
            idx, address = queue.get()
            location = safe_geocode(address)
            results.append((idx, location))
            queue.task_done()
            
            # Atualizar mapa com marcador do endereço geocodificado
            if location:
                folium.Marker(
                    location=[location.latitude, location.longitude],
                    popup=df.at[idx, 'ENDERECO_COMPLETO']
                ).add_to(mapa)
                mapa.save('mapaenderecosvalidados.html')

    # Definir o número máximo de threads
    num_threads = 5
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(worker) for _ in range(num_threads)]
        queue.join()  # Aguardar até que todos os itens da fila sejam processados

def main():
    """
    Função principal para carregar, limpar, geocodificar e mapear os endereços.
    """
    try:
        df = pd.read_csv('ends_prova_bi.csv', encoding='latin1')
    except UnicodeDecodeError:
        print("Erro de decodificação. Tentando com outro encoding...")
        df = pd.read_csv('ends_prova_bi.csv', encoding='iso-8859-1')

    df = df.drop_duplicates()
    df = df.apply(lambda x: x.str.strip().replace(r'\s+', ' ', regex=True) if x.dtype == 'object' else x)
    df['LOGRADOURO'] = df['LOGRADOURO'].str.replace('ROD', 'RODOVIA', case=False)
    df['LOGRADOURO'] = df['LOGRADOURO'].str.replace('AV', 'AVENIDA', case=False)
    df['ENDERECO_COMPLETO'] = df['LOGRADOURO'] + ', ' + df['NOME'] + ', ' + df['NOME_CIDADE'] + ', ' + df['NOME_ESTADO'] + ', Brasil'
    

    
    # Criar o mapa inicial
    centro_mapa = [-15.788497,-47.879873]  # Coordenadas de Brasília, por exemplo
    mapa = folium.Map(location=centro_mapa, zoom_start=6)
    
    # Geocodificar assincronamente e adicionar marcadores ao mapa dinamicamente
    geocode_async(df, mapa)

if __name__ == '__main__':
    main()
