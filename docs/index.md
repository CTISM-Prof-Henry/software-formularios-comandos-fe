# Comandos FE

O **Comandos FE** é um sistema web Django para apoiar a gestão de riscos de unidades institucionais. A aplicação permite cadastrar usuários, unidades/setores e análises de risco com informações de probabilidade, impacto, controles, resposta, ação e situação.

Esta documentação foi criada para substituir o README genérico por uma referência navegável em MkDocs, com foco em instalação, arquitetura, regras de acesso, modelo de dados, testes e telas do projeto.

## Visão geral

| Item | Descrição |
| --- | --- |
| Linguagem | Python |
| Framework | Django 5 |
| Banco de dados local | SQLite |
| Interface | Templates Django, CSS estático e Bootstrap via template |
| Autenticação | Login local e autenticação externa pela biblioteca da UFSM |
| Testes | pytest, pytest-django e coverage |
| Qualidade | pylint configurado no repositório |

## Principais funcionalidades

- Login via sistema local ou via credenciais da biblioteca da UFSM.
- Cadastro local de usuário.
- Atualização obrigatória de cadastro quando o perfil local está incompleto.
- Controle de permissão por perfil: administrador, gestão de riscos e estudante sem acesso.
- CRUD administrativo de usuários.
- CRUD administrativo de unidades.
- CRUD de análises de riscos.
- Filtragem de riscos por unidade para usuários de gestão de riscos.
- Impressão/visualização detalhada de uma análise de risco.
- Healthcheck em `/health/`.

## Estrutura resumida

```text
software-formularios-comandos-fe/
+-- app/
|   +-- gestao_riscos/     # configuração Django, autenticação, middleware e permissões
|   +-- riscos/            # análises de risco, formulários, views e regras de visibilidade
|   +-- unidades/          # unidades/setores
|   +-- usuarios/          # perfis locais de usuário
|   +-- templates/         # templates HTML
|   +-- static/            # CSS e assets
|   +-- tests/             # testes automatizados
|   +-- manage.py
+-- docs/                  # documentação MkDocs e imagens de design
+-- mkdocs.yml
+-- requirements-docs.txt
```

## Leitura recomendada

1. Leia [Como Executar](instalacao.md) para preparar o ambiente local.
2. Leia [Arquitetura](arquitetura.md) para entender a organização do projeto.
3. Leia [Autenticação e Permissões](autenticacao-permissoes.md) antes de alterar views ou middlewares.
4. Leia [Testes e Qualidade](testes-qualidade.md) antes de validar mudanças.

