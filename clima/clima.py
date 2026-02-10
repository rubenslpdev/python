import requests
from datetime import datetime

# Configurações de cores ANSI
RED = '\033[91m'
BLUE = '\033[94m'
CYAN = '\033[96m'
BOLD = '\033[1m'
RESET = '\033[0m'

# Dicionário de tradução dos códigos climáticos (WMO)
WEATHER_CODES = {
    0: "Céu Limpo",
    1: "Principalmente Limpo", 2: "Parcialmente Nublado", 3: "Encoberto",
    45: "Neblina", 48: "Neblina com Gelo",
    51: "Garoa Leve", 53: "Garoa Moderada", 55: "Garoa Densa",
    61: "Chuva Leve", 63: "Chuva Moderada", 65: "Chuva Forte",
    71: "Neve Leve", 73: "Neve Moderada", 75: "Neve Forte",
    80: "Pancadas de Chuva Leves", 81: "Pancadas de Chuva", 82: "Pancadas Violentas",
    95: "Trovoada", 96: "Trovoada com Granizo Leve", 99: "Trovoada com Granizo Forte"
}

def obter_localizacao():
    try:
        response = requests.get('http://ip-api.com/json/', timeout=5)
        dados = response.json()
        return dados['lat'], dados['lon'], dados['city']
    except:
        return -23.55, -46.63, "São Paulo (Local Padrão)"

def buscar_previsao():
    lat, lon, cidade = obter_localizacao()
    
    # URL com temperaturas e códigos de clima para 5 dias
    url = (f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
           f"&daily=temperature_2m_max,temperature_2m_min,weathercode&timezone=auto&forecast_days=5")

    try:
        resposta = requests.get(url, timeout=5)
        dados = resposta.json()
        
        diario = dados['daily']
        datas = diario['time']
        maximas = diario['temperature_2m_max']
        minimas = diario['temperature_2m_min']
        codigos = diario['weathercode']

        print(f"\n{BOLD}{CYAN}🌍 Localização: {cidade}{RESET}")
        print(f"{'Data':<15} | {'Mínima':<12} | {'Máxima':<12} | {'Condição'}")
        print("-" * 70)

        for i in range(len(datas)):
            obj_data = datetime.strptime(datas[i], "%Y-%m-%d")
            data_formatada = obj_data.strftime("%d/%m (%a)")

            # Traduz o código do clima
            condicao = WEATHER_CODES.get(codigos[i], "Desconhecido")

            # Formatação com cores
            min_str = f"{BLUE}{minimas[i]:>4}°C{RESET}"
            max_str = f"{RED}{maximas[i]:>4}°C{RESET}"

            print(f"{data_formatada:<15} | {min_str:<21} | {max_str:<21} | {condicao}")
        
        print(f"\n{BOLD}Tenha um ótimo dia!{RESET}\n")

    except Exception as e:
        print(f"Erro ao conectar com o serviço de clima: {e}")

if __name__ == "__main__":
    buscar_previsao()