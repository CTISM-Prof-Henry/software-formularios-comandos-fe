# Comandos FE

## Como Rodar

```powershell
git clone https://github.com/Brunofcrosa/comandos-fe.git
cd comandos-fe
```

Crie e ative o ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instale as dependencias:

```powershell
pip install -r requirements.txt
```
Crie ou atualize o banco SQLite:
```powershell
python manage.py migrate
```

Inicie o servidor:

```powershell
python manage.py runserver
```

Depois acesse:

- sistema: `http://127.0.0.1:8000/`

## Testes

```powershell
python manage.py test
```

## pytest
- python -m coverage run -m pytest -v
- python -m coverage report
- python -m coverage html
- htmlcov/index.html no seu navegador.
