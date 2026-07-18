---
name: sprint-context-generator
description: Generates comprehensive sprint documentation (spec.md, plan.md, tasks.md, research.md, features.xml) following Spec-Driven Development methodology with multi-persona analysis (Architect, Dev, QA, Designer, PM, BA). Use when planning new features or refactoring existing ones. Compatible with long-running-agent. Automatically researches documentation (WebSearch/WebFetch), creates 50-100 granular tasks with E2E (Playwright) and TDD coverage, generates sequential feature IDs (FEAT-XXX), and creates git branch/commit. Always asks interactive questions to gather requirements before generating complete, production-ready context.
---

# Sprint Context Generator

## Visão Geral

Gera documentação completa e estruturada para alimentar a skill `long-running-agent`. Segue metodologia **Spec-Driven Development** inspirada no spec-kit do GitHub, incorporando análises de múltiplas personas e garantindo cobertura completa de testes E2E e TDD.

Esta skill transforma uma ideia de feature em documentação executável através de:
- Coleta interativa de requisitos com confirmação
- Pesquisa automatizada de documentação e melhores práticas (WebSearch/WebFetch)
- Análise multi-perspectiva (6 personas: Arquiteto, Dev, QA, Designer, PM, BA)
- Geração de 50-100 tasks granulares e específicas
- Validação automática de qualidade e compatibilidade

## Quando Usar Esta Skill

Use esta skill quando você precisa:
- ✅ Planejar novas features para um projeto
- ✅ Refatorar features existentes com documentação adequada
- ✅ Criar contexto estruturado para desenvolvimento prolongado
- ✅ Preparar trabalho para delegação a SubAgents
- ✅ Garantir que todos os stakeholders (Arquiteto, QA, PM, etc.) tenham input
- ✅ Gerar documentação compatível com `long-running-agent`

**NÃO use** para:
- ❌ Implementação direta de código (use `long-running-agent` após gerar docs)
- ❌ Tarefas triviais que não requerem planejamento
- ❌ Apenas consultar informações (use `general-purpose` ou `Explore`)

## O Que Esta Skill Gera

### 5 Arquivos de Documentação Completa:

1. **spec.md** (~800-1200 linhas)
   - Especificação detalhada com análises das 6 personas
   - User stories e casos de uso
   - Critérios de aceitação
   - Requisitos de performance/segurança
   - Dependências e bloqueadores

2. **plan.md** (~600-900 linhas)
   - Plano técnico de arquitetura
   - Stack tecnológica recomendada
   - Estrutura de diretórios
   - Componentes e módulos
   - APIs e contratos
   - Variáveis de ambiente
   - Decisões técnicas e riscos

3. **tasks.md** (~400-800 linhas)
   - 50-100 tasks granulares organizadas por tipo:
     - 🏗️ Setup/Arquitetura (5-10 tasks)
     - 💻 Backend (15-25 tasks)
     - 🎨 Frontend/UI (20-30 tasks)
     - ✅ Testes Unitários (10-15 tasks)
     - ✅ Testes E2E (10-15 tasks)
     - 📝 Documentação (3-5 tasks)

4. **research.md** (~300-600 linhas)
   - Documentação de tecnologias externas pesquisadas
   - Melhores práticas (Clean Arch, TDD, E2E, Linting, Husky)
   - Artigos e recursos relevantes
   - Exemplos de implementação

5. **features.xml**
   - Formato XML compatível com `long-running-agent`
   - Feature com ID sequencial (FEAT-XXX)
   - Status, prioridade, categoria
   - Critérios de aceitação
   - Referência aos docs gerados

**Localização de saída:** `docs/context-log-running/<feature-name>/`

**Extras:**
- Branch Git criada automaticamente: `feature/FEAT-XXX-<feature-name>`
- Commit com mensagem padronizada
- Validação automática de qualidade e compatibilidade
- Resumo com estimativa de complexidade e próximos passos

---

## Workflow Principal

Esta skill executa **5 fases sequenciais** para garantir documentação completa e de alta qualidade.

---

### FASE 1: Coleta de Informações (Interactive Discovery)

Objetivo: Entender completamente o contexto do projeto e os requisitos da feature através de perguntas interativas.

#### 1.1. Verificar Estrutura Existente (CRÍTICO)

**1.1.1. Verificar se `.claude/` existe:**

Execute:
```bash
ls -la .claude/
```

**Cenário A: `.claude/` NÃO EXISTE (projeto novo/legado)**

Pergunte ao usuário:
```
⚠️ Este projeto ainda não tem estrutura de long-running-agent (.claude/).

A skill long-running-agent precisa dessa estrutura para executar as tasks automaticamente.

Deseja inicializá-la agora?
1. Sim, inicializar estrutura completa (recomendado)
2. Não, criar apenas documentação da feature (sem integração com long-running-agent)
```

**Se opção 1 (SIM):**
- Informar: "Vou inicializar a estrutura .claude/ para você."
- Executar: `python "${SKILLS_DIR}/long-running-agent/scripts/init_project.py"` (substitua `${SKILLS_DIR}` pelo caminho onde a skill `long-running-agent` está instalada)
- Aguardar conclusão
- Continuar normalmente com geração de ID sequencial

**Se opção 2 (NÃO):**
- ⚠️ **AVISO**:
  ```
  IMPORTANTE: Sem `.claude/`, a skill long-running-agent NÃO funcionará.
  Você terá apenas a documentação em docs/context-log-running/<feature-name>/.

  Você poderá inicializar .claude/ mais tarde executando:
  python skills/long-running-agent/scripts/init_project.py
  ```
- Criar apenas `docs/context-log-running/<feature-name>/`
- Usar **FEAT-001** como ID padrão
- Pular integração com `.claude/features.xml` global
- Gerar apenas o `features.xml` local em `docs/context-log-running/<feature-name>/`

**Cenário B: `.claude/` EXISTE mas `features.xml` está vazio/ausente**

- Criar `features.xml` inicial em `.claude/`
- Usar **FEAT-001** como primeiro ID

**Cenário C: `.claude/features.xml` TEM features (cenário normal)**

- Ler arquivo: `cat .claude/features.xml`
- Extrair último ID (ex: `<feature id="FEAT-015"...`)
- Incrementar sequencialmente: FEAT-016
- **Fallback**: Se XML corrompido:
  - Avisar usuário: "features.xml parece corrompido. Usando FEAT-001 como ID padrão."
  - Usar FEAT-001

**1.1.2. Verificar tech stack do projeto:**

Detectar framework/linguagem através de arquivos de configuração:

```bash
# Tentar package.json (Node.js/JavaScript)
cat package.json 2>/dev/null

# Se não existir, tentar requirements.txt (Python)
cat requirements.txt 2>/dev/null

# Se não existir, tentar pom.xml (Java/Maven)
cat pom.xml 2>/dev/null

# Se não existir, tentar Cargo.toml (Rust)
cat Cargo.toml 2>/dev/null
```

**Extrair informações:**
- Framework principal (Next.js, React, Express, Django, Spring Boot, etc.)
- Linguagem (TypeScript, JavaScript, Python, Java, Rust, etc.)
- Dependências principais
- Framework de testes atual (se houver)

**Se nenhum arquivo encontrado:**
- Perguntar ao usuário: "Não detectei o stack tecnológico automaticamente. Qual framework/linguagem você está usando?"

---

#### 1.2. Perguntas Interativas (Sequenciais, Uma por Vez, com Confirmação)

**IMPORTANTE:** Fazer perguntas **uma por vez**, aguardar resposta e confirmar compreensão antes de continuar.

---

**Q1: Nome da Feature**

Pergunte:
```
Qual o nome/título da feature que você quer planejar?

Exemplos:
- "Sistema de Autenticação JWT"
- "Dashboard de Analytics em Tempo Real"
- "Integração com API de Pagamento Stripe"

Nome da feature:
```

[Aguardar resposta do usuário]

**Confirmação Q1:**
```
Entendi! Nome da feature: "[resposta do usuário]"

Isso está correto? (Sim/Não)
```

[Aguardar confirmação. Se "Não", perguntar novamente]

---

**Q2: Descrição da Feature**

Pergunte:
```
Descreva detalhadamente a feature:
- O que ela faz?
- Qual problema resolve?
- Como o usuário vai interagir com ela?

Seja específico e detalhado.

Descrição:
```

[Aguardar resposta do usuário]

**Confirmação Q2:**
```
Resumindo sua feature:
"[Resumo conciso da resposta em 2-3 frases]"

Isso captura corretamente o que você quer? (Sim/Não)
```

[Aguardar confirmação. Se "Não", pedir esclarecimentos]

---

**Q3: User Stories**

Pergunte:
```
Quais são as user stories principais para esta feature?

Use o formato: "Como [tipo de usuário], quero [ação], para [benefício]"

Exemplos:
- Como usuário, quero fazer login com email e senha, para acessar minha conta de forma segura
- Como admin, quero resetar senhas de usuários, para ajudá-los quando esquecerem
- Como visitante, quero criar uma conta, para começar a usar o sistema

Liste de 2 a 5 user stories:
```

[Aguardar resposta do usuário]

**Validação:**
Se usuário não usar formato adequado, reformatar e confirmar:
```
Reformatei suas user stories no formato padrão:

1. Como [tipo], quero [ação], para [benefício]
2. Como [tipo], quero [ação], para [benefício]
...

Está correto? (Sim/Não)
```

---

**Q4: Tecnologias Externas**

Pergunte:
```
Esta feature usa tecnologias externas? (APIs, bibliotecas, serviços de terceiros)

Se SIM, forneça:
- Nome da tecnologia
- Link da documentação oficial
- Versão (se souber)

Exemplos:
- Stripe API: https://stripe.com/docs/api
- NextAuth.js: https://next-auth.js.org/getting-started/introduction
- Prisma ORM: https://www.prisma.io/docs

Se NÃO usa tecnologias externas, digite "Nenhuma".

Tecnologias externas:
```

[Aguardar resposta do usuário]

**Se forneceu links:**
- Confirmar: "Vou pesquisar a documentação de [tecnologia 1], [tecnologia 2]... durante a Fase 2."

**Se respondeu "Nenhuma":**
- Confirmar: "Entendido. Feature não depende de tecnologias externas."

---

**Q5: Requisitos de Performance/Segurança**

Pergunte:
```
Há requisitos específicos de performance ou segurança para esta feature?

Exemplos de requisitos:
- SEGURANÇA: "Autenticação deve usar JWT com algoritmo RS256"
- SEGURANÇA: "Senhas devem ser hash com bcrypt (custo 12)"
- SEGURANÇA: "Dados sensíveis devem ser criptografados em repouso (AES-256)"
- PERFORMANCE: "Tempo de resposta < 200ms para todas as APIs"
- PERFORMANCE: "Suportar 1000 requisições simultâneas"
- PERFORMANCE: "Rate limiting: max 100 requests/min por IP"

Se NÃO há requisitos específicos, digite "Padrões normais".

Requisitos:
```

[Aguardar resposta do usuário]

**Confirmação:**
```
Requisitos de performance/segurança anotados:
[Listar requisitos fornecidos ou "Aplicar padrões normais de segurança e performance"]

Correto? (Sim/Não)
```

---

**Q6: Dependências e Bloqueadores**

Pergunte:
```
Esta feature depende de outras features ou infraestrutura ainda não implementada?

Exemplos de dependências:
- "Depende de FEAT-003 (Sistema de Autenticação)" ← feature existente
- "Requer banco de dados PostgreSQL configurado" ← infraestrutura
- "Precisa de Redis para cache" ← serviço externo
- "Depende de FEAT-010 (API de Usuários)" ← outra feature

Se NÃO há dependências, digite "Nenhuma".

Dependências:
```

[Aguardar resposta do usuário]

**Se houver dependências:**

- Perguntar:
  ```
  Qual o status dessa dependência?

  Se for uma feature: forneça o ID (ex: FEAT-003)
  Se for infraestrutura: ela já está implementada? (Sim/Não)
  ```

- **Se dependência NÃO está pronta:**
  - Marcar feature como `status="blocked"` em features.xml
  - Adicionar nota: `Blocked: Requires [FEAT-XXX] ou [descrição da infraestrutura]`
  - ⚠️ **AVISO ao usuário**:
    ```
    ATENÇÃO: Esta feature está BLOQUEADA.

    Bloqueador: [descrição]

    Você deve implementar/configurar o bloqueador ANTES de usar long-running-agent para esta feature.
    A documentação será gerada normalmente, mas a implementação só poderá começar após resolver o bloqueador.
    ```

---

**Q7: Categoria da Feature**

Pergunte:
```
Esta feature pertence a qual categoria?

Categorias comuns:
- Authentication (login, registro, sessões)
- Dashboard (visualizações, gráficos, métricas)
- API (endpoints REST/GraphQL)
- Database (modelos, migrações, queries)
- UI Components (componentes reutilizáveis)
- Payment (integrações de pagamento)
- Admin (painéis administrativos)
- Notifications (emails, push, in-app)

Baseado na descrição da feature, sugiro: "[categoria sugerida baseada em Q2]"

Qual categoria deseja usar? (Pode usar a sugerida ou outra)
```

[Aguardar resposta do usuário]

---

**1.3. Resumo da Coleta**

Após todas as perguntas, exibir resumo:

```
✅ Coleta de informações completa!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 RESUMO DA FEATURE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Feature: [Nome]
ID: FEAT-XXX
Categoria: [Categoria]
Status: [Pending/Blocked]

Descrição: [Resumo de 1-2 linhas]

User Stories: [N] stories coletadas
Tecnologias externas: [N] tecnologias identificadas
Requisitos especiais: [Lista]
Dependências: [Nenhuma/Bloqueada por X]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Agora vou pesquisar documentação e melhores práticas... (Fase 2)
```

---

### FASE 2: Pesquisa e Contextualização (Detalhada)

Objetivo: Pesquisar documentação oficial, melhores práticas e exemplos de implementação para enriquecer o contexto.

---

#### 2.1. Pesquisar Documentação de Tecnologias Externas

**Para cada link fornecido pelo usuário em Q4:**

1. **Usar WebFetch para extrair conteúdo:**
   ```
   WebFetch(url=link_fornecido, prompt="Extraia as seguintes informações:
   - Seção 'Getting Started' ou 'Quick Start'
   - Principais métodos/funções da API
   - Exemplos de código básicos
   - Requisitos de instalação
   - Versão mais recente recomendada

   Retorne em formato markdown organizado.")
   ```

2. **Focar em:**
   - Seções "Getting Started", "Quick Start", "Introduction"
   - Métodos/APIs principais (top 5-10 mais usados)
   - Exemplos de código práticos (preferir código a teoria)
   - Requisitos de instalação/configuração
   - Versões recomendadas/compatibilidade

3. **Limites (evitar sobrecarga de contexto):**
   - Máximo **3 páginas por tecnologia**
   - Extrair apenas seções relevantes (não página inteira)
   - Priorizar exemplos de código sobre explicações teóricas longas
   - Se documentação > 10.000 palavras, fazer 2-3 WebFetch focados em seções diferentes

4. **Fallback se link inacessível (404, timeout, erro):**
   - Usar WebSearch: `"[Nome da Tecnologia] official documentation 2026"`
   - Buscar 2-3 resultados mais relevantes
   - Priorizar:
     - Domínio oficial (.org, site oficial, GitHub oficial)
     - Documentação atualizada (2024-2026)
     - Fontes confiáveis (npm, PyPI, Maven Central)

**Exemplo de extração estruturada:**

```markdown
### NextAuth.js
- **Link**: https://next-auth.js.org/getting-started/introduction
- **Versão**: 4.24.0 (latest stable)
- **Instalação**:
  ```bash
  npm install next-auth
  ```

- **Principais métodos:**
  - `signIn(provider, options)`: Iniciar autenticação com provedor (Google, GitHub, etc.)
  - `signOut(options)`: Encerrar sessão do usuário
  - `useSession()`: Hook React para acessar dados da sessão atual
  - `getServerSession(req, res, authOptions)`: Obter sessão no server-side

- **Exemplo básico de configuração:**
  ```typescript
  // pages/api/auth/[...nextauth].ts
  import NextAuth from "next-auth"
  import GoogleProvider from "next-auth/providers/google"

  export default NextAuth({
    providers: [
      GoogleProvider({
        clientId: process.env.GOOGLE_ID,
        clientSecret: process.env.GOOGLE_SECRET,
      }),
    ],
    callbacks: {
      async session({ session, token }) {
        session.user.id = token.sub
        return session
      },
    },
  })
  ```

- **Configurações importantes:**
  - Variáveis de ambiente: `NEXTAUTH_SECRET`, `NEXTAUTH_URL`
  - Providers suportados: 50+ (Google, GitHub, Facebook, Email, etc.)
  - Suporte a JWT e Database sessions

- **Links úteis:**
  - Configuração avançada: https://next-auth.js.org/configuration/options
  - Provedores: https://next-auth.js.org/providers
```

**Informar progresso ao usuário:**
```
🔍 Pesquisando documentação de [Tecnologia 1]...
✅ NextAuth.js: Documentação extraída (principais métodos, exemplos, config)

🔍 Pesquisando documentação de [Tecnologia 2]...
✅ Stripe API: Documentação extraída (payment intents, webhooks, exemplos)
```

---

#### 2.2. Pesquisar Melhores Práticas (WebSearch Focado)

**Executar 5 buscas estratégicas baseadas no tech stack detectado:**

**Busca 1: Clean Architecture**

Query:
```
"Clean Architecture [tech-stack detectado] best practices 2026"
```

Exemplo real:
```
"Clean Architecture Next.js TypeScript best practices 2026"
```

**Coletar:**
- 2-3 resultados top (priorizar: dev.to, medium engineering blogs, GitHub repos populares)

**Extrair:**
- Padrões de estrutura de diretórios
- Separação de camadas (presentation, business, data)
- Dependency injection patterns
- Exemplos de código de estrutura

---

**Busca 2: Testes E2E com Playwright**

Query:
```
"Playwright E2E testing patterns examples [framework detectado] 2026"
```

Exemplo real:
```
"Playwright E2E testing patterns examples Next.js 2026"
```

**Coletar:**
- 2-3 artigos/repositórios

**Extrair:**
- Estrutura de testes recomendada (Page Object Model, etc.)
- Fixtures e helpers comuns
- Exemplos de testes E2E completos
- Configuração do Playwright

---

**Busca 3: TDD (Test-Driven Development)**

Query:
```
"TDD [tech-stack] practical guide examples 2026"
```

Exemplo real:
```
"TDD TypeScript Jest practical guide examples 2026"
```

**Coletar:**
- 2 guias práticos

**Extrair:**
- Workflow Red-Green-Refactor com exemplos
- Estrutura de testes unitários
- Mocking e test doubles
- Coverage tools e targets

---

**Busca 4: Linting e Formatação**

Query:
```
"ESLint Prettier setup [framework] best config 2026"
```

Exemplo real:
```
"ESLint Prettier setup Next.js TypeScript best config 2026"
```

**Coletar:**
- 2 configurações recomendadas

**Extrair:**
- Arquivos `.eslintrc.js` ou `eslint.config.js`
- Arquivo `.prettierrc`
- Regras essenciais recomendadas
- Plugins úteis (typescript-eslint, etc.)

---

**Busca 5: Husky Git Hooks**

Query:
```
"Husky git hooks pre-commit pre-push configuration tutorial 2026"
```

**Coletar:**
- 1-2 tutoriais atualizados

**Extrair:**
- Setup completo do Husky
- Scripts de hooks (pre-commit, pre-push, commit-msg)
- Integração com lint-staged
- Exemplos de configuração

---

**Para cada busca:**
- Coletar **máximo 3 resultados** mais relevantes
- Extrair padrões e **exemplos de código**
- **Priorizar fontes oficiais e reconhecidas:**
  - Documentação oficial
  - GitHub oficial da ferramenta
  - Blogs técnicos reconhecidos (dev.to, Medium engineering, LogRocket, etc.)
  - Repositórios GitHub com muitas stars (>1k stars)
- **Evitar:**
  - Tutoriais desatualizados (>2 anos, antes de 2024)
  - Fontes não confiáveis ou blogs pessoais obscuros
  - Conteúdo muito genérico que não traz valor

**Informar progresso ao usuário:**
```
🔍 Pesquisando melhores práticas...
✅ Clean Architecture para [stack]
✅ Testes E2E com Playwright
✅ TDD patterns
✅ ESLint/Prettier configs
✅ Husky hooks setup

Pesquisa concluída! Consolidando em research.md...
```

---

#### 2.3. Consolidação em research.md

**Organizar em 4 seções principais:**

```markdown
# Pesquisa e Documentação: FEAT-XXX - [Nome da Feature]

**Data da pesquisa:** [YYYY-MM-DD]
**Tecnologias pesquisadas:** [N] tecnologias
**Melhores práticas:** 5 áreas (Clean Arch, E2E, TDD, Linting, Hooks)

---

## Índice

1. [Tecnologias Utilizadas](#tecnologias-utilizadas)
2. [Melhores Práticas Pesquisadas](#melhores-práticas-pesquisadas)
3. [Artigos Relevantes](#artigos-relevantes)
4. [Exemplos de Implementação](#exemplos-de-implementação)

---

## 1. Tecnologias Utilizadas

[Uma subseção por tecnologia pesquisada]

### 1.1. [Nome da Tecnologia 1]
- **Link oficial**: [URL]
- **Versão**: [version]
- **Descrição**: [1-2 frases sobre o que é]
- **Instalação**:
  ```bash
  [comando de instalação]
  ```

- **Principais métodos/APIs**:
  - `método1()`: [descrição sucinta]
  - `método2()`: [descrição sucinta]
  - `método3()`: [descrição sucinta]

- **Exemplo básico**:
  ```[linguagem]
  [código de exemplo extraído da documentação]
  ```

- **Configurações importantes**:
  - [Config 1]: [descrição]
  - [Config 2]: [descrição]

- **Links úteis**:
  - [Seção da doc]: [URL]

---

### 1.2. [Nome da Tecnologia 2]
[Mesmo formato]

---

## 2. Melhores Práticas Pesquisadas

### 2.1. Clean Architecture

**Fontes:**
- [Título do artigo/repo](URL)
- [Título do artigo/repo](URL)

**Resumo dos principais pontos:**
- **Estrutura de diretórios recomendada:**
  ```
  src/
  ├── presentation/    # Controllers, rotas, UI
  ├── application/     # Use cases, serviços de aplicação
  ├── domain/          # Entidades, regras de negócio
  └── infrastructure/  # DB, APIs externas, frameworks
  ```

- **Princípios chave:**
  - Dependências apontam para dentro (domain não depende de nada)
  - Use cases orquestram o fluxo
  - Inversão de dependência para acesso a dados

- **Exemplo de estrutura aplicada ao [stack detectado]:**
  ```
  [Estrutura específica para o projeto]
  ```

---

### 2.2. Testes E2E com Playwright

**Fontes:**
- [Título](URL)
- [Título](URL)

**Estrutura recomendada:**
```
tests/
├── e2e/
│   ├── fixtures/           # Dados de teste, helpers
│   ├── pages/              # Page Object Model
│   │   ├── login.page.ts
│   │   └── dashboard.page.ts
│   └── specs/
│       ├── auth.spec.ts
│       └── dashboard.spec.ts
└── playwright.config.ts
```

**Patterns úteis:**
- **Page Object Model**: Encapsular lógica de página
- **Fixtures customizados**: Compartilhar setup entre testes
- **Auto-waiting**: Playwright espera automaticamente por elementos

**Exemplo de teste E2E:**
```typescript
[Exemplo extraído da pesquisa]
```

---

### 2.3. TDD (Test-Driven Development)

**Fontes:**
- [Título](URL)

**Workflow Red-Green-Refactor:**
1. 🔴 **Red**: Escrever teste que falha
2. 🟢 **Green**: Implementar código mínimo para passar
3. 🔵 **Refactor**: Melhorar código mantendo testes passando

**Exemplo prático:**
```[linguagem]
// Red: Teste falha
test('should authenticate user with valid credentials', () => {
  const result = authService.login('user@example.com', 'password123')
  expect(result.success).toBe(true)
  expect(result.token).toBeDefined()
})

// Green: Implementação mínima
class AuthService {
  login(email, password) {
    return { success: true, token: 'fake-jwt-token' }
  }
}

// Refactor: Implementação real
class AuthService {
  login(email, password) {
    const user = db.findByEmail(email)
    if (!user || !bcrypt.compare(password, user.passwordHash)) {
      return { success: false, error: 'Invalid credentials' }
    }
    const token = jwt.sign({ userId: user.id }, SECRET)
    return { success: true, token }
  }
}
```

**Metas de cobertura:**
- Unitários: >80%
- Integração: >70%
- E2E: Fluxos principais 100%

---

### 2.4. Linting (ESLint/Prettier)

**Fontes:**
- [Título](URL)

**Configuração recomendada:**

**`.eslintrc.js`:**
```javascript
[Configuração extraída da pesquisa]
```

**`.prettierrc`:**
```json
[Configuração extraída da pesquisa]
```

**Scripts package.json:**
```json
{
  "scripts": {
    "lint": "eslint . --ext .ts,.tsx",
    "lint:fix": "eslint . --ext .ts,.tsx --fix",
    "format": "prettier --write \"**/*.{ts,tsx,json,md}\""
  }
}
```

---

### 2.5. Husky Git Hooks

**Fontes:**
- [Título](URL)

**Setup completo:**

1. **Instalação:**
   ```bash
   npm install --save-dev husky lint-staged
   npx husky init
   ```

2. **Configurar pre-commit** (`.husky/pre-commit`):
   ```bash
   #!/usr/bin/env sh
   . "$(dirname -- "$0")/_/husky.sh"

   npx lint-staged
   ```

3. **Configurar lint-staged** (`package.json`):
   ```json
   {
     "lint-staged": {
       "*.{ts,tsx}": [
         "eslint --fix",
         "prettier --write"
       ],
       "*.{json,md}": [
         "prettier --write"
       ]
     }
   }
   ```

4. **Configurar pre-push** (`.husky/pre-push`):
   ```bash
   #!/usr/bin/env sh
   . "$(dirname -- "$0")/_/husky.sh"

   npm run test
   ```

---

## 3. Artigos Relevantes

Lista de artigos, tutoriais e recursos para leitura futura:

- [Título do artigo 1](URL) - Resumo de 1 linha sobre o conteúdo
- [Título do artigo 2](URL) - Resumo de 1 linha
- [Título do artigo 3](URL) - Resumo de 1 linha
[... até 10 artigos]

---

## 4. Exemplos de Implementação

Repositórios GitHub de referência que implementam padrões similares:

### 4.1. [Nome do Repositório 1]
- **Link**: [URL do GitHub]
- **Stars**: [N] ⭐
- **Stack**: [Tecnologias usadas]
- **O que aproveitar**:
  - [Insight 1: ex: "Estrutura de diretórios muito clara"]
  - [Insight 2: ex: "Excelente cobertura de testes E2E"]
  - [Insight 3: ex: "Padrão de error handling robusto"]

### 4.2. [Nome do Repositório 2]
[Mesmo formato]

---

**Fim do research.md**
```

**Objetivo:** research.md deve ser consultável rapidamente (índice no topo), bem estruturado e conter exemplos práticos, não apenas links.

**Informar usuário:**
```
✅ research.md gerado com sucesso!
   - [N] tecnologias documentadas
   - 5 áreas de melhores práticas pesquisadas
   - [N] artigos relevantes coletados
   - [N] repositórios de exemplo identificados

Agora vou fazer análise multi-persona... (Fase 3)
```

---

### FASE 3: Análise Multi-Persona

Objetivo: Analisar a feature sob 6 perspectivas diferentes para garantir cobertura holística de todos os aspectos (técnicos, negócio, UX, qualidade).

**Para cada persona, gerar análise específica que será incluída no spec.md:**

---

#### 3.1. 🏗️ Arquiteto de Soluções

**Foco:** Estrutura técnica, arquitetura, dependências, escalabilidade

**Perguntas que o Arquiteto responde:**
- Como organizar o código? (estrutura de diretórios)
- Quais packages/dependências instalar?
- Há necessidade de refatoração de código existente?
- Qual padrão de arquitetura aplicar? (MVC, Clean, Hexagonal, etc.)
- Como garantir escalabilidade e manutenibilidade?

**Análise a gerar:**

```markdown
## 🏗️ Análise do Arquiteto de Soluções

### Estrutura de Diretórios Proposta

Baseado em Clean Architecture e melhores práticas de [framework detectado]:

```
[Estrutura específica para o projeto]
```

**Justificativa:**
- [Explicar escolha da estrutura]
- [Separação de responsabilidades]
- [Facilita testes e manutenção]

### Dependências Necessárias

**Produção:**
```json
{
  "[package1]": "^[version]",  // [Justificativa]
  "[package2]": "^[version]",  // [Justificativa]
}
```

**Desenvolvimento:**
```json
{
  "[dev-package1]": "^[version]",  // [Justificativa]
  "[dev-package2]": "^[version]",  // [Justificativa]
}
```

### Refatorações Necessárias

[Se aplicável, listar código existente que precisa ser refatorado]

**Exemplo:**
- **Módulo X**: Atualmente monolítico, deve ser separado em serviços menores
- **Componente Y**: Deve ser extraído para reutilização

### Padrões de Arquitetura

**Padrão escolhido:** [Clean Architecture / MVC / Hexagonal / etc.]

**Camadas:**
1. **Presentation Layer**: [Responsabilidades]
2. **Application Layer**: [Responsabilidades]
3. **Domain Layer**: [Responsabilidades]
4. **Infrastructure Layer**: [Responsabilidades]

**Fluxo de dados:**
```
[Diagrama em ASCII ou descrição textual]
User Request → Controller → Use Case → Repository → Database
            ← DTO        ← Entity   ← Model      ←
```

### Decisões de Escalabilidade

- [Decisão 1]: [ex: "Usar cache Redis para sessões"]
- [Decisão 2]: [ex: "Implementar rate limiting no Nginx"]
- [Decisão 3]: [ex: "Preparar para horizontal scaling com stateless design"]
```

---

#### 3.2. 💻 Requisitos do Desenvolvedor

**Foco:** Implementação prática, padrões de código, APIs, variáveis de ambiente

**Perguntas que o Desenvolvedor responde:**
- Que componentes/módulos/classes criar?
- Quais APIs implementar (endpoints REST/GraphQL)?
- Que padrões de código seguir? (DRY, SOLID, etc.)
- Quais variáveis de ambiente são necessárias?
- Como estruturar o código para ser testável?

**Análise a gerar:**

```markdown
## 💻 Requisitos do Desenvolvedor

### Componentes/Módulos a Criar

**Backend:**
1. **AuthService** (`src/services/auth.service.ts`)
   - Responsabilidade: Lógica de autenticação (login, logout, validação de token)
   - Métodos principais:
     - `login(email, password): Promise<{token, user}>`
     - `validateToken(token): Promise<User | null>`
     - `logout(userId): Promise<void>`

2. **UserRepository** (`src/repositories/user.repository.ts`)
   - Responsabilidade: Acesso a dados de usuários
   - Métodos principais:
     - `findByEmail(email): Promise<User | null>`
     - `create(userData): Promise<User>`
     - `updateLastLogin(userId): Promise<void>`

[...continuar para todos os módulos backend]

**Frontend:**
1. **LoginForm** (`components/auth/LoginForm.tsx`)
   - Responsabilidade: Formulário de login com validação
   - Props: `onSuccess, onError`
   - State: `email, password, loading, errors`

2. **AuthContext** (`contexts/AuthContext.tsx`)
   - Responsabilidade: Gerenciar estado global de autenticação
   - Funções exportadas: `useAuth(), login(), logout(), isAuthenticated()`

[...continuar para todos os componentes frontend]

### APIs a Implementar

**REST Endpoints:**

1. **POST /api/auth/login**
   - Descrição: Autenticar usuário com email e senha
   - Request body:
     ```json
     {
       "email": "string",
       "password": "string"
     }
     ```
   - Response (200):
     ```json
     {
       "success": true,
       "token": "jwt-token",
       "user": {
         "id": "uuid",
         "email": "string",
         "name": "string"
       }
     }
     ```
   - Response (401):
     ```json
     {
       "success": false,
       "error": "Invalid credentials"
     }
     ```

2. **POST /api/auth/logout**
   [Formato similar]

[...continuar para todas as APIs]

### Padrões de Código (DRY, SOLID, etc.)

**DRY (Don't Repeat Yourself):**
- Extrair validação de email para helper: `utils/validators.ts`
- Criar hook customizado `useFormValidation()` para reutilizar lógica de formulários

**SOLID:**
- **Single Responsibility**: Cada serviço tem uma responsabilidade única
- **Dependency Inversion**: Usar interfaces para repositories

**Padrões específicos:**
- Usar DTOs para transferência de dados entre camadas
- Implementar error handling centralizado
- Usar constants para mensagens de erro

### Variáveis de Ambiente

**Arquivo `.env.example`:**
```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# JWT
JWT_SECRET=your-secret-key-minimum-32-characters
JWT_EXPIRATION=7d

# External APIs
[Nome da API]_API_KEY=your-api-key
[Nome da API]_API_URL=https://api.example.com

# Environment
NODE_ENV=development
PORT=3000
```

**Documentar no README:**
- Como obter cada chave de API
- Valores padrão para desenvolvimento
- Valores de produção (onde configurar)
```

---

#### 3.3. 🎨 Especificações de Design/UX

**Foco:** Interface do usuário, acessibilidade, responsividade, experiência

**Perguntas que o Designer responde:**
- Como a UI deve se parecer?
- Quais componentes UI reutilizáveis criar?
- Como garantir acessibilidade (WCAG)?
- Como garantir responsividade (mobile, tablet, desktop)?
- Qual a jornada do usuário?

**Análise a gerar:**

```markdown
## 🎨 Especificações de Design/UX

### Wireframes/Mockups

[Se houver, descrever ou referenciar. Caso contrário, descrever textualmente]

**Tela de Login:**
- Layout centralizado verticalmente
- Card com sombra sutil
- Campos: Email (input), Senha (input type=password)
- Botão primário: "Entrar"
- Link secundário: "Esqueci minha senha"
- Logo da aplicação no topo

### Componentes UI Reutilizáveis

**1. Button** (`components/ui/Button.tsx`)
- Variantes: primary, secondary, danger, ghost
- Tamanhos: small, medium, large
- Estados: normal, hover, focus, disabled, loading

**2. Input** (`components/ui/Input.tsx`)
- Tipos: text, email, password, number
- Estados: normal, error, disabled
- Features: label, helper text, error message, icon

**3. Card** (`components/ui/Card.tsx`)
- Variantes: elevated, outlined, flat
- Slots: header, body, footer

[...continuar para todos os componentes UI]

### Acessibilidade (WCAG 2.1 Level AA)

**Requisitos obrigatórios:**
- ✅ Todos os inputs têm `<label>` associados
- ✅ Formulários têm `aria-label` ou `aria-labelledby`
- ✅ Botões têm texto descritivo (não apenas ícones)
- ✅ Contraste de cores mínimo 4.5:1 para texto normal
- ✅ Contraste de cores mínimo 3:1 para texto grande
- ✅ Navegação completa por teclado (Tab, Enter, Escape)
- ✅ Focus indicators visíveis
- ✅ Mensagens de erro anunciadas por screen readers (`role="alert"`)

**Implementação:**
```tsx
// Exemplo de input acessível
<div>
  <label htmlFor="email" className="sr-only">Email</label>
  <input
    id="email"
    type="email"
    placeholder="Digite seu email"
    aria-required="true"
    aria-invalid={errors.email ? "true" : "false"}
    aria-describedby={errors.email ? "email-error" : undefined}
  />
  {errors.email && (
    <p id="email-error" role="alert" className="text-red-600">
      {errors.email}
    </p>
  )}
</div>
```

### Responsividade

**Breakpoints:**
- Mobile: 0-640px
- Tablet: 641px-1024px
- Desktop: 1025px+

**Adaptações por device:**

**Mobile:**
- Layout em coluna única
- Botões full-width
- Navegação em hamburger menu
- Font-size base: 16px (evitar zoom no iOS)

**Tablet:**
- Layout em 2 colunas onde apropriado
- Sidebar colapsável
- Font-size base: 16px

**Desktop:**
- Layout em grid (até 3-4 colunas)
- Sidebar fixa
- Font-size base: 16px
- Max-width do conteúdo: 1280px

**Implementação (Tailwind CSS):**
```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  {/* Cards responsivos */}
</div>
```

### Jornada do Usuário (User Flow)

**Fluxo de Login:**
1. Usuário acessa `/login`
2. Vê formulário de login
3. Preenche email e senha
4. Clica "Entrar"
5. **Se sucesso**: Redirecionado para `/dashboard`
6. **Se erro**: Vê mensagem de erro inline, foco retorna ao primeiro campo com erro

**Estados de carregamento:**
- Botão "Entrar" mostra spinner durante request
- Botão fica disabled durante loading
- Cursor muda para `wait`

**Estados de erro:**
- Mensagens de erro aparecem abaixo dos campos
- Cor vermelha (#DC2626)
- Ícone de alerta ao lado da mensagem
- Screen reader anuncia erro
```

---

#### 3.4. ✅ Requisitos de QA (Quality Assurance)

**Foco:** Estratégia de testes, cobertura, casos extremos, performance

**Perguntas que o QA responde:**
- Que casos de teste são necessários? (unitários, integração, E2E)
- Qual cobertura de testes atingir?
- Quais edge cases testar?
- Como testar performance?
- Que cenários de erro cobrir?

**Análise a gerar:**

```markdown
## ✅ Requisitos de QA (Quality Assurance)

### Estratégia de Testes

**Pirâmide de testes:**
```
        /\
       /E2E\        ← 10-15 testes (fluxos principais)
      /______\
     /  INT   \     ← 20-30 testes (integração de módulos)
    /__________\
   /   UNIT     \   ← 50-70 testes (lógica de negócio)
  /______________\
```

**Frameworks:**
- **Unitários**: [Jest / Vitest / Mocha] (detectado do projeto)
- **Integração**: [Jest com supertest / etc.]
- **E2E**: Playwright

### Casos de Teste (Unitários)

**AuthService:**
1. `login()`
   - ✅ Deve retornar token JWT válido com credenciais corretas
   - ✅ Deve retornar erro com credenciais inválidas
   - ✅ Deve retornar erro se usuário não existe
   - ✅ Deve retornar erro se senha incorreta
   - ✅ Deve atualizar lastLoginAt do usuário
   - ✅ Deve hash a senha antes de comparar

2. `validateToken()`
   - ✅ Deve validar token JWT correto
   - ✅ Deve rejeitar token expirado
   - ✅ Deve rejeitar token malformado
   - ✅ Deve rejeitar token com assinatura inválida

[...continuar para todos os serviços/componentes]

**Exemplo de teste unitário:**
```typescript
describe('AuthService', () => {
  describe('login', () => {
    it('should return JWT token with valid credentials', async () => {
      const mockUser = { id: '1', email: 'test@example.com', passwordHash: 'hashed' }
      userRepository.findByEmail = jest.fn().mockResolvedValue(mockUser)
      bcrypt.compare = jest.fn().mockResolvedValue(true)

      const result = await authService.login('test@example.com', 'password123')

      expect(result.success).toBe(true)
      expect(result.token).toBeDefined()
      expect(jwt.verify(result.token, SECRET)).toBeTruthy()
    })

    it('should return error with invalid credentials', async () => {
      userRepository.findByEmail = jest.fn().mockResolvedValue(null)

      const result = await authService.login('invalid@example.com', 'wrong')

      expect(result.success).toBe(false)
      expect(result.error).toBe('Invalid credentials')
    })
  })
})
```

### Casos de Teste (Integração)

**API /api/auth/login:**
1. ✅ POST com credenciais válidas retorna 200 e token
2. ✅ POST com credenciais inválidas retorna 401
3. ✅ POST sem email retorna 400
4. ✅ POST sem senha retorna 400
5. ✅ POST com email malformado retorna 400
6. ✅ POST com Content-Type errado retorna 415

[...continuar para todas as APIs]

### Casos de Teste (E2E com Playwright)

**Fluxo de Autenticação:**

1. **E2E: Usuário faz login com credenciais válidas**
   - Navegar para `/login`
   - Preencher email: `testuser@example.com`
   - Preencher senha: `ValidPassword123!`
   - Clicar botão "Entrar"
   - **Verificar**: Redireciona para `/dashboard`
   - **Verificar**: Token salvo no localStorage
   - **Verificar**: Header mostra nome do usuário

2. **E2E: Usuário tenta login com credenciais inválidas**
   - Navegar para `/login`
   - Preencher email: `testuser@example.com`
   - Preencher senha: `WrongPassword`
   - Clicar botão "Entrar"
   - **Verificar**: Permanece em `/login`
   - **Verificar**: Mensagem de erro aparece: "Credenciais inválidas"
   - **Verificar**: Campo de senha é limpo
   - **Verificar**: Foco retorna ao campo de email

3. **E2E: Validação de email inválido (client-side)**
   - Navegar para `/login`
   - Preencher email: `invalid-email`
   - Preencher senha: `password123`
   - Clicar botão "Entrar"
   - **Verificar**: Mensagem de erro: "Email inválido"
   - **Verificar**: Request não é enviado ao servidor

4. **E2E: Tratamento de erro de servidor (500)**
   - [Mock do servidor para retornar 500]
   - Navegar para `/login`
   - Preencher credenciais válidas
   - Clicar botão "Entrar"
   - **Verificar**: Mensagem de erro: "Erro no servidor. Tente novamente."
   - **Verificar**: Botão volta ao estado normal

5. **E2E: Fluxo completo (criar conta → login → acessar dashboard)**
   - Navegar para `/register`
   - Preencher formulário de registro
   - Submeter e criar conta
   - **Verificar**: Redirecionado para `/login`
   - Fazer login com credenciais recém-criadas
   - **Verificar**: Redirecionado para `/dashboard`
   - **Verificar**: Dashboard mostra dados do usuário

[...continuar para todos os fluxos principais]

**Exemplo de teste E2E:**
```typescript
// tests/e2e/auth.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Authentication', () => {
  test('should allow user to login with valid credentials', async ({ page }) => {
    await page.goto('/login')

    await page.fill('input[name="email"]', 'testuser@example.com')
    await page.fill('input[name="password"]', 'ValidPassword123!')
    await page.click('button[type="submit"]')

    await expect(page).toHaveURL('/dashboard')

    const token = await page.evaluate(() => localStorage.getItem('authToken'))
    expect(token).toBeTruthy()

    await expect(page.locator('[data-testid="user-name"]')).toContainText('Test User')
  })
})
```

### Cobertura de Testes

**Metas:**
- **Unitários**: >90% de cobertura de código
- **Integração**: 100% das APIs testadas
- **E2E**: 100% dos fluxos principais (happy paths + principais error paths)

**Ferramentas:**
- Coverage: `jest --coverage` ou `vitest --coverage`
- Reports: HTML coverage report em `coverage/index.html`

### Edge Cases e Cenários de Erro

**Lista de edge cases a testar:**
1. ✅ Email com caracteres especiais válidos (ex: `test+tag@example.com`)
2. ✅ Senha com todos os tipos de caracteres especiais permitidos
3. ✅ Email com domínio internacional (IDN)
4. ✅ Múltiplas tentativas de login falhadas (rate limiting)
5. ✅ Login simultâneo de múltiplos dispositivos
6. ✅ Token expira durante navegação (refresh automático)
7. ✅ Conexão de rede perdida durante login
8. ✅ Request timeout (servidor lento)
9. ✅ Browser sem suporte a localStorage
10. ✅ JavaScript desabilitado (graceful degradation)

**Lista de cenários de erro a testar:**
1. ✅ Servidor retorna 500 (Internal Server Error)
2. ✅ Servidor retorna 503 (Service Unavailable)
3. ✅ Request timeout (>30s)
4. ✅ Network error (sem conexão)
5. ✅ CORS error (configuração incorreta)
6. ✅ JSON malformado na resposta
7. ✅ Token expirado no meio da sessão
8. ✅ Banco de dados indisponível

### Testes de Performance

**Requisitos:**
- Tempo de resposta API `/api/auth/login`: <200ms (95th percentile)
- Tempo de carregamento inicial página `/login`: <1s
- Time to Interactive (TTI): <2s

**Ferramentas:**
- Lighthouse CI para métricas de performance
- Artillery ou k6 para load testing de API

**Cenários de load testing:**
1. 100 requests/segundo durante 1 minuto
2. 1000 usuários simultâneos
3. Pico de 500 requests/segundo por 10 segundos
```

---

#### 3.5. 📊 Análise do Gerente de Projeto

**Foco:** Priorização, riscos, estimativas, critérios de aceitação

**Perguntas que o PM responde:**
- Qual a prioridade desta feature? (High/Medium/Low)
- Quais são os riscos potenciais?
- Qual a estimativa de complexidade e tempo?
- Quais são os critérios de aceitação?
- Há dependências críticas?

**Análise a gerar:**

```markdown
## 📊 Análise do Gerente de Projeto

### Prioridade da Feature

**Prioridade:** [High / Medium / Low]

**Justificativa:**
[Explicar por que esta prioridade]

Exemplo:
- **High**: Bloqueador para outras features, afeta funcionalidade core
- **Medium**: Melhoria importante mas não urgente
- **Low**: Nice-to-have, pode ser adiado

### Riscos Potenciais

**Risco 1: [Nome do risco]**
- **Probabilidade:** [Alta / Média / Baixa]
- **Impacto:** [Alto / Médio / Baixo]
- **Descrição:** [Descrição do risco]
- **Mitigação:** [Como reduzir ou eliminar o risco]

**Exemplo:**
- **Risco:** Integração com API externa pode falhar
- **Probabilidade:** Média
- **Impacto:** Alto
- **Descrição:** A API de pagamento tem histórico de instabilidade (uptime 99.5%)
- **Mitigação:**
  - Implementar retry logic com backoff exponencial
  - Circuit breaker para evitar sobrecarga
  - Modo fallback (processar pagamento depois)
  - Monitoramento e alertas

[...listar 2-5 riscos principais]

### Estimativa de Complexidade e Tempo

**Complexidade:** [Baixa / Média / Alta]

**Critérios de complexidade:**
- **Baixa**: 10-30 tasks, sem integrações externas, stack conhecida
- **Média**: 31-70 tasks, 1-2 integrações externas, alguma incerteza técnica
- **Alta**: 71+ tasks, múltiplas integrações, stack nova/experimental

**Esta feature: [XX] tasks → Complexidade [X]**

**Estimativa de tempo:**
- **Desenvolvimento**: [X-Y] dias
- **Testes**: [X-Y] dias
- **Code Review + Ajustes**: [X-Y] dias
- **Total**: [X-Y] dias (assumindo 1 desenvolvedor full-time)

**Notas:**
- Estimativas baseadas em tasks granulares geradas
- Podem variar baseado em experiência do desenvolvedor com stack
- Incluem tempo para testes unitários, integração e E2E

### Critérios de Aceitação

**A feature será considerada completa quando:**

1. ✅ **Funcional:**
   - [User story 1] implementada e funcionando
   - [User story 2] implementada e funcionando
   - [User story 3] implementada e funcionando

2. ✅ **Qualidade:**
   - Cobertura de testes unitários >90%
   - Todos os testes E2E passando
   - Sem erros críticos ou bloqueadores
   - Performance dentro dos requisitos (<200ms, etc.)

3. ✅ **Não-Funcional:**
   - Código segue padrões de estilo (ESLint/Prettier)
   - Acessibilidade WCAG 2.1 Level AA
   - Responsivo em mobile, tablet, desktop
   - Documentação atualizada (README, JSDoc)

4. ✅ **Aprovação:**
   - Code review aprovado por [N] reviewers
   - QA testou e aprovou
   - [Se aplicável] Product Owner aprovou UI/UX

### Dependências Críticas

**Dependências internas:**
[Listar features ou módulos do projeto que são dependências]

**Dependências externas:**
[Listar serviços, APIs, infraestrutura externa necessária]

**Exemplo:**
- ⚠️ **Bloqueador**: Requer FEAT-001 (Sistema de Usuários) completado
- ℹ️ **Nice-to-have**: FEAT-005 (Notificações) para enviar email de confirmação

### Marcos (Milestones)

**Marco 1**: Backend APIs funcionando (Tasks 001-030)
**Marco 2**: Frontend UI implementado (Tasks 031-060)
**Marco 3**: Testes completos (Tasks 061-085)
**Marco 4**: Code review e deploy (Tasks 086-090)
```

---

#### 3.6. 💼 Requisitos de Negócio (Business Analyst)

**Foco:** Valor de negócio, KPIs, impacto no usuário, ROI

**Perguntas que o BA responde:**
- Qual o valor de negócio desta feature?
- Que KPIs medir para avaliar sucesso?
- Qual o impacto nos usuários?
- Qual o ROI esperado?
- Como esta feature alinha com objetivos de negócio?

**Análise a gerar:**

```markdown
## 💼 Requisitos de Negócio (Business Analyst)

### Valor de Negócio

**Problema que resolve:**
[Descrição do problema de negócio que a feature resolve]

**Exemplo:**
"Atualmente, usuários abandonam o carrinho devido a processo de checkout complexo e demorado (taxa de abandono: 68%). Esta feature simplifica o checkout para 3 passos, reduzindo fricção e aumentando conversão."

**Benefícios esperados:**
1. [Benefício 1]: [Descrição e impacto]
2. [Benefício 2]: [Descrição e impacto]
3. [Benefício 3]: [Descrição e impacto]

**Exemplo:**
1. **Aumento de conversão**: Reduzir abandono de carrinho de 68% para 45% (estimativa baseada em benchmarks)
2. **Melhor experiência**: Reduzir tempo de checkout de 5min para 2min
3. **Vantagem competitiva**: Parear com padrão de mercado (concorrentes já têm checkout simplificado)

### KPIs (Key Performance Indicators)

**KPIs principais a medir:**

1. **[Nome do KPI]**
   - **Métrica**: [O que medir]
   - **Baseline atual**: [Valor antes da feature]
   - **Meta pós-feature**: [Valor esperado após feature]
   - **Prazo**: [Quando medir - ex: 30 dias após deploy]

**Exemplo:**

1. **Taxa de Conversão no Checkout**
   - **Métrica**: % de usuários que completam compra após iniciar checkout
   - **Baseline**: 32%
   - **Meta**: 55%
   - **Prazo**: 60 dias após deploy

2. **Tempo Médio de Checkout**
   - **Métrica**: Tempo médio do início ao fim do checkout
   - **Baseline**: 5 minutos
   - **Meta**: 2 minutos
   - **Prazo**: 30 dias após deploy

3. **Taxa de Abandono de Carrinho**
   - **Métrica**: % de usuários que abandonam carrinho
   - **Baseline**: 68%
   - **Meta**: 45%
   - **Prazo**: 60 dias após deploy

[...listar 3-5 KPIs principais]

**Ferramentas de tracking:**
- Google Analytics para funil de conversão
- Mixpanel/Amplitude para eventos customizados
- Hotjar/FullStory para session recordings e heatmaps

### Impacto no Usuário

**Personas afetadas:**
1. **[Nome da Persona]** (ex: "Maria, compradora frequente")
   - **Como afeta**: [Descrição do impacto]
   - **Sentimento esperado**: [Positivo / Neutro / Negativo]

**Exemplo:**
1. **Maria, 35, compradora frequente**
   - **Como afeta**: Processo de checkout mais rápido, menos cliques
   - **Sentimento**: Muito positivo - menos fricção, mais satisfação

2. **João, 22, comprador eventual**
   - **Como afeta**: Processo mais intuitivo, menos chances de erro
   - **Sentimento**: Positivo - reduz ansiedade no pagamento

**Jornada do usuário - Antes vs Depois:**

**ANTES:**
1. Usuário adiciona item ao carrinho
2. Clica "Checkout"
3. Preenche 3 páginas de formulários (dados pessoais, endereço, pagamento)
4. Revisa pedido
5. Confirma
- **Tempo**: ~5 minutos
- **Fricção**: Alta (muitos campos, múltiplas páginas)

**DEPOIS:**
1. Usuário adiciona item ao carrinho
2. Clica "Checkout"
3. Preenche 1 página única (dados já preenchidos se logado)
4. Confirma
- **Tempo**: ~2 minutos
- **Fricção**: Baixa (poucos campos, 1 página)

### ROI (Return on Investment)

**Investimento:**
- Custo de desenvolvimento: [X] dias × [Y] $/dia = $[Z]
- Custo de design/UX: $[A]
- Custo de QA/testes: $[B]
- **Total**: $[Z + A + B]

**Retorno esperado:**

**Cálculo:**
- Baseline: 1000 checkouts/mês × 32% conversão = 320 vendas/mês
- Pós-feature: 1000 checkouts/mês × 55% conversão = 550 vendas/mês
- **Ganho**: +230 vendas/mês
- Ticket médio: $50
- **Receita adicional/mês**: 230 × $50 = $11,500
- **Receita adicional/ano**: $138,000

**Break-even:**
- Investimento: $[Z + A + B]
- Receita adicional/mês: $11,500
- **Meses para break-even**: [Investimento] / $11,500 = [X] meses

**ROI em 12 meses:**
- ROI = (Receita adicional - Investimento) / Investimento × 100
- ROI = ($138,000 - $[Investimento]) / $[Investimento] × 100 = [X]%

### Alinhamento com Objetivos de Negócio

**Objetivo estratégico da empresa:**
[Ex: "Aumentar receita em 30% no próximo ano"]

**Como esta feature contribui:**
[Ex: "Esta feature contribui diretamente ao aumentar conversão no checkout, impactando 40% da receita total da empresa"]

**Prioridade estratégica:**
[Alta / Média / Baixa] baseado em alinhamento com roadmap

**Alternativas consideradas:**
1. **[Alternativa 1]**: [Por que foi descartada]
2. **[Alternativa 2]**: [Por que foi descartada]

**Decisão:**
Implementar esta feature é a melhor opção porque [justificativa].
```

---

**Informar usuário:**
```
✅ Análise multi-persona completa!
   - 🏗️ Arquiteto: Estrutura e dependências definidas
   - 💻 Desenvolvedor: [N] componentes e [M] APIs mapeados
   - 🎨 Designer: UI/UX especificado com acessibilidade
   - ✅ QA: [X] testes unitários + [Y] E2E planejados
   - 📊 PM: Prioridade [X], [N] riscos identificados
   - 💼 BA: KPIs definidos, ROI calculado

Agora vou gerar os 5 arquivos de documentação... (Fase 4)
```

---

### FASE 4: Geração de Documentação

Objetivo: Gerar os 5 arquivos de documentação usando as análises das Fases 1-3 e os templates disponíveis.

**Criar diretório de saída:**
```bash
mkdir -p "docs/context-log-running/[feature-name-slug]"
```

Onde `[feature-name-slug]` é o nome da feature em lowercase com hífens (ex: `sistema-autenticacao-jwt`)

---

#### 4.1. Gerar spec.md

**Conteúdo completo do spec.md:**

```markdown
# FEAT-XXX: [Nome da Feature]

📂 **Documentação Relacionada:**
- [Plano Técnico](plan.md) - Arquitetura e decisões técnicas
- [Lista de Tasks](tasks.md) - Tarefas detalhadas ([N] tasks)
- [Pesquisa](research.md) - Documentação e referências

---

## Visão Geral

[Descrição detalhada da feature coletada em Q2]

**Categoria:** [Categoria da Q7]
**Prioridade:** [Alta/Média/Baixa da análise do PM]
**Status:** [Pending/Blocked]

[Se bloqueada]
⚠️ **BLOQUEADOR:** [Descrição do bloqueador da Q6]

---

## User Stories

[User stories coletadas em Q3, formatadas]

1. Como [tipo de usuário], quero [ação], para [benefício]
2. Como [tipo de usuário], quero [ação], para [benefício]
...

---

[INSERIR ANÁLISE COMPLETA DO ARQUITETO (seção 3.1)]

[INSERIR ANÁLISE COMPLETA DO DESENVOLVEDOR (seção 3.2)]

[INSERIR ANÁLISE COMPLETA DO DESIGNER/UX (seção 3.3)]

[INSERIR ANÁLISE COMPLETA DO QA (seção 3.4)]

[INSERIR ANÁLISE COMPLETA DO PM (seção 3.5)]

[INSERIR ANÁLISE COMPLETA DO BA (seção 3.6)]

---

## Critérios de Aceitação

[Critérios de aceitação da análise do PM, formatados como checklist]

- [ ] [Critério 1]
- [ ] [Critério 2]
- [ ] [Critério 3]
...

---

## Requisitos de Performance/Segurança

[Requisitos coletados em Q5]

**Segurança:**
- [Requisito de segurança 1]
- [Requisito de segurança 2]

**Performance:**
- [Requisito de performance 1]
- [Requisito de performance 2]

---

## Dependências

[Dependências identificadas em Q6]

**Dependências internas:**
- [Dependência 1]

**Dependências externas:**
- [Dependência 2]

[Se houver bloqueadores]
⚠️ **AÇÃO NECESSÁRIA:** Implementar/configurar [bloqueador] antes de começar esta feature.

---

**Gerado automaticamente por:** sprint-context-generator skill
**Data:** [YYYY-MM-DD]
```

**Ação:** Usar Write tool para criar `docs/context-log-running/[feature-name-slug]/spec.md`

---

#### 4.2. Gerar plan.md

**Conteúdo completo do plan.md:**

```markdown
# Plano Técnico: FEAT-XXX - [Nome da Feature]

📂 **Documentação Relacionada:**
- [Especificação](spec.md) - Requisitos e análise de personas
- [Lista de Tasks](tasks.md) - Tarefas detalhadas ([N] tasks)
- [Pesquisa](research.md) - Documentação e referências

---

## Arquitetura Proposta

[Descrição da arquitetura da análise do Arquiteto]

[Diagrama ASCII ou descrição textual do fluxo de dados]

```
[Diagrama de arquitetura]
```

**Princípios arquiteturais:**
- [Princípio 1]
- [Princípio 2]

---

## Stack Tecnológica

**Linguagem:** [Detectada na Fase 1]
**Framework:** [Detectado na Fase 1]

**Frontend:**
- [Tech1]: [Versão]
- [Tech2]: [Versão]

**Backend:**
- [Tech1]: [Versão]
- [Tech2]: [Versão]

**Database:**
- [DB]: [Versão]

**Testing:**
- E2E: Playwright
- Unitários: [Framework detectado]
- Coverage: Jest/Vitest

**DevOps/Tooling:**
- Linting: ESLint + Prettier
- Git Hooks: Husky
- CI/CD: [Se aplicável]

---

## Estrutura de Diretórios

[Estrutura proposta pelo Arquiteto]

```
[Árvore de diretórios detalhada]
```

---

## Componentes/Módulos

[Lista de componentes da análise do Desenvolvedor]

### Backend

#### 1. [Nome do Módulo]
- **Responsabilidade**: [Descrição]
- **Dependências**: [Lista]
- **Arquivos**:
  - `[path/to/file1.ts]`
  - `[path/to/file2.ts]`

[...continuar para todos os módulos backend]

### Frontend

#### 1. [Nome do Componente]
- **Responsabilidade**: [Descrição]
- **Props**: [Lista de props]
- **State**: [Lista de state]
- **Arquivos**:
  - `[path/to/Component.tsx]`

[...continuar para todos os componentes frontend]

---

## APIs e Contratos

[APIs da análise do Desenvolvedor]

### REST Endpoints

#### 1. [METHOD] /api/[endpoint]
**Descrição:** [Descrição]

**Request:**
```json
{
  [request body]
}
```

**Response (200):**
```json
{
  [response body success]
}
```

**Response (4XX/5XX):**
```json
{
  [response body error]
}
```

[...continuar para todas as APIs]

---

## Variáveis de Ambiente

[Variáveis da análise do Desenvolvedor]

**Arquivo `.env.example`:**
```env
[Conteúdo do .env.example]
```

**Documentação:**
- `[VAR_NAME]`: [Descrição, onde obter, valor padrão]

---

## Setup e Configurações

### ESLint/Prettier

[Configurações da seção 2.4 do research.md]

**`.eslintrc.js`:**
```javascript
[Configuração]
```

**`.prettierrc`:**
```json
[Configuração]
```

### Husky Hooks

[Configurações da seção 2.5 do research.md]

**`.husky/pre-commit`:**
```bash
[Script]
```

**`.husky/pre-push`:**
```bash
[Script]
```

**`package.json` (lint-staged):**
```json
{
  "lint-staged": {
    [Configuração]
  }
}
```

---

## Decisões Técnicas

[Decisões importantes que foram tomadas]

### 1. [Título da Decisão]
- **Decisão**: [O que foi decidido]
- **Razão**: [Por que esta escolha]
- **Alternativas consideradas**: [Outras opções]
- **Trade-offs**: [Vantagens e desvantagens]

[...continuar para decisões principais]

---

## Riscos Técnicos

[Riscos da análise do PM]

### 1. [Nome do Risco]
- **Probabilidade**: [Alta/Média/Baixa]
- **Impacto**: [Alto/Médio/Baixo]
- **Descrição**: [Descrição do risco]
- **Mitigação**: [Estratégia de mitigação]

[...continuar para todos os riscos]

---

**Gerado automaticamente por:** sprint-context-generator skill
**Data:** [YYYY-MM-DD]
```

**Ação:** Usar Write tool para criar `docs/context-log-running/[feature-name-slug]/plan.md`

---

#### 4.3. Gerar tasks.md

**IMPORTANTE:** Tasks devem ser:
- **Específicas**: Mencionar arquivo/componente exato
- **Atômicas**: Completáveis em 15-30 minutos
- **Testáveis**: Critério de conclusão claro
- **Sequenciais**: Numeradas (TASK-001, TASK-002, etc.)

**Estrutura de tasks.md:**

```markdown
# Lista de Tarefas: FEAT-XXX - [Nome da Feature]

📂 **Documentação Relacionada:**
- [Especificação](spec.md) - Requisitos e análise de personas
- [Plano Técnico](plan.md) - Arquitetura e decisões técnicas
- [Pesquisa](research.md) - Documentação e referências

**Total: [N] tasks | Complexidade: [Baixa/Média/Alta]**

---

## Legenda

- 🏗️ Arquitetura/Setup
- 💻 Desenvolvimento Backend
- 🎨 Desenvolvimento Frontend/UI
- ✅ Testes
- 📝 Documentação

---

## 1. Setup e Configuração ([N] tasks)

- [ ] 🏗️ **TASK-001:** Instalar dependências [lista de packages] via `npm install`
- [ ] 🏗️ **TASK-002:** Criar arquivo `.eslintrc.js` com configuração baseada em research.md seção 2.4
- [ ] 🏗️ **TASK-003:** Criar arquivo `.prettierrc` com configuração baseada em research.md seção 2.4
- [ ] 🏗️ **TASK-004:** Configurar Husky com `npx husky init`
- [ ] 🏗️ **TASK-005:** Criar hook `.husky/pre-commit` com lint-staged baseado em research.md seção 2.5
- [ ] 🏗️ **TASK-006:** Criar hook `.husky/pre-push` para rodar testes
- [ ] 🏗️ **TASK-007:** Criar estrutura de diretórios conforme plan.md seção "Estrutura de Diretórios"
- [ ] 🏗️ **TASK-008:** Criar arquivo `.env.example` com variáveis de plan.md
- [ ] 🏗️ **TASK-009:** Atualizar `.gitignore` para incluir `.env` e `node_modules`
- [ ] 🏗️ **TASK-010:** Configurar Playwright com `npm init playwright@latest`

---

## 2. Backend ([N] tasks)

[Para cada módulo/serviço/API da análise do Desenvolvedor, criar tasks]

### 2.1. Modelos de Dados

- [ ] 💻 **TASK-011:** Criar schema de banco de dados [Entity] em `src/models/[entity].model.ts`
- [ ] 💻 **TASK-012:** Adicionar validação com [Zod/Joi] no schema [Entity]
- [ ] 💻 **TASK-013:** Criar migration `create_[table]_table` usando [Prisma/TypeORM]
- [ ] 💻 **TASK-014:** Rodar migration no banco de desenvolvimento

### 2.2. Repositories

- [ ] 💻 **TASK-015:** Criar interface `I[Entity]Repository` em `src/repositories/interfaces/`
- [ ] 💻 **TASK-016:** Implementar `[Entity]Repository` em `src/repositories/[entity].repository.ts`
- [ ] 💻 **TASK-017:** Implementar método `findByEmail(email)` retornando `Promise<User | null>`
- [ ] 💻 **TASK-018:** Implementar método `create(userData)` retornando `Promise<User>`
- [ ] 💻 **TASK-019:** Implementar método `updateLastLogin(userId)` retornando `Promise<void>`

### 2.3. Services

- [ ] 💻 **TASK-020:** Criar `[Service]Service` em `src/services/[service].service.ts`
- [ ] 💻 **TASK-021:** Implementar método `login(email, password)` retornando `Promise<{token, user}>`
- [ ] 💻 **TASK-022:** Adicionar hash de senha com bcrypt (custo 12) no método login
- [ ] 💻 **TASK-023:** Implementar geração de JWT com secret de `.env` e expiração 7d
- [ ] 💻 **TASK-024:** Implementar método `validateToken(token)` retornando `Promise<User | null>`
- [ ] 💻 **TASK-025:** Adicionar tratamento de erro para credenciais inválidas

### 2.4. Controllers/Routes

- [ ] 💻 **TASK-026:** Criar `[controller].controller.ts` em `src/controllers/`
- [ ] 💻 **TASK-027:** Implementar endpoint `POST /api/auth/login` chamando AuthService.login()
- [ ] 💻 **TASK-028:** Adicionar validação de request body (email e password obrigatórios)
- [ ] 💻 **TASK-029:** Adicionar middleware de error handling para retornar JSON padronizado
- [ ] 💻 **TASK-030:** Registrar rotas no app principal

### 2.5. Middlewares

- [ ] 💻 **TASK-031:** Criar middleware `authenticate` em `src/middlewares/auth.middleware.ts`
- [ ] 💻 **TASK-032:** Implementar validação de JWT no header `Authorization: Bearer <token>`
- [ ] 💻 **TASK-033:** Adicionar middleware em rotas protegidas

[...continuar até cobrir TODOS os componentes backend]

---

## 3. Frontend/UI ([N] tasks)

### 3.1. Componentes UI Base

- [ ] 🎨 **TASK-034:** Criar componente `Button` em `components/ui/Button.tsx` com variantes (primary, secondary, danger)
- [ ] 🎨 **TASK-035:** Adicionar estados (normal, hover, focus, disabled, loading) ao Button
- [ ] 🎨 **TASK-036:** Criar componente `Input` em `components/ui/Input.tsx` com tipos (text, email, password)
- [ ] 🎨 **TASK-037:** Adicionar validação visual de erro no Input (borda vermelha, mensagem)
- [ ] 🎨 **TASK-038:** Criar componente `Card` em `components/ui/Card.tsx` com slots (header, body, footer)

### 3.2. Componentes de Feature

- [ ] 🎨 **TASK-039:** Criar componente `LoginForm` em `components/auth/LoginForm.tsx`
- [ ] 🎨 **TASK-040:** Adicionar campos email e password usando componente Input
- [ ] 🎨 **TASK-041:** Implementar validação client-side com [React Hook Form/Formik]
- [ ] 🎨 **TASK-042:** Adicionar estado de loading durante submit (botão disabled + spinner)
- [ ] 🎨 **TASK-043:** Exibir mensagens de erro inline abaixo dos campos
- [ ] 🎨 **TASK-044:** Implementar submit que chama API `/api/auth/login`
- [ ] 🎨 **TASK-045:** Armazenar token no localStorage após login bem-sucedido
- [ ] 🎨 **TASK-046:** Redirecionar para `/dashboard` após login

### 3.3. Context/State Management

- [ ] 🎨 **TASK-047:** Criar `AuthContext` em `contexts/AuthContext.tsx`
- [ ] 🎨 **TASK-048:** Implementar `AuthProvider` com state (user, token, isAuthenticated)
- [ ] 🎨 **TASK-049:** Criar hook `useAuth()` para consumir AuthContext
- [ ] 🎨 **TASK-050:** Implementar função `login(email, password)` no context
- [ ] 🎨 **TASK-051:** Implementar função `logout()` limpando token e redirecionando para /login

### 3.4. Páginas

- [ ] 🎨 **TASK-052:** Criar página `LoginPage` em `pages/login.tsx` (ou `app/login/page.tsx` se Next.js App Router)
- [ ] 🎨 **TASK-053:** Renderizar LoginForm na LoginPage
- [ ] 🎨 **TASK-054:** Adicionar logo e título na LoginPage
- [ ] 🎨 **TASK-055:** Criar página `DashboardPage` em `pages/dashboard.tsx`

### 3.5. Estilos e Responsividade

- [ ] 🎨 **TASK-056:** Aplicar estilos CSS/Tailwind no Button conforme design specs
- [ ] 🎨 **TASK-057:** Aplicar estilos CSS/Tailwind no Input conforme design specs
- [ ] 🎨 **TASK-058:** Aplicar estilos CSS/Tailwind no LoginForm (centralizado, card, sombra)
- [ ] 🎨 **TASK-059:** Implementar breakpoints responsivos (mobile: col-1, desktop: col-2)
- [ ] 🎨 **TASK-060:** Testar layout em mobile (375px), tablet (768px), desktop (1280px)

### 3.6. Acessibilidade

- [ ] 🎨 **TASK-061:** Adicionar `<label>` para cada input com `htmlFor` correto
- [ ] 🎨 **TASK-062:** Adicionar `aria-label` nos botões com ícones
- [ ] 🎨 **TASK-063:** Garantir navegação por teclado (Tab, Enter, Escape)
- [ ] 🎨 **TASK-064:** Adicionar `role="alert"` nas mensagens de erro
- [ ] 🎨 **TASK-065:** Verificar contraste de cores (mínimo 4.5:1) com ferramenta de acessibilidade
- [ ] 🎨 **TASK-066:** Testar com screen reader (NVDA ou VoiceOver)

[...continuar até cobrir TODOS os componentes frontend]

---

## 4. Testes Unitários ([N] tasks)

[Para cada módulo/componente, criar tasks de testes unitários]

### 4.1. Backend Tests

- [ ] ✅ **TASK-067:** Criar arquivo `auth.service.spec.ts` em `tests/unit/services/`
- [ ] ✅ **TASK-068:** Testar `AuthService.login()` com credenciais válidas retorna token
- [ ] ✅ **TASK-069:** Testar `AuthService.login()` com credenciais inválidas retorna erro
- [ ] ✅ **TASK-070:** Testar `AuthService.login()` com usuário inexistente retorna erro
- [ ] ✅ **TASK-071:** Testar `AuthService.validateToken()` com token válido retorna user
- [ ] ✅ **TASK-072:** Testar `AuthService.validateToken()` com token expirado retorna null
- [ ] ✅ **TASK-073:** Testar `AuthService.validateToken()` com token malformado retorna null
- [ ] ✅ **TASK-074:** Mock do UserRepository para isolar testes
- [ ] ✅ **TASK-075:** Criar arquivo `user.repository.spec.ts` em `tests/unit/repositories/`
- [ ] ✅ **TASK-076:** Testar `UserRepository.findByEmail()` encontra usuário existente
- [ ] ✅ **TASK-077:** Testar `UserRepository.findByEmail()` retorna null para email inexistente
- [ ] ✅ **TASK-078:** Testar `UserRepository.create()` cria usuário e retorna objeto

### 4.2. Frontend Tests

- [ ] ✅ **TASK-079:** Criar arquivo `LoginForm.spec.tsx` em `tests/unit/components/`
- [ ] ✅ **TASK-080:** Testar renderização do LoginForm (campos email e senha presentes)
- [ ] ✅ **TASK-081:** Testar validação client-side de email inválido mostra erro
- [ ] ✅ **TASK-082:** Testar validação client-side de senha vazia mostra erro
- [ ] ✅ **TASK-083:** Testar submit com credenciais válidas chama API corretamente
- [ ] ✅ **TASK-084:** Testar submit com erro de API exibe mensagem de erro
- [ ] ✅ **TASK-085:** Testar botão fica disabled durante loading
- [ ] ✅ **TASK-086:** Criar arquivo `Button.spec.tsx` em `tests/unit/components/ui/`
- [ ] ✅ **TASK-087:** Testar Button renderiza texto corretamente
- [ ] ✅ **TASK-088:** Testar Button com variante 'primary' tem classe CSS correta
- [ ] ✅ **TASK-089:** Testar Button disabled não chama onClick

### 4.3. Cobertura

- [ ] ✅ **TASK-090:** Rodar `npm run test:coverage` e verificar cobertura >90%
- [ ] ✅ **TASK-091:** Identificar módulos com cobertura <90% e adicionar testes faltantes
- [ ] ✅ **TASK-092:** Gerar relatório HTML de cobertura em `coverage/index.html`

---

## 5. Testes E2E ([N] tasks)

[Baseado nos casos de teste E2E da análise do QA]

### 5.1. Setup Playwright

- [ ] ✅ **TASK-093:** Criar `playwright.config.ts` com configuração para 3 browsers (chromium, firefox, webkit)
- [ ] ✅ **TASK-094:** Configurar baseURL para `http://localhost:3000`
- [ ] ✅ **TASK-095:** Criar diretório `tests/e2e/` para testes E2E

### 5.2. Testes de Autenticação

- [ ] ✅ **TASK-096:** Criar arquivo `auth.spec.ts` em `tests/e2e/`
- [ ] ✅ **TASK-097:** E2E: Usuário faz login com credenciais válidas e é redirecionado para /dashboard
- [ ] ✅ **TASK-098:** E2E: Validar que token foi salvo no localStorage após login
- [ ] ✅ **TASK-099:** E2E: Validar que nome do usuário aparece no header após login
- [ ] ✅ **TASK-100:** E2E: Usuário tenta login com credenciais inválidas e vê mensagem de erro
- [ ] ✅ **TASK-101:** E2E: Validar que campo de senha é limpo após erro
- [ ] ✅ **TASK-102:** E2E: Validação client-side de email inválido impede submit
- [ ] ✅ **TASK-103:** E2E: Tratamento de erro de servidor (mock 500) exibe mensagem adequada
- [ ] ✅ **TASK-104:** E2E: Botão "Entrar" mostra spinner durante request

### 5.3. Fluxos Completos

- [ ] ✅ **TASK-105:** E2E: Fluxo completo - Criar conta → Login → Acessar dashboard → Logout
- [ ] ✅ **TASK-106:** E2E: Usuário logado acessa /login e é redirecionado para /dashboard
- [ ] ✅ **TASK-107:** E2E: Usuário não logado acessa /dashboard e é redirecionado para /login

### 5.4. Edge Cases

- [ ] ✅ **TASK-108:** E2E: Email com caracteres especiais (test+tag@example.com) funciona
- [ ] ✅ **TASK-109:** E2E: Múltiplas tentativas de login falhadas ativa rate limiting (se aplicável)
- [ ] ✅ **TASK-110:** E2E: Token expira e usuário é redirecionado para login

### 5.5. Performance

- [ ] ✅ **TASK-111:** Configurar Playwright para medir métricas de performance
- [ ] ✅ **TASK-112:** Validar que página /login carrega em <1s (LCP)
- [ ] ✅ **TASK-113:** Validar que Time to Interactive (TTI) é <2s

---

## 6. Documentação ([N] tasks)

- [ ] 📝 **TASK-114:** Atualizar README.md com seção sobre feature [Nome]
- [ ] 📝 **TASK-115:** Documentar endpoints da API em README.md ou arquivo separado `API.md`
- [ ] 📝 **TASK-116:** Adicionar comentários JSDoc nos métodos principais de [Service]
- [ ] 📝 **TASK-117:** Criar arquivo `.env.example` documentando todas as variáveis
- [ ] 📝 **TASK-118:** Atualizar CHANGELOG.md com entrada para esta feature
- [ ] 📝 **TASK-119:** Criar guia de uso da feature para usuários finais (se aplicável)

---

## Resumo de Tasks

| Categoria | Quantidade |
|-----------|------------|
| 🏗️ Setup  | [N] tasks  |
| 💻 Backend | [N] tasks  |
| 🎨 Frontend | [N] tasks  |
| ✅ Testes  | [N] tasks  |
| 📝 Docs    | [N] tasks  |
| **TOTAL**  | **[N] tasks** |

**Complexidade:** [Baixa/Média/Alta]
**Estimativa:** [X-Y] dias de desenvolvimento

---

**Gerado automaticamente por:** sprint-context-generator skill
**Data:** [YYYY-MM-DD]
```

**VALIDAÇÃO DE QUALIDADE (Fase 5.2):**
Após gerar tasks.md, validar cada task:
1. Tem >40 caracteres? ✅
2. Menciona arquivo/componente específico? ✅
3. Usa verbo de ação específico? ✅
4. É atômica (15-30 min)? ✅

Se alguma task falhar, refinar antes de finalizar.

**Ação:** Usar Write tool para criar `docs/context-log-running/[feature-name-slug]/tasks.md`

---

#### 4.4. Gerar research.md

**research.md já foi gerado na Fase 2.3!**

**Ação:** Usar Write tool para criar `docs/context-log-running/[feature-name-slug]/research.md` com conteúdo da Fase 2.3

---

#### 4.5. Gerar features.xml

**Conteúdo do features.xml:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<features project="[Nome do Projeto]" total="[N]" completed="[X]">

  <category name="[Categoria da Q7]">
    <feature id="FEAT-XXX" status="[pending/blocked]" priority="[high/medium/low]">
      <description>[Descrição curta da feature]</description>
      <steps>
        [Para cada critério de aceitação da análise do PM]
        <step>[Critério 1]</step>
        <step>[Critério 2]</step>
        <step>[Critério 3]</step>
      </steps>
      <notes>Tasks: [N] | Docs: docs/context-log-running/[feature-name-slug]/ | Complexity: [Baixa/Média/Alta]</notes>
    </feature>
  </category>

</features>
```

**Detalhes:**
- `project`: Nome do projeto (detectado ou perguntado)
- `total`: Total de features no projeto (ler do `.claude/features.xml` se existir)
- `completed`: Features completadas (ler do `.claude/features.xml` se existir)
- `id`: FEAT-XXX (gerado na Fase 1)
- `status`:
  - `pending` se não há bloqueadores
  - `blocked` se há dependências não resolvidas (Q6)
- `priority`: high/medium/low (da análise do PM)
- `description`: Descrição curta da feature (Q2, resumida em 1 frase)
- `steps`: Critérios de aceitação (da análise do PM)
- `notes`: Informações adicionais (número de tasks, localização dos docs, complexidade)

**Ação:** Usar Write tool para criar `docs/context-log-running/[feature-name-slug]/features.xml`

**Se `.claude/` existe:**
Também atualizar ou criar `.claude/features.xml` global adicionando esta feature.

---

**Informar usuário:**
```
✅ Documentação completa gerada!

Arquivos criados em docs/context-log-running/[feature-name-slug]/:
   - spec.md      ([N] linhas)
   - plan.md      ([M] linhas)
   - tasks.md     ([X] tasks)
   - research.md  ([Y] linhas)
   - features.xml

Agora vou validar qualidade e compatibilidade... (Fase 5)
```

---

### FASE 5: Validação e Finalização

Objetivo: Validar arquivos gerados, garantir qualidade e compatibilidade, criar branch Git, exibir resumo.

---

#### 5.1. Validar Estrutura de Arquivos

**Verificar que todos os 5 arquivos foram criados:**

```bash
ls -la "docs/context-log-running/[feature-name-slug]/"
```

**Esperado:**
```
spec.md
plan.md
tasks.md
research.md
features.xml
```

**Se algum arquivo faltando:**
- ⚠️ Avisar usuário: "Arquivo [X] não foi gerado corretamente. Tentando novamente..."
- Recriar arquivo faltante

---

#### 5.2. Validar Qualidade de Tasks (CRÍTICO)

**Para cada task em tasks.md:**

Ler arquivo tasks.md e extrair todas as tasks (linhas com `- [ ]`).

**Para cada task, validar:**

1. **Tamanho:** Task tem >40 caracteres?
   - ❌ Se <40 chars: Marcar como suspeita

2. **Especificidade:** Task menciona arquivo ou componente específico?
   - ✅ Bom: "Criar componente `LoginForm.tsx`"
   - ❌ Ruim: "Criar componente de login"

3. **Verbo de ação:** Task usa verbo específico?
   - ✅ Bons verbos: Criar, Implementar, Adicionar, Escrever, Configurar + [objeto específico]
   - ❌ Verbos vagos: Implementar [sem objeto], Configurar [sem detalhe]

4. **Atomicidade:** Task parece atômica (15-30 min)?
   - ❌ Muito ampla: "Implementar autenticação completa"
   - ✅ Atômica: "Implementar método `login(email, password)` retornando JWT"

**Se detectar tasks vagas:**

**Opção A: Refinar automaticamente**
- Tentar refinar task adicionando contexto baseado no plan.md e spec.md
- Exemplo:
  ```
  ANTES: "- [ ] Implementar autenticação"

  DEPOIS (refinado em 4 tasks):
  - [ ] Criar `AuthService` em `src/services/auth.service.ts`
  - [ ] Implementar método `login(email, password)` retornando `{token, user}`
  - [ ] Adicionar validação de credenciais com bcrypt
  - [ ] Criar endpoint POST /api/auth/login chamando AuthService.login()
  ```

**Opção B: Marcar e alertar usuário**
- Se não conseguir refinar automaticamente, marcar task:
  ```
  - [ ] [NEEDS_REFINEMENT] Implementar autenticação
  ```
- No final, avisar usuário:
  ```
  ⚠️ Encontrei [N] tasks que precisam ser refinadas:
  - TASK-XXX: [descrição]
  - TASK-YYY: [descrição]

  Recomendo revisar e detalhar estas tasks antes de usar com long-running-agent.
  ```

**Validação bem-sucedida:**
```
✅ Validação de qualidade de tasks completa!
   - [N] tasks validadas
   - [M] tasks refinadas automaticamente
   - [X] tasks marcadas para revisão ([NEEDS_REFINEMENT])
```

---

#### 5.3. Validar Compatibilidade XML (long-running-agent)

**Executar script de validação:**

```bash
python "${SKILLS_DIR}/sprint-context-generator/scripts/validate-compatibility.py" "docs/context-log-running/[feature-name-slug]/features.xml"
```

**O script valida:**
1. ✅ XML bem formado (sintaxe correta, pode ser parseado)
2. ✅ Atributos obrigatórios presentes:
   - Tag `<features>` tem `project`, `total`, `completed`
   - Tag `<category>` tem `name`
   - Tag `<feature>` tem `id`, `status`, `priority`
3. ✅ ID no formato `FEAT-XXX` (onde XXX é número de 3 dígitos)
4. ✅ Status é um dos valores válidos: `pending`, `in-progress`, `complete`, `blocked`
5. ✅ Priority é um dos valores válidos: `high`, `medium`, `low`
6. ✅ Tag `<steps>` existe e contém pelo menos 1 `<step>`

**Se validação falhar:**

**Opção A: Corrigir automaticamente (se possível)**
- Ex: Status="Pending" (maiúscula) → corrigir para "pending"
- Ex: ID="FEAT-5" → corrigir para "FEAT-005"
- Reescrever features.xml corrigido

**Opção B: Alertar usuário com detalhes**
```
❌ Validação de features.xml falhou!

Erros encontrados:
- Linha 5: Atributo 'status' tem valor inválido "Started" (deve ser: pending, in-progress, complete, blocked)
- Linha 8: ID "FEAT-5" está no formato incorreto (deve ser FEAT-XXX com 3 dígitos)

Por favor, corrija manualmente ou delete o arquivo e regenere a documentação.
```

**Se validação bem-sucedida:**
```
✅ features.xml validado com sucesso!
   - Sintaxe XML correta
   - Todos os atributos obrigatórios presentes
   - Formato compatível com long-running-agent
```

---

#### 5.4. Adicionar Links Inteligentes entre Arquivos

**Já incluídos nos templates da Fase 4!**

No topo de cada arquivo (spec.md, plan.md, tasks.md), já adicionamos:

```markdown
📂 **Documentação Relacionada:**
- [Link para outro arquivo] - Descrição
```

Verificar que links estão presentes. Se não, adicionar via Edit tool.

---

#### 5.5. Calcular Estimativa de Complexidade

**Baseado nas tasks geradas:**

```python
num_tasks = [Contar tasks no tasks.md]
has_external_integrations = [Q4 tinha tecnologias externas?]
is_new_stack = [Stack detectado é desconhecido/novo?]

def estimate_complexity(num_tasks, has_external_integrations, is_new_stack):
    if num_tasks <= 30 and not has_external_integrations and not is_new_stack:
        return "Baixa", "1-2 dias"
    elif num_tasks <= 70 or (has_external_integrations and num_tasks <= 50):
        return "Média", "3-5 dias"
    else:
        return "Alta", "5-10 dias"

complexity, time_estimate = estimate_complexity(num_tasks, has_external_integrations, is_new_stack)
```

**Armazenar para uso no resumo final.**

---

#### 5.6. Criar Branch Git

**Verificar se projeto é repo Git:**

```bash
git rev-parse --git-dir
```

**Se SIM (repo Git existe):**

1. Criar branch:
   ```bash
   git checkout -b feature/FEAT-XXX-[feature-name-slug]
   ```

   Exemplo: `git checkout -b feature/FEAT-005-sistema-autenticacao-jwt`

2. Se branch já existe:
   - Avisar: "Branch feature/FEAT-XXX-[nome] já existe. Usando branch existente."
   - Fazer checkout: `git checkout feature/FEAT-XXX-[nome]`

**Se NÃO (não é repo Git):**
- Pular step de Git
- ⚠️ Avisar usuário:
  ```
  ⚠️ Este projeto não está em um repositório Git.

  Recomendo inicializar Git para versionamento:
  git init
  git add .
  git commit -m "Initial commit"

  Depois você poderá criar branches para features.
  ```

**Informar usuário:**
```
✅ Branch Git criada: feature/FEAT-XXX-[nome]
```

---

#### 5.7. Criar Commit

**Se projeto é repo Git:**

```bash
git add docs/context-log-running/[feature-name-slug]/
git commit -m "docs: Add context for FEAT-XXX - [Nome da Feature]

- Spec with 6 persona analyses (Architect, Dev, QA, Designer, PM, BA)
- Technical plan with architecture and tech stack
- [N] granular tasks (high detail)
- Research with [M] external docs and best practices
- features.xml compatible with long-running-agent
- Complexity: [Baixa/Média/Alta]"
```

**Capturar hash do commit:**
```bash
git log -1 --format="%H"
```

**Se NÃO é repo Git:**
- Pular step de commit

**Informar usuário:**
```
✅ Commit criado: [short-hash] - "docs: Add context for FEAT-XXX..."
```

---

#### 5.8. Exibir Resumo Final

**Formato do resumo:**

```
✅ Sprint planejada com sucesso!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  FEAT-XXX: [Nome da Feature]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Resumo:
   ID: FEAT-XXX
   Categoria: [Categoria]
   Prioridade: [High/Medium/Low]
   Status: [Pending/Blocked]
   Total de tasks: [N]
   Complexidade: [Baixa/Média/Alta]
   Tempo estimado: [X-Y] dias

📦 Arquivos gerados:
   ✅ docs/context-log-running/[feature-name-slug]/spec.md      ([N] linhas)
   ✅ docs/context-log-running/[feature-name-slug]/plan.md      ([M] linhas)
   ✅ docs/context-log-running/[feature-name-slug]/tasks.md     ([X] tasks)
   ✅ docs/context-log-running/[feature-name-slug]/research.md  ([Y] linhas)
   ✅ docs/context-log-running/[feature-name-slug]/features.xml

🔧 Git:
   Branch: feature/FEAT-XXX-[feature-name-slug]
   Commit: [hash] - "docs: Add context for FEAT-XXX - [Nome]"

🚀 Próximos passos:

   1. REVISAR documentação gerada:
      - Leia spec.md para validar requisitos
      - Revise plan.md para aprovar arquitetura
      - Verifique tasks.md (tasks granulares e específicas?)

   2. EXECUTAR long-running-agent:

      /long-running-agent FEAT-XXX

      O agente vai:
      - Ler tasks.md e executar uma por vez
      - Marcar tasks como completadas em tempo real
      - Fazer commits após cada feature completada
      - Atualizar .claude/progress.md com progresso

   3. ACOMPANHAR progresso:
      - Monitorar .claude/progress.md
      - Revisar commits criados pelo agente
      - Testar feature conforme implementação avança

[Se status="blocked"]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  ATENÇÃO: Feature está BLOQUEADA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   Bloqueador: [descrição do bloqueador da Q6]

   Ação necessária: Implementar/configurar [bloqueador] ANTES de usar long-running-agent.

   Após resolver bloqueador:
   - Edite features.xml e mude status de "blocked" para "pending"
   - Execute: /long-running-agent FEAT-XXX

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

**FIM DO WORKFLOW PRINCIPAL**

---

## Referências

Esta skill possui arquivos de referência complementares. Consulte conforme necessário:

### Exemplo Completo de Documentação Gerada

Veja `references/example-generated-docs.md` para um exemplo completo de **FEAT-005: Sistema de Autenticação JWT**, mostrando:
- spec.md completo com todas as 6 análises de personas
- plan.md com arquitetura e decisões técnicas
- tasks.md com 87 tasks granulares
- research.md com pesquisa de NextAuth.js, bcrypt, JWT
- features.xml no formato correto

Este exemplo mostra o **nível de detalhe esperado** em cada arquivo.

### Guia de Personas

`references/persona-guidelines.md` detalha o que cada uma das 6 personas deve analisar e fornecer:
- 🏗️ Arquiteto de Soluções
- 💻 Desenvolvedor
- 🎨 Designer/UX
- ✅ QA
- 📊 Gerente de Projeto
- 💼 Business Analyst

Consulte para entender profundamente cada perspectiva.

### Checklist de Qualidade de Tasks

`references/task-quality-checklist.md` lista:
- Red flags (tasks vagas a evitar)
- Green signals (tasks bem definidas)
- Exemplos de refinamento
- Critérios de validação automática

Use para validar se tasks estão granulares e específicas.

### Templates

Arquivos de template para cada tipo de documentação:
- `references/spec-template.md`
- `references/plan-template.md`
- `references/tasks-template.md`
- `references/research-template.md`
- `references/features-xml-template.xml`

Consulte para manter consistência na geração.

### Script de Validação XML

`scripts/validate-compatibility.py` valida o features.xml:
- Sintaxe XML correta
- Atributos obrigatórios presentes
- Formato de IDs (FEAT-XXX)
- Valores de status e priority válidos

Execute manualmente se precisar validar:
```bash
python scripts/validate-compatibility.py path/to/features.xml
```

---

## Integração com long-running-agent

Esta skill gera arquivos **100% compatíveis** com a skill `long-running-agent`:

**features.xml:**
- Formato XML esperado pelo long-running-agent
- IDs sequenciais (FEAT-XXX)
- Status e prioridades definidas
- Referência aos docs em `notes`

**Fluxo completo:**
1. **Você**: Usa `sprint-context-generator` para planejar feature
2. **sprint-context-generator**: Gera spec.md, plan.md, tasks.md, research.md, features.xml
3. **Você**: Revisa documentação gerada e aprova
4. **Você**: Executa `/long-running-agent FEAT-XXX`
5. **long-running-agent**: Lê tasks.md e implementa tasks automaticamente
6. **long-running-agent**: Marca tasks como completadas, faz commits, atualiza progress.md

**Vantagens:**
- Contexto rico para o long-running-agent trabalhar
- Tasks granulares facilitam implementação autônoma
- Documentação completa permite que agente tome decisões informadas
- Validação automática garante compatibilidade

---

## Notas Técnicas

- **Linguagem**: Sempre responder em Português (seguindo CLAUDE.md do usuário)
- **Formato de saída**: Markdown + XML
- **Compatibilidade**: Windows (caminhos com `\`)
- **Git**: Assume que projeto está em git repo (avisar se não estiver)
- **Pesquisa**: Usa WebSearch e WebFetch nativos do Claude Code (não requer MCPs externos)
- **Validações**: Automáticas (qualidade de tasks, compatibilidade XML)
- **Estimativas**: Baseadas em número de tasks e complexidade técnica

---

## Troubleshooting

**Problema:** "features.xml não é compatível com long-running-agent"
- **Solução**: Execute `python scripts/validate-compatibility.py docs/context-log-running/[feature]/features.xml` para ver detalhes do erro. Corrija manualmente ou delete o arquivo e regenere.

**Problema:** "Tasks muito vagas ou genéricas"
- **Solução**: Revise `references/task-quality-checklist.md` para entender critérios. Edite tasks.md manualmente para adicionar especificidade (mencionar arquivos, componentes, métodos específicos).

**Problema:** "WebFetch/WebSearch falharam ao pesquisar documentação"
- **Solução**: Links inacessíveis são comuns. A skill usa fallback automático (WebSearch). Se mesmo assim falhar, adicione documentação manualmente ao research.md.

**Problema:** "Branch Git já existe"
- **Solução**: Normal se você já planejou esta feature antes. A skill faz checkout da branch existente. Se quiser começar do zero, delete a branch: `git branch -D feature/FEAT-XXX-[nome]`

**Problema:** ".claude/ não existe e não quero usar long-running-agent"
- **Solução**: Escolha opção "Não" na Fase 1 quando perguntado. Você terá apenas a documentação em `docs/context-log-running/` sem integração com long-running-agent.

---

**Skill criada por:** Claude Code Skill Creator
**Versão**: 1.0.0
**Compatível com**: long-running-agent v1.x
**Última atualização:** 2026-01-13
