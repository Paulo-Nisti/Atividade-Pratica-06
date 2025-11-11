# Crie um programa que consulte a cotação atual de uma moeda estrangeira em relação ao Real Brasileiro (BRL). 
# O usuário deve informar o código da moeda desejada (ex: USD, EUR, GBP), e o programa deve exibir o valor atual, 
# máximo e mínimo da cotação, 
# além da data e hora da última atualização. Utilize a API da AwesomeAPI para obter os dados de cotação.

import requests
from datetime import datetime

def consultar_cotacao():
    """
    Solicita um código de moeda (ex: USD), consulta a AwesomeAPI
    e exibe a cotação em BRL (Real Brasileiro).
    """
    
    print("--- Consulta de Cotação de Moeda (em BRL) ---")
    
    # 1. Obter e formatar a entrada do usuário
    moeda_input = input("Digite o código da moeda (ex: USD, EUR, GBP): ")
    
    # Limpa espaços em branco e converte para maiúsculas (padrão da API)
    moeda_formatada = moeda_input.strip().upper()
    
    if not moeda_formatada:
        print("\n[ERRO] Você não digitou um código de moeda.")
        return

    # 2. Montar a URL da API
    # A API espera o formato: MOEDA-BRL (ex: USD-BRL)
    url = f"https://economia.awesomeapi.com.br/json/last/{moeda_formatada}-BRL"
    
    # A chave principal que a API retorna (ex: 'USDBRL')
    chave_api = f"{moeda_formatada}BRL"
    
    print(f"\nBuscando cotação para {moeda_formatada} -> BRL...")

    try:
        # 3. Fazer a requisição GET
        response = requests.get(url, timeout=10)
        
        # 4. Levantar um erro se a requisição falhou (ex: 404, 500)
        response.raise_for_status()
        
        # 5. Converter a resposta JSON em um dicionário
        data = response.json()
        
        # 6. Verificar se a moeda foi encontrada
        if chave_api not in data:
            print(f"\n[ERRO] A API não retornou dados para '{chave_api}'.")
            print("Verifique se o código da moeda está correto.")
            return

        # 7. Extrair as informações
        cotacao_info = data[chave_api]
        
        nome_moeda = cotacao_info.get("name", "Nome não disponível")
        valor_atual_str = cotacao_info.get("bid", "0") # 'bid' é o valor de compra (atual)
        maximo_str = cotacao_info.get("high", "0")
        minimo_str = cotacao_info.get("low", "0")
        data_atualizacao_str = cotacao_info.get("create_date", "")

        # 8. Formatar os dados para exibição
        
        # Formatar valores monetários
        try:
            valor_atual = f"R$ {float(valor_atual_str):.2f}"
            maximo = f"R$ {float(maximo_str):.2f}"
            minimo = f"R$ {float(minimo_str):.2f}"
        except (ValueError, TypeError):
            print("\n[ERRO] Não foi possível formatar os valores monetários recebidos.")
            valor_atual, maximo, minimo = "N/A", "N/A", "N/A"

        # Formatar a data
        data_formatada = "N/A"
        if data_atualizacao_str:
            try:
                # Converte a string da API (ex: "2023-10-25 10:00:00")
                data_obj = datetime.strptime(data_atualizacao_str, "%Y-%m-%d %H:%M:%S")
                # Formata para o padrão brasileiro (ex: "25/10/2023 às 10:00:0S")
                data_formatada = data_obj.strftime("%d/%m/%Y às %H:%M:%S")
            except ValueError:
                data_formatada = f"Data não pôde ser formatada ({data_atualizacao_str})"

        # 9. Exibir os resultados
        print("\n--- Resultado da Consulta ---")
        print(f"Moeda: {nome_moeda}")
        print(f"Valor Atual (Compra): {valor_atual}")
        print(f"Cotação Máxima (dia): {maximo}")
        print(f"Cotação Mínima (dia): {minimo}")
        print(f"Última Atualização:   {data_formatada}")

    # --- Bloco de Tratamento de Erros ---
    except requests.exceptions.HTTPError as http_err:
        if http_err.response.status_code == 404:
            print(f"\n[ERRO 404] Moeda não encontrada.")
            print(f"Não foi possível encontrar a cotação para '{moeda_formatada}-BRL'.")
        else:
            print(f"\n[ERRO HTTP]: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"\n[ERRO DE CONEXÃO]: {conn_err}")
        print("Não foi possível conectar. Verifique sua conexão com a internet.")
    except requests.exceptions.Timeout as timeout_err:
        print(f"\n[ERRO DE TIMEOUT]: {timeout_err}")
        print("A consulta demorou demais para responder.")
    except Exception as e:
        print(f"\n[ERRO INESPERADO]: {e}")

# --- Ponto de Entrada do Programa ---
if __name__ == "__main__":
    consultar_cotacao()