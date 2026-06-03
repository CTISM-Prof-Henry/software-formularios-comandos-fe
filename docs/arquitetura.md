# Arquitetura

O projeto segue uma arquitetura Django tradicional, organizada em apps por domínio. A raiz funcional da aplicação está em `app/`.

## Componentes principais

| Caminho | Responsabilidade |
| --- | --- |
| `app/manage.py` | Entrada de comandos administrativos do Django. |
| `app/gestao_riscos/settings.py` | Configuração do projeto: apps, middleware, banco, templates, static files e autenticação. |
| `app/gestao_riscos/urls.py` | Roteamento principal. |
| `app/gestao_riscos/auth.py` | Backend de autenticação externa da biblioteca da UFSM. |
| `app/gestao_riscos/middleware.py` | Exigência de login, atualização de perfil e permissão. |
| `app/gestao_riscos/permissions.py` | Funções e mixins de autorização. |
| `app/gestao_riscos/crud.py` | Views genéricas reutilizáveis para CRUD. |
| `app/usuarios/` | Perfil local de usuários e formulários de cadastro. |
| `app/unidades/` | Cadastro de unidades e relacionamento hierárquico. |
| `app/riscos/` | Cadastro, listagem, edição, exclusão e impressão de análises de risco. |
| `app/templates/` | Templates HTML compartilhados e específicos. |
| `app/static/` | CSS e imagens. |
| `app/tests/` | Testes automatizados. |

## Fluxo de requisição

1. O usuário acessa uma URL definida em `gestao_riscos/urls.py`.
2. O `LoginRequiredMiddleware` associa contexto do usuário atual à requisição.
3. O middleware verifica se a rota exige login, perfil atualizado e permissão.
4. A view correspondente processa a requisição.
5. Templates em `app/templates/` renderizam a resposta.

## Padrão de CRUD

O arquivo `gestao_riscos/crud.py` centraliza classes base para listagem, formulário e exclusão:

- `CrudListView`
- `CrudCreateView`
- `CrudUpdateView`
- `CrudDeleteView`

Esse padrão reduz duplicação nas views de usuários, unidades e riscos. Ao criar um novo CRUD, a abordagem recomendada é reaproveitar essas classes, definindo apenas `model`, `form_class`, `success_url`, títulos e nomes de rotas.

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

Para produção, o ideal é migrar para um banco gerenciado, como PostgreSQL, e configurar credenciais via variáveis de ambiente.

## Templates e arquivos estáticos

Os templates ficam em `app/templates/` e os arquivos estáticos em `app/static/`.

O `settings.py` configura:

```python
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
```

Em produção, será necessário executar `collectstatic` e servir estáticos com uma estratégia adequada, como WhiteNoise, Nginx ou storage externo.

