# Como Executar

Esta pagina descreve a execucao local do sistema Django e da documentacao MkDocs.

## Pre-requisitos

- Python 3.11 ou superior.
- Git.
- PowerShell no Windows ou shell equivalente no Linux/macOS.
- Acesso de rede se for testar autenticacao externa da biblioteca da UFSM.

## Preparar a aplicacao

Entre na pasta da aplicacao Django:

```powershell
cd app
```

Crie o ambiente virtual fora da pasta `app`, mantendo o padrao indicado no README original:

```powershell
python -m venv ..\.venv
```

Ative o ambiente virtual:

```powershell
..\.venv\Scripts\Activate.ps1
```

Instale as dependencias da aplicacao:

```powershell
pip install -r requirements.txt
```

Crie o arquivo `.env` a partir do exemplo:

```powershell
Copy-Item .env.example .env
```

Execute as migracoes:

```powershell
python manage.py migrate
```

Suba o servidor de desenvolvimento:

```powershell
python manage.py runserver
```

Acesse:

```text
http://127.0.0.1:8000/
```

## Variaveis de ambiente

As configuracoes ficam em `app/.env`.

| Variavel | Finalidade | Valor de exemplo |
| --- | --- | --- |
| `SECRET_KEY` | Chave secreta do Django. Deve ser trocada em producao. | `django-insecure-dev-key-change-in-production` |
| `DEBUG` | Ativa/desativa modo de debug. | `True` |
| `ALLOWED_HOSTS` | Hosts aceitos pela aplicacao. | `127.0.0.1,localhost,testserver` |
| `UFSM_LIBRARY_AUTH_URL` | Endpoint externo usado para autenticacao pela biblioteca. | `https://portal.ufsm.br/biblioteca/leitor/j_security_check` |
| `UFSM_LIBRARY_AUTH_TIMEOUT` | Timeout da chamada externa em segundos. | `15` |
| `LOGIN_REDIRECT_URL` | Rota pos-login. | `/` |
| `LOGOUT_REDIRECT_URL` | Rota pos-logout. | `/login/` |

!!! warning "Seguranca"
    Nao use a `SECRET_KEY` de exemplo em producao. Tambem nao mantenha `DEBUG=True` fora do ambiente de desenvolvimento.

## Executar a documentacao MkDocs

Na raiz do repositorio, instale a dependencia da documentacao:

```powershell
pip install -r requirements-docs.txt
```

Inicie o servidor local do MkDocs:

```powershell
mkdocs serve
```

A documentacao ficara disponivel em:

```text
http://127.0.0.1:8000/
```

Se a aplicacao Django ja estiver usando a porta `8000`, execute o MkDocs em outra porta:

```powershell
mkdocs serve -a 127.0.0.1:8001
```

## Gerar site estatico

Para gerar a documentacao final em HTML:

```powershell
mkdocs build
```

O resultado sera criado na pasta `site/`.

