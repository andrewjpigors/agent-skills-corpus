---
name: processi-aziendali
description: Use when classifying a work activity, task, GitLab issue, or time entry into Opencity Labs business processes. Triggers for questions like "where do I log this?", "which process?", "how do I categorize?", "which area?", or when filling a timesheet.
---

# Opencity Labs – Processi Aziendali

## Scopo

Elenco dei 14 processi aziendali di Opencity Labs con relative regole di classificazione per rendicontazione, timesheet, imputazione costi, planning.

## Processi e regole di classificazione

| Processo | Cosa include | Segnali chiave |
|---|---|---|
| **Gestione economico-finanziaria** | Bilancio, budget, fatturazione, ciclo attivo/passivo, controllo costi, ISO9001, rimborsi spese, acquisti, segreteria | Fatture, ordini, budget, rimborsi, fornitori, ISO9001 |
| **Gestione risorse umane** | Recruiting, onboarding, performance review, benessere, formazione interna, cultura aziendale, carichi di lavoro | Colloqui, review delle persone, retribuzioni, welfare |
| **Supporto e assistenza clienti** | Risposta ticket, helpdesk 1° e 2° livello, analisi problematiche su segnalazioni, call di supporto, knowledge base | Ticket Freshdesk, segnalazione cliente, bug report ricevuto da cliente, call di supporto |
| **Delivery** | Attivazione istanze, configurazione tenant in produzione, rilascio prodotti già costruiti senza personalizzazione | Creazione nuovo tenant/sito/area personale, go-live, configurazione standard |
| **Demand planning & QA** | Backlog grooming, stime, descrizione task, pianificazione quarter, SAL settimanali, sessioni di test a fine sprint, demo di verifica | Sprint planning, backlog, SAL, stima, QA, test session, demo |
| **Platform** | Manutenzione componenti applicativi, deploy, infrastruttura cloud, sicurezza, GDPR, ISO27001, ACN, ottimizzazione costi AWS | Issue non legate a epiche di prodotto, infra AWS, Docker Swarm, Traefik, monitoring, CVE, certificazioni |
| **Vendite** | Acquisizione nuovi clienti, offerte, listini reseller, trattative commerciali | Offerte, gare, prospect, reseller, nuovi contratti |
| **Accounting** | Gestione clienti chiave esistenti, upselling, consulenza strategica, accompagnamento partner (Clesius, Geopartner, e-fil, Maggioli, AS, Municipia…) | Partner tecnici, clienti chiave, upselling, affiancamento |
| **Progettazione e sviluppo del prodotto** | Ideazione, design, sviluppo nuove funzioni o evoluzioni significative di funzioni esistenti legate a epiche di prodotto | Epica, nuova funzionalità, frontend/backend/API su roadmap prodotto, POC |
| **Integrazioni** | Nuove integrazioni con piattaforme abilitanti (PDND, IO, pagamenti, protocolli), documentazione, use case | PDND, pagoPA, IO, protocollo, nuovo connettore |
| **Soluzioni custom** | Personalizzazioni per singolo cliente, componenti ad hoc, migrazioni contenuti, integrazioni custom | Custom, ad hoc, migrazione contenuti, cliente specifico |
| **Ricerca e innovazione** | Studio nuove tecnologie, trend, blockchain, AI, POC esplorativi, progetti EU | AI, blockchain, POC esplorativo, ricerca, innovazione, progetto EU |
| **Formazione a partner ed a clienti** | Corsi, materiali e-learning, sessioni formative per clienti/partner | Corso, formazione, e-learning, sessione formativa esterna |
| **Marketing** | Eventi, campagne comunicazione, analisi competitiva, monitoraggio mercato | Evento, comunicato, social, competitor, campagna |

## Casi ambigui – regole di precedenza

- **Ticket cliente → analisi interna**: fino a quando si analizza e si pianifica la fix va su **Supporto e assistenza clienti**; dal momento in cui si apre la issue GitLab e si pianifica lo sviluppo va su **Platform** (se manutenzione) o **Progettazione e sviluppo del prodotto** (se nuova funzione da roadmap).
- **Test**: se è sessione di QA a fine sprint → **Demand planning & QA**. Se è test di una fix su segnalazione cliente → **Supporto e assistenza clienti**.
- **Deploy**: se è rilascio di prodotto già costruito senza personalizzazioni → **Delivery**. Se è deploy di una nuova versione con fix o evoluzioni → **Platform**.
- **Meeting con cliente**: se si concordano specifiche di sviluppo o si fa demo di verifica → **Demand planning & QA**. Se è supporto post-vendita o problema → **Supporto e assistenza clienti**. Se è upselling o gestione relazione cliente chiave → **Accounting**.
- **Partner tecnici (Clesius, Geopartner, Maggioli…)**: accompagnamento e consulenza → **Accounting**. Sviluppo integrazioni con loro sistemi → **Integrazioni**.
- **Sicurezza**: patch, CVE, hardening → **Platform**. ISO27001, GDPR, adempimenti → **Platform**.

## Output atteso

Per ogni attività descritta, rispondi con:
1. **Processo**: nome esatto del processo
2. **Motivazione**: 1 frase secca che spiega perché
3. **Dubbio** (solo se ambiguo): alternativa plausibile e criterio per scegliere

Se ti vengono passate più attività in lista, restituisci una tabella con colonne: Attività | Processo | Note.
