---
name: aws-access-keys
description: Use when a developer asks to add AWS credentials to a service, configure
  AWS_ACCESS_KEY_ID or AWS_SECRET_ACCESS_KEY, rotate AWS keys, or migrate hardcoded
  AWS keys out of YAML config files. Also use when setting up Docker Secrets for AWS
  or adding the aws-key-wrapper entrypoint to a Dockerfile.
---

# AWS Access Keys — Opencity Labs

## Regola fondamentale

Non inserire mai `AWS_ACCESS_KEY_ID` e `AWS_SECRET_ACCESS_KEY` direttamente nei
file YAML dei servizi. Le credenziali AWS vanno sempre gestite tramite
**Docker Secrets** + **aws-key-rotator**. Se vedi chiavi hardcoded in un file,
segnalalo e proponi la migrazione.

---

## Come procedere — chiedi prima, poi genera

Quando un developer chiede di aggiungere credenziali AWS, raccogli queste
informazioni **prima** di generare qualsiasi file:

1. **Nome dell'utente IAM** — es. `my-service-s3`. Se non è ancora stato creato,
   di' al developer di chiederlo al team Ops.
2. **Le chiavi AWS sono già disponibili?** — Access Key ID e Secret Access Key.
   Se no, il developer deve prima ottenerle da Ops.
3. **Nomi delle env var nel container** — di solito `AWS_ACCESS_KEY_ID` e
   `AWS_SECRET_ACCESS_KEY`, ma possono essere custom (es. `BACKUP_AWS_ACCESS_KEY_ID`).
4. **Il servizio usa SES SMTP?** — se sì, serve anche `AWS_DEFAULT_REGION`.

---

## Passo 1 — Crea il Docker Secret

Genera questo comando da eseguire su **boat-manager** (sostituisci i valori reali):

```bash
printf '{"new_access_key_id":"<ACCESS_KEY_ID>","new_secret_access_key":"<SECRET_ACCESS_KEY>"}' \
  | docker secret create <UTENTE_IAM>-$(date -u +"%Y%m%dT%H%M%SZ") -
```

---

## Passo 2 — Modifica stack.yml

Leggi il `stack.yml` del servizio, poi proponi queste modifiche.

**Rimuovi** da `environment`:
```yaml
AWS_ACCESS_KEY_ID: ...
AWS_SECRET_ACCESS_KEY: ...
```

**Aggiungi** a livello radice e nel servizio:
```yaml
secrets:
  <NOME>:
    external: true
    name: "<UTENTE_IAM>-${LATEST}"

services:
  <servizio>:
    environment:
      AWS_GROUP: <UTENTE_IAM>
    secrets:
      - <NOME>
```

`<NOME>` è il nome logico del segreto nel compose (es. `aws-creds`).

**Caso speciale — SES SMTP:** aggiungi `AWS_DEFAULT_REGION: eu-central-1`
nell'`environment`. Serve al rotatore per generare le credenziali SMTP corrette.

---

## Passo 3 — Entrypoint nel container

Ricorda al developer che deve aggiungere un entrypoint wrapper al Dockerfile.
Il container riceverà il segreto in `/run/secrets/` e l'entrypoint deve leggerlo
e impostare le env var AWS prima di avviare il processo principale.

Lo script di riferimento è `aws-key-wrapper.sh` disponibile in
`gitlab.com/opencity-labs/ops/-/blob/master/aws-key-wrapper.sh`.

Se il developer chiede aiuto per configurarlo o integrarlo nel Dockerfile,
ecco i dettagli:

- Nello script, sostituire `NOME_GIUSTO_ACCESS_KEY_ID` e
  `NOME_GIUSTO_SECRET_ACCESS_KEY` con i nomi delle env var corretti
  (es. `AWS_ACCESS_KEY_ID` e `AWS_SECRET_ACCESS_KEY`)
- Nel Dockerfile:
  ```dockerfile
  COPY aws-wrapper.sh /usr/local/bin/aws-wrapper.sh
  RUN chmod 0555 /usr/local/bin/aws-wrapper.sh

  ENTRYPOINT ["/usr/local/bin/aws-wrapper.sh"]
  CMD [...]
  ```
- Se esiste già un entrypoint, chiedi quando servono le variabili AWS e
  posiziona `aws-wrapper.sh` di conseguenza (prima o dopo).

---

## Verifica finale

Controlla che non siano rimaste chiavi hardcoded nel repo:
```bash
grep -r "AKIA" .
grep -rn "AWS_ACCESS_KEY_ID\s*:" . --include="*.yml"
grep -rn "AWS_SECRET_ACCESS_KEY\s*:" . --include="*.yml"
```
