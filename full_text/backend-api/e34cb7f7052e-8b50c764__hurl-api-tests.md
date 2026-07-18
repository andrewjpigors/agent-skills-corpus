---
name: hurl-api-tests
description: Use when adding or changing a ReST API to a service, writing API tests,
  adding a tests/ directory to a repository,
  configuring a CI stage for end-to-end API tests, or reviewing existing .hurl files.
  Covers file structure, auth patterns, assertions, cleanup, and CI integration.
---

# Test automatici API con Hurl — Opencity Labs

Opencity Labs usa **GitLab CI**. La CI è sempre configurata tramite `.gitlab-ci.yml`
che include `devops.yml` dal gruppo (vedi skill `repo-setup`). Non chiedere mai
quale piattaforma CI usa il team.

Ogni API deve avere test automatici scritti con [Hurl](https://hurl.dev).
I file `.hurl` vivono nella directory `tests/` del repository e vengono eseguiti
in CI ad ogni push.

## Struttura dei file

```
repo/
└── tests/
    ├── auth.hurl          # test di autenticazione
    ├── categories.hurl    # test per il dominio principale
    └── cleanup.hurl       # se il cleanup non è inline
```

Un file `.hurl` contiene una sequenza di richieste HTTP con asserzioni.
Ogni richiesta è separata da una riga vuota.

## Pattern base — CRUD con autenticazione

Questo è il pattern completo: login → operazione → verifica → cleanup.

```hurl
# 1. Login — cattura il token
POST https://{{host}}/api/auth
{
  "username": "{{user}}",
  "password": "{{pass}}"
}

HTTP 200
[Asserts]
jsonpath "$.token" != null
[Captures]
token: jsonpath "$.token"


# 2. Crea una risorsa
POST https://{{host}}/api/categories
Authorization: Bearer {{token}}
{
  "name": "Test Category",
  "description": "Creata durante il test, da rimuovere"
}

HTTP 201
[Asserts]
jsonpath "$.id" != null
jsonpath "$.slug" == "test-category"
jsonpath "$.description" == "Creata durante il test, da rimuovere"
[Captures]
category_id: jsonpath "$.id"


# 3. Leggi la risorsa appena creata
GET https://{{host}}/api/categories/{{category_id}}

HTTP 200
[Asserts]
jsonpath "$.id" == {{category_id}}
jsonpath "$.slug" == "test-category"


# 4. Cleanup — cancella la risorsa di test
DELETE https://{{host}}/api/categories/{{category_id}}
Authorization: Bearer {{token}}

HTTP 204
```

## Regole obbligatorie

**Credenziali:** non scrivere mai username, password o token direttamente nel file `.hurl`.
Usare sempre variabili (`{{variabile}}`) passate via CI o via file di variabili.

**Cleanup:** ogni test che crea dati deve eliminarli alla fine.
Se il test fallisce a metà, il cleanup non viene eseguito — su ambienti condivisi
(bugliano-qa) questo può lasciare dati sporchi. Tenerlo in mente e pulire
manualmente se necessario.

**Naming:** usa nomi descrittivi nelle risorse di test:
`"name": "Test Category — created by hurl test, safe to delete"`

## Asserzioni comuni

```hurl
[Asserts]
# Status code (alternativa al blocco HTTP)
status == 200

# JSON path
jsonpath "$.id" != null
jsonpath "$.status" == "active"
jsonpath "$.items" count == 3
jsonpath "$.items[0].name" == "primo"

# Header
header "Content-Type" contains "application/json"

# Durata massima risposta (ms)
duration < 500
```

## Ambiente bugliano-qa

Se non è possibile replicare l'ambiente in CI (es. dipende da servizi esterni),
usare bugliano-qa e impostare l'esecuzione manuale:

```yaml
end2end_test:
  stage: test
  when: manual
  ...
```

Per gli ambienti replicabili in CI, l'esecuzione deve essere automatica (no `when: manual`).

## Integrazione CI — stage obbligatorio

```yaml
end2end_test:
  stage: test
  image:
    name: ghcr.io/orange-opensource/hurl:latest
    entrypoint: [""]
  script:
    - hurl --test --glob "./tests/*.hurl"
  variables:
    HOST: $QA_HOST      # variabile definita a livello di repo o gruppo
    USER: $QA_USER
    PASS: $QA_PASS
```

Le variabili `QA_HOST`, `QA_USER`, `QA_PASS` vanno definite nelle
**variabili CI del progetto** (Settings → CI/CD → Variables), non nel file `.gitlab-ci.yml`.

## Esecuzione locale

```bash
# Con variabili inline
hurl --test --variable host=localhost:8080 --variable user=admin --variable pass=secret \
  tests/categories.hurl

# Con file di variabili
echo "host=localhost:8080\nuser=admin\npass=secret" > .hurl-vars
hurl --test --variables-file .hurl-vars tests/categories.hurl

# Tutti i test
hurl --test --variables-file .hurl-vars --glob "tests/*.hurl"
```

Aggiungere `.hurl-vars` al `.gitignore`.

## Aggiungere Kafka ai test CI

Se il microservizio consuma eventi Kafka, aggiungerlo come servizio CI:

```yaml
end2end_test:
  stage: test
  services:
    - name: docker.redpanda.com/redpandadata/redpanda:v23.2.19
      alias: kafka
      command:
        - redpanda
        - start
        - --kafka-addr internal://0.0.0.0:9092,external://0.0.0.0:19092
        - --advertise-kafka-addr internal://kafka:9092,external://localhost:19092
        - --smp 1
        - --memory 1G
        - --mode dev-container
        - --set redpanda.auto_create_topics_enabled=true
  variables:
    KAFKA_BOOTSTRAP_SERVERS: "kafka:9092"
```
