import urllib.parse
import urllib.request

URL = "http://localhost:8000/api/v1/auth/login"

form_data = {
    'username': 'ana.silva@email.com',
    'password': 'senha123'
}

data = urllib.parse.urlencode(form_data).encode()
req = urllib.request.Request(URL, data=data, method='POST')
req.add_header('Content-Type', 'application/x-www-form-urlencoded')

try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        body = resp.read().decode()
        print('Resposta do login:')
        print(body)
except Exception as e:
    print('Erro ao testar login:', e)
