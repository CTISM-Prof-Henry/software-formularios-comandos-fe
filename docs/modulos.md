# Módulos do Sistema

## Gestão de riscos

O app `gestao_riscos` contém a configuração central do projeto e as regras transversais:

- autenticação;
- autorização;
- middleware;
- views de login, logout, dashboard, healthcheck e atualização cadastral;
- classes base de CRUD.

Rotas principais:

| Rota | Nome | Finalidade |
| --- | --- | --- |
| `/` | `index` | Dashboard inicial. |
| `/login/` | `login` | Tela de login. |
| `/cadastro-local/` | `local-registration` | Cadastro local de usuário. |
| `/atualizar-cadastro/` | `atualizar-cadastro` | Complemento de perfil após login. |
| `/sem-permissao/` | `sem-permissao` | Página de acesso negado. |
| `/logout/` | `logout` | Encerramento de sessão. |
| `/health/` | `healthcheck` | Endpoint simples de saúde. |

## Usuários

O app `usuarios` gerencia o perfil institucional/local do usuário.

Modelo principal: `Usuario`.

Campos relevantes:

- matrícula;
- nome;
- e-mail;
- unidade;
- perfil de acesso;
- senha local definida.

Rotas:

| Rota | Nome | Permissão |
| --- | --- | --- |
| `/usuarios/` | `usuario-list` | Admin |
| `/usuarios/novo/` | `usuario-create` | Admin |
| `/usuarios/<uuid>/editar/` | `usuario-update` | Admin |
| `/usuarios/<uuid>/excluir/` | `usuario-delete` | Admin |

## Unidades

O app `unidades` representa unidades e setores da instituição.

Modelo principal: `Unidade`.

Campos relevantes:

- sigla;
- nome;
- tipo de unidade;
- unidade pai.

Rotas:

| Rota | Nome | Permissão |
| --- | --- | --- |
| `/unidades/` | `unidade-list` | Admin |
| `/unidades/novo/` | `unidade-create` | Admin |
| `/unidades/<uuid>/editar/` | `unidade-update` | Admin |
| `/unidades/<uuid>/excluir/` | `unidade-delete` | Admin |

## Riscos

O app `riscos` concentra o fluxo principal do sistema: análise e tratamento de riscos.

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
- nível de risco calculado;
- eficácia dos controles;
- nível residual calculado;
- resposta;
- ação;
- datas de início e fim;
- situação;
- usuário e unidade criadores.

Rotas:

| Rota | Nome | Permissão |
| --- | --- | --- |
| `/riscos/` | `risco-list` | Admin ou Gestão de Riscos |
| `/riscos/novo/` | `risco-create` | Admin ou Gestão de Riscos |
| `/riscos/<uuid>/editar/` | `risco-update` | Admin ou usuário autorizado pela unidade |
| `/riscos/<uuid>/excluir/` | `risco-delete` | Admin ou usuário autorizado pela unidade |
| `/riscos/<uuid>/imprimir/` | `risco-print` | Admin ou usuário autorizado pela unidade |

## Regra de visibilidade dos riscos

Na listagem de riscos:

- administradores enxergam todos os registros;
- usuários de gestão de riscos enxergam apenas riscos vinculados às unidades retornadas por `get_current_user_units()`.

Essa regra está em `RiscoListView.get_queryset()`.

