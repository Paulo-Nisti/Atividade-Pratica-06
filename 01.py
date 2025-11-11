# Crie um programa que gera uma senha aleatória com o módulo random, utilizando caracteres especiais, 
# possibilitando o usuário a informar a quantidade de caracteres dessa senha aleatória.


import random
import string
import sys # Usado para o caso de o pool de caracteres ser vazio

def gerar_senha_aleatoria(tamanho: int) -> str:
    """
    Gera uma senha aleatória com o tamanho especificado.

    A senha incluirá uma mistura de letras maiúsculas, minúsculas,
    números e caracteres especiais.

    Parâmetros:
        tamanho (int): A quantidade de caracteres desejada para a senha.

    Retorna:
        str: A senha aleatória gerada.
    """
    
    # 1. Criar o "pool" de caracteres
    #    string.ascii_letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    #    string.digits = '0123456789'
    #    string.punctuation = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    
    letras = string.ascii_letters
    numeros = string.digits
    especiais = string.punctuation # Caracteres especiais

    # Combinar todos os caracteres em uma única string
    pool_de_caracteres = letras + numeros + especiais
    
    if not pool_de_caracteres:
        # Verificação de segurança, embora com o string module seja improvável
        print("Erro: O pool de caracteres está vazio.", file=sys.stderr)
        return ""
        
    # 2. Gerar a senha
    #    random.choices(populacao, k=tamanho)
    #    - 'choices' (plural) é a função ideal: ela escolhe 'k' itens
    #      da 'populacao' (nosso pool), permitindo repetições.
    #    - O resultado é uma LISTA de caracteres (ex: ['a', '!', '5', 'T'])
    lista_de_caracteres = random.choices(pool_de_caracteres, k=tamanho)
    
    # 3. Converter a lista de volta para uma string
    #    "".join(lista) é a forma mais eficiente de juntar
    #    uma lista de caracteres em uma única string.
    senha_gerada = "".join(lista_de_caracteres)
    
    return senha_gerada

# --- Bloco Principal de Execução ---
# Este código só roda quando o arquivo é executado diretamente
if __name__ == "__main__":
    
    print("--- Gerador de Senha Aleatória ---")
    
    try:
        # 1. Solicitar o tamanho da senha ao usuário
        tamanho_str = input("Digite a quantidade de caracteres desejada para a senha: ")
        
        # 2. Converter a entrada para um número inteiro
        tamanho_desejado = int(tamanho_str)
        
        # 3. Validar o tamanho
        if tamanho_desejado <= 0:
            print("\n[ERRO] A quantidade de caracteres deve ser um número positivo.")
        else:
            # 4. Chamar a função para gerar a senha
            senha = gerar_senha_aleatoria(tamanho_desejado)
            
            # 5. Exibir o resultado
            print("\nSua senha aleatória gerada é:")
            print(f"-> {senha}")

    except ValueError:
        # Captura o erro se o usuário digitar "abc" ou "1.5"
        print(f"\n[ERRO] Entrada inválida ('{tamanho_str}'). Por favor, digite um NÚMERO inteiro.")
    
    except Exception as e:
        # Captura qualquer outro erro inesperado
        print(f"\n[ERRO INESPERADO]: {e}")