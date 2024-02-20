from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
modelo = "gpt-3.5-turbo"

def carrega(nome_do_arquivo):
    try:
        with open(nome_do_arquivo, "r") as arquivo:
            dados = arquivo.read()
            return dados
    except IOError as e:
        print(f"Erro no carregamento de arquivo: {e}")

def salva(nome_do_arquivo, conteudo):
    try:
        with open(nome_do_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(conteudo)
    except IOError as e:
        print(f"Erro ao salvar o arquivo: {e}")

def analisar_transacao(lista_de_transacoes):
    print("1. Executando a análise dee transação")
    
    prompt_sistema = """
    Analise as transações financeiras a seguir e identifique se cada uma delas é uma "Possível Fraude" ou deve ser "Aprovada". 
    Adicione um atributo "Status" com um dos valores: "Possível Fraude" ou "Aprovado".

    Cada nova transação deve ser inserida dentro da lista do JSON.

    # Possíveis indicações de fraude
    - Transações com valores muito discrepantes
    - Transações que ocorrem em locais muito distantes um do outro
    
        Adote o formato de resposta abaixo para compor sua resposta.
        
    # Formato Saída 
    {
        "transacoes": [
            {
            "id": "id",
            "tipo": "crédito ou débito",
            "estabelecimento": "nome do estabelecimento",
            "horário": "horário da transação",
            "valor": "R$XX,XX",
            "nome_produto": "nome do produto",
            "localização": "cidade - estado (País)"
            "status": ""
            },
        ]
    } 
    """
    
    lista_mensagens = [
        {
            "role" : "system",
            "content" : prompt_sistema
        },
        {
            "role" : "user",
            "content" : f"Considere o CSV abaixo, onde cada linha é uma transação diferente: {lista_de_transacoes}. Sua resposta deve adotar o #Formato de Resposta (apenas um json sem outros comentários)"
        }
    ]
    
    resposta = cliente.chat.completions.create(
        messages=lista_mensagens,
        model=modelo,
        temperature=0
    )
    
    conteudo = resposta.choices[0].message.content.replace("'", '"')
    print("\nConteúdo:", conteudo)
    json_resultado = json.loads(conteudo)
    print("\nJSON:", json_resultado)
    return json_resultado

lista_transacoes = carrega("dados/transacoes.csv")
analisar_transacao(lista_transacoes)