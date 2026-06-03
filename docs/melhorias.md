# Melhorias Futuras

Esta pagina lista melhorias tecnicas identificadas durante a leitura do projeto.

## Corrigir encoding dos textos

Alguns arquivos exibem textos como `GestÃ£o`, `UsuÃ¡rios` e `AÃ§Ã£o`, indicando problema de encoding.

Impacto:

- piora a legibilidade;
- prejudica apresentacao do projeto;
- pode aparecer diretamente na interface.

Recomendacao:

- padronizar arquivos como UTF-8;
- revisar strings em models, forms, views, templates e README;
- validar no navegador depois da correcao.

## Atualizar testes para refletir permissao atual

Os testes de CRUD acessam rotas protegidas sem autenticar usuario com perfil adequado. A regra de seguranca do sistema e valida, entao a suite de testes deve acompanhar essa regra.

Recomendacao:

- criar fixtures para usuario admin;
- criar fixtures para usuario de gestao de riscos;
- testar acesso negado para estudante/sem permissao;
- testar redirecionamento para login quando anonimo.

## Cobrir regras de risco com testes

Faltam testes especificos para:

- calculo de `nivel_risco`;
- calculo de `nivel_residual`;
- validacao de `data_fim >= data_inicio`;
- validacao de objetivo vinculado ao desafio;
- filtragem de riscos por unidade;
- permissao de edicao/exclusao por unidade.

## Separar regras de dominio se o projeto crescer

Hoje parte das regras esta em models, forms, views e helpers. Para o tamanho atual, isso e aceitavel. Se o sistema crescer, pode valer criar uma camada de services para regras mais complexas, principalmente no modulo de riscos.

Exemplos:

- `riscos/services.py` para calculos e regras de visibilidade;
- `usuarios/services.py` para sincronizacao de perfil;
- testes unitarios focados nesses services.

## Melhorar configuracao de producao

Antes de publicar o sistema, revisar:

- `DEBUG=False`;
- `SECRET_KEY` obrigatoria por variavel de ambiente;
- banco externo em vez de SQLite;
- configuracao de arquivos estaticos;
- HTTPS;
- logs;
- politicas de timeout para autenticacao externa;
- tratamento de indisponibilidade do servico da UFSM.

## Padronizar nomenclatura

O codigo usa termos como "risco" e "analise de riscos", enquanto algumas telas e labels usam "plano".

Recomendacao:

- definir um glossario do dominio;
- padronizar nomes de telas, botoes e rotas;
- evitar que o usuario interprete "plano" e "risco" como entidades diferentes se forem o mesmo fluxo.

