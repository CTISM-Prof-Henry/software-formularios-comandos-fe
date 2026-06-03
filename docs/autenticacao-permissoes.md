# Autenticação e Permissões

O sistema combina autenticação local do Django com um backend externo que valida credenciais contra o endpoint da biblioteca da UFSM.

## Fontes de autenticação

| Fonte | Como funciona |
| --- | --- |
| Sistema local | Usa usuário e senha armazenados no modelo padrão de autenticação do Django. |
| Biblioteca UFSM | Envia `j_username` e `j_password` ao endpoint configurado em `UFSM_LIBRARY_AUTH_URL`. |

O backend externo está em `gestao_riscos/auth.py`, na classe `LibraryAuthenticationBackend`.

## Login

A view `login_page` recebe:

- `auth_source`: define se o login é local ou UFSM.
- `matricula`: usada como `username`.
- `senha`: senha informada pelo usuário.
- `next`: URL segura para redirecionamento após login.

O projeto valida o parâmetro `next` com `url_has_allowed_host_and_scheme`, evitando redirecionamento aberto para domínios externos.

## Cadastro local

A view `local_registration` usa `CadastroLocalForm`. O formulário:

- exige matrícula, nome e e-mail;
- valida duplicidade de matrícula e e-mail em `Usuario` e no modelo de usuário do Django;
- cria o perfil local `Usuario`;
- cria o usuário de autenticação do Django;
- salva senha local com `set_password`.

## Atualização de cadastro

Quando o usuário autentica pela UFSM e ainda não possui perfil local completo, o middleware redireciona para `atualizar-cadastro/`.

O formulário `AtualizarCadastroForm` vincula:

- unidade/setor;
- senha local;
- confirmação de senha;
- matrícula obtida do usuário autenticado.

## Perfis de acesso

O modelo `Usuario` define os perfis:

| Perfil | Valor | Acesso esperado |
| --- | --- | --- |
| Administrador | `ADMIN` | Acesso administrativo completo. |
| Gestão de Riscos | `GESTAO_RISCOS` | Acesso ao módulo de riscos conforme unidade. |
| Sem acesso | `ESTUDANTE` | Usuário autenticado sem permissão para o módulo. |

## Regras de autorização

As regras estão em `gestao_riscos/permissions.py`.

| Função/classe | Responsabilidade |
| --- | --- |
| `is_admin` | Verifica se o usuário é administrador. |
| `is_risk_manager` | Verifica se o usuário tem perfil de gestão de riscos e não é admin. |
| `can_access_risk_module` | Permite acesso ao módulo para admin ou gestão de riscos. |
| `AdminRequiredMixin` | Restringe views administrativas. |
| `RiskModuleRequiredMixin` | Restringe views do módulo de riscos. |

## Middleware

O `LoginRequiredMiddleware` aplica três verificações principais:

1. Se a rota exige usuário autenticado.
2. Se o usuário precisa atualizar o cadastro.
3. Se o usuário possui permissão para acessar a rota.

Rotas públicas:

- `/login/`
- `/cadastro-local/`
- `/health/`
- `/atualizar-cadastro/` em contexto de atualização
- `/logout/`
- arquivos estáticos
- `/admin/`

!!! note "Ponto de atenção"
    O admin do Django foi tratado como rota pública no middleware. Isso não remove a autenticação do admin, pois o próprio Django Admin exige login, mas é importante entender que o middleware customizado não bloqueia essa área.

