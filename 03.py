# Desenvolva um programa que consulte informações de endereço a partir de um CEP fornecido pelo usuário, 
# utilizando a API ViaCEP. 
# O programa deve exibir o logradouro, bairro, cidade e estado correspondentes ao CEP consultado.


import requests
import re

def limpar_cep(cep_sujo: str) -> str:
    """
    Remove todos os caracteres não numéricos de uma string de CEP.
    Ex: "12345-678" -> "12345678"
    """
    # Usa uma expressão regular para encontrar tudo que NÃO é um dígito (\D)
    # e substituir por uma string vazia ("")
    return re.sub(r'\D', '', cep_sujo)

def consultar_cep():
    """
    Solicita um CEP ao usuário, consulta a API ViaCEP e exibe
    o endereço formatado.
    """
    
    print("--- Consulta de Endereço por CEP (ViaCEP) ---")
    
    cep_input = input("Digite o CEP para consulta (ex: 12345-678): ")
    
    # 1. Limpar e validar o CEP
    cep = limpar_cep(cep_input)
    
    if len(cep) != 8:
        print(f"\n[ERRO] O CEP '{cep_input}' é inválido.")
        print("Um CEP válido deve conter 8 números.")
        return
        
    # 2. Montar a URL da API
    url = f"https://viacep.com.br/ws/{cep}/json/"
    
    print(f"\nConsultando o CEP {cep}...")

    try:
        # 3. Fazer a requisição GET
        response = requests.get(url, timeout=10)
        
        # 4. Levantar um erro para status ruins (404, 500, etc.)
        response.raise_for_status()
        
        # 5. Converter a resposta JSON em um dicionário
        data = response.json()
        
        # 6. Verificar se a API retornou um erro interno (CEP não encontrado)
        #    A ViaCEP retorna 200 OK com {"erro": true} se o CEP não existe.
        if data.get("erro"):
            print(f"\n[ERRO] O CEP {cep} não foi encontrado na base de dados.")
            return

        # 7. Extrair os dados (usando .get() para segurança)
        #    'localidade' é o nome do campo para 'cidade' na ViaCEP
        logradouro = data.get("logradouro", "N/A")
        bairro = data.get("bairro", "N/A")
        cidade = data.get("localidade", "N/A")
        estado = data.get("uf", "N/A")
        
        # 8. Exibir os resultados formatados
        print("\n--- Endereço Encontrado ---")
        print(f"CEP:         {data.get('cep', cep)}")
        print(f"Logradouro:  {logradouro}")
        print(f"Bairro:      {bairro}")
        print(f"Cidade:      {cidade}")
        print(f"Estado (UF): {estado}")

    # --- Bloco de Tratamento de Erros ---
    except requests.exceptions.HTTPError as http_err:
        print(f"\n[ERRO HTTP]: {http_err}")
        print("Ocorreu um erro ao tentar acessar o servidor (ex: 404).")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"\n[ERRO DE CONEXÃO]: {conn_err}")
        print("Não foi possível conectar. Verifique sua conexão com a internet.")
    except requests.exceptions.Timeout as timeout_err:
        print(f"\n[ERRO DE TIMEOUT]: {timeout_err}")
        print("A consulta demorou demais para responder.")
    except requests.exceptions.RequestException as req_err:
        print(f"\n[ERRO NA REQUISIÇÃO]: {req_err}")
    except Exception as e:
        print(f"\n[ERRO INESPERADO]: {e}")

# --- Ponto de Entrada do Programa ---
if __name__ == "__main__":
    consultar_cep()