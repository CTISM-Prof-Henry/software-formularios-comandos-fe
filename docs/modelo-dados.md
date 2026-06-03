# Modelo de Dados

Esta página resume os modelos principais da aplicação.

## Usuário

Arquivo: `app/usuarios/models.py`

| Campo | Tipo | Observação |
| --- | --- | --- |
| `id` | UUID | Chave primária. |
| `unidade` | FK `Unidade` | Opcional. |
| `matricula` | `CharField` | Única, opcional. |
| `nome` | `CharField` | Nome completo. |
| `email` | `EmailField` | Único, opcional. |
| `perfil_acesso` | choices | `ADMIN`, `GESTAO_RISCOS` ou `ESTUDANTE`. |
| `senha_local_definida` | boolean | Indica se o usuário configurou senha local. |

## Unidade

Arquivo: `app/unidades/models.py`

| Campo | Tipo | Observação |
| --- | --- | --- |
| `id` | UUID | Chave primária. |
| `sigla` | `CharField` | Única. |
| `nome` | `CharField` | Nome da unidade. |
| `tipo_unidade` | choices | Reitoria, diretoria ou coordenação. |
| `unidade_pai` | FK para `Unidade` | Permite hierarquia entre unidades. |

## Risco

Arquivo: `app/riscos/models.py`

| Campo | Tipo | Observação |
| --- | --- | --- |
| `id` | UUID | Chave primária. |
| `unidade` | FK `Unidade` | Unidade relacionada ao risco. |
| `tipo_risco` | choices | Estratégico, operacional, financeiro, conformidade ou imagem. |
| `desafio` | FK `Desafio` | Desafio associado. |
| `objetivo` | FK `Objetivo` | Objetivo associado ao desafio. |
| `macroprocesso` | FK `Macroprocesso` | Macroprocesso relacionado. |
| `risco_identificado` | `TextField` | Descrição do risco. |
| `probabilidade` | choices inteiros | Escala de 1 a 5. |
| `impacto` | choices inteiros | Escala de 1 a 5. |
| `nivel_risco` | inteiro | Calculado automaticamente. |
| `eficacia_controles` | choices | Inexistente, fraca, mediana, satisfatória ou forte. |
| `nivel_residual` | inteiro | Calculado automaticamente. |
| `resposta` | choices | Aceitar, mitigar, transferir ou evitar. |
| `acao` | choices | Preventiva, corretiva, monitoramento ou contingência. |
| `data_inicio` | data | Início do plano/ação. |
| `data_fim` | data | Fim previsto. |
| `situacao` | choices | Não iniciado, em andamento, concluído ou atrasado. |
| `criado_por_nome` | texto | Nome do usuário criador. |
| `criado_por_unidade` | FK `Unidade` | Unidade do usuário criador. |

## Cálculo do nível de risco

O nível de risco inicial é calculado no método `save()`:

```python
self.nivel_risco = int(self.probabilidade) * int(self.impacto)
```

Como a escala vai de 1 a 5, o resultado possível fica entre 1 e 25.

## Cálculo do nível residual

O nível residual subtrai uma redução conforme a eficácia dos controles:

| Eficácia | Redução |
| --- | --- |
| Inexistente | 0 |
| Fraca | 1 |
| Mediana | 2 |
| Satisfatória | 3 |
| Forte | 4 |

O resultado mínimo é 1:

```python
return max(self.nivel_risco - reducao, 1)
```

## Relacionamentos principais

| Origem | Relação | Destino |
| --- | --- | --- |
| `Usuario` | pertence a | `Unidade` |
| `Unidade` | pode possuir | subunidades |
| `Risco` | pertence a | `Unidade` |
| `Risco` | referencia | `Desafio` |
| `Risco` | referencia | `Objetivo` |
| `Risco` | referencia | `Macroprocesso` |
| `Objetivo` | pertence a | `Desafio` |

