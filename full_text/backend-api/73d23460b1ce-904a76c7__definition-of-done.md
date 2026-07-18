---
name: definition-of-done
description: Use when closing an issue, opening a merge request, preparing a sprint
  release, or checking if a feature is ready for QA. Covers API DoD, frontend DoD,
  and mandatory security checks for new attack surfaces.
---

# Definition of Done — Opencity Labs

Una issue è **done** solo se soddisfa tutti i criteri applicabili.
Le issue che non superano la DoD tornano in backlog — non si chiudono.

## DoD — API

- [ ] **Swagger / OpenAPI**: endpoint documentato, validato con
  [OpenAPI Checker](https://italia.github.io/api-oas-checker/) senza errori
- [ ] **Test automatici con Hurl**: file `.hurl` presenti in `tests/`,
  pipeline CI verde (@hurl-api-tests per come scriverli)
- [ ] **CI completa senza errori**: SAST, secret detection, code quality
- [ ] **Variabili d'ambiente**: tutte documentate nel README
  (nome, descrizione, valore di default se ha senso)
- [ ] **README aggiornato**: include la nuova funzionalità o la modifica
- [ ] **docker-compose.yml funzionante**: `docker-compose up` produce un ambiente
  locale minimale con dati di test già inclusi
- [ ] **Deploy in QA**: servizio aggiornato sull'ambiente di QA e verificabile
  dai tester senza configurazione aggiuntiva

## DoD — Frontend

- [ ] **Design system**: componenti aderenti al design system aziendale
- [ ] **Mobile-first**: verificato su viewport mobile prima che su desktop
- [ ] **Criteri di accettazione**: tutti i "verificare che..." della issue
  eseguiti senza errori in QA
- [ ] **Peer review**: almeno un collega del team ha fatto review del codice
- [ ] **MR su docs**: se la feature è documentata, la MR su docs.opencityitalia.it
  è aperta (non necessariamente merged)
- [ ] **README aggiornato**
- [ ] **docker-compose.yml funzionante**
- [ ] **Deploy in QA**

## DoD — Sicurezza (obbligatorio per nuove superfici di attacco)

Si applica quando si introduce un nuovo microservizio, una nuova API pubblica,
o modifiche all'autenticazione/autorizzazione.

- [ ] Solo i metodi HTTP dichiarati sono effettivamente usabili
  (verifica con Nuclei o manualmente)
- [ ] Gli endpoint protetti restituiscono `401` o `403` se chiamati senza auth
- [ ] I tentativi di accesso falliti sono loggati a livello `warning`
- [ ] Metriche di errore di sicurezza esposte: chiamate con verbi proibiti,
  chiamate non autenticate, errori 403 — con label distinte
- [ ] Snyk test su Dockerfile e dipendenze: nessun `critical` o `high` con
  known exploit
- [ ] DAST con Nuclei sull'ambiente QA:
  ```bash
  docker run -i --rm projectdiscovery/nuclei:latest -u <URL-QA>
  ```
  (Falsi positivi accettabili sulle API: `cross-origin-*`, `content-security-policy`,
  `x-permitted-cross-domain-policies`)
- [ ] Secret scanner pulito:
  ```bash
  docker run -i --rm -v /var/run/docker.sock:/var/run/docker.sock \
    deepfenceio/deepfence_secret_scanner:2.0.0 -image-name <imgname>
  ```

## Production readiness (primo deploy di un nuovo servizio)

Per il primo deploy in produzione, oltre alla DoD standard:

- [ ] Build multipiattaforma CI: x86 e arm
- [ ] Policy cancellazione immagini non taggate abilitata in GitLab
- [ ] Docker healthcheck configurato (Traefik lo usa per il blue/green)
- [ ] Errori inviati a Sentry con ambiente (`production`/`qa`) e versione corretti
- [ ] Alert su Slack configurati: `#alerts` per critici, `#test` per warning
  (soglia: >5-10 errori/ora)
- [ ] Blue/Green deployment: Traefik con healthcheck abilitato

## Changelog

Ogni release include un changelog nella prospettiva di chi usa il software.

**Regole:**
- Scrivi dal punto di vista di chi beneficia della modifica (operatore, cittadino, admin)
- Non descrivere come hai risolto il problema, ma quale problema hai risolto
- Conciso: una riga per voce

| ❌ Non scrivere | ✅ Scrivere invece |
|-----------------|-------------------|
| `creare metodo POST /config/items` | `aggiunta la possibilità di configurare X per gli amministratori` |
| `Fix CSS per rendering anteprima` | `corretto errore di visualizzazione nell'anteprima dell'appuntamento` |
| `fare strip del carattere \n nel CSV` | `corretto errore 500 causato dal file CSV malformato` |

## Ambiente di QA — responsabilità del developer

Prima del giorno di test, il developer che ha sviluppato la feature deve:

1. Fare deploy della propria feature in QA
2. Preparare **tutte le condizioni necessarie per il test** (servizi, calendari,
   utenti, operatori, dati di esempio) — non delegare questa preparazione al tester
3. Verificare che `docker-compose up` nel repo funzioni senza istruzioni extra

I servizi in QA sono organizzati per aree (`pagamenti`, `protocolli`, `form.io`, ecc.).
Tenere l'ambiente pulito è responsabilità condivisa di tutto il team.
