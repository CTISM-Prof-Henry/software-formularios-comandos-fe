# Modelo de Dados

Esta pagina resume os modelos principais da aplicacao.

## Usuario

Arquivo: `app/usuarios/models.py`

| Campo | Tipo | Observacao |
| --- | --- | --- |
| `id` | UUID | Chave primaria. |
| `unidade` | FK `Unidade` | Opcional. |
| `matricula` | `CharField` | Unica, opcional. |
| `nome` | `CharField` | Nome completo. |
| `email` | `EmailField` | Unico, opcional. |
| `perfil_acesso` | choices | `ADMIN`, `GESTAO_RISCOS` ou `ESTUDANTE`. |
| `senha_local_definida` | boolean | Indica se o usuario configurou senha local. |

## Unidade

Arquivo: `app/unidades/models.py`

| Campo | Tipo | Observacao |
| --- | --- | --- |
| `id` | UUID | Chave primaria. |
| `sigla` | `CharField` | Unica. |
| `nome` | `CharField` | Nome da unidade. |
| `tipo_unidade` | choices | Reitoria, diretoria ou coordenacao. |
| `unidade_pai` | FK para `Unidade` | Permite hierarquia entre unidades. |

## Risco

Arquivo: `app/riscos/models.py`

| Campo | Tipo | Observacao |
| --- | --- | --- |
| `id` | UUID | Chave primaria. |
| `unidade` | FK `Unidade` | Unidade relacionada ao risco. |
| `tipo_risco` | choices | Estrategico, operacional, financeiro, conformidade ou imagem. |
| `desafio` | FK `Desafio` | Desafio associado. |
| `objetivo` | FK `Objetivo` | Objetivo associado ao desafio. |
| `macroprocesso` | FK `Macroprocesso` | Macroprocesso relacionado. |
| `risco_identificado` | `TextField` | Descricao do risco. |
| `probabilidade` | choices inteiros | Escala de 1 a 5. |
| `impacto` | choices inteiros | Escala de 1 a 5. |
| `nivel_risco` | inteiro | Calculado automaticamente. |
| `eficacia_controles` | choices | Inexistente, fraca, mediana, satisfatoria ou forte. |
| `nivel_residual` | inteiro | Calculado automaticamente. |
| `resposta` | choices | Aceitar, mitigar, transferir ou evitar. |
| `acao` | choices | Preventiva, corretiva, monitoramento ou contingencia. |
| `data_inicio` | data | Inicio do plano/acao. |
| `data_fim` | data | Fim previsto. |
| `situacao` | choices | Nao iniciado, em andamento, concluido ou atrasado. |
| `criado_por_nome` | texto | Nome do usuario criador. |
| `criado_por_unidade` | FK `Unidade` | Unidade do usuario criador. |

## Calculo do nivel de risco

O nivel de risco inicial e calculado no metodo `save()`:

```python
self.nivel_risco = int(self.probabilidade) * int(self.impacto)
```

Como a escala vai de 1 a 5, o resultado possivel fica entre 1 e 25.

## Calculo do nivel residual

O nivel residual subtrai uma reducao conforme a eficacia dos controles:

| Eficacia | Reducao |
| --- | --- |
| Inexistente | 0 |
| Fraca | 1 |
| Mediana | 2 |
| Satisfatoria | 3 |
| Forte | 4 |

O resultado minimo e 1:

```python
return max(self.nivel_risco - reducao, 1)
```

## Relacionamentos principais

| Origem | Relacao | Destino |
| --- | --- | --- |
| `Usuario` | pertence a | `Unidade` |
| `Unidade` | pode possuir | subunidades |
| `Risco` | pertence a | `Unidade` |
| `Risco` | referencia | `Desafio` |
| `Risco` | referencia | `Objetivo` |
| `Risco` | referencia | `Macroprocesso` |
| `Objetivo` | pertence a | `Desafio` |

