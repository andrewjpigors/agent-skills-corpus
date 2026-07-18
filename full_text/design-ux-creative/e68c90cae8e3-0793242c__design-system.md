---
name: design-system
description: "Design System Blueprint — premium design system construction with small palettes, 8-point modular spacing, typography pairing, radius families, soft shadows, token-based components, signature motion, and a final build checklist. Use when building, refactoring, or auditing a design system, visual identity, UI tokens, or premium-looking interfaces."
metadata:
  domains: design-system,ui,visual-identity,tokens,components,motion,premium
  tools: css,scss,tailwind,figma,design-tokens
---

# Design System Blueprint (PT-BR)

> **The Design System Blueprint** — construa um design system que faz qualquer site parecer caro.
> 

Este é o método exato por trás das interfaces premium: as regras de simetria, espaçamento (a escala de Fibonacci/modular), cor, tipografia, bordas, sombras, componentes e movimento — cada uma apresentada com um exemplo claro e desenvolvido. Sem enrolação. Toda regra vem com o raciocínio, os valores reais e um **Faça isso** que você aplica ao seu próprio trabalho.

**Como usar:** leia de cima a baixo uma vez para absorver o método e depois mantenha o checklist final aberto enquanto constrói o seu próprio sistema. Tudo é agnóstico de ferramenta — os princípios funcionam no Figma, no código ou com um agente de IA.

---

## 1. Por que sistemas parecem caros

*O visual que você não consegue nomear é apenas restrição, aplicada em todo lugar ao mesmo tempo.*

**A regra** — Premium não é mais; é menos decisões, repetidas com disciplina: uma paleta pequena, uma ou duas famílias tipográficas, um acento, uma escala de espaçamento — aplicadas em cada tela sem exceção.

**Por que funciona** — O olho lê consistência como intenção, e intenção como qualidade. Quando cada raio de canto, espaçamento e cinza vem do mesmo conjunto minúsculo, o cérebro para de notar elementos individuais e passa a perceber um todo — essa continuidade é o que "caro" realmente transmite. O trabalho amador parece barato não porque uma escolha isolada esteja errada, mas porque há escolhas demais e sem relação disputando atenção. As restrições removem esse ruído; a coesão é o que sobra.

**Exemplo** — O mesmo botão, construído de duas maneiras.

```jsx
AMATEUR — every value improvised
  bg #3B82F6      radius 6px     padding 11px 18px
  font Roboto     shadow 0 2px 8px rgba(0,0,0,.25)
  hover #2563EB   (a different blue than anywhere else)
  ...next button: radius 10px, padding 14px 20px, another blue

SYSTEM — every value drawn from the set
  bg  #2F6FED (the one accent)     radius 12px (from the radii family)
  padding 16px 24px (8-pt scale)   font Inter (the one body sans)
  hover #4C82FF (defined accent variant, not a new color)
  ...next button: identical tokens. And the one after that.
```

Nada na coluna "system" é mais sofisticado. É simplesmente o *mesmo* — e essa igualdade, mantida ao longo de um site inteiro, é o truque por completo.

**Faça isso**

1. Limite sua paleta antes de desenhar: um canvas quente, um quase-preto para o texto, dois cinzas, um acento com duas variantes. Anote os valores hex; trate a lista como fechada.
2. Escolha no máximo duas famílias tipográficas — uma de display, uma de corpo — e apague todas as outras fontes do arquivo.
3. Escolha um acento e só um. Todo link, anel de foco e botão primário usa ele; nada mais pode usar.
4. Defina uma escala de espaçamento e uma família de raios, e então proíba a si mesmo qualquer valor que não esteja nelas.
5. Audite uma tela existente: conte os azuis, raios e tamanhos de fonte distintos. Todo número acima de um por função é uma decisão a ser eliminada.

**Evite** — Adicionar uma exceção "só dessa vez". O primeiro valor fora do sistema é permissão para os próximos cinquenta, e a coesão desmorona no momento em que o padrão é quebrado.

---

## 2. Grid, simetria e a escala modular

*O espaço em branco não é vazio; é ritmo — e ritmo precisa de uma batida.*

**A regra** — Toda medida na página — margens, padding, gaps, deslocamentos — se encaixa em uma única escala de espaçamento construída sobre uma base de 8 pontos (ou uma razão modular de ~1.5), de modo que nada esteja "mais ou menos" alinhado.

**Por que funciona** — Espaçamento consistente cria um grid invisível que o olho sente mesmo quando não o vê; elementos que compartilham um ritmo se leem como relacionados, e elementos relacionados se leem como projetados. Uma base de 8 pontos funciona porque divide de forma limpa em diferentes densidades de tela e se compõe em uma progressão musical — 8, 16, 24, 32 — em vez de 13s e 27s arbitrários. Espaço em branco generoso e *escalonado* é o sinal mais forte de premium: diz ao observador que o conteúdo tem confiança suficiente para respirar. Simetria e alinhamento óptico então fazem o acabamento — o cérebro recompensa o equilíbrio e pune o quase-certo.

**Exemplo** — A escala de espaçamento do sistema de exemplo. Tudo na página é um destes números, nada entre eles.

| Token | Valor | Uso típico |
| --- | --- | --- |
| `space-1` | 8px | Espaço entre ícone e rótulo, espaçamento inline apertado |
| `space-2` | 16px | Padding dentro de controles compactos, espaço entre itens de lista |
| `space-3` | 24px | Padding de card, espaço entre blocos relacionados |
| `space-4` | 32px | Espaço entre componentes dentro de uma seção |
| `space-5` | 48px | Padding interno de seção, separações maiores |
| `space-6` | 64px | Ritmo vertical entre seções principais |

```css
Section padding : 64px top/bottom (space-6)
Card padding    : 24px all sides  (space-3)
Heading -> body : 16px            (space-2)
Body -> button  : 32px            (space-4)
Icon -> label   : 8px             (space-1)
```

Nota óptica: centralização matemática nem sempre é centralização visual. Uma seta apontando para a direita ou um triângulo parece descentralizado quando sua caixa delimitadora está centralizada — desloque-o 1–2px em direção à sua massa visual para que ele *pareça* centralizado. Confie no olho, não nas coordenadas.

**Faça isso**

1. Defina a escala — 8 / 16 / 24 / 32 / 48 / 64 — como tokens nomeados e use apenas esses valores para todo gap e padding.
2. Estabeleça uma unidade base de 8px e faça todas as dimensões de componentes caírem em múltiplos dela; se algo precisa de 20px, decida entre 16 e 24 em vez de inventar 20.
3. Estabeleça o ritmo vertical: escolha um valor grande (64px) para o espaço entre seções principais e mantenha-o em todo o site para que a página tenha uma pulsação constante.
4. Aumente o espaço em branco antes de aumentar o conteúdo — quando um layout parece barato, a correção normalmente é mais espaço, não mais elementos.
5. Verifique a simetria sobre um grid real sobreposto e depois corrija a olho: alinhe às bordas ópticas (a massa visual) em vez das caixas delimitadoras, especialmente para ícones, glifos e tipos em itálico.
6. Deixe itens relacionados compartilharem um gap menor e itens não relacionados um gap maior — a proximidade deve codificar agrupamento, não acidente.

**Evite** — Empurrar elementos à mão livre até que "pareçam mais ou menos certos". Valores fora do grid com poucos pixels de diferença criam uma vibração sutil que o observador não sabe nomear, mas sempre sente como amadora.

---

## 3. Cor — o método da paleta pequena

*Um canvas quente, uma tinta confiante, um acento usado como pontuação — essa é a paleta inteira.*

**A regra** — Construa a partir de uma paleta pequena e fixa: um canvas branco-quebrado quente (nunca o `#FFFFFF` puro), uma tinta quase-preta, dois cinzas e exatamente um acento com duas variantes — porque **acento é um momento, nunca uma superfície.**

**Por que funciona** — Branco puro e chapado é a impressão digital de um template padrão, intocado; um canvas sutilmente quente se lê como escolhido, e "escolhido" se lê como trabalhado. Tinta quase-preta em vez de `#000` suaviza o contraste a um nível que o olho acha refinado em vez de agressivo. A contenção no acento é o que o torna poderoso: quando o azul aparece só no único link, na única ação primária, no único anel de foco, cada uso carrega peso — inunde uma superfície inteira com ele e o sinal cai para ruído. Dois cinzas bastam para construir toda uma hierarquia de texto secundário e bordas; mais cinzas só embaçam a escada.

**Exemplo** — A paleta completa do sistema de exemplo. Note o gradiente vertical no canvas — calor que se move — e o quão estreitamente o acento é escopado.

| Função | Valor | Onde aparece |
| --- | --- | --- |
| Canvas (topo) | `#FAFAF8` | Fundo da página, topo de um gradiente vertical suave |
| Canvas (base) | `#F4F3EF` | Mesmo fundo, branco-quebrado quente, base do gradiente |
| Tinta | `#16181D` | Texto principal, títulos — quase-preto, nunca `#000` |
| Tinta suave | `#1D2027` | Títulos secundários, corpo de alta ênfase |
| Cinza secundário | `#8B8F98` | Legendas, rótulos, texto de apoio |
| Borda | `rgba(22,24,29,0.12)` | Fios finos, divisórias, contornos de inputs |
| Acento | `#2F6FED` | O único azul — links, botão primário, anel de foco |
| Acento hover | `#4C82FF` | Estado de hover / ativo dos elementos de acento |
| Acento profundo | `#1E5AD6` | Estado pressionado, texto de acento onde é preciso mais contraste |
| Superfície escura | `#0E0F12` / `#16181D` | Seções invertidas opcionais, rodapés |

```css
/* Warm canvas — the gradient is the point; flat white is not */
background: linear-gradient(180deg, #FAFAF8 0%, #F4F3EF 100%);

/* Accent as a moment, not a surface */
.link,
.btn-primary { color/background: #2F6FED; }   /* the one place blue lives */
.btn-primary:hover  { background: #4C82FF; }
.btn-primary:active { background: #1E5AD6; }
/* Sections, cards, and heroes stay on the warm canvas — never the accent */
```

**Faça isso**

1. Substitua todo `#FFFFFF` por um branco-quebrado quente (`#FAFAF8`) e dê ao fundo da página um gradiente vertical sutil em direção a `#F4F3EF` para que o canvas tenha profundidade, não chapado.
2. Defina o texto do corpo em uma tinta quase-preta (`#16181D`), nunca `#000000` — esse pequeno passo para trás em relação ao preto puro é o que se lê como pensado.
3. Escolha um acento e dê a ele exatamente duas variantes — um hover mais claro e um estado pressionado mais profundo — e então use-o apenas em momentos interativos: links, a ação primária, estados de foco.
4. Construa toda a sua hierarquia de texto a partir da tinta, da tinta suave e de um cinza (`#8B8F98`); use uma tinta de baixa opacidade para bordas (`rgba(22,24,29,0.12)`) para que os fios finos fiquem *dentro* da superfície em vez de sobre ela.
5. Reserve grandes campos de cor para uma única superfície escura opcional (`#0E0F12`); deixe o contraste entre o canvas quente e o escuro profundo carregar o drama, não o acento.
6. Teste a paleta em escala de cinza — se a hierarquia ainda se lê com a cor removida, os valores estão fazendo o trabalho e o acento fica livre para ser decoração, não muleta.

**Evite** — Preencher um hero, card ou seção inteira com a cor de acento. No momento em que o azul vira uma superfície ele deixa de ser especial, e a página despenca de premium de volta para template.

---

## 4. Tipografia — o sistema de duas famílias

*Uma de display, uma de trabalho — uma escala fixa faz o resto.*

**A regra** — Escolha exatamente duas famílias tipográficas: uma serifada expressiva para os títulos e uma sans geométrica neutra para todo o resto, e então dimensione cada trecho de texto a partir de uma única escala fixa em vez de escolher números pelo feeling.

**Por que funciona** — Duas famílias dão contraste sem caos: a serifada carrega personalidade, a sans carrega informação, e o olho lê o par como "pensado". Uma escala modular fixa remove a dúzia de tamanhos de fonte arbitrários que fazem sites amadores parecerem barulhentos — quando cada tamanho é deliberado, a página se lê como projetada em vez de montada. A tensão entre uma serifada de display quente e uma sans geométrica fria é exatamente o que marcas caras alugam para parecer premium.

**Exemplo** — O sistema de exemplo combina uma serifada de display (ex.: Fraunces) com uma sans geométrica de corpo (ex.: Inter), e trava cada tamanho em uma única escala:

| Token | Tamanho | Altura de linha | Tracking | Caixa | Família | Uso |
| --- | --- | --- | --- | --- | --- | --- |
| Rótulo / chip | 12px | 1.3 | +1px | UPPERCASE | Sans | Sobretítulos, tags |
| Botão | 14px | 1.0 | +1.5px | UPPERCASE | Sans | CTAs, controles |
| Nav | 16px | 1.4 | 0 | Sentence | Sans | Menus, links |
| Corpo | 18px | 1.5 | 0 | Sentence | Sans | Parágrafos |
| Lead | 20px | 1.5 | 0 | Sentence | Sans | Introduções, subtítulos |
| H1 mobile | 28px | 1.1 | -0.25px | Sentence | Serif | Títulos (pequenos) |
| H1 desktop | 56px | 0.95–1.0 | -0.5px | Sentence | Serif | Títulos de hero |

As regras que governam: **a altura de linha aperta conforme o tamanho cresce** (o corpo fica solto em 1.5; o display de 56px colapsa para ~0.95–1.0 para que o título se leia como uma única forma). **O espaçamento entre letras se move ao contrário do tamanho** — texto pequeno em caixa alta se abre (+1 a +1.5px) para que as maiúsculas não se amontoem, enquanto o texto grande de display aperta (-0.5px) para fechar as folgas que letras grandes criam. **A caixa é uma função, não uma decoração**: a caixa alta pertence apenas a rótulos minúsculos e botões; títulos e corpo sempre permanecem em caixa de sentença.

**Faça isso**

1. Escolha suas duas famílias — uma serifada de display, uma sans geométrica — e apague todas as outras fontes do projeto.
2. Copie a escala acima como tokens (`--text-body: 18px`, etc.) e proíba qualquer tamanho de fonte que não seja um deles.
3. Defina o corpo em 18px/1.5 como âncora e então aperte a altura de linha passo a passo conforme os tamanhos sobem em direção ao display de 56px em ~0.95.
4. Adicione +1 a +1.5px de tracking a qualquer coisa de 14px ou menos que esteja em caixa alta; adicione -0.5px ao display de 56px.
5. Reserve a caixa alta apenas para rótulos e botões — nunca títulos, nunca parágrafos.
6. Teste o par primeiro na escala de hero: se o H1 serifado e o lead sans não transmitirem tensão-mais-harmonia, você escolheu as duas fontes erradas, não os tamanhos errados.

**Evite** — Definir tipos grandes de display com a altura de linha do corpo (1.5). Um título de 56px em 1.5 se solta em linhas desconectadas; ele precisa ficar apertado (~0.95–1.0) para se ler como uma única afirmação confiante.

---

## 5. Bordas e raios — a família de raios

*Arredonde tudo — mas arredonde na medida certa.*

**A regra** — Nunca entregue um canto reto de 0px; em vez disso, defina uma pequena família de raios e combine o raio ao tamanho do elemento, usando bordas, sombras e preenchimentos como uma ordem estrita de decisão em vez de sobrepor os três.

**Por que funciona** — Cantos retos se leem como padrão, sem estilo, engenharia-em-primeiro-lugar. Cantos suavizados se leem como projetados e físicos, como objetos reais. Mas um único raio aplicado em todo lugar fica pior do que nenhum — um botão e um card de largura total precisam de curvaturas diferentes para parecer proporcionais. Combinar o raio ao tamanho mantém a redondeza *visual* consistente mesmo que os valores em pixels sejam diferentes, e é isso que faz a superfície inteira parecer um único sistema.

**Exemplo** — O sistema de exemplo usa uma família de raios, escalonada ao tamanho do elemento:

| Token | Raio | Aplica-se a |
| --- | --- | --- |
| `radius-input` | 8px | Inputs, selects, controles pequenos |
| `radius-card` | 12px | Cards padrão, tiles, popovers |
| `radius-card-lg` | 16px | Cards grandes, modais, blocos de mídia |
| `radius-button` | 24px | Botões, pílulas proeminentes |
| `radius-pill` | 999px | Chips, tags, avatares, toggles |

Os cantos nunca são retos — o piso é 8px. O princípio: **elementos menores recebem raios menores, elementos maiores recebem raios maiores**, para que um input de 40px em 8px e um card de 480px em 16px pareçam igualmente arredondados ao olho.

Depois siga uma **ordem de decisão** estrita para separar uma superfície de outra — escolha a primeira que funcionar, não empilhe as três:

```jsx
1. FILL      — separate by background color first.
              A card is a lighter/darker surface than the page. Cheapest, calmest.
2. SHADOW    — if fill isn't enough, lift it with elevation (see section 6).
              Implies the card floats above the page.
3. BORDER    — only if it must sit flush with no elevation.
              Use a hairline, never a hard 1px solid grey.
```

Em superfícies escuras, as bordas devem ser **fios finos construídos a partir de alpha**, não cinza opaco — isso as mantém lendo-se como uma borda suave de luz em vez de uma linha desenhada:

```jsx
Dark surface:    #0E0F12
Hairline border:  1px solid rgba(255,255,255,0.10)
```

**Faça isso**

1. Defina os cinco tokens de raio acima e proíba cantos crus de `0` em todo o projeto.
2. Atribua o raio pelo tamanho do elemento, não pelo gosto: inputs 8px, cards 12–16px, botões 24px, chips 999px.
3. Para cada painel, aplique a ordem de decisão em sequência — o preenchimento sozinho consegue separá-lo? Então a sombra? Só então recorra a uma borda.
4. Substitua todas as bordas cinza opacas em superfícies escuras por fios finos `rgba(255,255,255,0.10)`.
5. Mantenha os fios finos em 1px — um "fio fino" de 2px ou de cinza duro deixa de ser um fio fino.
6. Verifique a redondeza proporcional a olho: um controle pequeno e um card grande devem parecer igualmente suaves, não idênticos em pixels.

**Evite** — Envolver um card em uma borda cinza sólida de 1px *e* uma sombra *e* uma mudança de preenchimento. Três separadores brigando pela mesma borda é o sinal mais certeiro de um layout amador; escolha um.

---

## 6. Sombras e elevação

*Suaves, de baixa opacidade, e um único brilho — esse é todo o vocabulário.*

**A regra** — Use no máximo três níveis de sombra, mantenha-os suaves e de baixa opacidade para que se leiam como luz ambiente em vez de drop-shadows, e gaste um único brilho colorido como um momento de acento deliberado — nunca como padrão.

**Por que funciona** — Sites baratos se entregam com sombras duras, escuras e deslocadas que parecem adesivos descolando da página. A elevação de verdade é sutil: blur grande, deslocamento minúsculo, opacidade muito baixa, tingida em direção à cor da tinta em vez de preto puro. Limitar o sistema a três níveis (repouso, elevado, flutuante) mantém a profundidade legível — o usuário consegue *sentir* a hierarquia. O brilho de acento funciona justamente porque é raro: quando todo o resto é uma sombra neutra suave, um único brilho azul se lê como ênfase intencional, um momento de luz, não decoração.

**Exemplo** — O conjunto completo de elevação do sistema de exemplo, tingido em direção à tinta (`#16181D` → `rgba(16,18,29,…)`) para que as sombras pareçam a própria sombra da superfície:

```css
/* three-step elevation — soft, low opacity, minimal offset */
shadow-sm:  0 1px 2px  rgba(16,18,29,0.06);   /* rest: inputs, flat cards */
shadow-md:  0 8px 24px rgba(16,18,29,0.10);   /* raised: cards, popovers */
shadow-lg:  0 20px 50px rgba(16,18,29,0.16);  /* floating: modals, menus */

/* one accent moment — used sparingly, mostly on dark surfaces */
glow-accent: 0 0 30px rgba(47,111,237,0.30);  /* accent blue #2F6FED @ 30% */
```

Note o padrão: conforme a elevação sobe, **o blur e o deslocamento crescem juntos** (deslocamento 1px→8px→20px, blur 2px→24px→50px) e a opacidade sobe apenas suavemente (0.06→0.10→0.16). Nada ultrapassa 0.16 — suave é o objetivo.

**Superfícies claras vs. escuras:**

```jsx
Light surface (page ~#FFFFFF):
  Elevation reads through the ink-tinted shadows above. Shadows do the work.

Dark surface (#0E0F12):
  Ink shadows nearly vanish — the eye can't see a dark shadow on a dark panel.
  Separate with a hairline instead:  1px solid rgba(255,255,255,0.10)
  Reserve the accent glow for the one element you want to feel lit:
    box-shadow: 0 0 30px rgba(47,111,237,0.30);
```

**Faça isso**

1. Defina exatamente três tokens de sombra (`sm`, `md`, `lg`) e um `glow-accent`; apague toda box-shadow improvisada.
2. Tinja as sombras em direção à sua cor de tinta, não preto puro — `rgba(0,0,0,…)` puro se lê mais frio e mais barato.
3. Mantenha a opacidade baixa: limite as sombras ambientes em torno de 0.16 e deixe o blur, não a escuridão, carregar a profundidade.
4. Em superfícies escuras, pare de depender de sombras — separe os painéis com o fio fino de alpha e deixe o brilho ser a única luz.
5. Gaste o brilho de acento em no máximo um elemento por tela (um CTA primário, um card em destaque) — seu poder está na raridade.
6. Mapeie a elevação ao significado: repouso = `sm`, interativo/elevado = `md`, overlay/flutuante = `lg`. A mesma altura z sempre recebe a mesma sombra.

**Evite** — Sombras duras, escuras e muito deslocadas como `0 4px 8px rgba(0,0,0,0.5)`. Alta opacidade somada a um tom de preto puro é a razão mais comum de um layout parecer inacabado; suavize e tinja em direção à tinta.

---

## 7. Componentes — construa tudo a partir de tokens

Componentes não são novas decisões. São seus tokens, montados.

**A regra** — Um componente só pode referenciar tokens que você já definiu; se um componente precisa de um valor que não é um token, você está sem um token, não sem um componente.

**Por que funciona** — Quando todo botão, chip e card puxa sua cor, espaçamento, raio e sombra das mesmas variáveis nomeadas, nada pode derivar. Mude o acento uma vez e todo componente se atualiza em sincronia. É isso que separa um sistema de uma pilha de estilos avulsos: a consistência deixa de ser uma disciplina que você impõe à mão e passa a ser uma propriedade da arquitetura. Defina um pequeno conjunto de componentes centrais — CTA/botão, chip de tag, card, input, header/nav — e defina cada estado (repouso, hover, foco, ativo, desabilitado) para que nada seja deixado para a improvisação depois.

**Exemplo** — Três componentes centrais no sistema de exemplo, cada um construído apenas a partir de tokens:

```css
/* Primary CTA — ink pill */
.cta {
  background: var(--ink);          /* #16181D */
  color: #fff;
  border-radius: var(--radius-xl); /* 24px */
  padding: var(--space-2) var(--space-4); /* 16px 32px */
  text-transform: uppercase;
  letter-spacing: 1.5px;
  box-shadow: var(--shadow-sm);
  transition: transform .3s var(--ease-signature),
              box-shadow .3s var(--ease-signature);
}
.cta:hover  { box-shadow: var(--shadow-md); }
.cta:active { transform: scale(0.97); }      /* the press */
.cta .icon  { color: var(--accent); }        /* #2F6FED arrow */

/* Tag chip — ink outline that fills on hover */
.chip {
  border: 1.5px solid var(--ink);
  border-radius: var(--radius-pill);   /* 999px */
  padding: var(--space-1) var(--space-2);
  text-transform: uppercase;
  letter-spacing: 1px;
  transition: background .2s var(--ease-signature),
              color .2s var(--ease-signature);
}
.chip:hover { background: var(--accent); border-color: var(--accent); color: #fff; }

/* Card — the neutral container */
.card {
  background: var(--paper);        /* #FAFAF8 */
  border: 1px solid var(--hairline);
  border-radius: var(--radius-md); /* 12px */
  padding: var(--space-3);         /* 24px */
  box-shadow: var(--shadow-sm);
}
.card--dark { background: var(--surface-dark); color: var(--paper); } /* #0E0F12 */
```

Repare que não há um único valor hex cru ou medida em pixels na lógica do componente. Todo valor é uma referência a um token.

**Faça isso**

1. Liste seus componentes centrais: CTA/botão, chip de tag, card, input, header/nav. Resista a adicionar mais até que estes estejam perfeitos.
2. Construa cada um usando apenas referências `var(--token)` — nenhum hex cru, nenhum número mágico de pixel.
3. Defina todos os cinco estados para componentes interativos: repouso, hover, foco, ativo, desabilitado.
4. Dê ao CTA primário um detalhe de assinatura (aqui, a seta de acento e o pressionar `scale(0.97)`) para que ele se leia como *seu*.
5. Quando um componente parecer precisar de um valor sem token, pare e adicione o token primeiro, depois referencie-o.
6. Reutilize tokens de espaçamento para padding em vez de inventar números por componente.

**Evite** — Copiar o CSS de um componente e ajustar uma cor codificada na mão para uma variante. No momento em que um valor cru vive dentro de um componente, a deriva já começou.

---

## 8. Movimento — o diferencial premium

Design estático te deixa polido. O movimento é o que faz parecer caro.

**A regra** — Uma única curva de easing de assinatura, aplicada em todo lugar, com durações consistentes — sem bounces, sem springs, sem exceções.

**Por que funciona** — Sites baratos animam de forma inconsistente: um elemento quica, outro estala, um terceiro suaviza de outro jeito. Sites caros se movem como se uma única mão controlasse tudo. Uma única curva de easing é a impressão digital dessa mão. A contenção se lê como confiança — um fade lento e unificado comunica "pensado" muito mais do que um bounce saltitante comunica "divertido". E respeitar `prefers-reduced-motion` não é um acabamento opcional; é a diferença entre um sistema construído por um amador e um construído por um profissional.

**Exemplo** — A receita de movimento completa do sistema de exemplo:

```css
:root {
  --ease-signature: cubic-bezier(0.16, 1, 0.3, 1); /* fast-out, gentle-settle */
  --dur-ui: .4s;        /* 0.3–0.5s for UI feedback */
  --dur-entrance: 1.2s; /* 1.0–1.4s for section entrances */
}

/* Section reveal — fade + rise, staggered */
.reveal {
  opacity: 0;
  transform: translateY(32px);          /* 24–40px */
  transition: opacity var(--dur-entrance) var(--ease-signature),
              transform var(--dur-entrance) var(--ease-signature);
}
.reveal.is-in { opacity: 1; transform: translateY(0); }
.reveal:nth-child(2) { transition-delay: .1s; }  /* stagger 0.1–0.2s */
.reveal:nth-child(3) { transition-delay: .2s; }

/* Hover link — opacity, not color */
.link { transition: opacity .2s var(--ease-signature); }
.link:hover { opacity: 0.6; }

/* Accessibility — always */
@media (prefers-reduced-motion: reduce) {
  * { animation: none !important; transition-duration: .01ms !important; }
  .reveal { opacity: 1; transform: none; }
}
```

**Faça isso**

1. Escolha uma curva de easing e armazene-a como `--ease-signature`. Use-a para toda transição e animação.
2. Defina duas faixas de duração: rápida para feedback de UI (0.3–0.5s), lenta para entradas de seção (1.0–1.4s).
3. Faça os reveals serem um fade mais um pequeno `translateY` (24–40px), nunca um slide vindo de fora da tela.
4. Escalone elementos agrupados em 0.1–0.2s para que entrem em sequência, não todos de uma vez.
5. No hover, reduza a opacidade para ~0.6 em vez de trocar cores — mais quieto, mais caro.
6. Adicione um bloco `prefers-reduced-motion` que neutraliza o movimento e revela o conteúdo instantaneamente.

**Evite** — Bounces e springs. Eles se leem como brincalhão, não premium, e quebram a ilusão de uma única mão no controle.

---

## 9. Tokens e documentação

Se um estranho — ou um agente de IA — não consegue aplicar o seu sistema, você não tem um sistema. Você tem uma memória.

**A regra** — Todo valor vive como um token nomeado em um único bloco `:root`, nomeado pelo que significa, para que o sistema inteiro possa ser entendido e aplicado sem você na sala.

**Por que funciona** — Uma única fonte de verdade elimina para sempre o problema do "qual azul era mesmo?". Nomes semânticos (`--accent`, `--space-3`, `--radius-md`) sobrevivem a redesigns que nomes literais (`--blue`, `--px-24`) não sobrevivem — quando o acento muda de azul para verde, `--accent` ainda faz sentido. E documentação é alavancagem: um arquivo de tokens bem nomeado é um briefing que um colega, um cliente ou um agente pode executar sem ambiguidade alguma. O sistema se torna portátil, ensinável e durável.

**Exemplo** — Toda a fundação do sistema de exemplo em um único bloco:

```css
:root {
  /* Color */
  --ink:          #16181D;
  --paper:        #FAFAF8;
  --accent:       #2F6FED;
  --surface-dark: #0E0F12;
  --hairline:     rgba(255,255,255,0.10);

  /* Spacing — 8-point scale */
  --space-1: 8px;   --space-2: 16px;  --space-3: 24px;
  --space-4: 32px;  --space-6: 48px;  --space-8: 64px;

  /* Radii */
  --radius-sm: 8px;   --radius-md: 12px;  --radius-lg: 16px;
  --radius-xl: 24px;  --radius-pill: 999px;

  /* Type */
  --font-display: "Fraunces", serif;
  --font-body:    "Inter", sans-serif;

  /* Shadows */
  --shadow-sm:   0 1px 2px  rgba(16,18,29,0.06);
  --shadow-md:   0 8px 24px rgba(16,18,29,0.10);
  --shadow-lg:   0 20px 50px rgba(16,18,29,0.16);
  --shadow-glow: 0 0 30px   rgba(47,111,237,0.30);

  /* Motion */
  --ease-signature: cubic-bezier(0.16, 1, 0.3, 1);
  --dur-ui: .4s;
  --dur-entrance: 1.2s;
}
```

> Um único arquivo. Entregue-o a qualquer pessoa — um desenvolvedor, um designer, um agente — e ela consegue construir uma página que parece ter saído de você.
> 

**Faça isso**

1. Reúna toda cor, espaço, raio, fonte, sombra e valor de movimento em um único bloco `:root`.
2. Nomeie os tokens pelo significado (`--accent`, `--space-3`), nunca pela aparência literal (`--blue`, `--px-24`).
3. Mantenha as escalas numeradas e ordenadas para que as relações sejam óbvias à primeira vista.
4. Adicione um comentário de uma linha por grupo para que um recém-chegado consiga navegar sem perguntar.
5. Referencie os tokens em tudo daí para frente — componentes e páginas não devem conter nenhum valor cru.
6. Trate este arquivo como o contrato: se não é um token, não entra.

**Evite** — Manter tokens em dois lugares (um arquivo de design e o código) que derivam e se afastam. Escolha uma fonte de verdade e derive todo o resto dela.

---

## 10. Exemplo desenvolvido — um sistema decodificado

A prova de que restrições, não adições, são o que faz um site parecer caro.

**A regra** — Um sistema coeso é construído a partir de um punhado de restrições travadas; a disciplina de *não* adicionar é o que produz o resultado premium.

**Por que funciona** — Percorra o sistema de exemplo de ponta a ponta e você vai notar que quase não há nada nele — e é exatamente esse o ponto. Cada decisão é singular e deliberada. A ausência de escolhas é o que o olho lê como caro. A coesão não é alcançada adicionando polimento por cima; é alcançada removendo a capacidade de ser inconsistente.

**Exemplo** — O sistema de exemplo, decodificado peça por peça:

> **O canvas** — Papel `#FAFAF8`, não branco puro. Um branco-quebrado quente já sinaliza "pensado" antes de uma única palavra ser lida.
> 

> **A tinta** — O texto é `#16181D`, um quase-preto com um traço de azul-acinzentado. Mais suave que `#000000`, para que a página se leia calma em vez de agressiva.
> 

> **Um acento, usado como momento** — O azul `#2F6FED` aparece exatamente onde merece atenção: a seta do CTA, o preenchimento de hover de um chip, um anel de foco. Por ser racionado, ele acerta. Um segundo acento teria cortado seu poder pela metade.
> 

> **Duas fontes, dois trabalhos** — Uma serifada de display carrega os títulos com autoridade editorial; uma sans de corpo cuida da leitura. A tensão entre as duas *é* a personalidade — nenhuma terceira fonte é convidada.
> 

> **A escala de 8** — Cada espaço é 8, 16, 24, 32, 48 ou 64. Nada entre eles. O ritmo é invisível, mas sentido: a página respira sobre um grid.
> 

> **Raios suaves** — 8/12/16/24, mais uma pílula de 999px para qualquer coisa que deva parecer humana. Uma família de raios, aplicada por função, nunca misturada ao acaso.
> 

> **Três sombras** — `sm` para cards em repouso, `md` para o levantar no hover, `lg` para elevação de verdade — mais um `glow` de acento reservado para um único momento de hero. Profundidade é um vocabulário de quatro, não um gradiente infinito de palpites.
> 

> **Um easing de assinatura** — `cubic-bezier(0.16, 1, 0.3, 1)` move tudo. Os reveals fazem fade e sobem 32px; os links fazem fade para 0.6 no hover; o CTA pressiona para `scale(0.97)`. Nada quica. Uma única mão controla tudo isso.
> 

> **O CTA em pílula de tinta** — Fundo de tinta, rótulo branco em caixa alta com +1.5px de tracking, raio de 24px, uma seta de acento e aquele pressionar quieto `scale(0.97)`. É memorável porque é contido.
> 

Amarre tudo e a lógica é inconfundível: **restrições → coesão → parece caro.** Um canvas, uma tinta, um acento, duas fontes, uma escala de espaçamento, uma família de raios, quatro sombras, um easing. O site parece caro não porque algo raro foi adicionado, mas porque tudo que era arbitrário foi removido. Esse é o método inteiro.

**Faça isso**

1. Audite o seu próprio sistema e conte suas decisões: quantos acentos, fontes, easings, valores de espaçamento?
2. Onde quer que a contagem seja maior que um (ou que os poucos que você pretendia), corte até que não seja.
3. Atribua a cada escolha sobrevivente um único trabalho e nunca a deixe desviar dele.
4. Racione o seu acento — reserve-o para momentos que merecem atenção, não para decoração.
5. Leia a página final e pergunte: um estranho conseguiria adivinhar as regras só de olhar? Se sim, o sistema é coerente.

**Evite** — Adicionar mais uma cor, fonte ou efeito "bacana" a um sistema que já funciona. A adição raramente o melhora e quase sempre dilui a coesão que você trabalhou para construir.

---

## Seu checklist de construção

Copie isto para o seu projeto. Marque cada caixa somente quando a decisão estiver travada.

- [ ]  **Canvas** — um fundo escolhido (branco-quebrado quente ou escuro de verdade), não `#FFFFFF` puro
- [ ]  **Tinta** — uma cor de texto principal, um quase-preto suavizado, não `#000000`
- [ ]  **Um acento + variantes** — um único acento com tons de hover/pressionado/sutil definidos; racionado para momentos
- [ ]  **Cinzas** — uma pequena rampa neutra para bordas, texto atenuado e superfícies
- [ ]  **Escala de espaçamento** — uma escala de 8 pontos (8/16/24/32/48/64); nada entre eles
- [ ]  **Duas fontes** — uma de display + uma de corpo, cada uma com um trabalho definido
- [ ]  **Escala tipográfica** — um conjunto fixo de tamanhos e pesos, sem valores improvisados
- [ ]  **Família de raios** — um conjunto (ex.: 8/12/16/24 + pílula 999), aplicado por função
- [ ]  **Conjunto de sombras** — um vocabulário de profundidade finito (sm/md/lg + um brilho opcional)
- [ ]  **Componentes centrais** — CTA/botão, chip de tag, card, input, header/nav — todos construídos a partir de tokens, todos os estados definidos
- [ ]  **Easing de assinatura** — uma curva, duas faixas de duração, fallback de movimento reduzido
- [ ]  **Tokens documentados** — todo valor nomeado em uma única fonte de verdade `:root`, pronto para um estranho ou um agente aplicar
