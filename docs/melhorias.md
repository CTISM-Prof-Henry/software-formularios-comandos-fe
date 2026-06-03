# Melhorias Futuras

Esta página lista melhorias técnicas identificadas durante a leitura do projeto.

## Corrigir encoding dos textos

Alguns arquivos exibem textos como `GestÃ£o`, `UsuÃ¡rios` e `AÃ§Ã£o`, indicando problema de encoding.

Impacto:

- piora a legibilidade;
- prejudica a apresentação do projeto;
- pode aparecer diretamente na interface.

Recomendação:

- padronizar arquivos como UTF-8;
- revisar strings em models, forms, views, templates e README;
- validar no navegador depois da correção.

## Atualizar testes para refletir permissão atual

Os testes de CRUD acessam rotas protegidas sem autenticar usuário com perfil adequado. A regra de segurança do sistema é válida, então a suíte de testes deve acompanhar essa regra.

Recomendação:

- criar fixtures para usuário admin;
- criar fixtures para usuário de gestão de riscos;
- testar acesso negado para estudante/sem permissão;
- testar redirecionamento para login quando anônimo.

## Cobrir regras de risco com testes

Faltam testes específicos para:

- cálculo de `nivel_risco`;
- cálculo de `nivel_residual`;
- validação de `data_fim >= data_inicio`;
- validação de objetivo vinculado ao desafio;
- filtragem de riscos por unidade;
- permissão de edição/exclusão por unidade.

## Separar regras de domínio se o projeto crescer

Hoje parte das regras está em models, forms, views e helpers. Para o tamanho atual, isso é aceitável. Se o sistema crescer, pode valer criar uma camada de services para regras mais complexas, principalmente no módulo de riscos.

Exemplos:

- `riscos/services.py` para cálculos e regras de visibilidade;
- `usuarios/services.py` para sincronização de perfil;
- testes unitários focados nesses services.

## Melhorar configuração de produção

Antes de publicar o sistema, revisar:

- `DEBUG=False`;
- `SECRET_KEY` obrigatória por variável de ambiente;
- banco externo em vez de SQLite;
- configuração de arquivos estáticos;
- HTTPS;
- logs;
- políticas de timeout para autenticação externa;
- tratamento de indisponibilidade do serviço da UFSM.

## Padronizar nomenclatura

O código usa termos como "risco" e "análise de riscos", enquanto algumas telas e labels usam "plano".

Recomendação:

- definir um glossário do domínio;
- padronizar nomes de telas, botões e rotas;
- evitar que o usuário interprete "plano" e "risco" como entidades diferentes se forem o mesmo fluxo.

