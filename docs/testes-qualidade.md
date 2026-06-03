# Testes e Qualidade

O projeto possui configuração para `pytest`, `pytest-django`, `coverage` e `pylint`.

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

O relatório HTML será gerado em:

```text
htmlcov/index.html
```

## Executar Pylint

Na raiz do repositório, com o ambiente virtual ativo:

```powershell
python -m pylint app -f colorized
```

## Testes existentes

| Arquivo | Cobertura principal |
| --- | --- |
| `app/tests/test_usuarios.py` | CRUD/listagem de usuários e acesso à página inicial. |
| `app/tests/test_unidades.py` | Modelo, formulário e CRUD de unidades. |

## Pontos de atenção nos testes

Os testes atuais fazem requisições para rotas administrativas sem criar um usuário autenticado com perfil adequado. Porém o middleware atual exige autenticação e permissão para rotas protegidas.

Isso pode indicar uma destas situações:

1. os testes foram escritos antes da regra de login obrigatória;
2. o middleware foi alterado e os testes não foram atualizados;
3. a configuração de testes deveria desabilitar ou adaptar a autenticação.

Tecnicamente, a melhor correção é atualizar os testes para criar usuários autenticados com os perfis corretos, em vez de relaxar a segurança da aplicação.

Exemplo de estratégia recomendada:

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

## Qualidade de código

Boas práticas recomendadas para evoluir o projeto:

- manter views pequenas, delegando validações para forms e regras de domínio para services quando crescerem;
- evitar lógica de negócio complexa em templates;
- adicionar testes para autenticação, permissões e regras de visibilidade por unidade;
- cobrir os cálculos de `nivel_risco` e `nivel_residual`;
- revisar strings com encoding quebrado no código fonte;
- não versionar `.env`, banco local ou arquivos gerados.

