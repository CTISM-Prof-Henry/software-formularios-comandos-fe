# Testes e Qualidade

O projeto possui configuracao para `pytest`, `pytest-django`, `coverage` e `pylint`.

## Executar testes com pytest

Entre na pasta `app`:

```powershell
cd app
```

Execute:

```powershell
python -m pytest -v
```

## Executar com coverage

```powershell
python -m coverage run -m pytest -v
python -m coverage report
python -m coverage html
```

O relatorio HTML sera gerado em:

```text
htmlcov/index.html
```

## Executar Pylint

Na raiz do repositorio, com o ambiente virtual ativo:

```powershell
python -m pylint app -f colorized
```

## Testes existentes

| Arquivo | Cobertura principal |
| --- | --- |
| `app/tests/test_usuarios.py` | CRUD/listagem de usuarios e acesso a pagina inicial. |
| `app/tests/test_unidades.py` | Modelo, formulario e CRUD de unidades. |

## Pontos de atencao nos testes

Os testes atuais fazem requisicoes para rotas administrativas sem criar um usuario autenticado com perfil adequado. Porem o middleware atual exige autenticacao e permissao para rotas protegidas.

Isso pode indicar uma destas situacoes:

1. os testes foram escritos antes da regra de login obrigatoria;
2. o middleware foi alterado e os testes nao foram atualizados;
3. a configuracao de testes deveria desabilitar ou adaptar a autenticacao.

Tecnicamente, a melhor correcao e atualizar os testes para criar usuarios autenticados com os perfis corretos, em vez de relaxar a seguranca da aplicacao.

Exemplo de estrategia recomendada:

```python
from django.contrib.auth import get_user_model

def criar_usuario_admin(client):
    user_model = get_user_model()
    user = user_model.objects.create_user(
        username="admin",
        password="senha-forte-teste",
        is_staff=True,
        is_superuser=True,
    )
    client.login(username="admin", password="senha-forte-teste")
    return user
```

## Qualidade de codigo

Boas praticas recomendadas para evoluir o projeto:

- manter views pequenas, delegando validacoes para forms e regras de dominio para services quando crescerem;
- evitar logica de negocio complexa em templates;
- adicionar testes para autenticacao, permissoes e regras de visibilidade por unidade;
- cobrir os calculos de `nivel_risco` e `nivel_residual`;
- revisar strings com encoding quebrado no codigo fonte;
- nao versionar `.env`, banco local ou arquivos gerados.

