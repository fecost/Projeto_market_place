
import requests
from bs4 import BeautifulSoup
import schedule
import time
from datetime import datetime

# Configurações
BACKEND_URL = "http://localhost:8000/produtos"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}
PROXIES = {
    "http": None,
    "https": None
}

# Função para cadastrar produto no backend
def cadastrar_produto(produto):
    try:
        response = requests.post(BACKEND_URL, json=produto)
        if response.status_code == 200:
            print(f"[{datetime.now()}] Produto cadastrado: {produto['nome']}")
        else:
            print(f"[{datetime.now()}] Erro ao cadastrar: {response.status_code}")
    except Exception as e:
        print(f"[{datetime.now()}] Falha na requisição: {e}")

# Scraper da Shopee (simples)
def buscar_shopee():
    url = "https://shopee.com.br/search?keyword=smartphone"
    try:
        r = requests.get(url, headers=HEADERS, proxies=PROXIES, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        for item in soup.select("div.shopee-search-item-result__item"):
            nome = item.select_one("div._10Wbs-").text if item.select_one("div._10Wbs-") else "Produto Shopee"
            preco = 199.99
            imagem_url = ""
            produto = {
                "nome": nome,
                "descricao": "Produto encontrado na Shopee",
                "preco": preco,
                "imagem_url": imagem_url
            }
            cadastrar_produto(produto)
    except Exception as e:
        print(f"[Shopee] Erro: {e}")

# Scraper do Mercado Livre (simples)
def buscar_mercado_livre():
    url = "https://lista.mercadolivre.com.br/smartphone"
    try:
        r = requests.get(url, headers=HEADERS, proxies=PROXIES, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        for item in soup.select("li.results-item"):
            nome = item.select_one("h2").text if item.select_one("h2") else "Produto ML"
            preco = 299.99
            imagem_url = ""
            produto = {
                "nome": nome,
                "descricao": "Produto encontrado no Mercado Livre",
                "preco": preco,
                "imagem_url": imagem_url
            }
            cadastrar_produto(produto)
    except Exception as e:
        print(f"[Mercado Livre] Erro: {e}")

# Scraper da Amazon (simples)
def buscar_amazon():
    url = "https://www.amazon.com.br/s?k=smartphone"
    try:
        r = requests.get(url, headers=HEADERS, proxies=PROXIES, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        for item in soup.select("div.s-main-slot div.s-result-item"):
            nome = item.select_one("span.a-text-normal")
            if nome:
                nome = nome.text
                preco = 399.99
                imagem_url = ""
                produto = {
                    "nome": nome,
                    "descricao": "Produto encontrado na Amazon",
                    "preco": preco,
                    "imagem_url": imagem_url
                }
                cadastrar_produto(produto)
    except Exception as e:
        print(f"[Amazon] Erro: {e}")

# Função principal
def executar_busca():
    print(f"[{datetime.now()}] Iniciando busca de produtos...")
    buscar_shopee()
    buscar_mercado_livre()
    buscar_amazon()

# Agendamento diário às 10h
schedule.every().day.at("10:00").do(executar_busca)

# Loop de execução
print("Buscador agendado iniciado. Aguardando horário...")
while True:
    schedule.run_pending()
    time.sleep(60)
