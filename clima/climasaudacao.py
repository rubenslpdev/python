import requests
import os
import socket
from datetime import datetime

# Cores ANSI
BLACK = "\033[0;30m"
RED = "\033[0;31m"
GREEN = "\033[0;32m"
BROWN = "\033[0;33m"
BLUE = "\033[0;34m"
PURPLE = "\033[0;35m"
CYAN = "\033[0;36m"
LIGHT_GRAY = "\033[0;37m"
DARK_GRAY = "\033[1;30m"
LIGHT_RED = "\033[1;31m"
LIGHT_GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
LIGHT_BLUE = "\033[1;34m"
LIGHT_PURPLE = "\033[1;35m"
LIGHT_CYAN = "\033[1;36m"
LIGHT_WHITE = "\033[1;37m"
BOLD = "\033[1m"
FAINT = "\033[2m"
ITALIC = "\033[3m"
UNDERLINE = "\033[4m"
RESET = '\033[0m'

WEATHER_CODES = {
    0: "Céu Limpo", 1: "Principalmente Limpo", 2: "Parcialmente Nublado", 3: "Encoberto",
    45: "Neblina", 48: "Neblina com Gelo", 51: "Garoa Leve", 53: "Garoa Moderada", 
    55: "Garoa Densa", 61: "Chuva Leve", 63: "Chuva Moderada", 65: "Chuva Forte",
    80: "Pancadas de Chuva Leves", 81: "Pancadas de Chuva", 82: "Pancadas Violentas",
    95: "Trovoada", 96: "Trovoada com Granizo", 99: "Trovoada Forte"
}

def obter_saudacao():
    hora = datetime.now().hour
    if 5 <= hora < 12: return "Bom dia"
    elif 12 <= hora < 18: return "Boa tarde"
    else: return "Boa noite"

def clima_compacto():
    try:
        # 1. Tenta obter o nome do usuário de forma mais segura para o Ubuntu
        try:
            usuario = os.getlogin().capitalize()
        except:
            usuario = os.getenv('USER', 'Usuário').capitalize()

        # 2. Localização (Aumentei o timeout para evitar falhas em conexões lentas)
        try:
            res_ip = requests.get('http://ip-api.com/json/', timeout=5).json()
            lat, lon, cidade = res_ip['lat'], res_ip['lon'], res_ip['city']
        except Exception as e:
            # Fallback caso a API de IP falhe
            lat, lon, cidade = -23.99, -46.41, "Praia Grande (Local Padrão)"

        # 3. Dados do Clima (Hoje)
        # URL com timezone explícito e pegando o tempo atual (current_weather)
        url = (f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
               f"&daily=temperature_2m_max,temperature_2m_min,weathercode,windspeed_10m_max"
               f"&current_weather=true&timezone=auto&forecast_days=1")
        
        res_clima = requests.get(url, timeout=5).json()
        
        # Dados do momento exato agora
        agora = res_clima['current_weather']
        temp_atual = agora['temperature']
        
        # Dados do dia (máxima e mínima)
        diario = res_clima['daily']
        max_t = f"{RED}{diario['temperature_2m_max'][0]}°C{RESET}"
        min_t = f"{BLUE}{diario['temperature_2m_min'][0]}°C{RESET}"
        
        # Usamos o código do tempo ATUAL para ser mais fiel ao que você vê na janela
        condicao = WEATHER_CODES.get(agora['weathercode'], "Tempo Estável").lower()
        vento = agora['windspeed']
        
        # 4. Formatação da Data
        data_hj = datetime.now().strftime("%d/%m - %a")
        
        # 5. Saída Final
        print(f"\n{LIGHT_BLUE}{obter_saudacao()}, {usuario}!{RESET}")
        print(f"Agora em {cidade} faz {temp_atual}°C com {condicao}.")
        print(f"Para hoje ({data_hj}), a mínima é de {min_t} e a máxima de {max_t}.")
        print(f"Vento atual de {vento}km/h.\n")

    except Exception as e:
        # Agora ele vai te dizer o erro real se algo falhar
        print(f"\n{RED}Erro no Clima:{RESET} {e}\n")

if __name__ == "__main__":
    clima_compacto()