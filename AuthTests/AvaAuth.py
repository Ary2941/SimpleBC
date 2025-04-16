import requests
from bs4 import BeautifulSoup

# CONFIGURAÇÕES DO USUÁRIO
cpf = input("cpf:")
senha = input("senha:")

# URL base
login_url = "https://sistemas.ufal.br/cas/login"
service_url = "https://ava.ufal.br/login/index.php"
perfil_url = "https://sistemas.ufal.br/perfil/"

# 1. Faz o GET da página de login
session = requests.Session()
response = session.get(login_url, params={"service": service_url})

soup = BeautifulSoup(response.text, "html.parser")

# 2. Extrai os campos hidden 'lt' e 'execution'
lt = soup.find("input", {"name": "lt"})["value"]
execution = soup.find("input", {"name": "execution"})["value"]

print(f"[+] lt = {lt}")
print(f"[+] execution = {execution}")

# 3. Prepara os dados para o POST
payload = {
    "username": cpf,
    "password": senha,
    "lt": lt,
    "execution": execution,
    "_eventId": "submit",
}

# 4. Envia o POST com os dados de login
post_response = session.post(login_url, params={"service": service_url}, data=payload, allow_redirects=False)

# 4. Acessa a página do perfil já logado
perfil_response = session.get(perfil_url)
perfil_html = BeautifulSoup(perfil_response.text, "html.parser")

# 5. Extrai os vínculos ativos
vinculos = []
vinculo_tag = perfil_html.find("strong", string="Vínculos ativos")
if vinculo_tag:
    ul_tag = vinculo_tag.find_next("ul")
    for li in ul_tag.find_all("li"):
        vinculos.append(li.get_text(strip=True))

# 6. Mostra os vínculos encontrados
if vinculos:
    print("[✅] Vínculos ativos encontrados:")
    for v in vinculos:
        print(f" - {v}")
else:
    print("[❌] Nenhum vínculo encontrado ou login falhou.")

# 7. Faz logout
logout_page = BeautifulSoup(perfil_response.text, "html.parser")
csrf_token_input = logout_page.find("input", {"name": "_csrf"})

if csrf_token_input:
    csrf_token = csrf_token_input["value"]
    logout_response = session.post("https://sistemas.ufal.br/perfil/logout", data={"_csrf": csrf_token})
    if logout_response.status_code == 200:
        print("[🚪] Logout realizado com sucesso.")
    else:
        print("[⚠️] Erro ao tentar fazer logout.")
else:
    print("[❌] Token CSRF para logout não encontrado.")