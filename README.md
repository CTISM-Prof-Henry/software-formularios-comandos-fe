# Comandos FE

Sistema web Django para gestao de riscos institucionais.

## Documentacao

A documentacao tecnica do projeto foi organizada com MkDocs na pasta `docs/`.

Para executar localmente:

```powershell
pip install -r requirements-docs.txt
mkdocs serve
```

Por padrao, o MkDocs abre em:

```text
http://127.0.0.1:8000/
```

Se a aplicacao Django ja estiver rodando na porta `8000`, execute a documentacao em outra porta:

```powershell
mkdocs serve -a 127.0.0.1:8001
```

Nesse caso, acesse:

```text
http://127.0.0.1:8001/
```

Para gerar o site estatico:

```powershell
mkdocs build
```

## Aplicacao

O codigo Django fica na pasta `app/`.

Execucao local resumida:

```powershell
cd app
python -m venv ..\.venv
..\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py migrate
python manage.py runserver
```

Acesse:

```text
http://127.0.0.1:8000/
```

## Testes

```powershell
cd app
python -m pytest -v
```

Com coverage:

```powershell
python -m coverage run -m pytest -v
python -m coverage report
python -m coverage html
```

## Qualidade

```powershell
python -m pylint app -f colorized
```

Para mais detalhes, consulte a documentacao em `docs/`.
