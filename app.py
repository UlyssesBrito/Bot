from flask import Flask, request, jsonify
import openai
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)

# Configura a chave da API do OpenAI
chave_api = os.getenv("OPENAI_API_KEY")
openai.api_key = chave_api

# Histórico de mensagens para manter a conversa contextualizada
historico = [{"role": "system", "content": "Você é um vendedor especializado em responder perguntas sobre a agência AtarDigital..."}]

@app.route('/webhook', methods=['POST'])
def webhook():
    global historico
    data = request.json

    # Extrai a mensagem recebida
    message = data.get("mensagem")

    # Verifica se a mensagem está presente
    if not message:
        return jsonify({"resposta": "Mensagem inválida!"})

    # Responde com uma mensagem padrão caso "humano" seja mencionado
    if "humano" in message.lower():
        return jsonify({"resposta": "Transferindo você para um atendente real. Aguarde um momento."})

    # Adiciona a mensagem do usuário ao histórico
    historico.append({'role': 'user', 'content': message})

    # Gera uma resposta usando o modelo do OpenAI
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=historico
    )

    # Extrai e armazena a resposta
    resposta = completion.choices[0].message.content
    historico.append({"role": "assistant", "content": resposta})

    # Retorna a resposta como JSON
    return jsonify({"resposta": resposta})

if __name__ == '__main__':
    app.run(port=5000)
