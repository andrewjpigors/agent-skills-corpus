---
name: douglas-voice
version: 1.0.0
description: |
  Captures Douglas Medeiros's authorial voice for the blog blog.douglasmedeiros.dev:
  tone, syntax, lexicon, rhetorical moves, recurring expressions, do's and don'ts
  learned from real review sessions. Use whenever transforming transcriptions into
  articles, drafting new posts, or reviewing text that should sound like Douglas.
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
---

# Douglas Voice: Estilo, Tom e Fingerprint Linguístico

Esta skill é referência primária de **voz autoral** para artigos do blog
`blog.douglasmedeiros.dev`. Use junto com:

- `.github/copilot-instructions.md` — define processo, estrutura de artigo,
  formatação markdown, workflow de transcrição e front matter.
- `.github/skills/humanizer/SKILL.md` — remove padrões genéricos de IA.
- `.github/agents/voice-reviewer.md` — agente revisor que aplica esta skill
  num draft pronto e devolve crítica estruturada.

**Em caso de conflito, `copilot-instructions.md` prevalece sobre esta skill.** Esta
skill complementa o processo dizendo *como o texto deve soar*, não *como ele é
estruturado mecanicamente*.

---

## Tom de Voz e Estilo de Escrita

### Características Principais

1. **Conversacional e Autêntico**: O estilo é descontraído, como uma conversa entre colegas. Use linguagem direta, sem
   formalidades excessivas.
    - ✅ "Vou ser sincero, demorou mais do que eu imaginava."
    - ✅ "E cá estamos..."
    - ✅ "Pense bem: quantas vezes você..."
    - ❌ "Neste trabalho, será apresentado de forma sistemática..."

2. **Uso de Gírias e Expressões Brasileiras**: O autor usa gírias e expressões coloquiais brasileiras naturalmente.
    - "kk" (risos)
    - "~~gambiarras~~" (texto riscado com humor)
    - "No final das contas"
    - "Da próxima vez"
    - "Aí vem as frases clássicas"
    - "Caiu a ficha"
    - "Spoiler: esse momento não existe"

3. **Autoironia e Humor Sutil**: O autor não se leva muito a sério e usa humor para conectar com o leitor.
    - "Como bom back-end, não foi fácil definir o layout"
    - "~~nem sempre na real~~" (texto riscado)
    - "soluções mais modernas ~~gambiarras~~"
    - "(kk não fui aprender Tailwind-CSS)"

4. **Pessoal e Experiencial**: O autor compartilha experiências pessoais e vulnerabilidades.
    - Use primeira pessoa ("eu", "minha")
    - Conte histórias reais
    - Admita erros e aprendizados
    - Seja vulnerável quando apropriado

5. **Provocativo e Reflexivo**: O autor faz perguntas diretas ao leitor para provocar reflexão.
    - "E você, já aplicou a Regra do Bom Escoteiro no seu código?"
    - "Mas legado é realmente um problema?"
    - "Por que desenhar?"
    - "Você não é ruim em comunicação, só não treinou o suficiente"

---

## Elementos de Escrita Específicos

### 1. Software Orientado a Fofoca

O autor criou este termo humorístico para descrever sistemas mal documentados onde o conhecimento está apenas nas
cabeças das pessoas. Use referências criativas e humor quando apropriado.

### 2. Analogias e Metáforas

O autor usa analogias do dia a dia para explicar conceitos técnicos:

- "É como uma dívida financeira: se você não a paga, ela só aumenta"
- "Como bons escoteiros sempre deixam o lugar mais limpo do que encontraram"
- "Sistemas são organismos vivos"
- "Uma boa analogia para isso é a rotina de atletas de alta performance"

### 3. Expressões de Transição

Use expressões naturais para conectar ideias:

- "No final das contas"
- "Pense bem"
- "A questão é que"
- "Aí vem"
- "E então"
- "Por exemplo"
- "Além disso"
- "Mais do que isso"
- "Claro"
- "É aí que"

### 4. Storytelling

Conte histórias de forma cronológica e envolvente:

- Apresente o contexto
- Mostre o problema
- Descreva a jornada
- Revele a solução/aprendizado
- Conclua com reflexão

### 5. Referências Técnicas e Culturais

O autor faz referências a:

- Tecnologias modernas (Docker, Kafka, Redis, PHP, etc.)
- Cultura pop tech (Mr. Robot, Matrix)
- Comunidade tech brasileira (Dev.to, TabNews)
- Práticas de desenvolvimento (SOLID, Clean Code, TDD)
- Livros técnicos

---

## Exemplos de Frases Típicas do Autor

Para referência, aqui estão exemplos de frases que capturam o estilo:

**Aberturas:**

- "Finalmente saiu! Ah, fazia tempo que eu queria..."
- "Se alguém tivesse me dito no início da minha carreira que..."
- "Fazer parte do time X é quase como um privilégio..."
- "Esses dias vi um cara no Twitter perguntando..."

**Transições:**

- "E aí veio o momento de clareza."
- "Foi um choque perceber que..."
- "Aí vem as frases clássicas..."
- "E então, o mundo real chega."
- "No final das contas..."

**Ênfases:**

- "E não, comunicação não é sobre 'falar bonito'..."
- "Sim, é exatamente sobre isso."
- "A real é que ninguém cresce sozinho."
- "E spoiler: esse momento não existe."

**Reflexões:**

- "Essa é a essência da Regra..."
- "Esse episódio foi meu choque de realidade..."
- "O verdadeiro diferencial acontece quando..."
- "No fim das contas, tudo se resume a..."

**Fechamentos:**

- "Nos vemos nos próximos posts! 🚀"
- "E você, já aplicou X? Compartilhe suas experiências..."
- "Então, da próxima vez que você..."
- "Espero que você me acompanhe nessa jornada."

---

## Fingerprint Linguístico do Douglas

Esta seção captura os padrões concretos de voz, sintaxe e argumentação do autor, extraídos por análise
estilométrica das transcrições e do artigo final aprovado. Use como referência primária para gerar texto que
soe como ele.

### Estrutura sintática

**Frases curtas a médias.** Mediana de ~18 palavras. Faixa produtiva: 8 a 28 palavras. Frases acima de 30
palavras aparecem mas sempre seguidas de uma frase curta compensatória.

**Coordenação sobre subordinação.** Encadeia com "e", "aí", "mas", "então", "porque". Construções com
"embora", "caso", "todavia" são praticamente inexistentes.

**Ritmo martelo-expansão-martelo.** Frase curta assertiva, desenvolvimento longo, frase curta que fecha. A
proporção é ~1 punch para cada 2-3 frases de desenvolvimento.

### Abertura de parágrafos e seções

Aberturas pessoais (eu / lembro / esses dias / semana passada) são o default. Pronome pessoal ou verbo
no passado na primeira posição é o padrão preferido.

Aberturas com **observação genérica curta** são aceitas, desde que **virem pessoal em 1-2 frases**. O que
não funciona é abrir com substantivo abstrato e ficar nele por um parágrafo inteiro.

- ✅ "Eu já vi a IA recomendar duas coisas contraditórias na mesma conversa"
- ✅ "Lembro quando o ChatGPT saiu, em 2022"
- ✅ "Tem um comportamento que me irrita mais do que ceticismo exagerado"
- ✅ "Sempre que pensamos em performance, a primeira coisa que vem à mente é cache." (genérico curto, mas
  o parágrafo seguinte vira "Eu também acreditava nisso, até trabalhar em um sistema...")
- ❌ "A inteligência artificial é amplamente reconhecida como..." (genérico que continua genérico)
- ❌ "O mercado de trabalho está passando por uma transformação..." (idem)

### Fechamento de seções

A última frase de cada seção carrega peso desproporcional. Precisa ser curta, afirmativa, sem condicional.
É a frase que o leitor vai lembrar. Não pode ser transição nem qualificação.

- "E o agricultor ainda precisava saber operar o trator."
- "Isso a IA não faz por você."
- "Isso não mudou."
- "Reconhecer as limitações não é ser anti-IA. É a única forma de usar a ferramenta com responsabilidade."

### Movimento retórico central: concessão-oposição

Quase todo argumento segue: [reconhece o mérito] + Mas/Só que + [crítica]. O "Mas" é a dobradiça. Nunca
critica sem conceder primeiro. Nunca concede sem virar.

- "Uso IA, gosto de usar, e vou continuar usando. Mas a ferramenta escreve código."
- "Tem verdade nisso, mas é uma verdade incompleta."
- "A ferramenta me dá produtividade... Só que tô meio de saco cheio com o discurso em volta."

### Pronomes

- **"a gente"** = experiência coletiva de engenheiros em texto reflexivo/opinativo. Default no tom de
  conversa. Ex: "se a gente entrega mais rápido, o gargalo muda de lugar".
- **"nós" (implícito ou explícito)** = experiência de equipe em texto técnico/narrativo. Aparece com
  verbos no passado de ação concreta: "tomamos uma decisão", "implementamos um cache LRU", "fizemos as
  contas", "nos deparamos com um cenário". Não é formal: é o registro técnico da equipe.
- **"eu"** = quando assume posição individual. "Eu já vi", "O que eu não faço".
- **"você"** = quando confronta o leitor. "Quando der errado, quem vão chamar é você."
- **Nunca usa impessoal** ("deve-se", "é necessário", "é importante ressaltar"). Isso é hardcoded.

Em um mesmo artigo, é normal alternar entre "a gente" (reflexão) e "nós" (relato de equipe). Não force
um só.

**Atenção em artigos sobre IA/agentes:** quando o texto fala de "agente" (LLM, Claude, Copilot) e de
"a gente" (nós) no mesmo trecho, evita colocar os dois muito próximos. Foneticamente são quase idênticos
e o leitor tropeça. Nesse caso, troca um deles por "nós" pra desambiguar.

- ❌ "O agente virou o engenheiro de software. A gente virou o arquiteto."
- ✅ "O agente virou o engenheiro de software. E nós? Nós viramos o arquiteto."

### Léxico e registro

Nível de formalidade: **4.5/10** (conversa séria entre pares técnicos). Contrações gramaticais são livres
("tô", "pra", "pro", "num"). Vulgaridade é cortada na edição ("mano", "caralho", "porra" da fala não vão
pro artigo). Exceção: o tachado irônico (**~~kk~~**, **~~ainda~~**, **~~gambiarras~~**) funciona como
válvula retórica de auto-defesa ou ressalva implícita. Dois usos válidos:

1. **Após admitir erro técnico próprio ou da ferramenta** — *"Tecnicamente, atingiu o objetivo. Só que
   pelo caminho errado e com o meu cartão. ~~kk~~"*
2. **Como ressalva temporal/implícita em afirmação categórica** — quando a frase precisa do peso
   absoluto mas o autor quer abrir uma fresta de dúvida. Ex: *"E julgamento ninguém terceirizou
   ~~ainda~~."* (a frase afirma; o tachado abre a possibilidade de o futuro inverter). Ex:
   *"soluções mais modernas ~~gambiarras~~"* (afirma "modernas"; o tachado admite que é eufemismo).

O que **não** vale: humor solto, risada genérica sem ancoragem, ou ironia que não carrega segundo
sentido. Se o tachado pode ser cortado sem mudar o significado da frase, ele é decorativo e deve sair.

**Palavras que são dele:** "bacana", "galera", "senso crítico", "delegar raciocínio", "alucinação/alucinado"
(usa pra LLMs e pra pessoas), "tiro no pé", "chão de fábrica", "a conta vai bater", "trade-off", "gargalo",
"perrengue", "vibe-codar", "refinamento técnico", "talks por aí", "conta de padaria", "ponta do lápis",
"fazer as contas", "caiu a ficha", "ficha caiu", "bolha dev" (nunca "grupos de
dev", "comunidade tech" ou similares — quando se refere ao circuito de devs
que circulam o mesmo conteúdo no Twitter/LinkedIn/grupos, é "bolha dev").

**Palavras que soam do assistente** (evitar ou reduzir): "subterfúgio", "iceberg inteiro que sustenta",
"relação ambígua com a ferramenta", "barroco" (palavra de crítica de arte, não de tech lead — usar
"pesado", "ritual" ou reformular). Quando o vocabulário ficar polido demais, reformular pro registro dele.

**Termos técnicos sem tradução:** corrotina, rate limit, breakpoint, code review, PagerDuty, war room,
postmortem, tokens, CLI, DDD, prompt. Assume que o leitor é dev.

### Argumentação

Sempre na ordem: **experiência pessoal concreta → reflexão abstrata**. Nunca o contrário. O episódio ancora
o argumento. O argumento sozinho flutua.

- ✅ [conta que o agente escalou a instância] → [reflete sobre limites de agentes autônomos]
- ❌ [tese sobre limites de agentes autônomos] → [menciona um caso como exemplo]

**Perguntas retóricas** são econômicas: 1-2 por artigo, posicionadas no final de blocos argumentativos como
desconforto pro leitor. Nunca no começo de seção. Nunca em excesso.

### Movimento retórico: "conta de padaria"

Recorrente. Pra ancorar argumento técnico em algo concreto, ele introduz cálculo informal com frases
como *"Vamos fazer uma conta de padaria"*, *"colocando na ponta do lápis"*, *"fizemos as contas"*. O
cálculo é simples (1ms × 1 milhão de mensagens = 1.000 segundos), mas serve pra **traduzir abstração em
número que o leitor sente**. Use sempre que o argumento técnico depender de magnitude.

**Uma vez por artigo.** A expressão é marca forte do léxico, mas perde efeito se repetida no mesmo
texto. Se já apareceu uma vez pra ancorar o argumento principal, segundas ocorrências viram tique
verbal. Pra outras comparações no mesmo artigo, use construções equivalentes ("a matemática é
simples", "é o oposto", "fazendo as contas") ou só reescreve sem invocar a fórmula. E só vale
"conta de padaria" quando há **cálculo de magnitude real** (multiplicação, escala, ordem de
grandeza); comparação direta de tempo ou contagem simples não justifica a expressão.

### Links internos como recurso de voz

Linkar pra artigos anteriores do próprio blog faz parte da construção do universo de ideias do autor.
Não é SEO, é continuidade de raciocínio. Use quando o artigo atual toca em tema já abordado:
*"Escrevi mais sobre isso em [Nem só de código vive o dev]"*. Aparece em posição natural no fluxo,
não no fim como CTA forçado.

### Analogias

Do mundo físico para problemas de software. Curtas (1-2 frases). Nunca se estendem em parábola. Se a
analogia não fecha em 2 frases, reformular ou cortar.

- ✅ "O trator não deu ao agricultor mais horas de descanso."
- ❌ "Imagine um fazendeiro que, ao receber seu primeiro trator, pensou que poderia finalmente descansar.
  No entanto, logo percebeu que..." (extenso, didático)

Analogia pela metade é pior que nenhuma analogia. Se não dá pra desenvolver até fechar, corta.

### Blockquotes como quebra de quarta parede

Blockquotes são **quebras de quarta parede** — momentos em que o autor sai da
narrativa principal e fala direto com o leitor, ou destaca algo que precisa
sair do fluxo. Não são ênfase genérica. Cada cor tem **função semântica
distinta** e essa função tem que ser respeitada.

#### `[!NOTE]` — pausa narrativa, voz lateral

Use para:

- **Meta-comentário sobre o artigo ou processo** — "Esse artigo quase ficou
  para abril. Fiz a transcrição em março, achei confuso e quase adiava."
- **Definição ou explicação curta** — "Explicando rápido, pra quem não pegou
  essa época: Bomberman é um jogo em que..."
- **Falas/diálogos citados** — "*'Ah, mas eu não sou bom em me comunicar…'*"
  ou "*'Abriu uma vaga aqui no meu time, bora tentar de novo?'*"
- **Recado lateral sobre próximos posts ou conteúdo paralelo** — "No próximo
  post vou contar sobre o conteúdo das palestras..."
- **Apartes do narrador** — "Como assim o Redis é o problema? Foi exatamente
  o que pensei."

Tom: pausa rápida, "olha aqui um segundo, deixa eu te contar uma coisa".

#### `[!IMPORTANT]` — contexto crítico ou provocação

Use para:

- **Contexto de origem do artigo** — "Este artigo começou como um tweet, foi
  transformado em um breve artigo no dev.to e agora chega ao meu blog..."
  ou "Este artigo nasceu da minha palestra '...'."
- **Pergunta direta ao leitor que abre reflexão** — "— Você já sentiu o
  desconforto de compartilhar uma ideia que ninguém deu atenção, mas quando
  outra pessoa repetiu a mesma coisa, todos se interessaram?"
- **Aviso técnico crítico** — "Senso crítico não é opcional quando você usa
  IA para produção..."
- **Referência a artigo anterior fundamental pro contexto** — "Para quem
  ficou curioso sobre a talk que palestrei no último Velho Oeste, eu
  transformei ela em um artigo chamado..."

Tom: peso, atenção, "isso aqui você precisa ler com calma".

#### `[!TIP]` — frase-mestra, mantra ou call-to-action

Use para:

- **Lição cunhada do próprio artigo** — "**Performance é contexto.** Antes de
  otimizar, meça."
- **Frase-mantra em itálico** — "*'Quem não é visto, não é lembrado'*"
- **Síntese final reflexiva** — "A comunidade me trouxe até aqui."
- **Call-to-action conversacional** — "E você, tem alguma história de guerra
  com banco de dados? Compartilha nos comentários, esse tipo de troca é o
  que faz a gente evoluir."

Tom: punch, frase pra grudar, fechamento elevado.

#### Regras gerais

- **Quantidade**: 2 a 4 blockquotes por artigo. Mais que isso dilui o efeito.
- **Posição**: nunca na primeira nem na última frase do artigo (se for
  fechamento, vira `[!TIP]` perto do final).
- **Não substitui parágrafo normal**: se o conteúdo flui bem na narrativa,
  deixa na narrativa. Blockquote é interrupção intencional.
- **Não vira lista de avisos**: se você tem 3 blockquotes seguidos com
  poucas linhas entre eles, está usando errado.

### Como detectar quebras de quarta parede em transcrições

Quando o Douglas grava o áudio, ele faz quebras de quarta parede o tempo
todo. Sinais que disparam um blockquote no artigo:

- **"Olha, antes de continuar..."** / **"Pera, deixa eu pausar aqui..."** →
  `[!NOTE]` com meta-comentário
- **"Antes de começar, quero..."** / **"Esse artigo veio de..."** →
  `[!IMPORTANT]` com contexto de origem
- **"Spoiler:"** / **"Ó, anota essa..."** → frase candidata a `[!TIP]`
- **"E você, já passou por isso?"** / **"Você já sentiu...?"** →
  `[!IMPORTANT]` com pergunta direta
- **Mudança brusca de tom de reflexão pra fala direta com o leitor** →
  candidato a quebra
- **Citação de fala alheia ou hipotética** ("aí o cara fala 'X'") →
  `[!NOTE]` com diálogo citado
- **Frase aforística cunhada na hora** ("performance é contexto", "quem não
  é visto não é lembrado") → `[!TIP]`

Se na transcrição aparecer um desses sinais e o conteúdo seguinte for
distinto da narrativa principal, **considere transformar em blockquote**.
A transcrição não vai marcar isso explicitamente — é trabalho de quem
transforma reconhecer o tom.

### Encerramento circular

Sempre que possível, a frase final do artigo ecoa uma imagem ou situação concreta da abertura, sem repetir
literalmente. O leitor que lembra, sorri. O leitor que não lembra, entende a frase no contexto imediato.

### O que sobrevive da fala para a escrita

Algumas construções orais funcionam escritas sem alteração e devem ser preservadas:

- Frases curtas assertivas com sujeito implícito ("Código era somente uma parte")
- Construções proverbiais ("A conta sempre vai bater uma hora")
- Cenários hipotéticos diretos ("Caiu a Anthropic. E aí? Vai ficar olhando a IDE?")
- A expressão "delegar raciocínio" (formulação cunhada por ele, conceito central)

### O que muda da fala para a escrita

- Enumerações em cascata da fala ("sabe contexto, sabe regra de negócio, sabe arquitetura") viram
  raciocínio causal na escrita ("porque valida o output, sabe quando está alucinando e consegue corrigir")
- "sabe?", "tá ligado?", "né?" são cortados (marcadores fáticos orais, sem função escrita)
- Repetições da fala são condensadas: se ele martelou o mesmo ponto 4 vezes no áudio, no artigo aparece 1
  vez com punch
- Hesitações, autocorreções e tangentes são eliminadas. Analogias que ficaram pela metade na fala são
  reformuladas ou descartadas
- **Autocorreções de registro são metainstruções, não conteúdo.** Quando ele diz "acho... acho não,
  acredito", "tipo... não, é exatamente", "talvez... na real, é certeza", ele está elevando o
  registro em tempo real e sinalizando qual versão preservar. **Use a versão forte e descarte a
  fraca.** Não vire isso em parêntese explicativo no artigo. Ex: *"Eu ainda acho (acho não,
  acredito) que..."* → *"Eu ainda acredito que..."*

---

## Lições Aprendidas em Revisões Reais

Esta seção acumula aprendizados de sessões de revisão com o autor para calibrar melhor as transformações futuras.

### Frases soltas entre parágrafos são proibidas

Uma frase sozinha entre dois parágrafos quase sempre é problema. Ou ela pertence ao parágrafo anterior (como
fechamento), ou ao próximo (como abertura), ou deveria virar um parágrafo inteiro com desenvolvimento. Frase
solta flutuando no meio do texto quebra o ritmo e parece nota mental não resolvida.

Exceção: quando a frase solta é intencional, como um punch line ou uma quebra de expectativa ("E o agricultor
ainda precisava saber operar o trator."). Nesse caso, ela funciona exatamente porque o contraste é o efeito
desejado. A diferença é que a frase intencional não precisaria de mais contexto, ela é autossuficiente.

### Listas disfarçadas de parágrafos

Se um "parágrafo" é na verdade uma sequência de frases curtas sem conexão ("IA alucina. Toma decisões sem
contexto. Não tem memória confiável."), ele precisa ser reescrito como prosa de verdade ou virar uma lista
explícita. Texto corrido com estrutura de bullet point é o pior dos dois mundos: nem flui nem organiza.

**Caso especial: frases curtas truncadas em sequência.** Quando duas ou três frases curtas aparecem
seguidas com pontos finais sem peso retórico claro, o texto fica truncado, com ritmo de checklist.
A leitura emperra. Quase sempre o melhor caminho é **unir com vírgula ou conectivo** e deixar fluir.

- ❌ "Não tem como um time central definir tudo. A complexidade é grande demais."
- ✅ "Não tem como um time central definir tudo nessa escala, a complexidade é grande demais."

- ❌ "Ainda sou eu que leio o que ele entregou. Rodo os testes. Fecho o PR. Garanto que aquilo faz o
  que tinha que fazer."
- ✅ "Ainda sou eu que leio o que ele entregou, rodo os testes, fecho o PR e garanto que aquilo faz
  o que tinha que fazer."

**A enumeração com vírgula** funciona quando cada verbo carrega complemento próprio que dá conteúdo
("leio **o que ele entregou**, rodo **os testes**, fecho **o PR**, garanto **que aquilo faz o que
tinha que fazer**"). O complemento puxa o leitor pra frente e o ritmo flui.

**Quebrar em períodos curtos** só funciona como **punch retórico intencional** — fechamento de
seção, contraste deliberado, ênfase em uma virada. Nesse caso, a frase curta é autossuficiente e
o ponto final é o efeito. Ex: *"E ela cai."* / *"Era a gente."* / *"Bacana."*

Regra prática: se duas frases curtas seguidas podem virar uma sem perder sentido, **virem uma**. Se
o ponto final está ali pra forçar uma pausa que muda o peso da frase, **mantenha**.

### Cada seção precisa ser desenvolvida, não apenas declarada

Se uma seção tem menos de 2-3 parágrafos, ela provavelmente está subdesenvolvida. O Douglas não cria seções para
declarar posições, ele desenvolve ideias. Cada seção deve ter substância reflexiva, não apenas afirmar algo e
seguir em frente. Se não tem o que dizer em 2-3 parágrafos, a seção não justifica existir como seção separada.

### Declarações de critério sem ancoragem

Frases curtas que anunciam um critério ou posição pessoal ficam truncadas quando empilhadas em sequência sem
ponte com o que vem antes ou depois. Cada frase declara, mas o leitor não vê por que aquele critério entrou
na conversa agora, como ele se manifestou em concreto, nem qual era a expectativa por trás. Resultado: parece
bullet de LinkedIn disfarçado de prosa.

Sinais:

- Sequência de 2-3 frases curtas declarativas no mesmo parágrafo, cada uma anunciando uma posição.
- Frase do tipo "O que importa é X", "O que mudou foi Y", "X nunca foi Z" sem desenvolver no mesmo fôlego.
- Critério abstrato ("gente boa do lado", "desafio grande") sem um exemplo específico do que aquilo significava
  na prática.
- Salto sem ponte entre "esse é meu critério" e "e foi por isso que aconteceu X".

Como adensar:

1. **Adiciona expectativa prévia.** Mostra que a escolha foi calculada, não constatação retrospectiva. "E aqui
   tinha os dois de sobra" → "E uma empresa do tamanho do PicPay eu tinha certeza que teria os dois de sobra".
2. **Nomeia o concreto.** Substitui o abstrato pela manifestação específica. "Gente boa" → "gente que me forçava
   a ler em diagonal pra acompanhar conversa". "Desafio grande" → "desafio que não cabia na cadeira em que eu
   entrei".
3. **Constrói contra um candidato rejeitado.** Quando a reflexão é "por que aconteceu X", abre com o candidato
   óbvio e descarta antes de oferecer a resposta real. "Fico pensando no porquê" sozinho fica suspenso. "Fico
   pensando no porquê, e a resposta nunca é esforço. Esforço eu sempre tive..." abre, descarta candidato,
   justifica o descarte, e entrega a resposta verdadeira.
4. **Ponte causal explícita.** Amarra a consequência ao critério com conector visível. "Lá dentro o caminho foi
   rápido" cai do céu depois de "o que prende é X". "O caminho foi rápido por causa disso" amarra.

Antes:

> Cargo nunca foi o que me prendeu. O que prende é com quem eu vou trabalhar e o tamanho do desafio que tô
> assumindo. Lá dentro o caminho foi rápido, virei sênior, depois tech lead, e agora tech manager.

Depois:

> Cargo nunca foi o que me prendeu, o que prende é com quem eu vou trabalhar e o tamanho do desafio que tô
> assumindo. E uma empresa do tamanho do PicPay eu tinha certeza que teria os dois de sobra: gente que me
> forçava a ler em diagonal pra acompanhar conversa, e desafio que não cabia na cadeira em que eu entrei. O
> caminho foi rápido por causa disso, virei sênior, depois tech lead, e agora tech manager.

### Ganchos narrativos entre seções

Seções não devem terminar no vácuo nem começar do zero. O fechamento de uma seção deve naturalmente conduzir ao
tema da próxima, como numa conversa onde um assunto puxa o outro. O leitor não deve sentir que mudou de artigo ao
trocar de seção.

- ❌ Seção A termina com uma reflexão fechada. Seção B começa com "Outro ponto importante é..."
- ✅ Seção A termina questionando uma consequência. Seção B abre dizendo "E essa consequência aparece de um jeito
  que me irrita mais do que ceticismo exagerado..."

### Memórias pessoais precisam de textura, não só fatos

Quando o Douglas narra um episódio do passado (infância, começo de carreira, primeiro emprego, fase específica
da vida), o parágrafo não pode ser uma lista de fatos secos. Memória sem textura vira currículo narrativo: o
leitor entende o que aconteceu, mas não sente que esteve lá. E sem essa sensação, a história não puxa pro
próximo parágrafo.

**Sinais de memória sem textura:**

- Sequência de fatos no passado simples ("comecei o curso, aprendi HTML, montei um site") sem nenhum detalhe
  sensorial, temporal ou cultural.
- Referência a tecnologia, jogo, programa ou produto da época sem contextualizar pro leitor que não viveu
  ("instalei TF2", "usei Dreamweaver", "abri MSN") — quem é mais novo lê o nome e não sabe nem o que era nem
  por que importa.
- Pular direto pro problema técnico/conflito sem deixar a paixão ou a obsessão respirar antes ("queria
  servidor próprio" sem antes mostrar **por que** queria, **o que sentia**, **quanto tempo gastava**).
- Marcador temporal ausente ou genérico ("nessa época", "naquele tempo") sem ancoragem em algo concreto da
  era (internet via rádio, MSN, Orkut, eMule, 2011 em si).

**Como dar textura:**

1. **Detalhe sensorial ou temporal específico.** Uma sensação ("virava madrugadas"), um som, um cheiro, um
   objeto da época ("internet via rádio de dez megas", "MSN", "garimpar no eMule"). Um item desses já
   muda o parágrafo de "currículo narrativo" pra "memória vivida".
2. **Contexto pra referência cultural.** Se cita TF2, Dreamweaver, Flash, Orkut, MSN, eMule: uma frase
   curta explicando o que era e por que importava pro leitor que não viveu. Sem virar enciclopédia. Uma
   linha basta: *"FPS daqueles que inspiraram um monte de outros depois: times, personagens com
   habilidades distintas, cada um com seu papel."* Ou *"naquela época isso era comum, vendiam curso de
   Office, de Windows, de manutenção de PC direto pra galera dentro da escola."*
3. **Deixar a paixão/obsessão respirar antes do problema técnico.** A estrutura natural é: primeiro a
   imersão emocional (eu virava madrugada, eu era obcecado, eu queria muito), depois o problema concreto
   (queria customizar, queria que rodasse em casa, queria meu próprio servidor). Quem pula direto pro
   problema mata o setup.
4. **Marcador temporal ancorado.** "2011" sozinho é número. "Em 2011 eu tinha acabado de fazer 18, tava
   no último ano do ensino médio" é ancoragem. O leitor sabe não só **quando** mas **em que fase da vida
   sua** aquilo aconteceu.

**Exemplo antes/depois:**

Antes (lista de fatos secos):
> Eu mexia em computador o suficiente pra entrar em chat, baixar jogo pirata, ler tópico aleatório no
> Orkut. E pra rodar servidor privado de Team Fortress 2. Queria jogar com os amigos num servidor
> próprio, com mapa, regra e modo customizados. Descobri que dava pra subir o servidor em casa.

Depois (com textura):
> Eu mexia em computador o suficiente pra abrir MSN, garimpar jogo pirata no eMule, ler tópico aleatório
> no Orkut sobre como deixar o Windows mais rápido. Coisa de adolescente com PC em 2011, nada de
> especial. Mas ali já tinha uma faísca: tentar rodar um servidor privado de Team Fortress 2.
>
> Nessa época eu virava madrugadas jogando online. O game era um FPS que a gente chamava carinhosamente
> de TF2, daqueles que inspiraram um monte de outros que vieram depois: times, personagens com
> habilidades distintas, cada um com seu papel. A gente jogava em servidores públicos abertos e numa
> dessas descobri que dava pra ter o meu, customizado.

A diferença não é tamanho, é presença. A versão com textura ancora o leitor na época (MSN, eMule, 2011,
madrugadas), explica o que TF2 era pra quem não viveu (FPS com times e habilidades distintas), e deixa a
obsessão respirar antes do problema técnico ("virava madrugadas" → depois "descobri que dava pra ter o
meu"). Quem é dev de 25 anos consegue se situar; quem é da geração TF2 reconhece o cheiro.

**Quando a transcrição já entrega textura, preservar.** O Douglas, falando, costuma trazer naturalmente
o detalhe sensorial ("eu virava madrugada jogando", "internet via rádio"). O risco é o redator achar que
isso é firula oral e cortar na edição. Não corte. Esse é o material que separa relato pessoal de
currículo narrativo.

### Credenciais sem virar currículo

Quando o Douglas menciona que tem agentes autônomos rodando em produção, não é pra impressionar. É pra
contextualizar de onde vem a opinião. A diferença entre credencial e currículo é intenção: credencial diz "eu sei
do que estou falando porque vivo isso", currículo diz "olha como eu sou foda". Se o trecho começar a soar como
LinkedIn, reescrever.

- ❌ "Tenho anos de experiência construindo sistemas de IA em escala para uma das maiores fintechs do país."
- ✅ "Hoje tenho agentes autônomos rodando no PicPay, sistemas que tomam decisão em produção sem esperar minha
  confirmação. Quando algo quebra, sou eu que depuro."

### Não ser arrogante nem professoral

O Douglas tem opinião forte, mas não se coloca acima do leitor. Frases que soam como "uma conta que as pessoas
não estão fazendo" ou "o que ninguém está dizendo" são condescendentes, pressupõem que o autor viu algo que os
outros são burros demais pra ver. Reformular pra algo que inclua o leitor na reflexão em vez de excluí-lo.

- ❌ "Tem uma consequência óbvia que ninguém está fazendo a conta."
- ✅ "E tem uma consequência óbvia disso que ninguém nas empresas está dizendo em voz alta."

A diferença é sutil, mas importante: "ninguém está dizendo em voz alta" é uma observação sobre o discurso público.
"Ninguém está fazendo a conta" é chamar os outros de incompetentes.

### A frase precisa combinar com o que vem antes e depois

Toda frase pertence a um fluxo. Se você trocar a frase de lugar e ela funcionar igual em qualquer outro parágrafo,
ela não está conectada ao contexto. Cada frase deve responder, complementar ou avançar o que a anterior disse.

Quando revisar, ler cada transição entre frases e perguntar: "a segunda frase faz mais sentido aqui do que em
qualquer outro lugar do texto?" Se não, reescrever a conexão.

### Estrangeirismos desnecessários

"Falando alto" (tradução literal de "saying out loud") não é português natural. O Douglas fala "dizendo em voz
alta". De forma geral, quando uma expressão parece tradução literal do inglês, provavelmente é. Trocar pela
expressão equivalente em português brasileiro. Isso vale especialmente pra expressões idiomáticas: "at the end of
the day" vira "no fim das contas", não "no final do dia".

Calques específicos a evitar:

- **"banda de revisão"** (de "review bandwidth") → "largura de banda de revisão" ou simplesmente
  "capacidade de revisão".
- **"falando alto"** (de "saying out loud") → "dizendo em voz alta".
- **"no final do dia"** (de "at the end of the day") → "no fim das contas".
- **"happy path"** → "caminho feliz". Apesar de circular em inglês na bolha dev, o autor prefere
  o equivalente em português. Vale pra qualquer contexto (teste, fluxo de UX, demo).
- **"fazer sentido"** quando claramente vem de "make sense" forçado → reescrever pra
  "ter lógica", "bater", "se encaixar". Em contexto natural ("isso faz sentido") tudo bem; em
  contexto traduzido ("isso faz sentido pra mim no momento atual") soa importado.

### Contradições honestas devem ficar em aberto

Se o Douglas diz que é fã e hater ao mesmo tempo, não resolva a contradição. Não escolha um lado. Não faça uma
síntese elegante que neutralize a tensão. A honestidade está exatamente em deixar a contradição exposta. Artigos
reflexivos que resolvem tudo de forma limpa soam falsos.

- ❌ "Apesar das críticas, no fundo a ferramenta entrega valor e merece reconhecimento."
- ✅ "Dependendo do dia que você me perguntar, vou estar mais crítico, mais entusiasmado ou mais cético. O que
  não muda é que ela me ajuda bastante e que ela erra bastante também."

### Transcrição é matéria-prima, não rascunho

O Douglas pensa em voz alta durante as gravações. O que sai na transcrição é um rascunho mental, com repetições,
analogias inacabadas e pensamentos interrompidos. A missão não é transcrever fielmente, é entender o raciocínio por
trás e reconstruir em texto com storytelling coerente.

Se uma analogia ficou pela metade na gravação (ex: "é como uma carroça... mas não é exatamente isso"), não publique
a analogia quebrada. Ou reformule de forma que funcione, ou descarte.

**Capturar o que ele quis dizer, não o que ele disse.** Se na transcrição ele enrola por três frases pra chegar
num ponto, no artigo aquele ponto deve aparecer direto. Se ele volta num assunto que já tinha deixado pra trás,
incorporar na seção certa, não na ordem que ele falou.

### Títulos de seção devem soar como alguém falando

A tendência atual é **sentence case com personalidade**, títulos curtos que o próprio Douglas falaria em
voz alta. É o padrão preferido em posts mais reflexivos/opinativos.

Em posts mais técnicos, **Title Case curto e descritivo** é aceitável quando o título é literalmente
um marcador de estrutura ("O Contexto", "A Descoberta", "Insights Finais"). Não é o ideal, mas não é
proibido — muitos posts antigos usam.

O que **nunca** funciona é cabeçalho de documentação técnica ou de slide corporativo.

- ✅ "O problema com 'mais produtividade'"
- ✅ "Na prática, então"
- ✅ "O Contexto" (Title Case curto, post técnico) — aceitável, mas prefira sentence case com mais sabor
- ❌ "Considerações sobre produtividade com IA"
- ❌ "Utilização prática da ferramenta"

### O parágrafo explicativo não pode soar como narrador externo

Quando o Douglas conta um episódio pessoal (ex: o agente que escalou a instância sem pedir), o parágrafo que
explica o que aconteceu de verdade deve soar como ele mesmo refletindo, não como um narrador técnico de fora. Se
o trecho começa a soar como um post-mortem de incidente corporativo, está errado.

- ❌ "O que ocorreu foi uma ausência de guardrail de confirmação em ação com efeito financeiro irreversível."
- ✅ "O agente achou uma brecha, uma situação que o meu prompt não cobria, e decidiu sozinho. É quase como um
  pen tester procurando onde o escopo não foi definido."

### Travessões são um sinal de alerta

O uso excessivo de travessão (—) é um dos marcadores mais visíveis de texto gerado por IA. O Douglas usa vírgula,
ponto e vírgula ou reestrutura a frase. Sempre que um travessão aparecer no rascunho, perguntar: dá pra trocar por
vírgula ou ponto? Se sim, trocar.

### A rejeição ao hype é parte da voz, não uma ressalva

Quando o Douglas diz que não gosta de falar de IA, não está sendo modesto nem se protegendo de críticas. É uma
posição genuína. Essa resistência inicial ao hype é parte do que dá credibilidade ao que ele diz depois. Preservar
esse tom no início do artigo é importante, não suavize para "apesar de ser um tema muito discutido...".

---

## Checklist Rápido de Voz

Antes de finalizar qualquer artigo, valide cada item:

- [ ] Abertura é pessoal (eu/lembro/esses dias) ou observação genérica curta que vira pessoal em 1-2 frases
- [ ] Frases médias (8-28 palavras), com pelo menos um punch curto por bloco
- [ ] Coordenação ("e", "mas", "aí") domina sobre subordinação ("embora", "caso")
- [ ] Tem ao menos um movimento concessão-oposição ([mérito] + Mas + [crítica])
- [ ] "A gente" em texto reflexivo; "nós/implementamos/tomamos" em texto técnico de equipe; "eu" pra posição individual; "você" pra confronto
- [ ] Sem impessoal ("deve-se", "é necessário", "é importante ressaltar")
- [ ] Vocabulário do registro dele (bacana, galera, trade-off, gargalo, conta de padaria, perrengue) e não do assistente
- [ ] Argumentos vêm depois do episódio concreto, nunca antes
- [ ] Quando há magnitude técnica, tem "conta de padaria" pra ancorar
- [ ] Analogias fecham em 2 frases ou foram cortadas
- [ ] No máximo 2-4 blockquotes no artigo inteiro, com cor (NOTE/IMPORTANT/TIP) coerente com a função semântica
- [ ] Quebras de quarta parede da transcrição foram capturadas como blockquotes apropriados
- [ ] Travessões substituídos por vírgula/ponto sempre que possível
- [ ] Tachado irônico (`~~kk~~`, `~~ainda~~`, `~~gambiarras~~`) só aparece em admissão de erro técnico ou como ressalva implícita que carrega segundo sentido — nunca como humor decorativo
- [ ] Linka pra artigo anterior do próprio blog quando o tema toca algo já abordado
- [ ] Nenhuma frase solta entre parágrafos sem ser punch intencional
- [ ] Cada seção tem 2+ parágrafos de desenvolvimento real
- [ ] Declarações de critério/posição vêm com expectativa prévia, âncora concreta ou ponte causal — nunca empilhadas soltas
- [ ] Memórias pessoais têm textura (detalhe sensorial/temporal, contexto pra referência cultural da época, paixão respirando antes do problema técnico) — não são lista de fatos secos
- [ ] Transições entre seções têm gancho narrativo, não "outro ponto importante"
- [ ] Credenciais soam como contexto, não como currículo
- [ ] Sem condescendência ("ninguém pensa nisso") nem tom professoral
- [ ] Estrangeirismos traduzidos pra português brasileiro natural
- [ ] Contradições honestas mantidas, não sintetizadas
- [ ] Títulos em sentence case com personalidade (Title Case curto aceitável em post técnico)
- [ ] Última frase de cada seção é curta, afirmativa, sem condicional
- [ ] Última frase do artigo ecoa imagem da abertura quando possível
