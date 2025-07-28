
from flask import Flask, render_template_string
from requests import get

app = Flask(__name__)

# URL do backend FastAPI
API_URL = "http://127.0.0.1:8000/produtos"

# Template HTML com tabela responsiva
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Painel de Produtos</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f4f4f4; }
        h1 { text-align: center; }
        table { width: 100%; border-collapse: collapse; background-color: white; }
        th, td { padding: 12px; border: 1px solid #ddd; text-align: left; }
        th { background-color: #007BFF; color: white; }
        tr:hover { background-color: #f1f1f1; }
        img { max-width: 100px; height: auto; }
    </style>
</head>
<body>
    <h1>Produtos Cadastrados</h1>
    <table>
        <thead>
            <tr>
                <th>Imagem</th>
                <th>Nome</th>
                <th>Descrição</th>
                <th>Preço (R$)</th>
            </tr>
        </thead>
        <tbody>
            {% for produto in produtos %}
            <tr>
                <td><img src="{{ produto.imagem_url }}" alt="Imagem do produto"></td>
                <td>{{ produto.nome }}</td>
                <td>{{ produto.descricao }}</td>
                <td>{{ "%.2f"|format(produto.preco) }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
"""

@app.route("/")
def painel():
    try:
        response = get(API_URL)
        produtos = response.json()
    except Exception as e:
        produtos = []
    return render_template_string(HTML_TEMPLATE, produtos=produtos)

if __name__ == "__main__":
    app.run(debug=True)
