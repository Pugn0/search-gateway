import requests
from bs4 import BeautifulSoup
import json
import os

def load_gateways():
    try:
        with open('gates.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ Erro: Arquivo gates.json não encontrado!")
        exit(1)
    except json.JSONDecodeError:
        print("❌ Erro: Formato inválido no arquivo gates.json!")
        exit(1)

def check_gate(url, GATEWAYS):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)

        soup = BeautifulSoup(response.text, 'html.parser')
        html = response.text.lower()

        result = {
            "URL": url,
            "Status Code": response.status_code,
            "Protecoes": {
                "Cloudflare": 'cloudflare' in response.headers.get('Server', '').lower(),
                "reCAPTCHA": {
                    "detectado": any(keyword in html for keyword in ["recaptcha", "g-recaptcha"]),
                    "versao": None,
                    "chave": None,
                    "host": None
                }
            },
            "Gateways": []
        }

        # Detecta gateways
        encontrados = []
        for chave in GATEWAYS:
            if chave in html:
                encontrados.append(GATEWAYS[chave])
        result["Gateways"] = list(set(encontrados))

        # Detecta reCAPTCHA
        if result["Protecoes"]["reCAPTCHA"]["detectado"]:
            scripts = soup.find_all("script")
            for script in scripts:
                if script.has_attr("src") and "recaptcha" in script["src"]:
                    src = script["src"]
                    result["Protecoes"]["reCAPTCHA"]["host"] = src.split("/")[2] if "://" in src else "google.com"
                    if "v2" in src:
                        result["Protecoes"]["reCAPTCHA"]["versao"] = "v2"
                    elif "enterprise.js" in src or "v3.js" in src:
                        result["Protecoes"]["reCAPTCHA"]["versao"] = "v3"
            site_key = soup.find(attrs={"data-sitekey": True})
            if site_key:
                result["Protecoes"]["reCAPTCHA"]["chave"] = site_key["data-sitekey"]

        return result

    except Exception as e:
        return {"Erro": str(e)}

def exibir_resultado(result):
    if "Erro" in result:
        print(f"❌ Erro ao verificar o site: {result['Erro']}")
        return

    print("\n🔎 VARREDURA REALIZADA")
    print("━━━━━━━━━━━━━━━━━━━━━━")
    print(f"🌐 URL: {result['URL']}")
    print(f"📡 STATUS HTTP: {result['Status Code']}")

    print("\n🔐 PROTEÇÕES ENCONTRADAS:")
    protecoes = result.get("Protecoes", {})
    protecao_exibida = False

    if protecoes.get("Cloudflare"):
        print("🛡️ Cloudflare")
        protecao_exibida = True

    recaptcha = protecoes.get("reCAPTCHA")
    if recaptcha and recaptcha.get("detectado"):
        versao = recaptcha.get("versao", "desconhecida")
        chave = recaptcha.get("chave", "não encontrada")
        host = recaptcha.get("host", "desconhecido")
        print(f"🧠 Google reCAPTCHA")
        print(f"   ├─ Versão: {versao}")
        print(f"   ├─ Chave: {chave}")
        print(f"   └─ Host: {host}")
        protecao_exibida = True

    if not protecao_exibida:
        print("❌ Nenhuma proteção detectada.")

    print("\n💳 GATEWAYS ENCONTRADOS:")
    gateways = result.get("Gateways", [])
    if gateways:
        for g in gateways:
            print(f"✅ {g}")
    else:
        print("❌ Nenhum gateway detectado.")

def analisar_url_manual():
    url = input("🔍 Digite a URL do site que deseja analisar: ").strip()
    if not url.startswith("http"):
        url = "https://" + url
    return url

def analisar_sites_txt():
    if not os.path.exists('sites.txt'):
        print("❌ Erro: Arquivo sites.txt não encontrado!")
        return []
    
    with open('sites.txt', 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def menu():
    while True:
        print("\n🔧 MENU PRINCIPAL")
        print("━━━━━━━━━━━━━━━━")
        print("1. Analisar URL manual")
        print("2. Analisar URLs do sites.txt")
        print("3. Sair")
        
        opcao = input("\nEscolha uma opção (1-3): ").strip()
        
        if opcao == "1":
            url = analisar_url_manual()
            GATEWAYS = load_gateways()
            resultado = check_gate(url, GATEWAYS)
            exibir_resultado(resultado)
        
        elif opcao == "2":
            urls = analisar_sites_txt()
            if not urls:
                continue
                
            GATEWAYS = load_gateways()
            print(f"\n📋 Analisando {len(urls)} URLs do sites.txt...")
            
            for i, url in enumerate(urls, 1):
                print(f"\n[{i}/{len(urls)}] Analisando: {url}")
                resultado = check_gate(url, GATEWAYS)
                exibir_resultado(resultado)
                print("\n" + "━" * 50)
        
        elif opcao == "3":
            print("\n👋 Encerrando programa...")
            break
        
        else:
            print("\n❌ Opção inválida! Tente novamente.")

if __name__ == "__main__":
    menu()
