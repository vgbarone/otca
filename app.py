{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "mount_file_id": "1ULLXO1GwO5KHEZxO2N5vpKI6qbEBsf2n",
      "authorship_tag": "ABX9TyPSoV/R1aGrcLCgLYf+Hkj4"
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "code",
      "source": [
        "# Configurações iniciais\n",
        "\n",
        "from flask import Flask, render_template, request, jsonify, session\n",
        "import google.generativeai as genai\n",
        "import json\n",
        "import datetime\n",
        "import gspread\n",
        "from oauth2client.client import GoogleCredentials\n",
        "import secrets # Importe secrets para gerar chave secreta\n",
        "\n",
        "app = Flask(__name__, template_folder='templates', static_folder='static')\n",
        "\n",
        "# Gere uma chave secreta aleatória para as sessões do Flask\n",
        "app.secret_key = secrets.token_urlsafe(16)\n",
        "\n",
        "#GOOGLE API KEY\n",
        "GOOGLE_API_KEY=\"AIzaSyAZaW5yTHSu911Xk18-nWkJzHr6S1B7-hY\"\n",
        "genai.configure(api_key=GOOGLE_API_KEY)"
      ],
      "metadata": {
        "id": "WhtSknfO0qyv"
      },
      "execution_count": 4,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "# Carrega o arquivo JSON com informações sobre a Lei de Crimes Ambientais\n",
        "with open('lei_crimes_ambientais.json', 'r') as f:\n",
        "    lei_data = json.load(f)"
      ],
      "metadata": {
        "id": "ngIOImvm8YI0"
      },
      "execution_count": 12,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "#Listando os modelos disponíveis\n",
        "for m in genai.list_models():\n",
        "  if 'generateContent' in m.supported_generation_methods:\n",
        "    print(m.name)"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 139
        },
        "id": "FYDQCq3y0yCh",
        "outputId": "223bb570-e7d1-4234-db65-b31d8bae6cc0"
      },
      "execution_count": 5,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "models/gemini-1.0-pro\n",
            "models/gemini-1.0-pro-001\n",
            "models/gemini-1.0-pro-latest\n",
            "models/gemini-1.0-pro-vision-latest\n",
            "models/gemini-1.5-pro-latest\n",
            "models/gemini-pro\n",
            "models/gemini-pro-vision\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "generation_config = {\n",
        "  \"candidate_count\": 1,\n",
        "  \"temperature\": 0.5,\n",
        "}"
      ],
      "metadata": {
        "id": "Y3UGdf6a0y5j"
      },
      "execution_count": 6,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "safety_settings={\n",
        "    'HATE': 'BLOCK_NONE',\n",
        "    'HARASSMENT': 'BLOCK_NONE',\n",
        "    'SEXUAL' : 'BLOCK_NONE',\n",
        "    'DANGEROUS' : 'BLOCK_NONE'\n",
        "    }"
      ],
      "metadata": {
        "id": "e49KxIip09oA"
      },
      "execution_count": 7,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "model = genai.GenerativeModel(model_name='gemini-1.0-pro',\n",
        "                                  generation_config=generation_config,\n",
        "                                  safety_settings=safety_settings,)"
      ],
      "metadata": {
        "id": "GXxV4TWi1A_H"
      },
      "execution_count": 8,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "chat = model.start_chat(history=[])"
      ],
      "metadata": {
        "id": "SxCClonK-UUH"
      },
      "execution_count": 9,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "# Função para salvar a denúncia no Google Sheets\n",
        "def salvar_denuncia(denuncia):\n",
        "    auth.authenticate_user()\n",
        "    gc = gspread.authorize(GoogleCredentials.get_application_default())\n",
        "\n",
        "    # ID da planilha (substitua pelo ID da sua planilha)\n",
        "    planilha_id = \"1jbC2vKsy-Ku6MEraouV4LIM58LPb8f8s0eUpPWi7-J4\" # Substitua pelo ID da sua planilha\n",
        "\n",
        "\n",
        "    # Abre a planilha\n",
        "    planilha = gc.open_by_key(planilha_id)\n",
        "\n",
        "    # Seleciona a primeira aba da planilha\n",
        "    aba = planilha.sheet1\n",
        "\n",
        "    # Adiciona a denúncia à planilha\n",
        "    aba.append_row([\n",
        "        denuncia['data_hora'],\n",
        "        denuncia['coordenadas'],\n",
        "        denuncia['nome'],\n",
        "        denuncia['email'],\n",
        "        denuncia['endereco'],\n",
        "        denuncia['uf'],\n",
        "        denuncia['municipio'],\n",
        "        denuncia['texto']\n",
        "    ])"
      ],
      "metadata": {
        "id": "_I2P50Q-84Lo"
      },
      "execution_count": 10,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "# Função para buscar informações na Lei de Crimes Ambientais\n",
        "def encontrar_informacao_lei(pergunta):\n",
        "    for item in lei_data:\n",
        "        if any(keyword in pergunta.lower() for keyword in item['keywords']):\n",
        "            return item['informacao']\n",
        "    return None\n",
        "\n",
        "@app.route('/')\n",
        "def index():\n",
        "    return render_template('index.html')\n",
        "\n",
        "@app.route('/enviar_mensagem', methods=['POST'])\n",
        "def enviar_mensagem():\n",
        "    mensagem = request.form['mensagem']\n",
        "\n",
        "    # Processar a mensagem com o Google Gemini\n",
        "    informacao_lei = encontrar_informacao_lei(mensagem)\n",
        "    if informacao_lei:\n",
        "        prompt_gemini = f\"Aqui está uma pergunta sobre a Lei de Crimes Ambientais: {mensagem}\\n\\n Aqui está alguma informação relevante da lei: {informacao_lei}\\n\\n Por favor, responda a pergunta de forma informativa.\"\n",
        "    else:\n",
        "        prompt_gemini = f\"Aqui está uma pergunta sobre a Lei de Crimes Ambientais: {mensagem}\\n\\n Por favor, responda a pergunta da melhor forma possível.\"\n",
        "\n",
        "    response = chat.send_message(prompt_gemini)\n",
        "\n",
        "    return jsonify({'resposta': response.text})\n",
        "\n",
        "@app.route('/salvar_coordenadas', methods=['POST'])\n",
        "def salvar_coordenadas():\n",
        "    latitude = request.form['latitude']\n",
        "    longitude = request.form['longitude']\n",
        "    nome = request.form['nome']\n",
        "    email = request.form['email']\n",
        "    endereco = request.form['endereco']\n",
        "    texto = request.form['texto']\n",
        "    uf = request.form['uf']  # Obtem UF do formulário\n",
        "    municipio = request.form['municipio']  # Obtem Município do formulário\n",
        "\n",
        "    # Coleta data e hora automaticamente\n",
        "    data_hora = datetime.datetime.now().strftime(\"%Y-%m-%d %H:%M:%S\")\n",
        "    coordenadas = f\"{latitude}, {longitude}\"\n",
        "\n",
        "    # Criar dicionário da denúncia\n",
        "    denuncia = {\n",
        "        \"data_hora\": data_hora,\n",
        "        \"coordenadas\": coordenadas,\n",
        "        \"nome\": nome,\n",
        "        \"email\": email,\n",
        "        \"endereco\": endereco,\n",
        "        \"texto\": texto,\n",
        "        \"uf\": uf,  # Adiciona UF ao dicionário\n",
        "        \"municipio\": municipio  # Adiciona Município ao dicionário\n",
        "    }\n",
        "\n",
        "    # Salvar denúncia no Google Sheets\n",
        "    salvar_denuncia(denuncia)\n",
        "\n",
        "    return jsonify({'status': 'success'})\n",
        "\n",
        "if __name__ == '__main__':\n",
        "    app.run(debug=True)"
      ],
      "metadata": {
        "id": "nukriY25Bw6J"
      },
      "execution_count": None,
      "outputs": []
    }
  ]
}
