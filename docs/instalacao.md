# Como Executar

Esta página descreve a execução local do sistema Django e da documentação MkDocs.

## Pré-requisitos

- Python 3.11 ou superior.
- Git.
- PowerShell no Windows ou shell equivalente no Linux/macOS.
- Acesso de rede se for testar autenticação externa da biblioteca da UFSM.

## Preparar a aplicação

Entre na pasta da aplicação Django:

```powershell
cd app
```

Crie o ambiente virtual fora da pasta `app`, mantendo o padrão indicado no README original:

```powershell
python -m venv ..\.venv
```

Ative o ambiente virtual:

```powershell
..\.venv\Scripts\Activate.ps1
```

Instale as dependências da aplicação:

```powershell
pip install -r requirements.txt
```

Crie o arquivo `.env` a partir do exemplo:

```powershell
Copy-Item .env.example .env
```

Execute as migrações:

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

## Variáveis de ambiente

As configurações ficam em `app/.env`.

| Variável | Finalidade | Valor de exemplo |
| --- | --- | --- |
| `SECRET_KEY` | Chave secreta do Django. Deve ser trocada em produção. | `django-insecure-dev-key-change-in-production` |
| `DEBUG` | Ativa/desativa modo de debug. | `True` |
| `ALLOWED_HOSTS` | Hosts aceitos pela aplicação. | `127.0.0.1,localhost,testserver` |
| `UFSM_LIBRARY_AUTH_URL` | Endpoint externo usado para autenticação pela biblioteca. | `https://portal.ufsm.br/biblioteca/leitor/j_security_check` |
| `UFSM_LIBRARY_AUTH_TIMEOUT` | Timeout da chamada externa em segundos. | `15` |
| `LOGIN_REDIRECT_URL` | Rota pós-login. | `/` |
| `LOGOUT_REDIRECT_URL` | Rota pós-logout. | `/login/` |

!!! warning "Segurança"
    Não use a `SECRET_KEY` de exemplo em produção. Também não mantenha `DEBUG=True` fora do ambiente de desenvolvimento.

## Executar a documentação MkDocs

Na raiz do repositório, crie e ative um ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instale a dependência da documentação dentro do ambiente virtual:

```powershell
pip install -r requirements-docs.txt
```

Inicie o servidor local do MkDocs:

```powershell
mkdocs serve
```

A documentação ficará disponível em:

```text
http://127.0.0.1:8000/
```

Se a aplicação Django já estiver usando a porta `8000`, execute o MkDocs em outra porta:

```powershell
mkdocs serve -a 127.0.0.1:8001
```

Nesse caso, acesse:

```text
http://127.0.0.1:8001/
```

## Gerar site estático

Para gerar a documentação final em HTML:

```powershell
mkdocs build
```

O resultado será criado na pasta `site/`.

