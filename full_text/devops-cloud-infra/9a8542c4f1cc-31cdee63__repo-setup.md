---
name: repo-setup
description: Use when creating a new repository, reviewing an existing repo structure,
  writing a Dockerfile, configuring gitlab-ci.yml, including devops.yml in CI pipeline,
  setting up CI/CD for a repo, preparing a project for first deploy, or starting work
  on a new branch. Enforces mandatory files, Docker proxy, OCI labels, CI security
  scanning, devops.yml include, and Claude Code review setup.
---

# Repository Setup — Opencity Labs

Opencity Labs usa **GitLab** come piattaforma principale. Il gruppo è `opencity-labs`
su `gitlab.com`. L'accesso ai repo va fatto **sempre via SSH**
(`git@gitlab.com:opencity-labs/...`), mai via HTTPS.

Esistono anche repository su **GitHub**:
- `github.com/opencity-labs` — solo quando strettamente necessario (es. integrazione
  con tool che supportano solo GitHub). Creare un repo qui richiede **approvazione del CTO**.
- `github.com/OpencontentCoop` — repository legacy del CMS, non creare repo nuovi qui.

Per qualsiasi nuovo repository, usare GitLab salvo esplicita indicazione contraria.

## File obbligatori in ogni repository

Ogni repo deve avere questi file nella root, senza eccezioni:

- `README.md` — struttura definita sotto
- `LICENSE` — testo AGPL-3.0
- `Dockerfile`
- `docker-compose.yml` — con dati di test per uso locale
- `.gitlab-ci.yml` — che include devops.yml del gruppo

Se c'è una persistenza: le migrazioni devono essere gestite da una libreria del
framework (es. Alembic per Python, migrate per Go, Doctrine per PHP) — non script manuali.

## README — struttura obbligatoria

In questo ordine:

1. Titolo e sottotitolo descrittivo (1-2 righe)
2. Descrizione **senza acronimi e gergo tecnico**: casi d'uso e finalità
3. Stato: `produzione` | `beta` | `in sviluppo attivo` | `abandoned`
4. Link a docs.opencityitalia.it (se esiste documentazione estesa)
5. Variabili d'ambiente per la configurazione (ricordare 12factor)
6. Monitoraggio: health-check (cosa controlla?) e metriche esposte
7. Come eseguire in locale (deve funzionare con `docker-compose up`)
8. Avvisi su scelte del docker-compose da rivedere prima di andare in produzione
9. Limitazioni e known issues
10. `Copyright Opencity Labs` — licenza AGPL-3.0

## Dockerfile

### FROM — proxy obbligatorio per Docker Hub

Il proxy evita il rate-limit di Docker Hub durante la build.

```dockerfile
# ❌ NON fare
FROM node:18-alpine

# ✅ Fare
FROM gitlab.com:443/opencity-labs/dependency_proxy/containers/node:18-alpine
```

Il proxy verifica automaticamente se l'immagine base è aggiornata senza consumare
il rate-limit.

### OCI Labels — obbligatorie

Le label sono già inserite se usate i job di build in devops.yml

```dockerfile
LABEL org.opencontainers.image.source="https://gitlab.com/opencity-labs/<nome-repo>"
LABEL org.opencontainers.image.authors="info@opencitylabs.it"
LABEL org.opencontainers.image.vendor="Opencity Labs"
LABEL org.opencontainers.image.documentation="https://docs.opencityitalia.it"
LABEL org.opencontainers.image.licenses="AGPL-3.0-or-later"
```

Opzionali, aggiungibili in CI:
- `org.opencontainers.image.title`
- `org.opencontainers.image.revision`
- `org.opencontainers.image.url`

## .gitlab-ci.yml

### Struttura minima obbligatoria

Questo garantisce i controlli di sicurezza, la scansione delle dipendenze, il labeling delle immagini docker, la firma crittografica e molte altre cose.

```yaml
stages:
  - build
  - test
  - deploy
  - review
  - dast
  - staging
  - canary
  - production
  - incremental rollout 10%
  - incremental rollout 25%
  - incremental rollout 50%
  - incremental rollout 100%
  - performance
  - cleanup

include:
  - project: 'opencity-labs/product'
    ref: main
    file: '.gitlab/ci/devops.yml'
```

Aggiungere di seguito eventuali step custom

### Build multipiattaforma in un solo step (solo per Go)

Per go o altri linguaggi compilati si può fare una buid unica

```yaml
variables:
  BUILD_DOCKER_MULTIPLATFORM: "true"
```

### Immagini Docker Hub negli step CI

Se uno step CI usa un'immagine da Docker Hub (non solo nel Dockerfile):

```yaml
mytest:
  image: ${CI_DEPENDENCY_PROXY_GROUP_IMAGE_PREFIX}/nome/immagine:tag
```

## Security scanning

### Snyk — attivare su ogni repo con dipendenze o Dockerfile

```yaml
variables:
  SNYK_ENABLED: "true"
  SNYK_SEVERITY_THRESHOLD: "high"
```

Se ci sono molte vulnerabilità note all'avvio, partire con `critical` e abbassare
progressivamente:
- `critical` → solo falle con exploit attivi
- `high` → soglia dichiarata nella ISO27001 aziendale
- `medium` / `low` → a discrezione del team

### GitGuardian — secrets nei commit

Abilitato di default via devops.yml. Se servono eccezioni (es. credenziali di test
nei README), creare `.gitguardian.yaml` in root:

```yaml
version: 2
secret:
  ignored_paths:
    - '**/README.md'
    - 'LICENSE'
  ignored_matches:
    - name: "test credential"
      match: "valore-esatto-del-falso-positivo"
```

### Firma immagini

Gestita automaticamente da devops.yml tramite SigStore/Cosign — non serve
configurazione aggiuntiva.

## Versioning

- Semantic versioning: `MAJOR.MINOR.PATCH`
- Tag ogni release: `git tag x.y.z && git push origin x.y.z`
- Policy immagini: abilitare cancellazione automatica delle immagini non taggate
  in `Settings → Packages & Registry` — conservare solo le release `x.y.z`

### Tag delle immagini Docker

I tag devono rispettare esattamente questi formati — nessun prefisso (no `v`, no `release-`):

**Build separate (default — `BUILD_DOCKER_MULTIPLATFORM` non attivo):**

| Tag | Architettura | Branch/evento |
|-----|-------------|---------------|
| `x.y.z-x86` | linux/amd64 | git tag `x.y.z` |
| `x.y.z-arm` | linux/arm64 | git tag `x.y.z` |
| `latest-x86` | linux/amd64 | default branch (main) |
| `latest-arm` | linux/arm64 | default branch (main) |

**Build multipiattaforma (`BUILD_DOCKER_MULTIPLATFORM=true`):**

| Tag | Branch/evento |
|-----|---------------|
| `x.y.z` | git tag `x.y.z` |
| `latest` | default branch (main) |

I tag sono generati automaticamente da devops.yml. Non aggiungerli manualmente.

```
# ❌ NON fare
v1.2.3
release-1.2.3
1.2.3-amd64
1.2.3-arm64

# ✅ Fare (build separate)
1.2.3-x86
1.2.3-arm
latest-x86
latest-arm

# ✅ Fare (multiplatform)
1.2.3
latest
```

## Visibilità del repo

- **Pubblico by default** — anche utility, demo e repo dimostrativi
- **Privato** solo se contiene logica del SaaS che ha senso solo sui grandi numeri che noi gestiamo nel nostro, non è mai necessario garantire una soluzione così sofisticata. Es. tenant manager, automazioni delivery.

## Posizionamento e permessi del repository

Quando crei un nuovo repo su GitLab ne diventi automaticamente **Owner**.

### Scegli il gruppo giusto

Metti il repo nel sottogruppo che corrisponde al prodotto su cui stai lavorando.
Per il catalogo completo dei prodotti e servizi consulta il
[foglio "Servizi erogati"](https://docs.google.com/spreadsheets/d/1roiXBNlm7bWoKDJEOwMJvtt5qZTEF9Z6d0IXQQyQ_8U/edit?gid=1250604092).

Tabella di riferimento rapido:

| Prodotto | Servizi inclusi | Sottogruppo GitLab |
|----------|-----------------|--------------------|
| **OC Website** | Sito Comunale, Sito ASL, Sito regionale/provinciale, Sito interno | `sito-istituzionale` |
| **OC Forms** | Pratiche a istanza | `area-personale` |
| **OC Booking** | Prenotazione appuntamento, Prenotazione advanced, Prenotazione Sale (a pagamento) | `catalogo-servizi-digitali` |
| **OC Helpdesk** | Richiesta assistenza, Segnalazione sul territorio, Segnalazione EVO | `catalogo-servizi-digitali` |
| **OC Forms** | Catalogo dei servizi digitali | `catalogo-servizi-digitali` |
| **OC Payments** | Importazione massiva dovuti | `integrations` |
| **OC Connect** | Invio messaggi massivi | `opencity-italia-connect` |
| **OC AI** | Chatbot, Motore di ricerca ibrido | `opencity-ai` |
| **OC Satisfy** | Customer satisfaction siti istituzionali | `satisfy` |
| **OC Agenda** | Agenda eventi | `openagenda` |
| **OC Analytics** | Dashboard su Google Sheet, Dashboard su Metabase | `business-intelligence` |

Scegliere il gruppo giusto non è solo una questione di ordine: determina quali colleghi
hanno visibilità e accesso al repo per default.

### Imposta i permessi a livello di progetto

Se il repo sta in un **sottogruppo di prodotto** (es. `sito-istituzionale` per OC Website,
`area-personale` per OC Forms) i permessi del sottogruppo sono intenzionali e stabili:
puoi fare affidamento su di essi e non devi ridefinirli sul singolo repo.

Non fare invece affidamento sui permessi ereditati dal **gruppo root `opencity-labs`**:
quelli sono generici e possono cambiare.

In ogni caso, aggiungi esplicitamente sul repo le persone che non sono già coperte
dal sottogruppo, seguendo questo schema:

| Chi | Livello |
|-----|---------|
| Tu (creatore) | Owner (50) — automatico |
| Colleghi del tuo team che ci lavorano | Maintainer (40) |
| Figure junior o persone esterne al team | Developer (30) |

**Aggiungi subito i Maintainer** al momento della creazione: in caso di tua assenza
devono poter gestire MR, hotfix e altre criticità senza bloccarsi.

## Claude Code Review automatica

`devops.yml` include un job `claude-review` che si attiva su ogni MR **se il repo
ha un file `REVIEW.md` nella root**. Senza quel file il job non parte — è opt-in.

Il file contiene le istruzioni di review personalizzate per il repo: cosa controllare,
quali standard seguire, cosa ignorare. Claude legge quelle istruzioni + il diff della
MR e pubblica la review come nota direttamente sulla MR.

### Struttura di REVIEW.md

Il file deve richiamare le istruzioni base del repo product, poi aggiungere le regole
specifiche del repo. Questo mantiene un baseline comune aggiornato e lascia spazio
per personalizzazioni per stack, convenzioni del team o aree critiche.

```markdown
# Istruzioni per la code review

Applica prima le istruzioni di review standard dal file base del repo product:
https://gitlab.com/opencity-labs/product/-/raw/main/REVIEW.md

Poi applica le istruzioni specifiche per questo repo riportate di seguito.

---

## Istruzioni specifiche per questo repo

<!-- Personalizza qui: stack tecnologico, convenzioni del team, aree critiche -->
```

Il template completo è in `templates/REVIEW.md` di questa skill.

### Quando creare REVIEW.md

**Se stai iniziando a lavorare su un nuovo branch in un repo che non ha ancora
`REVIEW.md`**, suggerisci di crearlo prima di aprire la MR:

```bash
curl -O https://gitlab.com/opencity-labs/company-skills/-/raw/main/claude/plugins/company-practices/skills/repo-setup/templates/REVIEW.md
# Personalizza per il repo corrente, poi committa
git add REVIEW.md && git commit -m "chore: add REVIEW.md for Claude Code CI review"
```

La review automatica vale subito per quella MR e per tutte le successive.

## Claude Code Issue Review

Analogamente alla code review, `devops.yml` include un job che si attiva
sulle issue **se il repo ha un file `ISSUES.md` nella root**. Senza quel file il job non parte — è opt-in.

Il file contiene i criteri di qualità per le issue. Claude legge quei criteri, analizza
l'issue e pubblica un commento con il report direttamente sull'issue.

### Struttura di ISSUES.md

Stessa logica di REVIEW.md: le istruzioni base vengono dal repo product, le aggiunte
specifiche stanno nel file locale.

```markdown
# Istruzioni per la gestione delle issue

Applica prima le istruzioni standard dal file base del repo product:
https://gitlab.com/opencity-labs/product/-/raw/main/ISSUES.md

Poi applica le istruzioni specifiche per questo repo riportate di seguito.

---

## Istruzioni specifiche per questo repo

<!-- Personalizza qui: criteri aggiuntivi, label specifiche, flussi del prodotto -->
```

Il template completo è in `templates/ISSUES.md` di questa skill.

### Quando creare ISSUES.md

```bash
curl -O https://gitlab.com/opencity-labs/company-skills/-/raw/main/claude/plugins/company-practices/skills/repo-setup/templates/ISSUES.md
# Personalizza, poi committa
git add ISSUES.md && git commit -m "chore: add ISSUES.md for Claude Code issue review"
```

## Checklist rapida prima del primo commit

- [ ] README con tutti e 10 i punti obbligatori
- [ ] LICENSE AGPL-3.0
- [ ] Dockerfile con FROM tramite proxy e OCI labels
- [ ] docker-compose.yml che funziona con `docker-compose up`
- [ ] .gitlab-ci.yml con stages completi e include devops.yml
- [ ] SNYK_ENABLED=true nelle variabili CI del progetto
- [ ] Policy cancellazione immagini non taggate abilitata
- [ ] Semantic versioning: primo tag `0.1.0` o `1.0.0`
- [ ] `REVIEW.md` nella root (opzionale ma consigliato — attiva la review automatica di Claude su ogni MR)
- [ ] `ISSUES.md` nella root (opzionale ma consigliato — attiva la review automatica di Claude sulle issue)
