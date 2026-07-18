---
name: opencity-platform-events
description: Use when producing or consuming Kafka events in any OpenCity product,
  defining a new event type, reviewing an event producer implementation, or documenting
  the event schema for a service. Covers CloudEvents envelope, header conventions,
  product slugs, and ce_type naming.
---

# OpenCity Platform Events — Formato standard Kafka

Tutti gli eventi Kafka prodotti dai prodotti OpenCity seguono il formato
[CloudEvents 1.0](https://cloudevents.io/) con binding Kafka: ogni attributo
CloudEvents è un **header** del messaggio Kafka, il **value** è il payload JSON
dell'applicativo.

## Header obbligatori

| Header | Valore | Note |
|--------|--------|------|
| `ce_specversion` | `1.0` | costante |
| `ce_id` | UUID v4 | generato al momento del produce |
| `ce_type` | `it.opencity.<product>.<domain>.<event>` | vedi convenzione sotto |
| `ce_source` | `urn:opencity:<product>:<tenant-uuid>` | UUID dal Tenant Manager |
| `ce_time` | ISO 8601 | momento del produce (non il timestamp semantico del payload) |
| `content-type` | `application/json` | costante |
| `oc_app_name` | es. `website-comuni` | variante specifica del prodotto che ha prodotto l'evento |
| `oc_app_version` | es. `1.5.1` | versione dell'applicativo — utile per debug e correlazione incidenti |

## Header opzionali

| Header | Valore | Note |
|--------|--------|------|
| `ce_dataschema` | `https://schemas.opencityitalia.it/<product>/<domain>/v<N>.json` | URI dello schema JSON del payload |

### Schema JSON — fortemente raccomandato

Ogni volta che si definisce un nuovo tipo di evento **pubblicare il JSON Schema**
corrispondente nel repo `opencity-labs/product`, che lo espone via GitLab Pages su
`schemas.opencityitalia.it`. Lo schema permette ai consumer di validare il payload
senza dipendenze dal codice del producer.

Regole di versioning:
- URL sempre versionato: `v1`, `v2`, ... — mai puntare a `main`
- Una versione già pubblicata in produzione **non si modifica**: aggiungere `v2`
- Breaking change (campo rimosso, tipo cambiato) → nuova major version

## Regole obbligatorie per il payload

Queste regole si applicano a **tutti** i campi del payload, sia in `entity.meta`
che in `entity.data`.

### Naming: snake_case

Tutti i nomi di campo devono essere in `snake_case`.

```json
// ✅ corretto
"published_at": "...",
"main_parent_remote_id": "..."

// ❌ sbagliato
"publishedAt": "...",
"MainParentRemoteId": "..."
```

### Date: ISO 8601 in UTC

Tutte le date devono essere stringhe ISO 8601 con timezone UTC esplicito (`Z`).

```json
// ✅ corretto
"published_at": "2026-03-31T14:00:00Z"

// ❌ sbagliato
"published_at": "2026-03-31 14:00:00",
"published_at": "2026-03-31T14:00:00+02:00"
```

### Valori assenti: null o campo omesso, mai stringa vuota

Se un campo non ha valore, si può ometterlo o impostarlo a `null`.
La stringa vuota `""` **non è mai un sostituto di "assente"**: va usata solo quando
il valore è effettivamente una stringa di lunghezza zero (es. testo lasciato vuoto
dall'utente).

```json
// ✅ corretto — omesso
{ "object_id": "42" }

// ✅ corretto — null esplicito
{ "object_id": "42", "remote_id": null }

// ❌ sbagliato — stringa vuota per dire "non c'è valore"
{ "object_id": "42", "remote_id": "" }
```

### Array e object vuoti: sempre presenti

Se un campo è di tipo array od object, deve comparire **sempre** nel payload,
anche quando è vuoto. Questo segnala esplicitamente ai consumer che il campo
è noto e il suo valore è "nessun elemento", non che il campo sia sconosciuto.

```json
// ✅ corretto
"languages": [],
"tree_placement": {}

// ❌ sbagliato — il consumer non sa se il campo è assente o vuoto
// (campo omesso quando è array/object)
```

## Struttura payload

Il payload contiene solo i dati dell'entità. I metadati dell'evento (id, tipo,
timestamp, produttore) stanno negli header CloudEvents — non vanno duplicati nel body.

```json
{
  "entity": {
    "meta": {
      "id": "<siteaccess>:<object_id>",
      "siteaccess": "<siteaccess>",
      "site_url": "https://...",
      "object_id": "...",
      "remote_id": "...",
      "type_id": "<entity-type>",
      "version": 1,
      "languages": ["it-IT"],
      "name": "...",
      "content_url": "https://...",
      "api_url": "https://...",
      "is_public": true,
      "tree_placement": {
        "main_parent_remote_id": "...",
        "parent_remote_ids": ["..."]
      },
      "published_at": "...",
      "updated_at": "...",
      "updated_by": "...",
      "published_by": "..."
    },
    "data": {
      "it-IT": { },
      "en-US": { }
    }
  }
}
```

`entity.meta.siteaccess` è il nome del siteaccess eZ Publish (identificativo interno
dell'istanza), distinto dal `tenant-uuid` in `ce_source` (identificativo nel Tenant Manager).
Entrambi sono utili: il siteaccess serve per costruire URL e identificare risorse
nell'applicativo, il Tenant Manager UUID serve per correlare eventi cross-prodotto.

## Convenzione `ce_type`

```
it.opencity.<product>.<domain>.<event>
```

`<domain>` e `<event>` sono definiti da ogni team per il proprio prodotto.
Usare nomi in inglese, sostantivo + participio passato.

### Slug per prodotto

| Prodotto | Slug |
|----------|------|
| OC Website | `website` |
| OC Booking | `booking` |
| OC Helpdesk | `helpdesk` |
| OC Identity | `identity` |
| OC Connect | `connect` |
| OC Docs | `docs` |
| OC AI | `ai` |
| OC Payments | `payments` |
| OC Satisfy | `satisfy` |
| OC Forms | `forms` |
| OC Agenda | `agenda` |
| OC Analytics | `analytics` |

Le varianti di prodotto (es. website-comune, website-asl, website-intranet) usano
tutte lo stesso slug — la variante è una configurazione del tenant, non un prodotto
diverso.

### Esempi `ce_type`

```
it.opencity.website.content.published
it.opencity.website.content.deleted
it.opencity.booking.appointment.created
it.opencity.helpdesk.ticket.opened
it.opencity.forms.submission.created
it.opencity.identity.user.registered
```

## Convenzione `ce_source`

```
urn:opencity:<product-slug>:<tenant-uuid>
```

Il `tenant-uuid` è l'UUID dell'istanza nel **Tenant Manager** — identifica
univocamente prodotto + organizzazione + istanza.

Una stessa organizzazione può avere più istanze dello stesso prodotto con UUID
distinti (es. sito pubblico, intranet, QA). I consumer che hanno bisogno di
raggruppare per organizzazione chiamano il Tenant Manager una volta e tengono
la risposta in cache.

## Convenzione `ce_time`

`ce_time` è il timestamp del **momento in cui l'evento è stato prodotto su Kafka**,
non il timestamp semantico del payload (es. data di pubblicazione del contenuto,
data dell'appuntamento). Usare il timestamp semantico come `ce_time` introdurrebbe
eventi fuori ordine per i consumer.

Il timestamp semantico resta nel payload nel campo specifico dell'applicativo.

## Generazione `ce_id`

UUID v4 tramite `random_bytes` — non usare `uniqid()` o timestamp.

**PHP 7.2:**
```php
$data = random_bytes(16);
$data[6] = chr(ord($data[6]) & 0x0f | 0x40); // version 4
$data[8] = chr(ord($data[8]) & 0x3f | 0x80); // variant RFC 4122
$uuid = vsprintf('%s%s-%s-%s-%s-%s%s%s', str_split(bin2hex($data), 4));
```

**Node.js (≥ 14.17):**
```js
import { randomUUID } from 'crypto';
const ceId = randomUUID();
```

## Struttura topic Kafka

I topic sono organizzati per **entità di dominio**, non per prodotto:

| Topic | Entità | Prodotti che scrivono |
|-------|--------|----------------------|
| `cms` | contenuti del sito | OC Website |
| `meetings` | appuntamenti e calendari | OC Booking |
| `applications` | pratiche | OC Forms |
| `users` | utenti | OC Identity |

Più prodotti possono scrivere sullo stesso topic. Usare `ce_type` e `ce_source`
per distinguere l'origine.

## Configurazione obbligatoria dei topic

Ogni topic in produzione deve essere creato con:

| Parametro | Valore raccomandato | Note |
|-----------|---------------------|------|
| `replication-factor` | 3 | Con 4 broker MSK: puoi perdere 1 broker senza bloccare la produzione |
| `min.insync.replicas` | 2 | Leader + almeno 1 follower devono aver scritto prima dell'ack |

**Come funziona `min.insync.replicas`:**
- `min.insync.replicas=2` = 2 repliche **totali** (leader + 1 follower), non "1+2=3"
- Con `replication-factor=3` e `min.insync.replicas=2` puoi perdere 1 broker e continuare a produrre
- Con `replication-factor=2` e `min.insync.replicas=2` non puoi perdere nessun broker

**Segnale di misconfiguration:** errore `Broker: Not enough in-sync replicas` → il topic
ha `replication-factor` inferiore a `min.insync.replicas`. Ricreare il topic con RF corretto.

## Implementazione producer robusta

Queste pratiche si applicano a qualsiasi producer Kafka, indipendentemente dal linguaggio.

### 1. Usare `acks=all`

Il producer deve aspettare che `min.insync.replicas` abbiano scritto prima di considerare
il messaggio consegnato. Qualsiasi valore inferiore (`acks=1`, `acks=0`) espone a perdita
di dati in caso di failover del broker leader.

### 2. Registrare sempre un delivery report callback

Le API Kafka producer sono **asincrone**: `produce()` accoda il messaggio localmente,
`flush()` attende che la coda si svuoti — ma "svuotata" non significa "consegnata con
successo". Gli errori di delivery (auth, topic inesistente, ISR insufficienti, timeout)
vengono notificati solo tramite callback. **Senza callback, i fallimenti sono silenziosi**
e il chiamante non sa se il messaggio è arrivato o no.

```python
# Python (confluent-kafka)
producer = Producer({
    'bootstrap.servers': brokers,
    'acks': 'all',
    'on_delivery': lambda err, msg: logger.error(f'Delivery failed: {err}') if err else None
})
```

```php
// PHP (php-rdkafka)
$conf->setDrMsgCb(function ($kafka, $message) {
    if ($message->err !== RD_KAFKA_RESP_ERR_NO_ERROR) {
        // loggare e propagare il fallimento
    }
});
```

```js
// Node.js (kafkajs)
await producer.send({ topic, messages });
// kafkajs è sincrono per design — send() risolve solo dopo l'ack del broker
```

```go
// Go (confluent-kafka-go)
p, _ := kafka.NewProducer(&kafka.ConfigMap{
    "bootstrap.servers": brokers,
    "acks":              "all",
})
// Il delivery channel è obbligatorio: senza, i fallimenti sono silenziosi
deliveryChan := make(chan kafka.Event, 1)
p.Produce(&kafka.Message{
    TopicPartition: kafka.TopicPartition{Topic: &topic, Partition: kafka.PartitionAny},
    Value:          payload,
}, deliveryChan)
e := <-deliveryChan
m := e.(*kafka.Message)
if m.TopicPartition.Error != nil {
    // loggare e propagare il fallimento
}
```

### 3. Rendere `acks` configurabile per ambiente

In sviluppo locale (Redpanda, topic a replica singola) `acks=all` fallisce sempre.
Esporre `acks` come variabile d'ambiente con default `all`:

```
KAFKA_ACKS=all          # produzione (default)
KAFKA_ACKS=1            # sviluppo locale con topic RF=1
```

## Configurazione consumer consigliata

```python
# Python (confluent-kafka) — pattern base
consumer = Consumer({
    'bootstrap.servers': brokers,
    'group.id': 'my-service-consumer-group',
    'auto.offset.reset': 'earliest',   # rilegge dall'inizio se il gruppo è nuovo
    'enable.auto.commit': False,        # commit manuale dopo processing confermato
})
consumer.subscribe(['cms'])

while True:
    msg = consumer.poll(timeout=1.0)
    if msg is None:
        continue
    if msg.error():
        logger.error(f'Consumer error: {msg.error()}')
        continue
    process(msg)
    consumer.commit(msg)  # commit solo dopo elaborazione riuscita
```

```go
// Go (confluent-kafka-go)
c, _ := kafka.NewConsumer(&kafka.ConfigMap{
    "bootstrap.servers":  brokers,
    "group.id":           "my-service-consumer-group",
    "auto.offset.reset":  "earliest",
    "enable.auto.commit": false,
})
c.Subscribe("cms", nil)
for {
    msg, err := c.ReadMessage(-1)
    if err != nil { continue }
    process(msg)
    c.CommitMessage(msg)
}
```

**Regole consumer:**
- Usare sempre `enable.auto.commit=false` + commit manuale: un crash prima del commit
  riprocessa il messaggio, non lo perde
- Il `group.id` deve essere univoco per servizio (non condividerlo tra servizi diversi)
- Usare `auto.offset.reset=earliest` per nuovi consumer group — in produzione decidere
  consapevolmente se rileggere i messaggi storici o partire dalla coda corrente

## Creazione topic — riferimento per 4 broker MSK

```bash
# Creare il topic con RF=3, min.insync.replicas=2
# (il --config sovrascrive il default MSK se diverso)
kafka-topics.sh --bootstrap-server $BROKERS --create \
  --topic cms \
  --partitions 6 \
  --replication-factor 3 \
  --config min.insync.replicas=2

# Verificare la configurazione
kafka-topics.sh --bootstrap-server $BROKERS --describe --topic cms
```

Con 4 broker e RF=3: ogni partizione ha 1 leader + 2 follower distribuiti su broker
distinti. Puoi perdere 1 broker qualsiasi senza bloccare producer né consumer.

Le partizioni si dimensionano in base al parallelismo atteso dei consumer:
`num_partitions >= num_consumer_instances_per_group`.

## AsyncAPI — file obbligatorio nel repo

Ogni servizio che produce o consuma eventi Kafka **deve avere un file `asyncapi.yml`
nella root del repo**. Il file descrive i canali, i messaggi e gli schemi in formato
[AsyncAPI 2.x](https://www.asyncapi.com/).

Struttura minima (AsyncAPI 3.0):

```yaml
asyncapi: "3.0.0"
info:
  title: OC Website Events
  version: "1.0.0"

channels:
  cms:
    address: cms
    messages:
      ContentPublished:
        $ref: "#/components/messages/ContentPublished"

operations:
  publishContent:
    action: send
    channel:
      $ref: "#/channels/cms"
    messages:
      - $ref: "#/channels/cms/messages/ContentPublished"

components:
  messages:
    ContentPublished:
      name: ContentPublished
      headers:
        properties:
          ce_type:
            const: it.opencity.website.content.published
          ce_source:
            example: "urn:opencity:website:550e8400-e29b-41d4-a716-446655440000"
      payload:
        $ref: "https://schemas.opencityitalia.it/website/content/v1.json"
```

Il file serve come contratto leggibile dai consumer e come sorgente per la generazione
di documentazione o stub. Committarlo nel repo è equivalente a firmare il contratto
con gli altri team.

## Responsabilità di ogni team

- Inserire `asyncapi.yml` nella root del repo prima del primo deploy in produzione
- Definire i propri `<domain>.<event>` e documentarli nel repo del servizio
- Configurare il `tenant-uuid` come variabile d'ambiente (non hardcoded)
- Non aggiungere attributi CloudEvents custom senza averli discussi con @lorello
- Se si pubblica uno schema, seguire il versioning (`v1`, `v2`, ...) e non modificare
  una versione già pubblicata in produzione
