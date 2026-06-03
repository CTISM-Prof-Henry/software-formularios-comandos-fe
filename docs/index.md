# Comandos FE

O **Comandos FE** e um sistema web Django para apoiar a gestao de riscos de unidades institucionais. A aplicacao permite cadastrar usuarios, unidades/setores e analises de risco com informacoes de probabilidade, impacto, controles, resposta, acao e situacao.

Esta documentacao foi criada para substituir o README generico por uma referencia navegavel em MkDocs, com foco em instalacao, arquitetura, regras de acesso, modelo de dados, testes e telas do projeto.

## Visao geral

| Item | Descricao |
| --- | --- |
| Linguagem | Python |
| Framework | Django 5 |
| Banco de dados local | SQLite |
| Interface | Templates Django, CSS estatico e Bootstrap via template |
| Autenticacao | Login local e autenticacao externa pela biblioteca da UFSM |
| Testes | pytest, pytest-django e coverage |
| Qualidade | pylint configurado no repositorio |

## Principais funcionalidades

- Login via sistema local ou via credenciais da biblioteca da UFSM.
- Cadastro local de usuario.
- Atualizacao obrigatoria de cadastro quando o perfil local esta incompleto.
- Controle de permissao por perfil: administrador, gestao de riscos e estudante sem acesso.
- CRUD administrativo de usuarios.
- CRUD administrativo de unidades.
- CRUD de analises de riscos.
- Filtragem de riscos por unidade para usuarios de gestao de riscos.
- Impressao/visualizacao detalhada de uma analise de risco.
- Healthcheck em `/health/`.

## Estrutura resumida

```text
software-formularios-comandos-fe/
├── app/
│   ├── gestao_riscos/     # configuracao Django, autenticacao, middleware e permissoes
│   ├── riscos/            # analises de risco, formularios, views e regras de visibilidade
│   ├── unidades/          # unidades/setores
│   ├── usuarios/          # perfis locais de usuario
│   ├── templates/         # templates HTML
│   ├── static/            # CSS e assets
│   ├── tests/             # testes automatizados
│   └── manage.py
├── docs/                  # documentacao MkDocs e imagens de design
├── mkdocs.yml
└── requirements-docs.txt
```

## Leitura recomendada

1. Leia [Como Executar](instalacao.md) para preparar o ambiente local.
2. Leia [Arquitetura](arquitetura.md) para entender a organizacao do projeto.
3. Leia [Autenticacao e Permissoes](autenticacao-permissoes.md) antes de alterar views ou middlewares.
4. Leia [Testes e Qualidade](testes-qualidade.md) antes de validar mudancas.

