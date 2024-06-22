import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import folium

user_agent = "my-cool-application"
geolocator = Nominatim(user_agent=user_agent, timeout=10)
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1, max_retries=3, error_wait_seconds=5)

def safe_geocode(address):
    print(address)
    print(geocode(address))
    try:
        return geocode(address)
    except Exception as e:
        print(f"Erro ao geocodificar {address}: {e}")
        return None
def main():
    try:
        df = pd.read_csv('ends_prova_bi.csv', encoding='latin1')
    except UnicodeDecodeError:
        print("Erro de decodificação. Tentando com outro encoding...")
        df = pd.read_csv('/home/bruno/Python/santri/ends_prova_bi.csv', encoding='iso-8859-1')

    
    df = df.drop_duplicates()
    df = df.apply(lambda x: x.str.strip().replace(r'\s+', ' ', regex=True) if x.dtype == 'object' else x)
    df['LOGRADOURO'] = df['LOGRADOURO'].str.replace('ROD', 'RODOVIA', case=False)
    df['LOGRADOURO'] = df['LOGRADOURO'].str.replace('AV', 'AVENIDA', case=False)
    df['ENDERECO_COMPLETO'] = df['LOGRADOURO'] + ', ' + df['NOME'] + ', ' + df['NOME_CIDADE'] + ', ' + df['NOME_ESTADO'] + ', Brasil'
       

    df['LOCATION'] = df['ENDERECO_COMPLETO'].apply(safe_geocode)
    df['LATITUDE'] = df['LOCATION'].apply(lambda loc: loc.latitude if loc else None)
    df['LONGITUDE'] = df['LOCATION'].apply(lambda loc: loc.longitude if loc else None)


    df_validados = df.dropna(subset=['LATITUDE', 'LONGITUDE'])
    centro_mapa = [df_validados['LATITUDE'].mean(), df_validados['LONGITUDE'].mean()]
    mapa = folium.Map(location=centro_mapa, zoom_start=6)

    for _, row in df_validados.iterrows():
        folium.Marker(
            location=[row['LATITUDE'], row['LONGITUDE']],
            popup=row['ENDERECO_COMPLETO']
        ).add_to(mapa)


    mapa.save('mapa_enderecos_validados.html')

    print("Mapa dos endereços validados salvo como 'mapa_enderecos_validados.html'")


if __name__ == '__main__':
     main()