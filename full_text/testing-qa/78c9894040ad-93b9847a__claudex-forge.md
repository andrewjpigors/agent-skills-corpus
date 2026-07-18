---
name: claudex-forge
description: |
  Plugin de desenvolvimento de software com revisao integrada do Codex (GPT). Ciclo completo: investigacao opcional -> plano -> revisao Codex -> implementacao com smoke test -> revisao em camadas -> revisao final.

  Acionar sempre que o usuario mencionar: implementar feature, corrigir bug, escrever migration, criar/editar funcao serverless, refatorar codigo, "manda pro codex", "revisa com codex", "codex review", "abre uma PR", "/claudex-forge".

  Filosofia: sequencial e continuo — nao pausa entre fases, so nos 7 casos taxativos abaixo. Fornece versionamento de plano + changelog, aprendizado entre runs, deteccao de loop e smoke test runtime.

  Tambem acionar quando o pedido vier so com os atalhos da skill: --build, --findbugs, --debug-browser, --full-investigate, --fiel, --desafio, --no-bench, --no-shot, "sem revisao", "so plano", "so implementa".

  NAO acionar para: consultas de dados no banco (usar MCP especifico do projeto), perguntas que nao envolvam codigo, leitura passiva de arquivos.
---

# /claudex-forge — Desenvolvimento com Revisao Integrada do Codex

> ⚠️ **Template — exige configuracao**
> Este plugin foi gerado a partir do template `claudex-forge`. Antes de usar, voce **precisa**:
> 1. Rodar `setup.sh` (na raiz do plugin) e preencher as variaveis do seu projeto (`claudex.config.json`)
> 2. Preencher `references/arquitetura.md` com a arquitetura do seu codebase
> 3. Preencher `references/boas-praticas.md` com convencoes do seu time
> 4. Preencher `references/codex-context.md` com as regras fixas que o Codex le antes de revisar
>
> Sem isso, a skill nao tem como saber o nome do seu projeto, paths, stack, MCPs disponiveis.

## ⚠️ Passo 0 — Sanity check rapido (PRIMEIRA acao)

O `setup.sh` ja verifica todos os pre-requisitos no momento da instalacao do plugin. Aqui em runtime, fazer apenas um **sanity check de 1 linha** pra cobrir o caso raro do usuario ter desinstalado algo apos o setup:

```bash
MISSING=""
for cmd in codex gh git; do
  command -v "$cmd" >/dev/null 2>&1 || MISSING="$MISSING $cmd"
done
[ -n "$MISSING" ] && echo "❌ Faltam CLIs:$MISSING — rode ./setup.sh no diretorio do plugin pra ver como instalar"
```

**Modo silencioso:** se passar, nao printar nada e seguir pra TodoList. Se faltar algo, mostrar a 1 linha acima e parar — o usuario rerroda o setup pra ver as instrucoes completas.

---

## ⚠️ PRIMEIRA acao obrigatoria — Criar TodoList do fluxo

**ANTES de qualquer outra coisa** (antes de ler references, antes de perguntar nada, antes de rodar Bash), crie a TodoList do fluxo usando o TaskCreate tool. Isso e o que mantem o fluxo coerente quando a skill esta dividida em capitulos — sem a TodoList, voce vai abrir o capitulo errado ou pular fase.

**Tarefas a criar (na ordem):**

1. `Setup inicial — gerar SLUG/TIMESTAMP/RUN_DIR/WORKTREE_DIR e detectar SO`
2. `Fase 0 — Investigacao (ler references/fase-0-investigacao.md)`
3. `Fase 1 — Plano: desenhar comportamento + plano + auditoria boas praticas (ler references/fase-1-plano.md)`
4. `Fase 2 — Revisao do Codex (ler references/fase-2-codex-revisao.md)`
5. `Fase 3 — Implementacao (ler references/fase-3-implementacao.md)`
6. `Fase 4 — Revisao e Relatorio (ler references/fase-4-revisao.md)`
7. `Fase 5 — Revisao final do Codex (ler references/fase-5-codex-final.md)`

**Regras de uso da TodoList:**
- Marcar `in_progress` ao ENTRAR em cada fase, antes de qualquer Read/Bash/Skill da fase.
- Marcar `completed` ANTES de avancar para a proxima tarefa.
- Se o atalho do usuario pular uma fase (ex: `--build` pula Fase 0; `"sem revisao"` pula Fases 2 e 5), marcar a fase pulada como `completed` com nota "pulada por atalho" no contexto.
- Se uma fase voltar (Codex pediu "Ajustar" e voce voltou pra Fase 2), criar nova entrada `Fase 2 — rodada 2` em vez de remarcar a antiga.

A TodoList aparece visivel pro usuario — se voce travar no meio, ele ve em qual fase parou.

---

## Estilo de comunicacao

**Aplicar o CLAUDE.md global** do projeto, se houver (`~/.claude/CLAUDE.md`):
- Linguagem de diretor (nao de engenheiro) — sem jargao denso; traduzir termo tecnico em 1 linha quando necessario
- Opcoes A/B/C com trade-off dos DOIS lados (o que ganha + o que perde)
- **Nao estimar tempo de implementacao** — usar risco/escopo/reversibilidade como criterio de decisao
- Tom direto, sem floreio; nao despejar saida crua de comando (filtrar antes)
- TL;DRs em formato de plano (problema / o que descobri / risco / solucao / decisao)

Essas regras valem em TODOS os artefatos desta skill (TL;DRs das Fases 1, 2 e 5, body de PR, AskUserQuestion, resumo final). Nao reescrever as regras aqui — referenciar.

**Matriz de escalonamento (LEI nesta skill) — o que sobe pro usuario e o que se decide sozinho:**
- **Decisao de engenharia pura NUNCA vira pergunta pro usuario** (nº de PRs, tamanho de PR, arquitetura interna, granularidade de commits, "revisabilidade", refactor agora-ou-depois): decide pelo padrao documentado, registra no `1-plan.md` ("decidi X porque Y, reversivel") e deixa os revisores da Fase 2 desafiarem. Perguntar isso so transfere chute pra quem nao tem como julgar.
- **SOBE SEMPRE, traduzido em consequencia observavel:** dado real de producao (recalcular historico, alterar/apagar registro existente), privacidade/seguranca/dados pessoais, dinheiro ou dependencia externa nova (servico pago, API externa, conta nova), prazo/interrupcao operacional, reversibilidade dificil, mudanca visivel na tela ou regra de negocio.
- **Todo risco exibido ao usuario tem 3 campos + veredito:** SE DER ERRADO (consequencia observavel) · QUANDO APARECERIA (agora / proximo deploy / quando crescer) · COMO DESCOBRIMOS E DESFAZEMOS (quem percebe + reversivel ou nao) → e fecha com veredito ("e por isso que recomendo A" ou "voce nao precisa decidir isso — trato como risco tecnico na PR"; nunca "pode ignorar").
- **Termos banidos em material de decisao** (descrevem desconforto do engenheiro, nao consequencia pro usuario): "dificulta revisao", "polui contexto", "PR grande", "complexidade", "manutenibilidade", "acoplamento", "debito tecnico", "escalabilidade" — achou um, reescreve em consequencia observavel antes de exibir.
- **Revisores nao substituem evidencia:** decisao registrada + revisada nao dispensa teste rodado, print, migration aplicada, diff conferido.

**A Fase 4 nao tem TL;DR formatado proprio** — usa linha unica de progresso (ver `references/fase-4-revisao.md` secao "Transicao para Fase 5"). O detalhe rico das 3 etapas vai pro `4-summary.md` em disco e aparece consolidado no template final da Fase 5.

---

## Maquina de estados

```
FASE 0 (Investigacao opcional) ──→ FASE 1 (Plano: P0 + 3 passos) ──→ FASE 2 (Revisao Codex) ──→ decisao?
        │                          P0 pesquisa/benchmark (cond.)        ↑                        │
        ├─ findbugs (codigo)       P1 desenhar comportamento            └── Ajustar ─────────────┘
        ├─ debug-browser (runtime) P2 plano + ancoragem                                          │
        └─ pular                   P3 auditoria boas praticas           Seguir ──────────────────┘
                                                                                       ↓
                                                FASE 3 (Implementacao) ──→ FASE 4 (Revisao + Relatorio)
                                                                               ↓
                                                              FASE 5 (Revisao Final Codex) ──→ Postar
```

**Regra de ouro:** ao terminar uma fase, anuncie "Fase X concluida. Iniciando Fase Y..." e avance. Nunca pare entre fases esperando permissao — o usuario ja autorizou o fluxo completo ao acionar esta skill.

### 🔒 SUSPENSAO DE MEMORIA GLOBAL durante /claudex-forge

**Enquanto este fluxo estiver ativo (Fase 0 ate fim da Fase 5), as seguintes regras globais ficam SUSPENSAS:**

- ❌ Qualquer regra do tipo "apos `gh pr create`, sempre abrir a URL da PR no navegador" — **SUSPENSA**. Nao abrir o link da PR no navegador em nenhuma fase exceto na Fase 5 com decisao "Seguir".

**Por que:** o usuario nao pode ver/clicar Merge na PR antes do Codex revisar o codigo final (Fase 5). Se a PR for aberta no navegador antes disso, ele acaba mergeando enquanto a revisao ainda esta rodando.

**Liberacao:** so na Fase 5, apos o Codex retornar "Seguir", roda `gh pr ready <PR>` (converte draft em pronta) e ai sim `$OPEN_CMD <URL>` (resolvido por SO no Setup inicial).

### 🚫 ExitPlanMode BANIDO durante /claudex-forge

**Nunca chamar o tool `ExitPlanMode` em nenhuma fase do fluxo /claudex-forge.** O box nativo do Claude Code ("Ready to code? / Here is Claude's plan / Would you like to proceed?") atropela o template da Fase 1 e despeja o plano completo cru no terminal, ignorando o TL;DR formatado (🧨/🔎/⏰/💡/👉).

**Por que:** o /claudex-forge ja tem checkpoint proprio de aprovacao de plano (Fase 2 final — o usuario aprova o plano final consolidado antes da Fase 3). ExitPlanMode duplica esse checkpoint com formato errado e quebra o fluxo de TL;DR + arquivo separado.

**Comportamento correto:**
- Se a sessao ja esta em plan mode quando /claudex-forge e acionado: avisar "saindo do plan mode pra rodar o fluxo /claudex-forge proprio" e continuar normalmente.
- **Nunca** entrar em plan mode dentro do /claudex-forge.
- **Nunca** chamar `ExitPlanMode` em nenhuma fase — o plano sempre vai pra `${RUN_DIR}/1-plan.md` + TL;DR formatado no terminal conforme `references/fase-1-plano.md`.

**Anti-padrao real (observado em uso):** o modelo entrou em plan mode no meio do fluxo e usou ExitPlanMode no fim da Fase 1, exibindo o plano tecnico completo de 200+ linhas no terminal em vez do TL;DR de 5 blocos. Resultado: o usuario nao tinha como ler aquilo em linguagem de diretor.

### Caminhos do run

**SEMPRE** use `${RUN_DIR}/...` com os nomes numerados:
- `${RUN_DIR}/1-plan.md` (arquivo de trabalho) + `1-plan-v<N>.md` (snapshots) + `1-plan-final.md`
- `${RUN_DIR}/2-review-r<N>.md` + `2-changelog.md`
- `${RUN_DIR}/3-smoke-test.md` (se aplicavel)
- `${RUN_DIR}/4-summary.md`
- `${RUN_DIR}/5-final-review.md`

`${RUN_DIR}` e definido pelo Setup inicial abaixo (resolve por SO automaticamente). Se voce nao tiver `${RUN_DIR}` na sessao, volte ao Setup inicial.

### Nao presumir — regua de fato vs. intencao

Antes de **afirmar algo como verdade** ou de **seguir com uma decisao**, classifique a duvida. As duas metades tem tratamento OPOSTO:

- **Duvida de FATO** (esse arquivo existe? a coluna se chama assim? a causa do bug e essa? essa API funciona desse jeito?) → **nunca chute e nunca pergunte ao usuario** — **VERIFIQUE na fonte real**: codigo (grep/Read), banco de dados (MCP do seu backend, se houver), doc viva (WebFetch / pesquisa web). O modelo "lembra" de um fato errado com a mesma confianca com que acerta; so a verificacao separa os dois. E perguntar ao usuario um fato que voce mesmo pode checar tambem e erro — ele ve o codigo/banco direto, nao quer ser o seu grep.
- **Duvida de INTENCAO / decisao de negocio** (qual escopo ele quer? qual das 2 interpretacoes? trocar esse comportamento muda uma regra de negocio?) → **nao presuma**: mostre as opcoes e pergunte (caso #5 abaixo + bloco 🔎 divergente da Fase 1).

O erro que esta regua existe pra matar e **cravar fato sem verificar** — causa-raiz de diagnostico errado (ex: cravar "a causa e a integracao externa X" sem testar; era um token vencido que um request de teste pegaria na hora). Ela aumenta a VERIFICACAO de fato, **nao** o numero de perguntas — esta skill e anti-interrupcao de proposito, e isso continua valendo.

### Quando parar para perguntar (taxativo)

Pause **APENAS** nestes 7 casos. Em qualquer outra situacao, anuncie a proxima fase e siga.

1. **Escolha da Fase 0** — perguntar opcao 1-5 (construir / findbugs / debug-browser / os dois / pular). Excecao: usuario usou atalho (`--build`, `--findbugs`, etc.).
2. **Codex retornou "Ajustar" (com algum item em produto/dado/regra de negocio) ou "Bloquear"** — Fase 2 ou Fase 5. Ver criterio detalhado em `references/fase-2-codex-revisao.md` secao "Como decidir o que aplicar". Se "Ajustar" com todos ajustes internos, NAO pausar — aplicar sozinho e seguir.
3. **RECIBO DE PLANO — aprovacao antes da Fase 3 (trava dura, sem excecao)** — a Fase 3 SO comeca se estes 4 itens existirem NO CHAT, visiveis: (a) o TL;DR do plano **FINAL pos-revisores** (a versao que o Codex aprovou — nunca uma versao anterior) exibido nos 5 blocos 🧨🔎⏰💡👉; (b) a decisao pedida ao usuario de forma explicita; (c) a aprovacao explicita dele; (d) escopo aprovado + o que ficou FORA do escopo. Se voce se pegar implementando sem ter exibido o plano — mesmo "achando" que ele ja sabia, mesmo que o pedido pareca obvio — e parada obrigatoria: exiba o recibo e aguarde. Anti-padrao real: solucao entregue sem plano na tela = usuario sem como decidir. Ver `fase-2-codex-revisao.md` secao "Aprovacao do plano final".
4. **Acao irreversivel pendente** — migration destrutiva (DROP, ALTER TYPE, RENAME, regra de seguranca modificada), force-push, reset --hard, deletar branch com trabalho. Mostrar o que vai fazer e pedir autorizacao especifica. Migrations aditivas (CREATE, ADD COLUMN nullable) nao precisam pausa adicional alem da Fase 2. **MAS classifique pelo EFEITO, nao so pela forma do DDL:** uma migration que ALTERA DADO REAL QUE JA EXISTE — backfill (UPDATE/DELETE em massa de registro existente), `INSERT ... SELECT` sobre dado de producao, trigger que muda o comportamento de escrita de dado de negocio — TAMBEM pausa e pede autorizacao especifica, mesmo sendo "aditiva" na forma. Por que: a Fase 3 aplica a migration no banco vivo ANTES do merge, entao isso entra em producao dentro do run automatico, sem o usuario ver. NAO confundir com trigger/funcao puramente tecnica sem impacto em dado real existente (essa segue normal) — o gatilho e: altera dado existente, dado sensivel, ou comportamento futuro de escrita em producao?
5. **Ambiguidade real no pedido original** — pedido vago com 2+ interpretacoes plausiveis. Criterio objetivo: e vago quando falta verbo de acao concreto OU falta objeto especifico. Exemplos: "melhora o CRM" (vago, sem alvo), "ajusta isso" (vago, sem objeto). Nao vago: "adiciona campo telefone na tela UserDetailModal" (claro). Quando vago: listar opcoes, esperar escolha.
6. **Usuario pediu pausa explicitamente** — "para ai", "deixa eu ver", "espera", "mostra antes".
7. **Checkpoint visual da Fase 3** — quando o diff toca tela, mostrar o screenshot e aguardar aprovacao visual ANTES de commitar (gate duro com escape `"sem print"`). Esta pausa e obrigatoria, nao cai nos anti-padroes de "nao pare". Ver `references/fase-3-implementacao.md` secao "Gate do checkpoint visual".

### Quando NAO parar (anti-padroes proibidos)

- ❌ **Apos fase concluida sem issues** ("Code Review nao achou nada. Sigo?") → seguir direto
- ❌ **Antes de fase de leitura/relatorio** (Fase 4 e Fase 5 nao tem efeito colateral no primeiro passo) → seguir direto
- ❌ **"Proximo passo: X. Sigo?"** quando X e a proxima fase prevista no fluxo → trocar por "Iniciando X." e executar
- ❌ **Mostrar tabela de resultados positivos e perguntar se continua** → mostra e segue na mesma mensagem
- ❌ **Pedir confirmacao para algo que o usuario ja autorizou ao acionar /claudex-forge** → o acionamento e a autorizacao do fluxo completo
- ❌ **Apos abrir PR (fim da Fase 3), perguntar "rodo a revisao agora?"** → Fase 4 e parte do fluxo, segue direto
- ❌ **Code Review (etapa 1 de 3 da Fase 4) terminou sem issues, perguntar "tem mais algo?" ou "sigo?"** → Code Review NAO e fim da Fase 4. Anunciar "Iniciando Simplify" e seguir direto.
- ❌ **Apos sub-skill (`code-review`, `simplify`, `security-review`) devolver controle, pausar antes de iniciar a proxima etapa** — sub-skill retornar NAO e um dos 7 casos taxativos de pausa. Anuncie o resultado E invoque a proxima coisa na MESMA mensagem. Padrao observado em uso real: o modelo pausa aqui mesmo com as regras "sequencial e continuo" carregadas — a regra existe mas fica longe do ponto de decisao. Cada etapa de `fase-4-revisao.md` tem um bloco 🚨 POS-RETORNO logo apos a invocacao da sub-skill pra reforcar isso no momento certo.
- ❌ **Rodar 2 etapas em paralelo na Fase 4** — cada etapa precisa do codigo pos-etapa-anterior. Ver `references/fase-4-revisao.md`.

### Sequencial e continuo — exemplos concretos

A Fase 4 (e a transicao Fase 4 → Fase 5) e o ponto onde o modelo mais erra. Use este padrao:

```
❌ ERRADO #1 — pausa esperando o usuario
"Code Review: 3 issues corrigidos. Sigo pra Simplify?"
[devolve controle pro chat e espera resposta]

❌ ERRADO #2 — pula pra paralelo
[invoca code-review E simplify na mesma chamada de tool]
→ quebra a corrente: simplify precisa do codigo JA corrigido pelo code-review.

✅ CERTO — sequencial e continuo
"Code Review: 3 issues corrigidos. Iniciando Simplify."
[NO MESMO TURNO, depois de atualizar state.json, invoca a Skill simplify
 — sem devolver controle pro chat, sem esperar autorizacao]
```

**Sequencial** = uma etapa termina, a proxima comeca (ordem fixa: code_review → simplify → security_review → finalize_phase_4.sh).
**Continuo** = sem devolver controle pro usuario entre as etapas.

"No mesmo turno" e diferente de "na mesma chamada de tool":
- Mesma chamada de tool = paralelo (proibido nas etapas de revisao)
- Mesmo turno = sequencial sem pausa de chat (correto)

A unica forma de pausa permitida dentro da Fase 4 e os 7 casos da secao "Quando parar para perguntar" acima.

### Tabela de decisao rapida

| Situacao | Acao |
|----------|------|
| Code Review terminou sem issues novos | Anunciar **Simplify** e seguir |
| Simplify terminou sem mudancas | Anunciar **Security Review** e seguir |
| Security Review terminou | Rodar `scripts/finalize_phase_4.sh` (1 chamada Bash que gera `4-summary.md`, atualiza state, imprime linha de progresso e dispara `codex exec` da Fase 5) — sua proxima resposta comeca com o tool call, sem texto antes |
| Codex (Fase 2 ou 5) retornou "Seguir" | Anunciar proxima fase e seguir |
| Codex retornou "Ajustar" — TODOS os ajustes internos | Aplicar/rejeitar sozinho, nova rodada no mesmo turno (NAO pausar) |
| Codex retornou "Ajustar" — algum item de produto/dado/regra | Pausar SO nesse item, perguntar em linguagem de diretor |
| Codex retornou "Bloquear" | Pausar, discutir |
| Codex pediu "Ajustar" pela 4a rodada seguida | Pausar (limite de 3 rodadas automaticas estourou) |
| Plano inclui migration aditiva (so estrutura, nao toca dado existente) | Avancar (autorizacao ja dada na Fase 2) |
| Plano inclui migration destrutiva | Pausar antes de aplicar, autorizacao especifica |
| Migration mexe em DADO REAL existente (backfill UPDATE/DELETE, trigger de escrita sobre dado de negocio) | Pausar antes de aplicar, autorizacao especifica (entra em producao antes do merge) |
| Pedido inicial era vago e ha 2+ interpretacoes | Pausar, listar opcoes |
| Pedido inicial estava claro | Seguir direto, sem perguntar |
| Fase 5 retornou "Seguir" | Informar PR pronta, fim do fluxo |

---

## ⚠️ Setup inicial OBRIGATORIO (PRIMEIRA acao apos criar a TodoList)

**Esta e a PRIMEIRA acao apos criar a TodoList, ANTES de qualquer fase, ANTES de qualquer pergunta ao usuario.**

**Regra:** se voce ainda nao definiu `RUN_DIR`, voce **NAO PODE** salvar planos, revisoes, relatorios ou qualquer arquivo do fluxo.

**Toda execucao de `/claudex-forge` comeca gerando um identificador unico** que vai ser usado em todas as fases. Isso evita colisao quando voce roda `/claudex-forge` em terminais paralelos.

> Os valores `{{...}}` abaixo sao substituidos pelo `setup.sh` lendo `claudex.config.json`. Se voce ainda ve `{{...}}` literal aqui, o setup nao rodou — pare e rode `./setup.sh` na raiz do plugin.

```bash
# Slug curto baseado no pedido. Python translitera acento (NFKD): o `tr -cd` puro APAGA
# acentos ("adicao de campo" virava "adio-de-campo"), e o `iconv //TRANSLIT` do BSD/Mac
# corrompe (mete til, come letras). Python normaliza igual nos 3 sistemas. Pedido vai por
# env var (nao argv/stdin) pra preservar UTF-8.
SLUG=$(PEDIDO_SLUG="$PEDIDO" python3 -c "import os,unicodedata,re; s=unicodedata.normalize('NFKD',os.environ.get('PEDIDO_SLUG','')).encode('ascii','ignore').decode().lower(); print(re.sub(r'[^a-z0-9]+','-',s).strip('-')[:30])" 2>/dev/null)
[ -z "$SLUG" ] && SLUG="task"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

# Guard: TIMESTAMP precisa ter formato YYYYMMDD-HHMMSS completo.
if ! [[ "$TIMESTAMP" =~ ^[0-9]{8}-[0-9]{6}$ ]]; then
  # Fallback no MESMO formato (8 digitos - 6 digitos), senao o nome do run sai fora do padrao
  TIMESTAMP="$(date +%Y%m%d)-$(printf '%06d' "$((RANDOM % 1000000))")"
  echo "⚠️  TIMESTAMP veio incompleto, ajustado pra: $TIMESTAMP"
fi

# Deteccao de SO — paths configurados via setup.sh, definidos em claudex.config.json
#
# SKILL_DIR_ABS = pasta absoluta DESTA skill (contem scripts/ e references/).
# FONTE DA VERDADE: o "Base directory for this skill" que o harness te informou ao
# carregar /claudex-forge. Se voce tem esse valor, exporte-o ANTES deste bloco
# (`export SKILL_DIR_ABS="<base dir>"`) — o `${SKILL_DIR_ABS:-...}` abaixo preserva ele.
# Os defaults por SO sao so fallback.
case "$(uname -s)" in
  MINGW*|MSYS*|CYGWIN*)
    OS_KIND="windows"
    RUN_DIR_BASE="{{RUN_DIR_BASE_WIN}}"
    WORKTREE_BASE="{{WORKTREE_BASE_WIN}}"
    REPO_DIR="{{REPO_PATH_WIN}}"
    OPEN_CMD="start"
    ;;
  Darwin)
    OS_KIND="mac"
    RUN_DIR_BASE="{{RUN_DIR_BASE_MAC}}"
    WORKTREE_BASE="{{WORKTREE_BASE_MAC}}"
    REPO_DIR="{{REPO_PATH_MAC}}"
    OPEN_CMD="open"
    ;;
  *)
    OS_KIND="linux"
    RUN_DIR_BASE="{{RUN_DIR_BASE_LINUX}}"
    WORKTREE_BASE="{{WORKTREE_BASE_LINUX}}"
    REPO_DIR="{{REPO_PATH_LINUX}}"
    OPEN_CMD="xdg-open"
    ;;
esac

# SKILL_DIR_ABS — use o "Base directory for this skill" do harness se exportado;
# senao tenta o caminho padrao de plugin instalado do Claude Code.
SKILL_DIR_ABS="${SKILL_DIR_ABS:-$HOME/.claude/plugins/cache/{{REPO_OWNER}}/claudex-forge/skills/claudex-forge}"

RUN_DIR="${RUN_DIR_BASE}/${SLUG}-${TIMESTAMP}"
WORKTREE_DIR="${WORKTREE_BASE}/${SLUG}-${TIMESTAMP}"
BRANCH="feat/${SLUG}-${TIMESTAMP}"

# Sanity check ANTES do mkdir: no Mac, `mkdir -p "D:/..."` criaria pasta
# literal `D:` dentro do CWD sem erro. Checar a string ANTES de criar — depois
# de criada, a pasta errada ja existe e o check nao desfaz nada.
if [ "$OS_KIND" != "windows" ] && [[ ! "$RUN_DIR" =~ ^/ ]]; then
  echo "❌ RUN_DIR nao e caminho absoluto Unix: $RUN_DIR — abort (nada foi criado)"
  exit 1
fi

mkdir -p "$RUN_DIR"
[ ! -d "$RUN_DIR" ] && echo "❌ mkdir falhou em $RUN_DIR" && exit 1

# ⚠️ ISOLAMENTO DE SESSAO — CRIAR WORKTREE IMEDIATAMENTE
#
# Usuarios frequentemente rodam varias sessoes /claudex-forge em paralelo.
# O working tree principal ($REPO_DIR) tem UM UNICO HEAD por pasta — se duas
# sessoes rodam `git checkout` simultaneamente la, uma sobrescreve a outra
# (HEAD nao tem locking). Resultado ja observado: commits indo parar em
# branches da outra sessao.
#
# Solucao: cada execucao do /claudex-forge tem seu proprio worktree (pasta
# separada apontando pro mesmo .git, com HEAD independente). Criado AQUI,
# no setup, antes de qualquer git command. Nao na Fase 3 — la e tarde demais
# (Fase 0/1/2 ja teriam rodado na pasta compartilhada).

if ! git -C "$REPO_DIR" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "❌ $REPO_DIR nao e um repo git valido — abort"
  exit 1
fi

# `fetch` sincroniza referencias do remoto SEM mexer no HEAD do working tree
# principal — outras sessoes nao sao afetadas. Usamos `origin/main` como base
# do worktree pra ele comecar atualizado.
git -C "$REPO_DIR" fetch --quiet origin main

if [ -d "$WORKTREE_DIR" ]; then
  echo "ℹ️  Worktree ja existe em $WORKTREE_DIR — reusando"
else
  git -C "$REPO_DIR" worktree add "$WORKTREE_DIR" -b "$BRANCH" origin/main \
    || { echo "❌ git worktree add falhou — abort"; exit 1; }
fi

# CWD da sessao = worktree. O working directory persiste entre chamadas Bash DIRETAS —
# mas sub-skills (code-review, simplify, etc) podem desvia-lo. Por isso existe o
# invariante de isolamento mais abaixo: ao voltar de qualquer sub-skill, conferir o CWD.
cd "$WORKTREE_DIR"

# Inicializar state.json com fase atual
echo '{"phase":0,"step":null,"status":"in_progress","pr":null}' > "$RUN_DIR/state.json"

# ⚠️ GUARD — SKILL_DIR_ABS precisa apontar pra pasta REAL da skill (com scripts/).
# Sem isso o finalize_phase_4.sh (transicao Fase 4 -> 5) aborta com exit 1, e o
# fluxo trava no fim da Fase 4 esperando voce pedir. Falha aqui, alto e cedo:
if [ ! -f "${SKILL_DIR_ABS}/scripts/finalize_phase_4.sh" ]; then
  echo "❌ SKILL_DIR_ABS errado: $SKILL_DIR_ABS (nao achei scripts/finalize_phase_4.sh)."
  echo "   Use o 'Base directory for this skill' que o harness te deu: exporte"
  echo "   SKILL_DIR_ABS=<base dir> e re-rode o setup inicial."
  exit 1
fi

# ⚙️ env.sh — fonte UNICA das variaveis do run. Em vez de cada fase remontar 10
# variaveis na mao (e esquecer SKILL_DIR_ABS — causa-raiz do trava da Fase 4->5),
# elas fazem `source "$RUN_DIR/env.sh"`. Valores ja resolvidos, baked no arquivo.
cat > "$RUN_DIR/env.sh" <<EOF
export SLUG="$SLUG"
export TIMESTAMP="$TIMESTAMP"
export OS_KIND="$OS_KIND"
export RUN_DIR="$RUN_DIR"
export RUN_DIR_BASE="$RUN_DIR_BASE"
export WORKTREE_BASE="$WORKTREE_BASE"
export WORKTREE_DIR="$WORKTREE_DIR"
export BRANCH="$BRANCH"
export REPO_DIR="$REPO_DIR"
export OPEN_CMD="$OPEN_CMD"
export SKILL_DIR_ABS="$SKILL_DIR_ABS"
EOF

# 🗺️ MAPA DO CODIGO (OPCIONAL) — pista de navegacao + impacto cruzado.
#
# Se a sessao tiver uma ferramenta de grafo de codigo disponivel (qualquer uma que
# gere um mapa de dependencias AST do repo), construa o mapa do worktree aqui e passe
# o caminho como PISTA pros revisores. E um ATALHO, NUNCA um pre-requisito: em qualquer
# maquina onde nao exista, o fluxo segue normal com grep/Read, sem avisar nem perguntar.
#
# Resolucao portatil: ache o binario pelo PATH (`command -v`). Nao dependa de um binario
# interno especifico — se a sua instalacao usa outro nome, ajuste GRAPH_TOOL no
# claudex.config.json. graphify-out/ deve estar no .gitignore -> nao suja a PR.
GRAPH_OK=false
GRAPH_PATH=""
GRAPH_TOOL_BIN="$(command -v "${GRAPH_TOOL:-graphify}" 2>/dev/null || true)"
if [ -n "$GRAPH_TOOL_BIN" ] && "$GRAPH_TOOL_BIN" --help >/dev/null 2>&1; then
  echo "🗺️  Grafo de codigo disponivel — construindo o mapa (cwd ja e o worktree)..."
  if "$GRAPH_TOOL_BIN" update >/dev/null 2>&1 && [ -f "$WORKTREE_DIR/graphify-out/graph.json" ]; then
    GRAPH_OK=true
    GRAPH_PATH="$WORKTREE_DIR/graphify-out/graph.json"
    echo "✅ Mapa do codigo pronto: $GRAPH_PATH"
  else
    echo "ℹ️  Ferramenta de grafo presente mas build falhou — fluxo segue com grep (sem mapa)"
  fi
else
  echo "ℹ️  Nenhum grafo de codigo disponivel — fluxo segue normal com grep/Read"
fi

# Anexa o estado do grafo ao env.sh (vazio/false quando nao houver — fases tratam isso)
cat >> "$RUN_DIR/env.sh" <<EOF
export GRAPH_OK="$GRAPH_OK"
export GRAPH_PATH="$GRAPH_PATH"
export GRAPH_TOOL_BIN="$GRAPH_TOOL_BIN"
EOF

echo "✅ Run setup: OS=$OS_KIND"
echo "   RUN_DIR=$RUN_DIR"
echo "   WORKTREE_DIR=$WORKTREE_DIR (branch $BRANCH)"
echo "   SKILL_DIR_ABS=$SKILL_DIR_ABS"
echo "   env.sh salvo — fases seguintes fazem: source \"\$RUN_DIR/env.sh\""
```

**Anote `SLUG`, `TIMESTAMP`, `OS_KIND`, `RUN_DIR`, `RUN_DIR_BASE`, `WORKTREE_BASE`, `WORKTREE_DIR`, `BRANCH`, `REPO_DIR`, `OPEN_CMD`, `SKILL_DIR_ABS`, `GRAPH_OK`, `GRAPH_PATH` no contexto da sessao.** Todas tambem ficam salvas em `${RUN_DIR}/env.sh` — qualquer fase que precise delas faz `source "$RUN_DIR/env.sh"` em vez de regerar. Isso vale especialmente pra Fase 2, Fase 4 e Fase 5, que dependem de `SKILL_DIR_ABS` (e era justamente ele que vinha vazio e travava a transicao Fase 4 -> 5).

### 🔒 Invariante de isolamento (vale em TODAS as fases)

Apos o setup inicial, o CWD da sessao **deve sempre** ser `$WORKTREE_DIR`. Nunca `cd "$REPO_DIR"` durante o fluxo (excecao unica: cleanup pos-merge, na Fase 5).

Se um comando reseta o CWD (alguns sub-skills fazem isso), **a proxima coisa que voce faz e voltar pro worktree**: `cd "$WORKTREE_DIR"`. Nao "vou rodar so uma coisinha no repo principal" — qualquer git command la quebra o isolamento.

Guard rapido no comeco de qualquer fase que tenha duvida:
```bash
if [ "$(pwd)" != "$WORKTREE_DIR" ]; then
  echo "⚠️  CWD desviou: $(pwd) — voltando pro worktree"
  cd "$WORKTREE_DIR"
fi
```

**Comunicacao obrigatoria ao usuario** apos o setup:

```
🗂️  Run iniciado: <SLUG>-<TIMESTAMP>
    RUN_DIR: <caminho>
    BRANCH: <nome>
```

Sem essa linha visivel ao usuario, ele nao sabe onde os arquivos do run estao.

**Estrutura de arquivos do run:**

```
${RUN_DIR}/
├── 0-findbugs-report.md           (opcional, Fase 0)
├── 0-debug-browser-report.md      (opcional, Fase 0)
├── 0-benchmark.md                 (opcional, Fase 1 Passo 0 — pesquisa de mercado quando organiza area de negocio)
├── 1-plan.md                      (arquivo de trabalho — sempre a versao atual)
├── 1-plan-v1.md                   (snapshot do plano original — nunca modificado)
├── 1-plan-v2.md                   (snapshot apos rodada 1 de ajustes)
├── 1-plan-v3.md                   (snapshot apos rodada 2 — se houver)
├── 1-plan-final.md                (copia da versao aprovada — usada pela Fase 3)
├── 1-plan-tldr.md                 (TL;DR do plano final, exibido no terminal)
├── 1-spec-items.md                (OBRIGATORIO sempre que houver referencia de design — Figma/print/prototipo; inventario numerado com extracao dupla cega; ausente so em task sem design)
├── handoff-pr-2.md                (so quando o run dividiu em 2 PRs — heranca da 2ª PR, escrito ANTES do merge da 1ª)
├── 2-review-r1.md                 (Fase 2 rodada 1 — markdown do Codex)
├── 2-review-r2.md                 (Fase 2 rodada 2, se houver)
├── 2-review-r3.md                 (Fase 2 rodada 3, se houver — max)
├── 2-review-tldr.md               (TL;DR consolidado de todas as rodadas)
├── 2-changelog.md                 (mudancas do plano original ao final, por rodada)
├── 3-smoke-test.md                (opcional — se Fase 3 rodou smoke test em funcao serverless/migration/RPC)
├── 4-summary.md                   (Fase 4 — input curto pro Codex Fase 5, gerado por finalize_phase_4.sh)
├── 5-final-review.md              (Fase 5 — output do Codex; sobrescrito a cada rodada se houver "Ajustar")
├── _achados-pendentes.md          (opcional — bugs achados FORA do escopo acumulados no run; efemero, decididos nos checkpoints [c]/[a]/[d])
├── state.json                     (checkpoint — fase/etapa atual)
└── env.sh                         (variaveis do run — fonte unica; fases fazem `source env.sh`)
```

**Acervo entre runs (em `${RUN_DIR_BASE}`, um nivel acima dos runs individuais):**
- `_patterns.md` — padroes tecnicos aprendidos (erros recorrentes que o Codex ja corrigiu). Lido no Passo 0 da Fase 1.
- `_benchmarks.md` — acervo de benchmark de produto por area de negocio (o que ja descobrimos sobre como o mercado organiza listas, kanban, fluxos de cadastro, etc). Lido e atualizado pelo Passo 0 da Fase 1 (ver `references/fase-1-benchmark.md`). E o que faz o repertorio de produto crescer entre features, em vez de pesquisar do zero toda vez.
- `_achados-adjacentes.md` — caderninho persistente de bugs achados FORA do escopo da tarefa. Cada `[a]` aprovado num checkpoint vira uma linha aqui, pronta pra virar tarefa propria (`/claudex-forge --build`). Ver `references/achados-adjacentes.md`.

## 📍 state.json — checkpoint do fluxo

`${RUN_DIR}/state.json` rastreia onde voce esta. **Toda acao com efeito colateral** (chamada Agent, `codex exec`, `gh pr`) **DEVE** comecar lendo este arquivo. **Toda transicao** (entre fases ou entre etapas da Fase 4) **DEVE** atualiza-lo ANTES de prosseguir.

**Schema:**
```json
{ "phase": 4, "step": "code_review", "status": "in_progress", "pr": 285 }
```

- `phase`: 0-5
- `step`: na Fase 4 — `code_review` | `simplify` | `security_review`. (Nao existem steps `summary`/`completed` na pratica: o `finalize_phase_4.sh` fecha a Fase 4 escrevendo direto `{phase: 5, step: null}` — nao espere encontra-los no state.json.) Na Fase 3, quando o diff toca tela — `visual_checkpoint` (gate do print, ver `references/fase-3-implementacao.md`). `null` nas demais fases.
- `status`: `in_progress` | `completed` | `blocked`
- `visual`: so quando houve checkpoint visual na Fase 3 — `approved` | `skipped_escape` | `blocked_failure`. So commitar UI com `approved` ou `skipped_escape`.
- `pr`: numero da PR (a partir da Fase 3)

**Quando escrever:**
- Inicio de cada fase: `{phase: N, step: <primeiro ou null>, status: in_progress}`
- Transicao entre etapas da Fase 4: `{phase: 4, step: <proxima>, status: in_progress}`
- Fim de fase: `{phase: N, status: completed}` ANTES de anunciar a proxima

---

## Fluxo das fases — leia o capitulo certo

A SKILL.md tem so o esqueleto. **Para cada fase, leia o arquivo de reference indicado abaixo NO MOMENTO em que entrar nessa fase** (nao antes — economia de contexto):

| Fase | Quando entra | Arquivo a ler |
|------|--------------|---------------|
| 0 | Apos Setup inicial, se houver duvida sobre investigacao | `references/fase-0-investigacao.md` |
| 1 | Apos Fase 0 (ou direto, se atalho `--build`) | `references/fase-1-plano.md` |
| 2 | Apos plano salvo em `1-plan.md` | `references/fase-2-codex-revisao.md` |
| 3 | Apos Codex aprovar plano + usuario aprovar plano final | `references/fase-3-implementacao.md` |
| 4 | Apos PR draft criada | `references/fase-4-revisao.md` |
| 5 | Apos `4-summary.md` salvo | `references/fase-5-codex-final.md` |

**Sequencia padrao em cada fase:**
1. Marcar a tarefa correspondente como `in_progress` na TodoList
2. Ler o arquivo de reference indicado acima (1 Read)
3. Executar os passos da fase conforme o reference
4. Atualizar `state.json` ao terminar
5. Marcar a tarefa como `completed` na TodoList
6. Anunciar "Fase X concluida. Iniciando Fase Y..." e avancar (sem perguntar)

---

## Atalhos

**Por padrao a Fase 1 roda o Passo 0 condicional + os 3 passos completos** (pesquisa/benchmark → desenhar comportamento → plano + ancoragem → auditoria de boas praticas). O usuario pode pular passos/fases dizendo:
- **"sem revisao"** — pula Fase 2 e Fase 5 (implementa direto, sem Codex)
- **"so plano"** — executa apenas Fase 1 e Fase 2
- **"so implementa"** ou **`--build`** — pula o Passo 0 e o Passo 1 (desenho) da Fase 1, vai direto pro plano/implementacao (quando o plano ja foi discutido)
- **"sem brainstorming"** ou **`--fiel`** — pula o Passo 1 de desenho de comportamento; usa o que ja foi dito
- **"sem benchmark"** ou **`--no-bench`** — pula o benchmark de produto do Passo 0; segue pro Passo 1
- **"sem pesquisa"** — pula o Passo 0 inteiro (benchmark de produto + pesquisa tecnica)
- **"sem skills"** — pula o Passo 3 (auditoria de boas praticas da stack) na Fase 1
- **"sem print"** ou **`--no-shot`** — pula o gate do checkpoint visual na Fase 3 (so pra mudanca de tela trivial; ver `references/fase-3-implementacao.md`)
- **`--desafio`** ou **"questiona antes"** — forca o Claude a desenhar/questionar o comportamento mesmo se a premissa parecer firme

> Nota: a Fase 1 NAO pergunta "Fiel ou Desafio?" / "decisao fechada ou pode mudar?". Por padrao ela desenha o comportamento (Passo 1, via `superpowers:brainstorming`) ANTES de listar arquivos, e audita o plano com as skills da stack (Passo 3) ANTES do Codex. Ver `references/fase-1-plano.md`.

**Atalhos da Fase 0 (investigacao):**
- **`--build`** ou **"so construir"** — pula a Fase 0 inteira, vai direto pra Fase 1
- **`--findbugs`** ou **"caca bug em [arquivo]"** — forca opcao 2 (so `findbugs`), pula a pergunta inicial
- **`--debug-browser`** ou **"investiga runtime de [tela]"** — forca opcao 3 (so `debug-browser`), pula a pergunta inicial
- **`--full-investigate`** ou **"investiga tudo em [tela]"** — forca opcao 4 (debug-browser + findbugs)

Quando um atalho pular uma fase, **ainda marcar a tarefa correspondente como `completed`** na TodoList com nota "pulada por atalho".

---

## Referencia rapida de arquivos

```
skills/claudex-forge/
├── SKILL.md                          (este arquivo — esqueleto + setup)
├── scripts/
│   ├── finalize_phase_4.sh          (encerra Fase 4 + dispara Fase 5 numa unica chamada, com vigia de tempo)
│   └── safe-merge.sh                (roda os checks e SO mergeia se todos passarem)
└── references/
    ├── arquitetura.md                (PREENCHIDO PELO USUARIO — schema, paginas, funcoes, componentes)
    ├── boas-praticas.md              (PREENCHIDO PELO USUARIO — conventional commits, regras de codigo, comandos de deploy)
    ├── codex-context.md              (PREENCHIDO PELO USUARIO — contexto fixo do projeto pra Codex; lido pelo finalize_phase_4.sh)
    ├── achados-adjacentes.md         (caderninho de bugs achados FORA do escopo — checkpoints [c]/[a]/[d])
    ├── fase-0-investigacao.md        (Fase 0)
    ├── fase-1-plano.md               (Fase 1)
    ├── fase-1-benchmark.md           (Fase 1 — Passo 0 benchmark de produto)
    ├── fase-2-codex-revisao.md       (Fase 2)
    ├── fase-3-implementacao.md       (Fase 3)
    ├── fase-4-revisao.md             (Fase 4)
    └── fase-5-codex-final.md         (Fase 5)
```

`arquitetura.md` e `boas-praticas.md` sao lidos sob demanda dentro da Fase 1 (planejar) e Fase 3 (implementar). `codex-context.md` e lido pelo `codex exec` automaticamente (ele e passado como path absoluto pro prompt do Codex). A skill `checks-local` (gate de testes/typecheck) e instalada separadamente como sub-skill do plugin — ver README.

---

## Ferramentas e ambiente — CONFIGURAR PELO USUARIO

**Esta secao e parcialmente auto-detectada pelo setup, mas o usuario deve revisar.** O detalhamento da stack vive em `references/arquitetura.md` e `references/boas-praticas.md`.

### CLIs esperadas

| CLI | Uso |
|---|---|
| `git` | Operacoes locais — OBRIGATORIO |
| `codex` | Revisao do plano (Fase 2) e revisao final (Fase 5) — OBRIGATORIO |
| `gh` | GitHub (PRs, draft, ready, merge, leitura de repo) — OBRIGATORIO. **No Mac**, se o `gh` nao estiver logado direto, pegar o token (ex: do Keychain) e usar via `GH_TOKEN="$TOKEN" gh ...`. No Windows/Linux geralmente funciona nativo. |
| `{{CLI_BACKEND}}` | CLI do seu backend (ex: supabase, firebase, planetscale) — opcional, conforme stack |
| `{{CLI_DEPLOY}}` | CLI do seu provedor de deploy (ex: vercel, netlify) — opcional, conforme stack |

### MCPs disponiveis

{{MCP_TABLE_PLACEHOLDER}}

Os MCPs do seu projeto sao detectados em runtime — **use so os que existirem** no seu ambiente. Exemplos comuns que valem mapear em `boas-praticas.md`: MCP do seu backend (migrations, deploy de funcao, leitura de logs), MCP de browser (testar UI), MCP de pesquisa web.

### Skills externas referenciadas

A skill referencia outras skills do ecossistema quando estao disponiveis. Se nao estiverem instaladas, segue sem.

| Skill | Quando usar |
|---|---|
| skill de pesquisa profunda (deep research / funil com fontes) | Fase 1 Passo 0 — benchmark de produto + pesquisa tecnica + confirmar fonte viva externa. Ver `references/fase-1-benchmark.md` |
| MCP de search/scrape (se houver) | Fase 1 Passo 0 — varredura leve / raspar URL de benchmark (fallback: jina.ai → WebFetch → anotar lacuna) |
| `superpowers:brainstorming` | Fase 1 Passo 1 — desenhar comportamento/regra de negocio antes do plano (padrao, salvo escape) |
| `superpowers:writing-plans` | Fase 1 Passo 2 — gerar plano detalhado (arquivos, tasks, riscos) |
| skills de boas praticas do seu stack (se instaladas) | Fase 1 Passo 3 + Fase 3 — ex: as oficiais de React, Postgres, Next, etc. Detecte e use so as que existem |
| skill de handoff de design (se instalada) | Fase 1 (porta de entrada) — quando o pedido traz design pronto (Figma/print/prototipo): gera o spec de implementacao ANTES do plano. Sem skill, extrair o spec + inventario numerado manualmente (ver `references/fase-1-plano.md`, Passo 1) |
| `frontend-design:frontend-design` | Fase 1 — apenas tela nova/redesign grande (NAO pra modificar componente existente, NAO pra implementar design ja pronto) |
| `code-review:code-review` | Fase 4 etapa 1 |
| `simplify` | Fase 4 etapa 2 |
| `security-review` | Fase 4 etapa 3 |
| `checks-local` (sub-skill deste plugin) | Fase 3 (gate antes da PR) + Fase 5 (gate antes do merge) — roda os checks do seu stack local |
| `findbugs` (sub-skill deste plugin) | Fase 0 opcao 2 ou 4 — pipeline de bug (3 fases / 5 agentes) |
| `debug-browser` | Fase 0 opcao 3 ou 4 (se instalada) |

### Mapa do codigo (graphify) — OPCIONAL, pista de navegacao + impacto cruzado

**So vale se a sessao tiver uma ferramenta de grafo de codigo disponivel.** Quando houver, o Setup constroi um mapa de dependencias (AST) do worktree em `$GRAPH_PATH` (so quando `GRAPH_OK=true`). Ele acelera DUAS buscas que senao sao feitas na mao com grep:
- **"onde fica / como funciona X"** — consultar o no e suas conexoes pelo grafo, depois confirmar no codigo
- **"quem depende de X" (impacto cruzado)** — listar os dependentes (com `arquivo:linha`) antes de mexer numa peca, pra nao quebrar de lado

**Trava de fallback (LER ANTES DE USAR):** o grafo e um ATALHO, nunca um pre-requisito. Em qualquer maquina onde ele nao exista ou esteja velho, **siga normalmente com grep/Read** — `GRAPH_OK=false` e o fluxo roda igual, sem travar nem perguntar.

**Regra de ouro: o grafo aponta, o codigo confirma.** Ele diz QUEM se conecta a quem; antes de afirmar um fato (causa de bug, contrato, nullability) voce ainda le o `arquivo:linha` real. O grafo e indice de navegacao, nao fonte de verdade de comportamento. Em especial: ele e CEGO pra chamada por TEXTO (nome de funcao/rota em string, coluna em SQL, valor de enum) — pra qualquer mudanca que toque banco/rota/SQL, faca o grep amplo AINDA QUE o mapa diga "sem dependentes".

**Escopo:** o mapa e construido no Setup, antes da implementacao — serve pra investigar/planejar/revisar o PLANO (codigo ainda nao mudou). As Fases 4/5 nao dependem dele.

---

## Aprendizado entre runs

Em `${RUN_DIR_BASE}/_patterns.md` fica um arquivo compartilhado entre runs que acumula padroes que o Codex pediu pra ajustar repetidamente. A Fase 1 le esse arquivo pra evitar erros recorrentes. A Fase 5 atualiza ele apos cada run.

Ver detalhes em `references/fase-5-codex-final.md` secao "Padroes recorrentes".
