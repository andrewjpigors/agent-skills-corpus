---
name: twelve-factor-app
description: Use when creating a new microservice or web application, reviewing an
  existing codebase for architectural compliance, auditing configuration management,
  checking how the app handles logs or processes, or evaluating portability and
  scalability of a service. Covers all 12 factors with compliance checklist, common
  violations, and correction patterns.
---

# Twelve-Factor App — Opencity Labs

La metodologia [Twelve-Factor App](https://12factor.net) definisce 12 principi
per costruire software-as-a-service portabile, scalabile e manutenibile.
In Opencity Labs questa metodologia si applica a tutti i microservizi e
alle web application. Usala sia per progettare nuovi servizi che per
verificare la conformità di servizi esistenti.

---

## Come usare questa skill

**Nuovo servizio:** segui i 12 fattori come checklist durante la progettazione.
Ogni fattore include pattern concreti per il contesto Opencity Labs
(Docker Swarm, GitLab CI, Python/Go, Kafka).

**Audit di un codebase esistente:** per ogni fattore, cerca i **segnali di violazione**
elencati. Se ne trovi, applica la **correzione** corrispondente.

---

## Fattore 1 — Codebase

**Principio:** un'unica codebase tracciata in version control, molti deploy.

### Conformità
- Un repository Git per servizio (monorepo è sconsigliato ma accettabile  se ogni servizio
  ha il proprio Dockerfile e ciclo di release indipendente che replica le funzionalità di devops.yml)
- Lo stesso codice va in tutti gli ambienti (locale, QA, produzione);
  le differenze sono solo nella configurazione, non nel codice

### Segnali di violazione
- Codice copiato e modificato tra repo per adattarlo all'ambiente
- Branch `production` con diff strutturali rispetto a `main`
- Più servizi che condividono lo stesso repository senza separazione
  di build/deploy indipendenti

### Correzione
Centralizza il codice in un unico repo, usa variabili d'ambiente per
le differenze di ambiente. Se un repo contiene più servizi logicamente
distinti, valuta la separazione in repo dedicati con il loro `gitlab-ci.yml`.

---

## Fattore 2 — Dipendenze

**Principio:** dichiara e isola esplicitamente le dipendenze.

### Conformità
- Il file di manifest delle dipendenze è presente e versionato (`requirements.txt`,
  `pyproject.toml`, `go.mod`, `package.json`, `pom.xml`, ecc.)
- Le dipendenze sono pinnate a versioni specifiche (non `>=`, ma `==` o lock file)
- Nessuna dipendenza implicita dal sistema operativo host

### Segnali di violazione
```
# Violazione: dipendenza non pinned
requests>=2.28.0

# Conformità: versione esatta o lock file
requests==2.31.0
```
- Comandi shell che assumono la presenza di tool di sistema (`curl`, `jq`, `wget`)
  senza installarli esplicitamente nel Dockerfile
- Assenza di lock file (`requirements.lock`, `poetry.lock`, `go.sum`)

### Correzione
```dockerfile
# Nel Dockerfile: installa esplicitamente ogni dipendenza di sistema
RUN apt-get install -y --no-install-recommends curl jq && \
    rm -rf /var/lib/apt/lists/*
```

Per Python usa `pip freeze > requirements.txt` o Poetry con lock file.
Per Go, `go.sum` è il lock file — non ignorarlo nel `.gitignore`.

---

## Fattore 3 — Configurazione

**Principio:** la configurazione è nell'ambiente, non nel codice.

### Conformità
- Tutto ciò che cambia tra ambienti (URL database, chiavi API, credenziali,
  feature toggle) viene letto da variabili d'ambiente
- Il codice sorgente non contiene segreti — nemmeno commentati
- Il file `.env` non è mai committato (sta in `.gitignore`)
- Un file `.env.example` documenta tutte le variabili richieste
- Se ci sono dei secrets che fanno da placeholder hanno prefisso test, es dbpassword = 'test13456787'

### Segnali di violazione
```python
# Violazione: URL hardcoded nel codice
DATABASE_URL = "postgresql://user:pass@prod-db:5432/mydb"

# Violazione: segreto in config file committato
API_KEY = "sk-abc123..."
```
```"

Nel docker-compose.ymml è ammmissibile l'uso di password di test che rendono l'ambiente creato subito
funzionante.


In CI GitLab, le variabili sensibili vanno in **Settings → CI/CD → Variables**
con flag "Masked" e "Protected". Non scriverle mai nel `.gitlab-ci.yml`.

In produzione (Docker Swarm), usa Docker Secrets per le credenziali
(vedi skill `aws-access-keys` per il pattern con aws-key-rotator).

---

## Fattore 4 — Backing Services

**Principio:** i servizi di supporto sono risorse collegate, non integrate.

### Conformità
- Database, broker Kafka, cache Redis, servizi email, storage S3:
  tutti configurati tramite URL/credenziali da variabili d'ambiente
- Il servizio può passare da database locale a database remoto
  senza modifiche al codice, solo cambiando la variabile d'ambiente

### Segnali di violazione
```python
# Violazione: connessione hardcoded a localhost
db = psycopg2.connect(host="localhost", database="mydb")

# Violazione: logica diversa per ambiente locale vs produzione
if os.getenv("ENV") == "production":
    db_host = "prod-db.internal"
else:
    db_host = "localhost"
```

### Correzione
```python
# Conformità: un solo punto di configurazione
import os
db = psycopg2.connect(os.environ["DATABASE_URL"])
```

```yaml
# In docker-compose.yml per sviluppo locale
services:
  app:
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
      - KAFKA_BOOTSTRAP_SERVERS=kafka:9092
  db:
    image: postgres:15
  kafka:
    image: docker.redpanda.com/redpandadata/redpanda:latest
```

---

## Fattore 5 — Build, Release, Run

**Principio:** separa nettamente le fasi di build, release ed esecuzione.

### Fasi
| Fase | Cosa fa | Artefatto |
|------|---------|-----------|
| **Build** | Compila il codice, scarica dipendenze, produce l'immagine Docker | Immagine Docker taggata |
| **Release** | Combina immagine con configurazione d'ambiente | Stack Docker con env vars |
| **Run** | Avvia i processi dal release nel runtime | Container in esecuzione |

### Conformità
- La CI produce un'immagine Docker immutabile con tag semantico (vedi `repo-setup`)
- La configurazione non è baked nell'immagine — viene iniettata al run time
- Non si esegue `docker build` direttamente in produzione

### Segnali di violazione
```dockerfile
# Violazione: configurazione baked nell'immagine
COPY .env /app/.env
ENV DATABASE_URL=postgresql://prod-db:5432/mydb
```

```yaml
# Violazione nel .gitlab-ci.yml: deploy che ricostruisce l'immagine
deploy:
  script:
    - docker build -t myapp .  # non farlo in produzione
    - docker run myapp
```

### Correzione
```dockerfile
# Conformità: nessuna configurazione nell'immagine
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ .
CMD ["python", "app.py"]
```

La configurazione arriva solo tramite `-e` / `--env-file` al momento del `docker run`
o tramite la sezione `environment` nello stack Swarm.

---

## Fattore 6 — Processi

**Principio:** esegui l'app come uno o più processi stateless.

### Conformità
- Ogni request è completamente soddisfatta senza stato persistente in memoria
- Lo stato condiviso vive nei backing service (database, Redis, Kafka), mai nel processo
- E' ammissibile l'uso della memoria del processo per cache temporanee a breve termmine e 
- solo per valori che non cambiano (es tenant_id, tenant_url)
- Il filesystem del container è usato solo per operazioni temporanee della singola request
- Non si usano sessioni sticky ("sticky sessions") come requisito funzionale
- Se il servizio richiede un webserver si può inserire nella stessa immagine un Caddy non webserver legacy Apache o Nginx 

### Segnali di violazione
```python
# Violazione: stato globale in memoria che accumula dati tra request
_cache = {}

@app.route("/items/<id>")
def get_item(id):
    if id not in _cache:
        _cache[id] = db.fetch(id)  # cache in-memory non condivisa tra istanze
    return _cache[id]
```

```python
# Violazione: upload salvato sul filesystem locale del container
@app.route("/upload", methods=["POST"])
def upload():
    file.save("/app/uploads/" + file.filename)  # perso al riavvio del container
```

### Correzione
- Per la cache: usa Redis (configurato via `REDIS_URL`) e verifica il supporto per Redis Cluster usato in produzione
- Per i file upload: usa S3 o storage esterno (configurato via `S3_BUCKET`)
- Per le sessioni: token stateless JWT o sessioni su Redis

---

## Fattore 7 — Port Binding

**Principio:** esporta i servizi tramite port binding.

### Conformità
- Il servizio si avvia autonomamente e si mette in ascolto su una porta
- La porta è configurabile tramite variabile d'ambiente (`PORT`)
- Non dipende da un application server esterno installato nell'OS host

### Pattern standard
```dockerfile
# Il servizio dichiara la porta che usa
EXPOSE 8080
CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
```

```python
import os
port = int(os.getenv("PORT", 8080))
app.run(host="0.0.0.0", port=port)
```

```yaml
# In docker-compose.yml
services:
  app:
    ports:
      - "8080:8080"
    environment:
      - PORT=8080
```

### Segnali di violazione
- Porta hardcoded senza possibilità di overriding via env var
- Il servizio richiede Apache/Nginx installato sull'host per funzionare
  (anziché includerlo nell'immagine o usare un server WSGI/ASGI embedded)

---

## Fattore 8 — Concorrenza

**Principio:** scala tramite il modello dei processi.

### Conformità
- L'app è progettata per essere scalata orizzontalmente (più repliche identiche)
- Tipi di lavoro diversi (web, worker, scheduler) sono processi separati
- Non si assume di essere l'unica istanza del servizio

### Pattern Docker Swarm
```yaml
# stack.yml — scala orizzontalmente
services:
  api:
    image: registry.gitlab.com/opencity-labs/myservice:1.2.3
    deploy:
      replicas: 3

  worker:
    image: registry.gitlab.com/opencity-labs/myservice:1.2.3
    command: ["python", "worker.py"]
    deploy:
      replicas: 2
```

### Segnali di violazione
- Lock file sul filesystem locale per operazioni critiche (non funziona con replicas > 1)
- Cron job avviato dal processo principale dell'app (duplicato su ogni replica)
- Assunzione che un job venga eseguito da una sola istanza senza meccanismo di coordinamento

### Correzione
- I cron job vanno in un processo/container separato con `replicas: 1`
- Per i cron è possibile usare replicas > 1 se avviene partizionamento dei job sui tenant 
- Per locking distribuito usa Redis non il database, costa troppo

---

## Fattore 9 — Disposability

**Principio:** massimizza la robustezza con startup veloce e graceful shutdown.

### Conformità
- Il servizio si avvia in pochi secondi (< 30s come target)
- E' acccettabile che esegua migrazioni e controlli all'avvio, ma l'avvio in assenza di migrazione da eseguire deve avviarsi rapidamente.
- All'avvio il servizio dichiara la propria versione nei log
- Alla ricezione di `SIGTERM` il processo completa le request in corso e si ferma pulitamente
- I job in coda vengono rilasciati al broker (non persi) quando il worker si ferma

### Pattern graceful shutdown (Python/FastAPI)
```python
import signal
import sys

def handle_shutdown(sig, frame):
    print("Shutting down gracefully...")
    # chiudi connessioni al db, rilascia risorse
    sys.exit(0)

signal.signal(signal.SIGTERM, handle_shutdown)
```

```python
# Per consumer Kafka: commit offset solo dopo processing completato
consumer = KafkaConsumer(enable_auto_commit=False)
for message in consumer:
    process(message)
    consumer.commit()  # commit esplicito dopo processing
```

### Segnali di violazione
- Startup che esegue operazioni pesanti bloccanti ad ogni avvio
- Nessun handler per `SIGTERM` (il processo viene killato bruscamente)
- Consumer Kafka con auto-commit che può perdere messaggi al riavvio

### Correzione
Le migration del database possono non essere parte del processo principale — 
ad esempio possono essere eseguite come **admin process** (Fattore 12)
prima del deploy, non all'avvio, ma in questo caso il processo principale
deve rifiutarsi di partire se non sono state eseguite le migrazioni necessarie.

---

## Fattore 10 — Dev/Prod Parity

**Principio:** mantieni sviluppo, staging e produzione il più simili possibile.

### Conformità
- Stesso database engine in locale e in produzione (no SQLite locale / PostgreSQL in prod)
- Se si usa storage cloud in produzione, anche il docker-compose per lo sviluppo locale deve usare cloud storage, no fall-back su filesystem locale.
- Stesso broker Kafka in CI (vedi `hurl-api-tests` skill per il setup Redpanda in CI)
- Il `docker-compose.yml` usa le stesse immagini Docker del deployment in produzione
- Gap temporale minimo tra scrittura del codice e deploy (CI/CD continuo)
- Nella CI si devono eseguire i test dopo la build dell'immagine e usando la stessa, non build volatile nel runner dei test.

### Segnali di violazione
```yaml
# Violazione: SQLite in locale, PostgreSQL in produzione
# settings.py
if DEBUG:
    DATABASES = {"ENGINE": "django.db.backends.sqlite3"}
else:
    DATABASES = {"ENGINE": "django.db.backends.postgresql"}
```

- Mocking di backing services nei test di integrazione (usa i veri servizi)
- `docker-compose.yml` con immagini diverse da quelle usate in produzione

### Correzione
```yaml
# Conformità: PostgreSQL in tutti gli ambienti
services:
  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=mydb
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
```

Usa Redpanda (compatibile Kafka) in CI per i test degli event consumer —
vedi la skill `hurl-api-tests` per la configurazione GitLab CI.

---

## Fattore 11 — Logs

**Principio:** tratta i log come stream di eventi.

### Conformità
- I log vengono scritti su `stdout`/`stderr` senza buffering
- Il servizio non gestisce rotazione, compressione o destinazione dei log
- Il formato è strutturato (JSON) per facilitare aggregazione e query
- I log NON contengono dati personali, quando ci si riferisce agli utenti si fa per user UUID (eventualmente abbreviato)

### Pattern (Python)
```python
import logging
import json
import sys

# Logging strutturato su stdout
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter(
    '{"time":"%(asctime)s","level":"%(levelname)s","msg":"%(message)s"}'
))
logging.basicConfig(handlers=[handler], level=logging.INFO)

logger = logging.getLogger(__name__)
logger.info("Service started", extra={"port": 8080})
```

### Segnali di violazione
```python
# Violazione: log su file
logging.basicConfig(filename="/var/log/app/app.log")

# Violazione: print invece di logger (nessun livello, no struttura)
print("Error processing request")
```

```dockerfile
# Violazione: il Dockerfile redirige stdout su file
CMD ["sh", "-c", "python app.py > /var/log/app.log 2>&1"]
```

### Correzione
In Docker, i log su `stdout` vengono automaticamente catturati da
`docker logs` e dall'aggregatore di log (Loki nel caso Opencity Labs).
Non configurare mai file handler nel codice applicativo.

---

## Fattore 12 — Admin Processes

**Principio:** esegui i task di amministrazione come processi one-off.

### Conformità
- Migration del database, script di backfill, task di manutenzione:
  tutti eseguiti come processi separati, non all'avvio dell'app
- Gli admin process usano lo stesso codice e la stessa configurazione del servizio principale
- Sono documentati e versioned nel repository

### Pattern GitLab CI
```yaml
# .gitlab-ci.yml — migration come job manuale o pre-deploy
migrate:
  stage: pre-deploy
  image: registry.gitlab.com/opencity-labs/myservice:${CI_COMMIT_TAG}
  script:
    - python manage.py migrate
  when: manual  # oppure automatico prima del deploy
  environment:
    name: production
```

### Pattern Docker (esecuzione manuale)
```bash
# Esegui migration sull'ambiente di produzione
docker run --rm \
  --env-file /run/secrets/myservice.env \
  registry.gitlab.com/opencity-labs/myservice:1.2.3 \
  python manage.py migrate

# REPL di debug (solo ambienti non-prod)
docker run --rm -it \
  registry.gitlab.com/opencity-labs/myservice:1.2.3 \
  python manage.py shell
```

### Segnali di violazione
```python
# Violazione: migration all'avvio del processo principale
if __name__ == "__main__":
    run_migrations()  # eseguito ad ogni restart, ad ogni replica
    app.run()
```

---

## Checklist di audit rapido

Usa questa checklist per verificare la conformità di un servizio esistente.

| # | Fattore | Domanda chiave | Verificare |
|---|---------|---------------|------------|
| 1 | Codebase | Un repo per servizio? | `git remote -v`, struttura del repo |
| 2 | Dipendenze | Lock file presente? Nessuna dipendenza implicita? | `requirements.txt`/`go.mod`/`package-lock.json`, Dockerfile |
| 3 | Config | Nessun segreto nel codice? Config da env var? | `grep -r "password\|secret\|api_key" --include="*.py"` |
| 4 | Backing services | Tutti i servizi esterni configurabili via env? | Cerca `localhost` hardcoded, URL hardcoded |
| 5 | Build/Release/Run | L'immagine è immutabile? Nessuna config baked? | Dockerfile, `.gitlab-ci.yml` |
| 6 | Processi | Nessuno stato in memoria? File upload su storage esterno? | Cerca variabili globali mutabili, path filesystem |
| 7 | Port binding | Porta configurabile? Server embedded? | Dockerfile EXPOSE, CMD, env PORT |
| 8 | Concorrenza | Funziona con replicas > 1? Cron separato? | stack.yml replicas, cron job |
| 9 | Disposability | Startup < 30s? Handler SIGTERM? | Benchmark avvio, signal handler |
| 10 | Dev/Prod parity | Stesso db engine ovunque? docker-compose aggiornato? | `docker-compose.yml` vs stack prod |
| 11 | Logs | Solo stdout/stderr? Formato strutturato? | Configurazione logging, Dockerfile CMD |
| 12 | Admin processes | Migration separata dall'avvio? | `__main__`, Dockerfile ENTRYPOINT |

---

## Comandi di audit utili

```bash
# Cerca credenziali hardcoded (Fattore 3)
grep -rn "password\s*=\s*['\"]" --include="*.py" --include="*.go" .
grep -rn "SECRET\|API_KEY\|TOKEN" --include="*.py" . | grep -v "os.getenv\|os.environ"

# Cerca localhost hardcoded (Fattore 4)
grep -rn "localhost\|127\.0\.0\.1" --include="*.py" --include="*.go" . \
  | grep -v "test\|spec\|_test"

# Cerca logging su file (Fattore 11)
grep -rn "filename=" --include="*.py" .
grep -rn "FileHandler\|RotatingFileHandler" --include="*.py" .

# Verifica che il Dockerfile non copi .env (Fattore 3)
grep -n "COPY.*\.env\|ADD.*\.env" Dockerfile

# Cerca stato globale mutabile (Fattore 6)
grep -n "^[A-Z_]* = {}\|^[A-Z_]* = \[\]" *.py
```
