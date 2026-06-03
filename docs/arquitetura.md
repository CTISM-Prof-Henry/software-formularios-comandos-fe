# Arquitetura

O projeto segue uma arquitetura Django tradicional, organizada em apps por dominio. A raiz funcional da aplicacao esta em `app/`.

## Componentes principais

| Caminho | Responsabilidade |
| --- | --- |
| `app/manage.py` | Entrada de comandos administrativos do Django. |
| `app/gestao_riscos/settings.py` | Configuracao do projeto: apps, middleware, banco, templates, static files e autenticacao. |
| `app/gestao_riscos/urls.py` | Roteamento principal. |
| `app/gestao_riscos/auth.py` | Backend de autenticacao externa da biblioteca da UFSM. |
| `app/gestao_riscos/middleware.py` | Exigencia de login, atualizacao de perfil e permissao. |
| `app/gestao_riscos/permissions.py` | Funcoes e mixins de autorizacao. |
| `app/gestao_riscos/crud.py` | Views genericas reutilizaveis para CRUD. |
| `app/usuarios/` | Perfil local de usuarios e formularios de cadastro. |
| `app/unidades/` | Cadastro de unidades e relacionamento hierarquico. |
| `app/riscos/` | Cadastro, listagem, edicao, exclusao e impressao de analises de risco. |
| `app/templates/` | Templates HTML compartilhados e especificos. |
| `app/static/` | CSS e imagens. |
| `app/tests/` | Testes automatizados. |

## Fluxo de requisicao

1. O usuario acessa uma URL definida em `gestao_riscos/urls.py`.
2. O `LoginRequiredMiddleware` associa contexto do usuario atual a requisicao.
3. O middleware verifica se a rota exige login, perfil atualizado e permissao.
4. A view correspondente processa a requisicao.
5. Templates em `app/templates/` renderizam a resposta.

## Padrao de CRUD

O arquivo `gestao_riscos/crud.py` centraliza classes base para listagem, formulario e exclusao:

- `CrudListView`
- `CrudCreateView`
- `CrudUpdateView`
- `CrudDeleteView`

Esse padrao reduz duplicacao nas views de usuarios, unidades e riscos. Ao criar um novo CRUD, a abordagem recomendada e reaproveitar essas classes, definindo apenas `model`, `form_class`, `success_url`, titulos e nomes de rotas.

## Banco de dados

Em desenvolvimento, o projeto usa SQLite:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
```

Para producao, o ideal e migrar para um banco gerenciado, como PostgreSQL, e configurar credenciais via variaveis de ambiente.

## Templates e arquivos estaticos

Os templates ficam em `app/templates/` e os arquivos estaticos em `app/static/`.

O `settings.py` configura:

```python
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
```

Em producao, sera necessario executar `collectstatic` e servir estaticos com uma estrategia adequada, como WhiteNoise, Nginx ou storage externo.

