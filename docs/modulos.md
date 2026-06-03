# Modulos do Sistema

## Gestao de riscos

O app `gestao_riscos` contem a configuracao central do projeto e as regras transversais:

- autenticacao;
- autorizacao;
- middleware;
- views de login, logout, dashboard, healthcheck e atualizacao cadastral;
- classes base de CRUD.

Rotas principais:

| Rota | Nome | Finalidade |
| --- | --- | --- |
| `/` | `index` | Dashboard inicial. |
| `/login/` | `login` | Tela de login. |
| `/cadastro-local/` | `local-registration` | Cadastro local de usuario. |
| `/atualizar-cadastro/` | `atualizar-cadastro` | Complemento de perfil apos login. |
| `/sem-permissao/` | `sem-permissao` | Pagina de acesso negado. |
| `/logout/` | `logout` | Encerramento de sessao. |
| `/health/` | `healthcheck` | Endpoint simples de saude. |

## Usuarios

O app `usuarios` gerencia o perfil institucional/local do usuario.

Modelo principal: `Usuario`.

Campos relevantes:

- `matricula`
- `nome`
- `email`
- `unidade`
- `perfil_acesso`
- `senha_local_definida`

Rotas:

| Rota | Nome | Permissao |
| --- | --- | --- |
| `/usuarios/` | `usuario-list` | Admin |
| `/usuarios/novo/` | `usuario-create` | Admin |
| `/usuarios/<uuid>/editar/` | `usuario-update` | Admin |
| `/usuarios/<uuid>/excluir/` | `usuario-delete` | Admin |

## Unidades

O app `unidades` representa unidades e setores da instituicao.

Modelo principal: `Unidade`.

Campos relevantes:

- `sigla`
- `nome`
- `tipo_unidade`
- `unidade_pai`

Rotas:

| Rota | Nome | Permissao |
| --- | --- | --- |
| `/unidades/` | `unidade-list` | Admin |
| `/unidades/novo/` | `unidade-create` | Admin |
| `/unidades/<uuid>/editar/` | `unidade-update` | Admin |
| `/unidades/<uuid>/excluir/` | `unidade-delete` | Admin |

## Riscos

O app `riscos` concentra o fluxo principal do sistema: analise e tratamento de riscos.

Modelo principal: `Risco`.

Campos relevantes:

- unidade;
- tipo de risco;
- desafio;
- objetivo;
- macroprocesso;
- risco identificado;
- probabilidade;
- impacto;
- nivel de risco calculado;
- eficacia dos controles;
- nivel residual calculado;
- resposta;
- acao;
- datas de inicio e fim;
- situacao;
- usuario e unidade criadores.

Rotas:

| Rota | Nome | Permissao |
| --- | --- | --- |
| `/riscos/` | `risco-list` | Admin ou Gestao de Riscos |
| `/riscos/novo/` | `risco-create` | Admin ou Gestao de Riscos |
| `/riscos/<uuid>/editar/` | `risco-update` | Admin ou usuario autorizado pela unidade |
| `/riscos/<uuid>/excluir/` | `risco-delete` | Admin ou usuario autorizado pela unidade |
| `/riscos/<uuid>/imprimir/` | `risco-print` | Admin ou usuario autorizado pela unidade |

## Regra de visibilidade dos riscos

Na listagem de riscos:

- administradores enxergam todos os registros;
- usuarios de gestao de riscos enxergam apenas riscos vinculados as unidades retornadas por `get_current_user_units()`.

Essa regra esta em `RiscoListView.get_queryset()`.

