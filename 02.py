# Crie um programa que gera um perfil de usuário aleatório usando a API 'Random User Generator'. 
# O programa deve exibir o nome, email e país do usuário gerado.

import requests

def gerar_perfil_usuario_aleatorio():
    """
    Busca um usuário aleatório da API 'randomuser.me' e exibe
    seu nome, email e país.
    """
    
    # URL da API
    url = "https://randomuser.me/api/"
    
    print("Buscando um perfil de usuário aleatório...")

    try:
        # 1. Fazer a requisição GET para a API
        response = requests.get(url, timeout=10)
        
        # 2. Levantar um erro se a requisição falhou (ex: status 404, 500)
        response.raise_for_status() 
        
        # 3. Converter a resposta JSON em um dicionário Python
        data = response.json()
        
        # 4. Extrair os dados do usuário
        # A API retorna uma lista 'results', pegamos o primeiro item [0]
        if not data.get('results'):
            print("Erro: A API não retornou resultados válidos.")
            return

        usuario_info = data['results'][0]
        
        # 5. Extrair os campos específicos
        # O nome é um objeto aninhado
        nome_completo = f"{usuario_info['name']['first']} {usuario_info['name']['last']}"
        
        email = usuario_info['email']
        
        # O país está dentro do objeto 'location'
        pais = usuario_info['location']['country']
        
        # 6. Exibir os resultados formatados
        print("\n--- Perfil Gerado com Sucesso ---")
        print(f"Nome:   {nome_completo}")
        print(f"Email:  {email}")
        print(f"País:   {pais}")

    except requests.exceptions.HTTPError as http_err:
        print(f"\n[ERRO HTTP]: {http_err}")
        print("Não foi possível buscar os dados. O servidor da API pode estar com problemas.")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"\n[ERRO DE CONEXÃO]: {conn_err}")
        print("Não foi possível conectar. Verifique sua conexão com a internet.")
    except requests.exceptions.Timeout as timeout_err:
        print(f"\n[ERRO DE TIMEOUT]: {timeout_err}")
        print("A requisição demorou demais para responder.")
    except requests.exceptions.RequestException as req_err:
        # Pega qualquer outro erro da biblioteca requests
        print(f"\n[ERRO NA REQUISIÇÃO]: {req_err}")
    except KeyError as key_err:
        # Pega um erro se a API mudar sua estrutura (ex: 'name' não existir)
        print(f"\n[ERRO DE DADOS]: Não foi possível encontrar a chave {key_err} nos dados recebidos.")
        print("A estrutura da API pode ter mudado.")
    except Exception as e:
        # Pega qualquer outro erro inesperado
        print(f"\n[ERRO INESPERADO]: {e}")

# --- Ponto de Entrada do Programa ---
# Este bloco só é executado quando o script é rodado diretamente
if __name__ == "__main__":
    gerar_perfil_usuario_aleatorio()