---
name: feature-flags
description: Use when creating a feature flag, integrating GrowthBook SDK, choosing
  flag type, defining targeting attributes, or reviewing code that uses feature flags.
---

# Feature Flags — Opencity Labs

Opencity Labs usa [GrowthBook](https://www.growthbook.io) per gestire i feature flag.

## Prerequisiti e accesso

- Se non hai accesso a GrowthBook, chiedi a **Team Ops**
- Prima di integrare l'SDK, crea una **SDK key dedicata** in GrowthBook per il tuo progetto
- Una SDK key deve essere usata da **un solo progetto** — mai condivisa tra servizi diversi
- La SDK key va salvata come variabile d'ambiente `GROWTHBOOK_SDK_KEY` e documentata nel README
- Ogni applicativo **deve sempre implementare** il flag `is_in_maintenance` di tipo Kill switch —
  è obbligatorio. È l'unica eccezione alla regola del prefisso di dominio: è globale e
  trasversale a tutti i prodotti

## Tipi di flag

| Tipo | Quando usarlo |
|------|---------------|
| **Release** | Rollout graduale di una nuova feature tecnica — si rimuove quando il rollout è completato |
| **Operational** | Comportamento configurabile a runtime (es. timeout, batch size) — può restare permanente |
| **Entitlement** | Diritto commerciale per piano/tenant — valore booleano (feature on/off) o numerico (quota/limite). Può restare permanente. **Se copre operazioni esposte via API, l'enforcement è sempre server-side**: il flag configura il valore, il backend lo applica. |
| **Kill switch** | Interruttore di emergenza per disabilitare l'applicativo (es. manutenzione) — **permanente**, non si rimuove |

### Esempi Entitlement

| Flag | Valore | Semantica |
|------|--------|-----------|
| `payment_bulk_import_enabled` | `bool` | Tenant può usare import massivo pagamenti |
| `payment_bulk_import_daily_limit` | `int` | Max pagamenti importabili al giorno (es. `1000`) |
| `forms_max_published` | `int` | Max form pubblicabili contemporaneamente |
| `sensor_realtime_enabled` | `bool` | Tenant ha accesso ai dati realtime |

I flag numerici **non enforceano da soli**: il backend legge il valore da GrowthBook, lo confronta
con il contatore corrente e rifiuta con HTTP 429 se il limite è raggiunto. GrowthBook è la sorgente
del valore configurabile per piano/tenant, non il punto di enforcement.

### Esempi Kill switch

| Flag | Scenario | Risposta |
|------|----------|----------|
| `is_in_maintenance` | Manutenzione globale pianificata o emergenza totale | HTTP 503 su tutto il servizio |
| `payment_circuit_breaker` | Provider pagamenti down o comportamento anomalo | Disabilita operazioni pagamento, mostra messaggio |
| `sensor_ingestion_halted` | Disco pieno, migrazione in corso, backend sovraccarico | Stop ricezione dati sensori |
| `forms_read_only` | Migrazione DB, intervento su dati critici | Form visibili ma non inviabili |

Pattern comune: evento esterno improvviso che richiede disabilitare un sottosistema **senza deploy**,
tempo di reazione sotto il minuto. `is_in_maintenance` è globale (nessun prefisso); tutti gli altri
Kill switch sono domain-scoped e seguono il naming standard.

## Come scegliere il tipo

```
Cosa rappresenta la regola?
│
├─ "chi è il chiamante / da dove viene?"
│   (identità, ruolo, IP, attributo utente, claim JWT)
│   └─ Chi può cambiarla?
│       ├─ Un admin dell'ente → PERMISSION
│       └─ Solo Opencity Labs → ENTITLEMENT FLAG
│
├─ "cosa ha contrattualizzato il tenant?"
│   (piano, quota, limite numerico — solo Opencity decide)
│   → ENTITLEMENT FLAG (bool o int)
│
├─ "questa feature è pronta per tutti?"
│   (rollout graduale, A/B, dark launch)
│   → RELEASE FLAG — rimuovi dopo rollout completo
│
├─ "voglio cambiare un parametro tecnico senza deploy?"
│   (timeout, batch size, soglie interne)
│   → OPERATIONAL FLAG
│
└─ "voglio poter spegnere un sottosistema in emergenza?"
    → KILL SWITCH — permanente, non rimuovere
```

**Test rapido se ancora in dubbio:**

| Domanda | Risposta → tipo |
|---------|-----------------|
| Se bypassato è un security incident? | Sì → Permission |
| Chi approva il cambio? Security/compliance → Permission; Product/ops → Feature flag |
| Il valore cambia per tenant/piano? | Sì → Entitlement |
| È temporaneo per design? | Sì → Release |

## Naming convention

Formato obbligatorio: `{dominio}_{nome_flag}` in snake_case.

Il dominio corrisponde al nome del prodotto/modulo (es. `payment`, `forms`, `sensor`, `login`).

```
payment_new_checkout_flow
forms_auto_save
login_social_providers
```

Uniche eccezioni: 
- `is_in_maintenance`
- `debug`, da usare per mostrare informazioni utili di natura tecnica

che non hanno prefisso (sono globali).

## Ciclo di vita

### Creazione

1. Scegli il tipo di flag prima di crearlo in GrowthBook
2. Aggiungi in GrowthBook una descrizione con: scopo, owner, data di scadenza prevista
   (obbligatoria per i flag Release)
3. Aggiungi `GROWTHBOOK_SDK_KEY` come variabile d'ambiente nel README (tutti i tipi)
4. Aggiungi il flag come variabile d'ambiente documentata solo se è di tipo Operational

### Verifica integrazione SDK

Dopo aver integrato l'SDK nell'applicativo, apri la UI di GrowthBook e verifica che:
- ci sia la **spunta verde** sulla connessione tra l'applicativo e il proxy GrowthBook
- ci sia la **spunta verde** tra proxy e server GrowthBook

Se una delle due spunte manca, l'SDK non è correttamente configurata — non procedere
con il rollout finché entrambe sono verdi.

### Rollout

- Inizia con un subset (es. un tenant interno) prima di aprire al 100%
- I flag Release non devono restare aperti oltre il ciclo di release in cui sono stati introdotti

### Rimozione (regola anti-zombie)

- Flag **Release**: rimuovi dal codice entro la release successiva al rollout completo
- Flag **Kill switch**: **non rimuovere** — sono permanenti per design (es. `is_in_maintenance`)
- Mai lasciare flag senza owner in GrowthBook; i flag Release devono avere anche una data di scadenza

## Attributi di targeting

Questi attributi vanno passati all'SDK GrowthBook al momento dell'inizializzazione.
Passa **sempre** almeno `tenant_id` e `app_name`.
Aggiungi gli altri in base al contesto (es. `user_id` se l'utente è autenticato).

Gli attributi marcati con ✓ nella colonna *Identifier* sono quelli usati per lo split
degli esperimenti — usali con coerenza.

| Attributo | Tipo | Descrizione | Identifier |
|-----------|------|-------------|:----------:|
| `id` | string | ID generico | ✓ |
| `url` | string | URL corrente | |
| `path` | string | Path corrente | |
| `host` | string | Host | |
| `query` | string | Query string | |
| `device_type` | enum: `desktop`, `mobile` | Tipo dispositivo | |
| `browser` | enum: `chrome` `edge` `firefox` `safari` `unknown` | Browser | |
| `utm_source` | string | Sorgente UTM | |
| `utm_medium` | string | Mezzo UTM | |
| `utm_campaign` | string | Campagna UTM | |
| `utm_term` | string | Termine UTM | |
| `utm_content` | string | Contenuto UTM | |
| `app_name` | string | Slug applicativo — deve corrispondere a un asset censito nell'**Assets Sheet** (chiedi a Team Ops se non lo trovi) | |
| `tenant_id` | string | UUID del tenant — deve corrispondere all'UUID nel **registro dei tenant** | ✓ |
| `tenant_name` | string | Slug del tenant (es. `comune-di-roma`) | |
| `user_id` | string | ID dell'utente dal sistema di autenticazione interno della piattaforma (non il codice fiscale né lo SPID code) | ✓ |
| `customer_id` | string | Identificativo del cliente (Ente) | ✓ |
| `external_id` | string | ID sistema esterno | ✓ |
| `ip` | string | IP del client | |

> `plan_name` non è ancora in uso — verrà introdotto in futuro.

## Integrazione SDK

### Endpoint

| Endpoint | URL | Chi usa |
|----------|-----|---------|
| **Proxy** | `https://growthbook-proxy.opencityitalia.it` | Applicativi (SDK) |
| **Server** | `https://growthbook.opencityitalia.it` | Solo UI/admin |

Gli applicativi devono puntare **sempre al proxy**, non al server diretto.
Nello snippet SDK, configura `apiHost` (o equivalente) con l'URL del proxy.

### Come ottenere il codice di integrazione

GrowthBook genera automaticamente lo snippet di integrazione aggiornato per il tuo linguaggio.
**Non copiare snippet da fonti esterne** — usa sempre quello fornito da GrowthBook:

1. Entra in GrowthBook → **SDK Connections**
2. Seleziona o crea la tua SDK key
3. GrowthBook mostra il codice di inizializzazione aggiornato per Go, React, Python, JS, PHP e altri
4. Copia da lì — è sempre allineato alla versione corrente dell'SDK

### Cosa aggiungere agli attributi di targeting

Nello snippet generato da GrowthBook, aggiungi gli attributi della sezione precedente.
Passa **sempre** almeno `tenant_id` e `app_name`; aggiungi gli altri in base al contesto:

```
app_name  → slug dell'applicativo (dall'Assets Sheet)
tenant_id → UUID dal registro dei tenant
user_id   → ID dal sistema auth interno (solo se utente autenticato)
```

### Kill switch obbligatorio

Dopo l'inizializzazione, ogni applicativo **deve** controllare `is_in_maintenance`
e bloccare il servizio se attivo. GrowthBook mostra come leggere un flag nello snippet —
applica lo stesso pattern a `is_in_maintenance` restituendo HTTP 503 (o equivalente).
