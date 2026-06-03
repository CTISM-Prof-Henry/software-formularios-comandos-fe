# Comandos FE

Sistema web Django para gestão de riscos institucionais.

## Documentação

A documentação técnica do projeto foi organizada com MkDocs na pasta `docs/`.

Para executar localmente, crie e ative um ambiente virtual na raiz do projeto:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-docs.txt
mkdocs serve
```

Por padrão, o MkDocs abre em:

```text
http://127.0.0.1:8000/
```

Se a aplicação Django já estiver rodando na porta `8000`, execute a documentação em outra porta:

```powershell
mkdocs serve -a 127.0.0.1:8001
```

Nesse caso, acesse:

```text
http://127.0.0.1:8001/
```

Para gerar o site estático:

```powershell
mkdocs build
```

## Aplicação

O código Django fica na pasta `app/`.

Execução local resumida:

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

Para mais detalhes, consulte a documentação em `docs/`.
