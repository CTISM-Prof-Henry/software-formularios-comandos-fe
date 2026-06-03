# Autenticacao e Permissoes

O sistema combina autenticacao local do Django com um backend externo que valida credenciais contra o endpoint da biblioteca da UFSM.

## Fontes de autenticacao

| Fonte | Como funciona |
| --- | --- |
| Sistema local | Usa usuario e senha armazenados no modelo padrao de autenticacao do Django. |
| Biblioteca UFSM | Envia `j_username` e `j_password` ao endpoint configurado em `UFSM_LIBRARY_AUTH_URL`. |

O backend externo esta em `gestao_riscos/auth.py`, na classe `LibraryAuthenticationBackend`.

## Login

A view `login_page` recebe:

- `auth_source`: define se o login e local ou UFSM.
- `matricula`: usada como `username`.
- `senha`: senha informada pelo usuario.
- `next`: URL segura para redirecionamento apos login.

O projeto valida o parametro `next` com `url_has_allowed_host_and_scheme`, evitando redirecionamento aberto para dominios externos.

## Cadastro local

A view `local_registration` usa `CadastroLocalForm`. O formulario:

- exige matricula, nome e e-mail;
- valida duplicidade de matricula e e-mail em `Usuario` e no modelo de usuario do Django;
- cria o perfil local `Usuario`;
- cria o usuario de autenticacao do Django;
- salva senha local com `set_password`.

## Atualizacao de cadastro

Quando o usuario autentica pela UFSM e ainda nao possui perfil local completo, o middleware redireciona para `atualizar-cadastro/`.

O formulario `AtualizarCadastroForm` vincula:

- unidade/setor;
- senha local;
- confirmacao de senha;
- matricula obtida do usuario autenticado.

## Perfis de acesso

O modelo `Usuario` define os perfis:

| Perfil | Valor | Acesso esperado |
| --- | --- | --- |
| Administrador | `ADMIN` | Acesso administrativo completo. |
| Gestao de Riscos | `GESTAO_RISCOS` | Acesso ao modulo de riscos conforme unidade. |
| Sem acesso | `ESTUDANTE` | Usuario autenticado sem permissao para o modulo. |

## Regras de autorizacao

As regras estao em `gestao_riscos/permissions.py`.

| Funcao/classe | Responsabilidade |
| --- | --- |
| `is_admin` | Verifica se o usuario e administrador. |
| `is_risk_manager` | Verifica se o usuario tem perfil de gestao de riscos e nao e admin. |
| `can_access_risk_module` | Permite acesso ao modulo para admin ou gestao de riscos. |
| `AdminRequiredMixin` | Restringe views administrativas. |
| `RiskModuleRequiredMixin` | Restringe views do modulo de riscos. |

## Middleware

O `LoginRequiredMiddleware` aplica tres verificacoes principais:

1. Se a rota exige usuario autenticado.
2. Se o usuario precisa atualizar o cadastro.
3. Se o usuario possui permissao para acessar a rota.

Rotas publicas:

- `/login/`
- `/cadastro-local/`
- `/health/`
- `/atualizar-cadastro/` em contexto de atualizacao
- `/logout/`
- arquivos estaticos
- `/admin/`

!!! note "Ponto de atencao"
    O admin do Django foi tratado como rota publica no middleware. Isso nao remove a autenticacao do admin, pois o proprio Django Admin exige login, mas e importante entender que o middleware customizado nao bloqueia essa area.

