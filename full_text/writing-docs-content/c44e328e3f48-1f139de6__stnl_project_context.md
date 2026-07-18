---
name: stnl_project_context
description: Levanta contexto factual do projeto e materializa ou ressincroniza docs em docs/core, docs/units e docs/features com modos BOOTSTRAP, RESYNC e TBD_SYNC.
---

# STNL Project Context

## Missão
Levantar contexto factual profundo e honesto do projeto e materializar memória durável reutilizável em `docs/INDEX.md`, `docs/TBDS.md`, `docs/core/*`, `docs/units/*` e `docs/features/*`.

Esta skill é um utilitário global. Ela não é um agent de workflow e deve continuar útil fora dele.

## Quando usar
- quando for preciso bootstrapar uma base documental operacional profunda a partir de evidência real
- quando for preciso ressincronizar uma feature explícita com delta factual denso e edição localizada
- quando for preciso tratar canonicamente um ou mais TBDs já registrados em `docs/TBDS.md`
- quando prompts ou agents precisarem de contexto reutilizável em `docs/`
- quando a releitura ampla da codebase estiver custosa e a base documental ainda estiver ausente, incompleta ou em drift

## Quando não usar
- para tocar `docs/workflow/*`
- para conduzir planning, execução, validação ou fechamento de rodada como agent de workflow
- para reescrever documentação inteira por conveniência
- para abrir `units` sem evidência suficiente
- para criar features arbitrárias sem alvo claro
- para transformar hipótese, intenção ou recomendação em memória durável

## Modos suportados
- `MODE=BOOTSTRAP`
- `MODE=RESYNC`
- `MODE=TBD_SYNC`

## Escopo operacional
- materializar documentação factual e operacional profunda apenas em `docs/INDEX.md`, `docs/TBDS.md`, `docs/core/*`, `docs/units/*` e `docs/features/*`
- seguir a ordem `core -> TBDS -> units -> features`
- usar o kit documental canônico disponível no ambiente apenas como apoio de materialização
- ignorar `docs/workflow/*`

## Contrato obrigatório do bundle interno
- antes de ler qualquer template documental interno da skill, ler primeiro `reference/MANIFEST.md`
- usar somente os paths explícitos listados em `reference/MANIFEST.md` e necessários para a rodada
- não descobrir templates internos por busca ampla, regex, glob, inspeção de árvore ou scan textual
- não usar fallback em `templates/**`, `skills/**`, `~/.agents/**`, filesystem externo ou qualquer cópia fora do bundle instalado da própria skill
- se `reference/MANIFEST.md` estiver ausente, bloquear com `BLOCKED_REFERENCE_BUNDLE_MISSING`
- se qualquer arquivo obrigatório listado em `reference/MANIFEST.md` estiver ausente, bloquear com `BLOCKED_REFERENCE_BUNDLE_MISSING`
- o bloqueio deve reportar a skill `stnl_project_context`, o arquivo ausente e a ação sugerida: `node sentinel.mjs install` e `node sentinel.mjs doctor`
- nunca reconstruir, adivinhar, simplificar ou procurar substituto para template interno ausente

## Modelo documental alvo
- `CONTEXT`: base factual do projeto ou recorte; domínio, superfícies, integrações relevantes, linguagem e lacunas observáveis
- `RULES`: regras ativas do projeto em estrutura simples; separar regras confirmadas de seeds e priorizar bullets operacionais por camada ou superfície
- `STATE`: mapa factual do que existe; entrypoints, paths, módulos, jobs, pipelines, testes e superfícies
- `CONTRACTS`: padrões, convenções e localização dos contratos importantes; nunca dump massivo de DTOs, endpoints ou interfaces
- `TESTING`: estratégia de validação, níveis de teste, mínimos por tipo de mudança, limites de prova e matriz factual canônica mínima de harness/checks; nunca catálogo exaustivo por inércia
- `TBDS`: consolidado canônico das lacunas arquiteturais, contratuais ou de boundary relevantes; docs locais ainda podem registrar `TBDs`, mas a consolidação fica aqui
- `docs/features/*/CONTEXT.md`: snapshot factual e operacional da feature; deve conter estado atual, escopo ativo, hot paths, dependências imediatas, referências úteis e lacunas reais sem substituir `RULES`, `STATE`, `CONTRACTS` ou `TESTING`

## Saídas esperadas
- navegação simples e útil em `docs/INDEX.md`, organizada para leitura operacional
- base factual profunda em `docs/core/*`, com separação clara entre contexto, regras, estado, contratos e testing
- `docs/TBDS.md` como consolidado canônico das lacunas relevantes
- `docs/units/*` apenas quando houver especialização útil de `unit` além do que cabe em `core`
- `docs/features/*` apenas quando houver alvo explícito ou feature canônica descoberta com evidência forte
- classificação de `repo shape`: `single-unit`, `multi-unit` ou `TBD`
- atualização localizada no `RESYNC`, com alta densidade factual no delta tocado
- tratamento auditável de TBDs registrados no `TBD_SYNC`, sem refresh amplo do projeto

## Princípios
- discovery guiado por evidência da codebase, docs existentes e paths reais
- profundidade máxima sustentável sob evidência, sem superficializar por contrato
- `TBD` ou marcação explícita de parcialidade no lugar de inferência
- blast radius mínimo
- memória durável factual, operacional e reutilizável para agents
- bootstrap para criar o que falta; resync para sincronizar delta factual orientado por feature; `TBD_SYNC` para tratar lacuna já registrada em `docs/TBDS.md`
- regra operacional concreta vale mais que princípio abstrato
- seed só entra como seed; não promover sem base observável
- não haverá skill separada para TBDs; o ownership documental de `docs/TBDS.md` e do ciclo de TBDs continua em `stnl_project_context`

## Regras de profundidade honesta e anti-alucinação
- profundidade não autoriza inventar
- quando houver evidência parcial, marcar isso explicitamente no texto
- não simular completude, inventário total ou cobertura total sem base observável
- quando a leitura vier de amostragem forte, preferir `principais padrões observados`, `paths principais` ou formulação equivalente
- quando uma área não sustentar profundidade factual suficiente, registrar a lacuna em vez de preencher com abstração vaga
- não promover hipótese fraca, convenção presumida ou naming provável a memória durável
- não inventar regra específica do projeto sem evidência
- se houver conflito entre padrões observados, registrar a tensão em `docs/TBDS.md`
- exaustividade só pode ser sugerida quando a evidência realmente sustentar isso

## Regras para materializar `RULES`
- usar a estrutura simples: `Objetivo`, `Regras invioláveis`, `Stop rules`, `Regras de mudança estrutural`, `Regras de arquitetura`, `Convenções globais`, `Seeds por stack ou superfície`, `Relação com TBDs`, `Referências`
- em `Regras invioláveis`, `Regras de arquitetura`, `Convenções globais` e `Exceções aprovadas`, registrar só regras confirmadas pela codebase ou por decisão explícita
- em `Seeds por stack ou superfície`, registrar apenas seeds genéricos, operacionais e ajustáveis por evidência
- não usar seed abstrato demais, slogan vago ou guideline genérica como `SOLID`, `Clean Code` ou `boa separação`
- preferir bullets acionáveis como `controller não concentra regra de negócio`, `UI não chama repository diretamente`, `integração externa passa por boundary canônica`
- preencher `Regras por superfície detectada` somente para superfícies que realmente existirem no projeto ou na unit
- registrar `Exceções aprovadas` apenas quando a exceção estiver observada e sustentada por evidência clara
- `RULES.md` não vira governança documental, workflow nem backlog de pendências

## Regras para materializar `docs/TBDS.md`
- tratar `docs/TBDS.md` como consolidado canônico das lacunas relevantes do projeto
- manter `docs/TBDS.md` sob ownership documental de `stnl_project_context`; não abrir skill separada para TBDs
- docs locais podem continuar marcando `TBDs`, mas a consolidação precisa apontar para `docs/TBDS.md`
- abrir ou atualizar item em `docs/TBDS.md` quando a lacuna bloquear decisão arquitetural, contratual, de boundary, compatibilidade ou integração crítica
- quando a lacuna afetar regra ativa, referenciar o item de `docs/TBDS.md` em `RULES.md`
- não usar `docs/TBDS.md` como backlog genérico de melhorias
- `docs/TBDS.md` não é leitura obrigatória em toda demanda normal; ele serve para discovery, bootstrap, resync, `TBD_SYNC` e ambiguidades relevantes
- no `MODE=TBD_SYNC`, sempre partir de um ou mais TBDs já existentes em `docs/TBDS.md`; esse modo não é refresh amplo
- alinhar o trabalho de status ao shape canônico de `templates/docs/TBDS.md`: `open`, `investigating`, `resolved`
- `open` registra a lacuna aberta
- `investigating` registra trabalho analítico sem fechamento suficiente
- `resolved` só fecha lacuna realmente sincronizada por evidência factual forte ou decisão humana explícita suficiente
- nunca marcar `resolved` quando houver apenas refinamento textual, recorte melhor do problema ou redução do escopo da dúvida
- quando a evidência seguir insuficiente, manter o item em `open` ou `investigating`
- quando houver decisão humana explícita, registrar a resolução como decisão, sem fingir que ela veio da codebase

## Regras para materializar `TESTING`
- tratar `docs/core/TESTING.md` como memória factual de validação e como matriz canônica mínima de harness/checks do projeto
- registrar por superfície, camada ou boundary real quando houver evidência suficiente: objetivos de prova típicos, comandos canônicos de lint, formatter/prettier, typecheck e build, suites relevantes, smoke ou manual paths aceitos, confiança do harness, gaps, pré-requisitos, env, fixtures, credenciais e observações de custo/sinal
- consolidar apenas comandos, suites, paths, requisitos e gaps sustentados pela codebase, CI, scripts, docs operacionais ou outra evidência forte equivalente
- usar `none` quando a ausência for confirmada e `TBD` quando a evidência for insuficiente; não inventar harness, comando, fixture, credencial ou roteiro manual
- a matriz informa validação local, mas não substitui artifact cut-scoped nem vira tutorial genérico ou checklist cego

## Heurísticas de `core`
- `docs/core/*` é a base global profunda do projeto e sempre vem primeiro
- materializar a maior densidade factual útil que a evidência sustentar para entendimento global
- distribuir o conteúdo conforme o papel correto de cada doc:
  - `CONTEXT`: visão factual, escopo, superfícies, integrações, linguagem e lacunas
  - `RULES`: regras confirmadas, boundaries, stop rules, mudança estrutural e seeds separados
  - `STATE`: mapa do que existe e onde fica
  - `CONTRACTS`: padrões estruturais, convenções e localização dos contratos
  - `TESTING`: estratégia, mínimos de validação, limites de prova e matriz factual mínima de harness/checks
  - `TBDS`: lacunas relevantes consolidadas em um único ponto canônico
- quando faltar fato global relevante, registrar `TBD`, parcialidade ou limite de exaustividade em vez de inferir

## Heurísticas de `units`
- `units` é camada condicional
- não assuma `units` por padrão
- classificar `repo shape` e materializar `docs/units/*` são decisões separadas
- `single-unit` significa apenas zero ou uma `unit` canônica possível; não obriga abrir `docs/units/*`
- materializar `docs/units/*` exige evidência adicional de especialização factual útil que não caiba adequadamente em `docs/core/*`
- em `repo shape = single-unit`, preferir por padrão apenas `docs/INDEX.md`, `docs/TBDS.md` e `docs/core/*`
- se a única `unit` candidata coincidir essencialmente com o nome do app, serviço, API principal ou entrypoint, isso por si só não basta para abrir `unit`
- monorepo não implica `multi-unit`
- não confundir `unit` com projeto técnico, assembly, camada interna ou particionamento arquitetural
- não abrir `unit` só porque existem múltiplos projetos técnicos, pastas ou assemblies `Api`, `Application`, `Domain`, `Data`, `IoC`, `Tests`, camadas de implementação ou um entrypoint principal com nome próprio
- esses sinais podem sustentar entendimento de arquitetura global e devem ir para `docs/core/*`, mas não bastam por si só para abrir `docs/units/*`
- só promover uma área a `unit` quando houver especialização factual útil, documentalmente distinta do `core`, sustentada por pelo menos um sinal forte claro; em casos limítrofes, corroborar com mais de um sinal

Evidência suficiente para abrir `unit`:
- fronteira funcional ou de domínio claramente distinta
- superfície própria com regras, contratos, state ou testing que mereçam especialização fora de `core`
- bounded context ou módulo canônico reconhecível e recorrente
- separação que faça sentido documental e não apenas estrutural ou técnica

Sinais fortes:
- entrypoint ou runtime próprio
- deploy, build ou package próprio
- contratos próprios
- testing ou harness próprio
- regras locais próprias

Se não houver essa especialização útil, trate como superfície, área ou arquitetura interna do projeto e registre em `docs/core/*`, não como `unit`.

## Heurísticas de `features`
- `docs/features/*` é contexto local
- feature não substitui `core`
- feature também não substitui `unit` quando `unit` existir
- no `MODE=BOOTSTRAP`, mesmo sem alvo explícito, tentar discovery inicial de 0 a 3 features canônicas
- o limite absoluto no `BOOTSTRAP` é 3; abrir 0, 1, 2 ou 3 é válido, e nunca há obrigação de fechar 3
- só materializar as features mais fortes, com evidência forte e não arbitrária
- se não houver feature forte o suficiente, abrir 0 é o comportamento correto
- feature candidata deve representar comportamento funcional, superfície útil ou recorte documental reconhecível; não apenas uma camada técnica
- só criar ou atualizar feature quando houver alvo explícito, evidência clara ou necessidade prática real
- a feature tocada deve concentrar estado atual, escopo ativo, hot paths, dependências imediatas e gaps reais sem virar mini-inventário, catálogo contratual ou política de testes
- a feature tocada não deve absorver seção detalhada de testes, mini catálogo contratual, dump de entidades, inventário estrutural amplo ou seção longa de dependências externas
- quando contratos, testes ou referências mais estáveis forem relevantes para a feature, apontar `docs/core/CONTRACTS.md`, `docs/core/TESTING.md`, `docs/units/*` quando existir, e paths reais do repo em vez de duplicar volume
- não abrir features arbitrariamente

Sinais que podem sustentar feature:
- fluxos funcionais recorrentes
- endpoints ou rotas agrupáveis por comportamento
- páginas, screens, routes ou áreas de produto
- services, handlers ou use-cases recorrentes com propósito funcional claro
- testes organizados por comportamento funcional
- contratos, schemas ou integrações que revelem um recorte funcional canônico
- módulos ou bounded contexts realmente reconhecíveis

Sinais que não bastam por si só:
- `Api`, `Application`, `Domain`, `Data`, `IoC`, `Tests`
- nomes de camada técnica
- pastas puramente arquiteturais
- entrypoint principal
- assemblies ou projetos técnicos
- nomes genéricos sem recorte funcional claro

Discovery de feature no `BOOTSTRAP`:
- fazer discovery por evidência real da codebase e de `docs/` existentes, conforme a stack observada
- usar até 3 tentativas internas de discovery para encontrar candidatas fortes antes de desistir
- não inventar agrupamentos nem promover hipótese fraca a feature materializada
- se houver candidatas de confiança média ou baixa, não abrir automaticamente; só registrar no output se isso ajudar sem poluir

## Heurísticas para materializar `RULES` por superfície
Aplicar somente com evidência. Se os sinais forem conflitantes ou insuficientes, registrar `TBD` ou `principais padrões observados`.

Superfícies que podem preencher `Regras por superfície detectada`:
- `API / controller / endpoint`
- `application / service / use case`
- `domain`
- `data / repository / infra`
- `UI / design system`
- `jobs / workers / schedulers`
- `adapters / integrations`

Ao preencher `Regras por superfície detectada`:
- incluir só as superfícies realmente presentes
- usar bullets operacionais e curtos
- evitar repetir seed genérico como se fosse regra confirmada
- registrar exceção real em `Exceções aprovadas`, não diluir no meio das regras

## Heurísticas práticas por stack
Aplicar somente com evidência. Se os sinais forem conflitantes ou insuficientes, registrar `TBD`.

### .NET / API / BFF
- detectar por `.sln`, `.csproj`, `Program.cs`, `Controllers/`, minimal APIs, `Application`, `Domain`, `Repository`, `DbContext`, `IoC`, `Migrations`, `Filters`, `Middlewares`, `ProblemDetails` e `Auth`
- procurar evidência de camada de borda, orquestração, domínio, persistência e autorização nos paths reais
- regras candidatas:
  - controller, endpoint handler ou minimal API não concentra regra de negócio
  - service ou use case orquestra o fluxo
  - domínio não conhece infra
  - acesso a dados passa pela boundary prevista
  - auth, claims e permission check acontecem na borda apropriada

### Angular / React / Next / UI
- detectar por `angular.json`, dependências `@angular/*`, `react`, `react-dom`, `next` e `next.config*`
- procurar evidência em componentes, telas, routes, pages, screens, hooks, stores, services, facades, adapters, clients, tokens, theme, design system, api layer, repository layer e data layer
- em Next, diferenciar `app router`, `pages router`, `app/api`, `pages/api` e server actions por evidência
- regras candidatas:
  - UI não chama repository diretamente
  - componente, page, screen ou route não concentra regra de negócio crítica
  - efeitos colaterais não ficam espalhados na camada visual
  - design system, tokens e primitives seguem o kit local

### Node / Nest / Express
- detectar por `package.json` com backend evidenciado, `nestjs`, `express`, `fastify` ou estrutura equivalente
- procurar evidência em controllers, routes, handlers, services, use-cases, repositories, DTOs, schemas, validators, adapters e clients
- regras candidatas:
  - rota ou controller fica fino
  - regra crítica fica em service ou use case
  - integração externa fica encapsulada
  - validação acontece na borda apropriada

### Jobs / workers / schedulers
- detectar por `jobs`, `workers`, `queues`, `consumers`, `schedulers`, `cron`, `Hangfire`, `Bull`, `Celery` ou infraestrutura equivalente
- procurar evidência de orquestração, payload, retry, idempotência e boundary de side effects
- regras candidatas:
  - job orquestra fluxo, não vira depósito de regra crítica
  - payload sensível não muda silenciosamente
  - retry e idempotência respeitam a boundary prevista

### Persistência / ORM / banco
- detectar por entities, models, migrations, mappings, configurations, repositories, conventions, helpers de schema, `DbContext`, `Prisma`, `TypeORM`, `Sequelize`, `EF Core` ou equivalentes
- procurar evidência de boundary de persistência, schema compatível, mapping e convenções recorrentes
- regras candidatas:
  - persistência segue a boundary definida
  - repository não concentra regra de negócio
  - convenções de schema e mapping que impactam compatibilidade precisam ser preservadas

## Entrevista guiada mínima
Perguntar só depois do discovery e apenas para fechar lacunas relevantes que bloqueiem a materialização factual honesta.

Limites:
- no máximo 2 rodadas curtas por execução
- no máximo o necessário para fechar tipo do projeto, objetivo, prioridade de feature ou forma de testar
- se a resposta não vier ou continuar inconclusiva, registrar `TBD` e seguir dentro do escopo seguro

## Restrições e proibições
- não considerar `docs/workflow/*`
- não inventar templates
- não inventar paths
- não inventar scripts
- não inventar hooks
- não inventar convenções
- não inventar mecanismo fora do contrato da skill e do ambiente disponível
- não duplicar o kit documental canônico por padrão
- não tratar hipótese como memória durável
- não tocar áreas fora do escopo sem necessidade direta
- não assumir `units` por padrão
- não assumir `multi-unit` só porque é monorepo
- não abrir `unit` só porque a solução tem múltiplos projetos técnicos ou camadas internas
- não tratar camada técnica ou pasta arquitetural como feature
- não reescrever arquivo inteiro se uma edição localizada resolver

## Stop conditions
- falta informação estrutural sem a qual qualquer decisão viraria chute
- a feature alvo do `RESYNC` não foi explicitada
- o delta factual do `RESYNC` está amplo demais para atualização localizada
- o `TBD_SYNC` não recebeu ao menos um `TBD_ID` já existente
- o `TARGET_SCOPE` do `TBD_SYNC` está ausente ou fora do shape `core`, `unit:<unit-slug>` ou `feature:<feature-path>`
- o `SOURCE_OF_TRUTH` do `TBD_SYNC` não aponta para paths reais que sustentem a análise
- o pedido deriva para `docs/workflow/*` ou refresh amplo fora do escopo
- a única saída possível seria inferir fatos não sustentados pela codebase

## Critérios para `repo shape`
- `single-unit`: zero ou uma `unit` canônica possível
- `multi-unit`: duas ou mais `units` canônicas
- `TBD`: quando não for possível decidir honestamente com a evidência disponível

A classificação de `repo shape` não materializa `docs/units/*` sozinha; ela apenas limita quantas `units` canônicas podem existir.

## `MODE=BOOTSTRAP`
`BOOTSTRAP` é create-only absoluto.

Contrato:
- criar somente docs ausentes
- produzir documentação robusta, factual e operacionalmente útil nos arquivos novos
- buscar profundidade máxima sustentada por evidência dentro do escopo da skill
- limitar o blast radius pelo escopo documental, nunca por superficialização artificial
- poder abrir de 0 a 3 features canônicas quando houver evidência forte

Regras obrigatórias:
- antes de criar qualquer doc alvo, verificar se ele já existe
- se existir, não editar e registrar `SKIPPED`
- não usar `BOOTSTRAP` para refresh de docs existentes
- usar `RESYNC` quando a necessidade for atualização localizada
- não gerar docs vazios só para completar estrutura
- tratar `docs/INDEX.md` como índice simples da documentação operacional criada, não como expansão de escopo
- tratar `docs/TBDS.md` como consolidado canônico das lacunas relevantes, mesmo quando houver poucos itens ou nenhum item aberto ainda

Matriz do que pode ser criado:
- sempre que faltar: `docs/INDEX.md`
- sempre que faltar: `docs/TBDS.md`
- sempre que faltar: `docs/core/CONTEXT.md`, `docs/core/RULES.md`, `docs/core/STATE.md`, `docs/core/CONTRACTS.md`, `docs/core/TESTING.md`
- somente com especialização útil de `unit` evidenciada além do que cabe em `core`: `docs/units/<unit-slug>/CONTEXT.md`, `RULES.md`, `STATE.md`, `CONTRACTS.md`, `TESTING.md`
- somente com evidência clara de superfície visual própria: `docs/units/<unit-slug>/UI_KIT.md`
- somente com feature alvo explícita ou feature inicial canônica com evidência forte: `docs/features/<feature-path>/CONTEXT.md`
- quando a feature for criada: `docs/features/<feature-path>/done/.gitkeep`

Regras de decisão para `BOOTSTRAP`:
- a ausência de `docs/units/*` é resultado válido e frequentemente preferível em `repo shape = single-unit`
- em `single-unit`, preferir criar apenas `docs/INDEX.md`, `docs/TBDS.md` e `docs/core/*`
- abrir `docs/units/*` apenas quando houver especialização factual útil fora de `core`
- se a única `unit` identificada coincidir essencialmente com o app, serviço, API principal ou entrypoint, manter em `core` salvo evidência adicional forte
- depois de materializar a base global profunda e decidir `units`, tentar semear de 0 a 3 features canônicas iniciais
- esse feature seeding vale para qualquer stack, inclusive frontend, backend, fullstack, `single-unit`, `multi-unit` e monorepo
- não usar `features` para compensar ausência de `unit`
- não abrir mais que 3 features no total durante o `BOOTSTRAP`
- não abrir feature a partir de camada técnica, assembly, projeto interno ou nome genérico sem recorte funcional forte

Ordem operacional:
1. ler a raiz do projeto e o `docs/` já existente
2. classificar stack, superfícies e `repo shape`
3. ler primeiro `reference/MANIFEST.md` e carregar apenas os templates listados nele que forem necessários
4. materializar primeiro `docs/core/*`
5. materializar `docs/TBDS.md` como consolidado canônico das lacunas relevantes
6. materializar `docs/INDEX.md` como navegação simples da base documental criada
7. decidir se existe evidência suficiente para materializar `units` além do `core`
8. se `repo shape = single-unit` e não houver especialização útil clara, seguir sem abrir `units`
9. abrir `units` apenas quando houver especialização factual útil evidenciada
10. fazer feature discovery inicial por evidência, com até 3 tentativas internas de discovery
11. abrir até 3 features canônicas de alta confiança
12. encerrar com saída verificável de criados, `SKIPPED`, `TBD` e candidatas não abertas quando isso for útil

## Regras de propagação controlada no `RESYNC`
`RESYNC` é o modo de atualização localizada.

Contrato:
- produzir a maior densidade factual honesta possível sobre a feature alvo e seu delta
- preservar `RESYNC` como modo orientado a delta factual com feature alvo; TBD registrado continua pertencendo a `TBD_SYNC`
- manter superfície mínima de edição: poucos arquivos e poucos trechos, quando isso bastar
- aprofundar factual e operacionalmente tudo o que tocar
- não reescrever tudo, não fazer refresh amplo e não responder com conteúdo raso só por ser localizado

Regras operacionais:
- começar e terminar na feature alvo
- por padrão, tocar apenas a camada da feature
- subir para `unit` só se a mudança alterar regra, contrato, state ou testing útil daquela `unit`
- subir para `core` só se a mudança alterar regra global, contrato global, convenção global, shape do projeto ou `docs/TBDS.md`
- limite padrão: no máximo 1 camada acima da feature, salvo justificativa explícita
- nunca aproveitar `RESYNC` para refresh amplo
- nunca reescrever documentação inteira se uma edição localizada resolver

## `MODE=TBD_SYNC`
`TBD_SYNC` é o modo canônico para tratar lacunas já registradas em `docs/TBDS.md`.

Contrato:
- partir sempre de um ou mais TBDs já existentes; nunca começar de refresh amplo
- não substituir `RESYNC`; `RESYNC` continua orientado a delta factual com feature alvo explícita
- tratar a lacuna de modo auditável, com atualização mínima e factual do consolidado canônico e da doc dona da lacuna
- manter o ownership de `docs/TBDS.md` e do ciclo documental de TBDs dentro de `stnl_project_context`

Entradas operacionais:
- `TBD_ID`: um ou mais IDs já existentes em `docs/TBDS.md`
- `TARGET_SCOPE`: obrigatório; usar exatamente `core`, `unit:<unit-slug>` ou `feature:<feature-path>`
- `SOURCE_OF_TRUTH`: obrigatório; informar paths reais que sustentam a análise
- `DECISION_INPUT`: opcional; usar quando a resolução depender de decisão humana explícita

Forma compacta adicional:
- aceitar uma ou mais linhas no formato `TBD-XXX: <instrução curta>`
- nessa forma, a skill deve ler `docs/TBDS.md` obrigatoriamente, localizar cada item pelo ID e tratar cada TBD como subunidade independente de análise
- `TARGET_SCOPE` e `SOURCE_OF_TRUTH` explícitos continuam válidos e preferenciais quando já vierem informados; a forma compacta é ergonomia adicional, não substituição do contrato explícito
- quando a instrução curta for claramente decisória, tratá-la como `DECISION_INPUT` implícito sem fingir que a decisão veio da codebase
- múltiplos TBDs no mesmo prompt compacto são permitidos como ergonomia de entrada, mas não autorizam fundir scopes distintos numa única análise documental

Resultados permitidos:
- resolvido por evidência factual
- resolvido por decisão explícita do usuário
- não resolvido, mas refinado ou reduzido com melhor delimitação da lacuna

Regra de fechamento:
- refinamento não equivale a resolução; se a lacuna só ficou mais precisa, ela continua `open` ou `investigating`

Heurística conservadora de inferência no formato compacto:
- ler primeiro `docs/TBDS.md` e inferir o `TARGET_SCOPE` inicial a partir do próprio item apenas quando a âncora estiver clara e sustentada
- inferir `unit:<unit-slug>` quando o TBD estiver claramente ancorado em library, módulo, pacote, pasta de unit ou boundary local bem definido
- inferir `feature:<feature-path>` quando o TBD estiver claramente ancorado em feature específica
- inferir `core` quando o item tratar de boundary entre projetos, segurança, CI, contrato global, arquitetura global ou quando não houver owner local claro
- se a inferência de `TARGET_SCOPE` continuar ambígua, não chutar; registrar insuficiência de base para inferência honesta
- derivar o `SOURCE_OF_TRUTH` inicial a partir de paths, arquivos, áreas, imports, módulos, boundaries e doc local explicitamente mencionados no próprio TBD
- expandir a leitura apenas minimamente quando necessário para análise honesta; isso não autoriza discovery ou refresh amplo
- se o item em `docs/TBDS.md` não trouxer base mínima para derivar leitura inicial honesta, parar e pedir ou esperar evidência melhor em vez de inventar

Guardrails para instruções curtas:
- interpretar instruções como `manter como está`, `aceitar como legado`, `resolver por decisão`, `não priorizar agora` e `continuar investigando` como direção documental auditável, não como boa prática genérica
- não fingir que decisão humana, postergação ou aceitação de legado veio da codebase
- não marcar `resolved` quando a instrução apenas posterga, reduz prioridade ou aceita contexto legado sem fechamento suficiente da lacuna
- quando a decisão humana for explícita e suficiente para encerrar a lacuna, pode marcar `resolved` como decisão documentada
- quando a instrução apenas mantiver investigação ou reduzir prioridade sem fechamento adequado, manter `open` ou `investigating`

## Regras de propagação controlada no `TBD_SYNC`
`TBD_SYNC` é o modo de sincronização localizada a partir de lacuna registrada.

Regras operacionais:
- começar sempre no item alvo em `docs/TBDS.md`
- sempre atualizar `docs/TBDS.md`
- atualizar a doc dona da lacuna quando aplicável
- propagar no máximo uma camada documental além da doc dona, salvo justificativa explícita
- para TBD de feature, tocar por padrão `docs/TBDS.md` e `docs/features/<feature-path>/CONTEXT.md`
- para TBD de unit, tocar por padrão `docs/TBDS.md` e a doc relevante em `docs/units/<unit-slug>/*`
- para TBD de core, tocar por padrão `docs/TBDS.md` e a doc relevante em `docs/core/*`
- não usar `TBD_SYNC` para refresh amplo de projeto
- não criar `features` ou `units` novas só para acomodar o fluxo
- não reclassificar arquitetura, `repo shape` ou shape do repo sem evidência excepcional e necessidade clara
- não inventar fatos para fechar TBD
- não fechar TBD por inferência fraca
- se a evidência continuar insuficiente, manter o item aberto ou em investigação

## Procedimento operacional
### `MODE=BOOTSTRAP`
1. Ler a raiz factual do projeto-alvo e o que já existir em `docs/`.
2. Fazer discovery guiado por evidência para classificar stack, superfícies e `repo shape`.
3. Antes de cada criação, verificar existência; se existir, registrar `SKIPPED`.
4. Criar primeiro `docs/core/*`.
5. Criar `docs/TBDS.md` quando faltar.
6. Criar `docs/INDEX.md` quando faltar.
7. Decidir se há ou não evidência suficiente para materializar `docs/units/*` além do `core`.
8. Se `repo shape = single-unit` e não houver especialização útil clara, seguir sem abrir `docs/units/*`; isso não é incompletude.
9. Criar `docs/units/*` somente para `units` com especialização útil evidenciada.
10. Fazer feature discovery inicial por evidência da codebase e `docs/` existentes, com até 3 tentativas internas de discovery.
11. Criar `docs/features/*` somente para feature alvo explícita ou para até 3 features canônicas de alta confiança.
12. Se as candidatas forem fracas, conflitantes ou genéricas, não materializar.
13. Registrar ou atualizar `docs/TBDS.md` apenas onde a lacuna afeta entendimento durável.

### `MODE=RESYNC`
1. Confirmar a feature alvo explícita.
2. Ler a feature alvo e apenas o entorno necessário para sustentar profundidade factual honesta sobre o delta.
3. Corrigir o drift factual nos trechos certos da feature, sem refresh amplo.
4. Atualizar `docs/TBDS.md` quando o delta revelar ou resolver lacuna arquitetural, contratual ou de boundary relevante.
5. Propagar no máximo uma camada acima apenas se a mudança afetar `unit` ou `core`.
6. Encerrar com edição localizada e profundidade máxima sustentada no que foi tocado.

### `MODE=TBD_SYNC`
1. Confirmar um ou mais `TBD_ID` já existentes em `docs/TBDS.md`.
2. Se a entrada vier no formato compacto `TBD-XXX: <instrução curta>`, ler `docs/TBDS.md` obrigatoriamente, localizar cada item e tratar cada TBD separadamente.
3. Confirmar `TARGET_SCOPE` no shape `core`, `unit:<unit-slug>` ou `feature:<feature-path>`; no formato compacto, inferir esse scope apenas quando o próprio item sustentar isso de forma clara.
4. Ler `docs/TBDS.md`, a doc dona da lacuna e apenas o `SOURCE_OF_TRUTH` necessário para análise honesta; no formato compacto, derivar o ponto de partida a partir do próprio TBD e expandir minimamente só se necessário.
5. Atualizar sempre o item alvo em `docs/TBDS.md`.
6. Atualizar a doc dona da lacuna e propagar no máximo uma camada adicional só quando a evidência exigir, sem colapsar TBDs de scopes distintos numa análise única.
7. Encerrar classificando cada TBD como `resolved`, `investigating` ou `open`, sem promover refinamento, postergação ou aceitação de legado a fechamento.

## Exemplos canônicos de invocação para `MODE=TBD_SYNC`
Os exemplos abaixo são de invocação. Eles não são template rígido obrigatório e não redefinem o contrato; os campos obrigatórios continuam sendo os já definidos acima.

### Exemplo explícito com fallback completo
```text
MODE=TBD_SYNC
TBD_ID=TBD-101
TARGET_SCOPE=feature:<feature-path>
SOURCE_OF_TRUTH=docs/TBDS.md,docs/features/<feature-path>/CONTEXT.md,src/<feature-area>/*
```
Leitura esperada: usar o contrato explícito atual como fallback completo, sem refresh amplo do projeto.

### Exemplo compacto com decisão curta
```text
MODE=TBD_SYNC
TBD-102: resolver por decisão explícita do usuário
```
Leitura esperada: ler `docs/TBDS.md`, localizar o item, inferir `TARGET_SCOPE` e `SOURCE_OF_TRUTH` iniciais só se o próprio TBD sustentar isso, e tratar a direção curta como `DECISION_INPUT` implícito quando aplicável.

### Exemplo compacto com direção investigativa
```text
MODE=TBD_SYNC
TBD-103: continuar investigando com base na evidência já citada no item
```
Leitura esperada: manter blast radius mínimo, iniciar pelos paths, arquivos, áreas ou boundaries já mencionados no TBD e manter `open` ou `investigating` se seguir sem base suficiente para fechamento.

### Exemplo compacto com múltiplos TBDs
```text
MODE=TBD_SYNC
TBD-104: aceitar como legado por agora
TBD-105: continuar investigando
```
Leitura esperada: aceitar múltiplos TBDs no mesmo prompt curto, mas tratar cada item separadamente, com propagação mínima por TBD e sem fundir scopes distintos numa única análise.

### Erros comuns
- usar `TBD_SYNC` sem `TBD_ID`
- usar `TARGET_SCOPE` fora do shape aceito `core`, `unit:<unit-slug>` ou `feature:<feature-path>`
- fundir TBDs de escopos diferentes numa única análise documental
- usar `TBD_SYNC` como refresh amplo
- assumir `TARGET_SCOPE` por chute quando `docs/TBDS.md` não sustenta inferência honesta
- inventar `SOURCE_OF_TRUTH` quando o item não trouxer base mínima para iniciar a análise

## Formato de saída operacional da skill
Use saída curta, verificável e factual.

Regra obrigatória de auditabilidade:
- em `docs criadas`, `docs alteradas` e `docs SKIPPED`, listar sempre paths completos relativos ao repo
- nunca retornar apenas nomes soltos como `INDEX.md`, `TBDS.md`, `CONTEXT.md`, `RULES.md`, `STATE.md`, `CONTRACTS.md` ou `TESTING.md`
- usar formatos como `docs/INDEX.md`, `docs/TBDS.md`, `docs/core/CONTEXT.md` ou `docs/features/<feature-path>/CONTEXT.md`
- o fechamento final deve ser o último bloco da resposta; não acrescentar observações, perguntas ou log depois dele
- não misturar output final com log intermediário, raciocínio, checklist operacional ou narrativa de execução
- nunca terminar com perguntas de continuação como `Continue to iterate?`
- nunca emitir lixo serializado como `[object Object]`
- se uma seção listar docs, cada item deve ser uma linha própria contendo apenas o path relativo completo

Formato canônico:
- usar exatamente os headings previstos para o modo em execução
- manter ordem fixa das seções
- quando não houver itens em uma seção listável, usar `- none`
- depois da última linha do fechamento, encerrar a resposta sem texto adicional

### Para `BOOTSTRAP`
- `MODE: BOOTSTRAP`
- `REPO SHAPE: <single-unit | multi-unit | TBD>`
- `DOCS CRIADAS:`
- `DOCS SKIPPED:`
- `INDICE CRIADO: <docs/INDEX.md | none>`
- `UNITS ABERTAS:`
- `FEATURES ABERTAS:`
- `FEATURES CANDIDATAS NAO ABERTAS:`
- `TBDS RELEVANTES:`

Template canônico de `BOOTSTRAP`:
```text
MODE: BOOTSTRAP
REPO SHAPE: <single-unit | multi-unit | TBD>
DOCS CRIADAS:
- docs/INDEX.md
- docs/TBDS.md
- docs/core/CONTEXT.md
DOCS SKIPPED:
- none
INDICE CRIADO: <docs/INDEX.md | none>
UNITS ABERTAS:
- none
FEATURES ABERTAS:
- docs/features/<feature-path>/CONTEXT.md
FEATURES CANDIDATAS NAO ABERTAS:
- none
TBDS RELEVANTES:
- TBD-001 - <titulo curto>
```

### Para `RESYNC`
- `MODE: RESYNC`
- `FEATURE ALVO: <feature-path>`
- `DOCS ALTERADAS:`
- `CAMADA ADICIONAL TOCADA: <core | unit:<unit-slug> | none>`
- `DELTA FACTUAL SINCRONIZADO:`
- `LIMITES MANTIDOS:`

Template canônico de `RESYNC`:
```text
MODE: RESYNC
FEATURE ALVO: <feature-path>
DOCS ALTERADAS:
- docs/TBDS.md
- docs/features/<feature-path>/CONTEXT.md
CAMADA ADICIONAL TOCADA: <core | unit:<unit-slug> | none>
DELTA FACTUAL SINCRONIZADO:
- <ajuste factual curto>
- <ajuste factual curto ou none>
LIMITES MANTIDOS:
- <limite mantido>
- <limite mantido ou none>
```

### Para `TBD_SYNC`
- `MODE: TBD_SYNC`
- `TBDS ALVO:`
- `TARGET SCOPE: <core | unit:<unit-slug> | feature:<feature-path>>`
- `DOCS ALTERADAS:`
- `STATUS FINAL DOS TBDS:`
- `DELTA RESOLVIDO:`
- `LIMITES MANTIDOS:`

Template canônico de `TBD_SYNC`:
```text
MODE: TBD_SYNC
TBDS ALVO:
- TBD-001
TARGET SCOPE: <core | unit:<unit-slug> | feature:<feature-path>>
DOCS ALTERADAS:
- docs/TBDS.md
- docs/features/<feature-path>/CONTEXT.md
STATUS FINAL DOS TBDS:
- TBD-001 -> resolved
DELTA RESOLVIDO:
- <o que foi realmente sincronizado>
LIMITES MANTIDOS:
- sem refresh amplo do projeto
- sem inferir fato não sustentado
```

## Exemplos canônicos de `TBD_SYNC`
### TBD de feature resolvido por evidência
```text
MODE: TBD_SYNC
TBDS ALVO:
- TBD-014
TARGET SCOPE: feature:billing/invoice-export
DOCS ALTERADAS:
- docs/TBDS.md
- docs/features/billing/invoice-export/CONTEXT.md
STATUS FINAL DOS TBDS:
- TBD-014 -> resolved
DELTA RESOLVIDO:
- exportação confirmada pelos paths `src/billing/invoice-export/*` e `tests/billing/invoice-export.spec.ts`
LIMITES MANTIDOS:
- sem subir além da feature
```

### TBD de core refinado, mas não resolvido
```text
MODE: TBD_SYNC
TBDS ALVO:
- TBD-003
TARGET SCOPE: core
DOCS ALTERADAS:
- docs/TBDS.md
- docs/core/CONTRACTS.md
STATUS FINAL DOS TBDS:
- TBD-003 -> investigating
DELTA RESOLVIDO:
- lacuna reduzida ao boundary de autenticação entre `src/auth/http/*` e `src/auth/domain/*`, sem prova suficiente para fechar
LIMITES MANTIDOS:
- refinamento mantido como investigação, não como resolução
```

### TBD resolvido por decisão explícita do usuário
```text
MODE: TBD_SYNC
TBDS ALVO:
- TBD-021
TARGET SCOPE: unit:payments
DOCS ALTERADAS:
- docs/TBDS.md
- docs/units/payments/RULES.md
STATUS FINAL DOS TBDS:
- TBD-021 -> resolved
DELTA RESOLVIDO:
- ownership do retry policy registrado por decisão explícita do usuário, sem atribuir a origem à codebase
LIMITES MANTIDOS:
- decisão documentada como decisão, não como evidência factual da implementação
```
