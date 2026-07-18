---
name: dm-architecture
description: "Architecture documentation skill combining C4 model ASCII diagrams with the 7 Fragen pro Vorhaben framework. Primary diagram types: Extended System Context Diagram (with team boundaries, system status, data stores, actors on sides) and Dynamic Diagram (numbered temporal interaction flows). For every architecture initiative, the skill systematically guides through seven key questions (Systemkontext, Security-Anbindung, Deployment-Modell, Datenresidenz & Datenschutz, SLA-Anforderungen, Technische Projektabhängigkeiten, Lösungsvarianten). Triggers include 'architecture diagram', 'C4 diagram', 'system context', 'container diagram', 'component diagram', 'deployment diagram', 'dynamic diagram', 'Systemlandschaft', 'Bebauungsplan', 'interface communication', 'Schnittstellenkommunikation', 'request flow', 'sequence', 'interaction', 'document architecture', 'visualize architecture', 'team boundaries', 'Verantwortungsbereiche', '7 Fragen', 'Architektur-Vorhaben', 'Architektur-Dokumentation', 'Architektur Rahmenbedingungen'. Target audience: Enterprise Architects, Integration Architects, Solution Architects."
---

# DM Architecture Documentation

Architecture documentation combining C4 model diagrams (ASCII notation) with the
**7 Fragen pro Vorhaben** framework to ensure every initiative is systematically
documented — technically (diagrams) and organisatorisch (Rahmenbedingungen).

---

## MANDATORY: Entry-Point Dialog (immer zuerst ausführen!)

**Bevor irgendeine Aktion gestartet wird**, MUSS der User gefragt werden, welchen
Modus er nutzen möchte. Zeige exakt folgende Auswahl an:

> **Welche Architektur-Aktivität möchtest du durchführen?**
>
> 1. **C4 System Context Diagram** — Erstellt ein erweitertes System-Kontext-Diagramm
>    (Akteure, Systeme, Schnittstellen, Team-Boundaries, Datenhaltung)
> 2. **C4 Dynamic Diagram** — Erstellt ein dynamisches Diagramm für einen konkreten
>    Anwendungsfall (nummerierte Interaktionsschritte, zeitlicher Ablauf)
> 3. **7 Fragen pro Vorhaben** — Systematische Klärung der Rahmenbedingungen
>    (Systemkontext, Security, Deployment, Datenschutz, SLAs, Abhängigkeiten, Lösungsvarianten)
>
> Bitte wähle **1**, **2** oder **3** (oder eine Kombination, z. B. „1 und 3").

### Regeln für den Entry-Point Dialog

- **Niemals überspringen.** Auch wenn der User-Prompt bereits einen Hinweis enthält
  (z. B. „erstelle ein C4 Diagramm"), IMMER zuerst die Auswahl zeigen und bestätigen lassen.
- **Erst nach Auswahl** den passenden Workflow-Abschnitt ausführen.
- **Kombination erlaubt.** Der User kann z. B. „1 und 3" wählen — dann nacheinander abarbeiten.

### Workflow nach Auswahl

| Auswahl | Workflow |
|---------|----------|
| **1 — System Context** | → Abschnitt „System Context — Interactive Dialog" (Step 1–5) ausführen |
| **2 — Dynamic Diagram** | → Abschnitt „Dynamic Diagram — Interactive Dialog" (Step 1–6) ausführen |
| **3 — 7 Fragen** | → Abschnitt „Interaktiver Dialog für die 7 Fragen" ausführen |

### Follow-Up nach Abschluss (immer anbieten!)

Nach Abschluss jeder Aktivität MUSS dem User eine passende Weiterführung angeboten werden.
Zeige kontextabhängig folgende Optionen:

**Nach einem System Context Diagram (1):**
> Nächste Schritte:
> - **A)** Für einen konkreten Anwendungsfall ein **Dynamic Diagram** erstellen (zeigt den zeitlichen Ablauf der Kommunikation)
> - **B)** Die **7 Fragen pro Vorhaben** systematisch durchgehen (Rahmenbedingungen klären)
> - **C)** Ein **Container Diagram** (Level 2) für ein bestimmtes System erstellen
> - **D)** Das Diagramm als **Markdown-Datei** speichern

**Nach einem Dynamic Diagram (2):**
> Nächste Schritte:
> - **A)** Ein weiteres **Dynamic Diagram** für einen anderen Anwendungsfall erstellen
> - **B)** Das zugehörige **System Context Diagram** erstellen oder aktualisieren
> - **C)** Die **7 Fragen pro Vorhaben** systematisch durchgehen
> - **D)** **Fehlerfälle / alternative Pfade** im Diagramm ergänzen
> - **E)** Das Diagramm als **Markdown-Datei** speichern

**Nach den 7 Fragen (3):**
> Nächste Schritte:
> - **A)** Auf Basis der Antworten ein **System Context Diagram** erstellen
> - **B)** Für einen kritischen Ablauf ein **Dynamic Diagram** erstellen
> - **C)** Offene Punkte als **ADR (Architecture Decision Record)** dokumentieren
> - **D)** Die Ergebnisse als **kompakte Übersichtstabelle** zusammenfassen
> - **E)** Die Ergebnisse als **Markdown-Datei** speichern

---

## Die 7 Fragen pro Vorhaben

Nicht alles muss sofort beantwortet werden — aber jede Frage sollte bewusst
gestellt und das Ergebnis (auch „noch unklar") festgehalten werden.

### F1 — Systemkontext

*Wer ist beteiligt und wie hängt alles zusammen?*

Diese Frage wird direkt durch das **System Context Diagram** beantwortet.

| Frage | Erläuterung |
|---|---|
| Welche **Benutzergruppen** gibt es? | Name, Rolle, ungefähre Anzahl |
| Welche **Systeme** sind beteiligt? | Bestehend oder neu? Welches Team verantwortet es? |
| Welche **Schnittstellen** bestehen? | Protokoll, Datenformat (JSON, XML, TIFF, …), Richtung |

### F2 — Security-Anbindung

*Wie wird sichergestellt, dass nur Berechtigte zugreifen können?*

| Frage | Erläuterung |
|---|---|
| Wie **authentifizieren** sich Benutzer? | z. B. Single Sign-On (SSO), Firmen-Login (AD/LDAP), Zwei-Faktor (MFA) |
| Wie werden **API-Aufrufe** zwischen Systemen abgesichert? | z. B. OAuth2-Token, Zertifikate (mTLS), API-Schlüssel |
| Gibt es **Netzwerk-Zonen**? | z. B. separates Netz für interne Systeme, Firewall-Regeln |

### F3 — Deployment-Modell

*Wo und wie laufen die Systeme?*

| Frage | Erläuterung |
|---|---|
| Läuft das System **On-Premise**, in der **Cloud** oder **beides**? | Beeinflusst Kosten, Security und Betriebsmodell |
| Welche **Umgebungen** gibt es? | Typisch: Entwicklung (DEV), Test (TEST), Produktion (PROD) |
| Wird eine **Container-Strategie** eingesetzt? | z. B. Docker, Kubernetes — oder klassische VM/Server? |

### F4 — Datenresidenz & Datenschutz

*Wo liegen die Daten und gelten besondere Schutzanforderungen?*

| Frage | Erläuterung |
|---|---|
| In welchem **Land / welcher Region** werden Daten gespeichert? | Relevant für DSGVO und Unternehmensrichtlinien |
| Werden **personenbezogene Daten** verarbeitet? | Falls ja: Datenschutz-Folgenabschätzung prüfen |
| Gibt es **DSGVO-Auflagen**? | z. B. Auftragsverarbeitungsvertrag (AVV), Löschkonzept |

### F5 — SLA-Anforderungen

*Wie zuverlässig und schnell muss das System sein?*

| Frage | Erläuterung |
|---|---|
| Welche **Verfügbarkeit** wird erwartet? | z. B. 99,5% = max. ~1,8 Tage Ausfall/Jahr |
| Zu welchen **Zeiten** muss das System laufen? | 24/7, Bürozeiten (Mo–Fr 8–17), Schichtbetrieb? |
| Wie schnell muss das System **antworten**? | z. B. „Zeichnung muss in unter 3 Sekunden laden" |

### F6 — Technische Projektabhängigkeiten

*Welche anderen Projekte beeinflussen dieses Vorhaben?*

| Frage | Erläuterung |
|---|---|
| Gibt es **laufende oder geplante Projekte**, die Auswirkungen haben? | z. B. ERP-Migration, Cloud-Umzug, Ablösung eines Altsystems |
| Welches Projekt muss **zuerst fertig** sein? | Zeitliche Abhängigkeiten erkennen (Critical Path) |
| Welche **anderen Teams** müssen eingebunden werden? | Kapazitäten und Zuständigkeiten frühzeitig klären |

### F7 — Lösungsvarianten / Systemevaluation

*Gibt es mehrere Optionen — und wie entscheiden wir?*

| Frage | Erläuterung |
|---|---|
| Welche **Lösungsvarianten** stehen zur Auswahl? | z. B. Eigenentwicklung vs. Zukauf, Produkt A vs. Produkt B |
| Nach welchen **Kriterien** wird bewertet? | Funktionalität, Kosten, Integrierbarkeit, Wartbarkeit |
| Ist die **Entscheidung dokumentiert**? | → Als ADR (Architecture Decision Record) festhalten |

### Vorgehen in vier Schritten

| Schritt | Was tun | Ergebnis |
|---|---|---|
| **1** | System Context Diagram erstellen | Überblick: Akteure, Systeme, Schnittstellen, Teams (beantwortet F1 + F6) |
| **2** | Für kritische Abläufe je ein Dynamic Diagram erstellen | Detail-Verständnis der Schnittstellenkommunikation |
| **3** | Fragen F2–F5 beantworten (auch stichwortartig reicht) | Rahmenbedingungen sind dokumentiert |
| **4** | Bei Neuanschaffungen: Variantenvergleich durchführen | Nachvollziehbare Entscheidung als ADR (F7) |

> **Wichtig:** Nicht alles muss perfekt sein. Ein Diagramm auf dem
> Whiteboard und drei Sätze pro Frage sind besser als gar keine Dokumentation.

### Interaktiver Dialog für die 7 Fragen

Wenn ein neues Vorhaben dokumentiert wird, folge diesem Ablauf:

1. **Frage nach Projektname und -ziel** — „Um welches Vorhaben geht es? Was ist das Ziel?"
2. **Durchlaufe F1–F7 systematisch** — Stelle die Fragen in der Reihenfolge. Halte Antworten fest.
3. **Kennzeichne offene Punkte** — Wenn eine Frage nicht beantwortet werden kann, notiere „[offen]" und schlage vor, wer die Antwort liefern könnte.
4. **Erstelle parallel das System Context Diagram** — F1 liefert die Grundlage für das Diagramm.
5. **Fasse zusammen** — Am Ende eine kompakte Übersicht der 7 Fragen mit Status (beantwortet / offen).

Nach Abschluss der 7 Fragen → **Follow-Up nach Abschluss** (siehe Entry-Point Dialog oben, Abschnitt "Nach den 7 Fragen") anbieten.

## C4 Diagram Levels

Select the appropriate level based on the documentation need:

| Level | Diagram Type | Audience | Shows | When to Create |
|-------|-------------|----------|-------|----------------|
| 1 | **System Context (Extended)** | Everyone | System + external actors, team boundaries, system status (existing/new), data stores, interfaces | Always (required — "Pflichtdiagramm") |
| 2 | **Container** | Technical | Apps, databases, services | Optional — when deeper technical detail is needed |
| 3 | **Component** | Developers | Internal components | Optional — only if adds value |
| 4 | **Deployment** | DevOps | Infrastructure nodes | Optional — for production systems |
| - | **Dynamic** | Integration/Solution Architects | Request flows (numbered, temporal) | For interface communication & complex workflows (second required diagram type) |

**Key Insight:** "Context + Dynamic diagrams are the two primary diagram types." The System Context Diagram (extended with team boundaries, system status, data stores) provides the landscape overview. Dynamic Diagrams detail the temporal interaction for specific use cases. Only create Container/Component/Deployment diagrams when they genuinely add value beyond these two.

---

## ASCII Notation Reference

### Element Types

```
Akteur (Person):         ┌──────────────────────┐
                         │  ☺ Name              │
                         │  [Rolle/Beschreibung]│
                         └──────────────────────┘

Zentrales System:        ╔══════════════════════╗
                         ║  <<system>>          ║
                         ║  Systemname          ║
                         ║  [Kurzbeschreibung]  ║
                         ╚══════════════════════╝

Internes System:         ┌──────────────────────┐
                         │  <<system>>          │
                         │  Systemname          │
                         │  [Beschreibung]      │
                         └──────────────────────┘

Externes System:         ┌ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─┐
                         │  <<external system>>  │
                         │  Systemname           │
                         │  [Beschreibung]       │
                         └ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─┘

Container:               ┌──────────────────────┐
                         │  <<container>>       │
                         │  Name                │
                         │  [Technologie]       │
                         │  Beschreibung        │
                         └──────────────────────┘

Container (Datenbank):   ┌──────────────────────┐
                         │  <<database>>        │
                         │  Name                │
                         │  [Technologie]       │
                         │  Beschreibung        │
                         └──────────────────────┘

Container (Queue):       ┌──────────────────────┐
                         │  <<queue>>           │
                         │  Name                │
                         │  [Technologie]       │
                         │  Beschreibung        │
                         └──────────────────────┘

Component:               ┌──────────────────────┐
                         │  <<component>>       │
                         │  Name                │
                         │  [Technologie]       │
                         │  Beschreibung        │
                         └──────────────────────┘
```

### System Status

```
Bestehendes System:      ┌──────────────────────┐
(bestehend)              │  <<system>>          │
                         │  Systemname          │
                         │  [bestehend]         │
                         └──────────────────────┘

Neues System/Komponente: ┌══════════════════════┐
(neu)                    │  <<system/new>>      │
                         │  Systemname          │
                         │  [neu]               │
                         └══════════════════════┘

Datenhaltung:            ╭──────────────────────╮
(Zylinder/Data Store)    │  <<data>>            │
                         │  TIFF, PDF           │
                         ╰──────────────────────╯
```

### Team / Verantwortungsbereich (Responsibility Boundary)

```
Team Boundary:           ┌ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─┐
(gestrichelt)            │  Team-Name                       │
                         │                                  │
                         │  ┌────────┐    ╭──────────╮     │
                         │  │ System │    │  Daten   │     │
                         │  └────────┘    ╰──────────╯     │
                         │                                  │
                         └ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─┘
```

### Relationships

```
Synchron:                ────── Beschreibung ──────→
                                [Protokoll]

Asynchron:               ─ ─ ─  Beschreibung  ─ ─ ─→
                                [Protokoll]

Bidirektional:           ←───── Beschreibung ─────→
                                [Protokoll]

Synchrone Antwort:       ←───── Antwort ──────────
                                [Protokoll]

Asynchrone Antwort:      ←─ ─ ─ Antwort ─ ─ ─ ─ ─
                                [Protokoll]
```

### Boundaries

```
System Boundary:         ┌─────────────────────────────┐
                         │  [System Name]               │
                         │  ┌────────┐  ┌────────┐     │
                         │  │ Elem A │  │ Elem B │     │
                         │  └────────┘  └────────┘     │
                         └─────────────────────────────┘

Trust Boundary:          ┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄
                         ┊  Boundary Name              ┊
                         ┊  ...Elemente...              ┊
                         ┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄

Enterprise Boundary:     ╔═════════════════════════════╗
                         ║  Enterprise Name             ║
                         ║  ┌────────┐  ┌────────┐     ║
                         ║  │ Sys A  │  │ Sys B  │     ║
                         ║  └────────┘  └────────┘     ║
                         ╚═════════════════════════════╝
```

### Deployment Nodes

```
Deployment Node:         ╭─────────────────────────────╮
                         │  <<node>>                    │
                         │  Name [Type]                 │
                         │  ┌────────┐  ┌────────┐     │
                         │  │ Cont A │  │ Cont B │     │
                         │  └────────┘  └────────┘     │
                         ╰─────────────────────────────╯
```

---

## Quick Start Examples

### System Context Diagram — Extended (Level 1, Pflichtdiagramm)

The System Context Diagram is the **mandatory diagram for every initiative**. It shows
users, systems (existing/new/external), interfaces, team boundaries, and data stores
on a single page — like a "Landkarte" (map) of the system landscape.

#### Example: IFS – Konverter – Siemens TeamCenter

```
  ☺ Benutzer                                                                        ☺ Techniker
  (~2500)                                                                           (600 Benutzer)
    │                                                                                    │
    │ Zeichnung                                                                          │ Zeichnung
    │ anzeigen                                                                           │ bearbeiten
    │                                                                                    │
    │   ┌ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─┐   ┌ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─┐  │
    │   │  ERP Team                            │   │  Engineering/CAD                  │  │
    │   │                                      │   │                                   │  │
    ├ ─ ─ ─ ─ ─ ─→  ┌──────────────────────┐  │   │  ┌══════════════════════┐         │  │
    │   │            │  <<system>>          │  │   │  │  <<system/new>>     │         │  │
    │   │            │  IFS                 │──┼─REST API──→│  Konverter         │         │  │
    │   │            │  [bestehend]         │  │   │  │  [neu]              │         │  │
    │   │            └──────────┬───────────┘  │   │  └══════════╤═════════╝         │  │
    │   │                      │               │   │             │                    │  │
    │   │            ╭─────────┴──────────╮    │   │             │  REST API          │  │
    │   │            │  <<data>>          │    │   │             │                    │  │
    │   │            │  TIFF, PDF         │    │   │             ▼                    │  │
    │   │            ╰────────────────────╯    │   │  ┌──────────────────────┐        │ ←┤
    │   │                                      │   │  │  <<system>>          │        │  │
    │   │                                      │   │  │  Siemens TeamCenter  │ ← ─ ─ ─ ─┤
    │   │                                      │   │  │  [bestehend]         │        │  │
    │   │                                      │   │  └──────────┬───────────┘        │  │
    │   │                                      │   │             │                    │  │
    │   │                                      │   │  ╭─────────┴──────────╮         │  │
    │   │                                      │   │  │  <<data>>          │         │  │
    │   │                                      │   │  │  DXF, DWG          │         │  │
    │   │                                      │   │  ╰────────────────────╯         │  │
    │   │                                      │   │                                   │  │
    │   └ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─┘   └ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─┘  │

  ╔═══════════════════════════════════════════════════════════════════════════════════════╗
  ║  LEGENDE                                                                            ║
  ╠═══════════════════════════════════════════════════════════════════════════════════════╣
  ║  ☺            = Benutzergruppe (Grösse)                                             ║
  ║  ─ ─ ─→      = Interaktion (Benutzer → System)                                     ║
  ║  ┌──────┐     = System / Komponente bestehend                                       ║
  ║  ┌══════┐     = System / Komponente neu                                             ║
  ║  ┌ ─ ─ ─┐    = Verantwortungsbereich (Team)                                        ║
  ║  ─────→      = Technische Schnittstelle (Protokoll auf Pfeil)                       ║
  ║  ╭──────╮     = Daten (Formate / Speicher)                                          ║
  ╚═══════════════════════════════════════════════════════════════════════════════════════╝
```

#### System Context — Interactive Dialog

When creating a System Context Diagram, follow this structured process:

**Step 1: Identify Scope**
Ask:
- Which **systems** are involved? (list all)
- Which **teams** own which systems?
- Are there **new systems/components** being introduced?

**Step 2: Identify Actors**
Ask:
- Which **user groups** interact with the landscape? (name + approximate count)
- Which user group interacts with which system? (entry/exit points)

**Step 3: Identify Interfaces**
Ask:
- How do the systems communicate? (REST API, SOAP, MQ, SFTP, etc.)
- What is the **direction of data flow**? (which system initiates?)
- Are calls synchronous or asynchronous?

**Step 4: Identify Data Stores**
Ask:
- Which **data formats** does each system handle? (TIFF, PDF, DXF, DWG, JSON, XML, ...)
- Are there shared databases or is data replicated?

**Step 5: Generate Diagram**
Apply these layout rules:
1. **Actors on left/right edges** (triggering actor left, consuming actor right)
2. **Systems horizontally** between actors, grouped by team boundaries
3. **Data stores below** their owning system
4. **Interfaces labeled** with protocol on the connecting arrows
5. **System status** indicated: `[bestehend]` (existing) or `[neu]` (new)
6. **Legend at the bottom** explaining all symbols

Nach Abschluss des System Context Diagrams → **Follow-Up nach Abschluss** (siehe Entry-Point Dialog oben, Abschnitt "Nach einem System Context Diagram") anbieten.

### Container Diagram (Level 2)

```
              ┌──────────────────┐
              │  ☺ User          │
              │  [Tracks         │
              │   workouts]      │
              └────────┬─────────┘
                       │
             Uses ─────┘
             [HTTPS]
                       │
                       ▼
  ┌─────────────────────────────────────────────────┐
  │  [Workout Tracker PWA]                          │
  │                                                 │
  │  ┌──────────────────┐   ┌──────────────────┐   │
  │  │  <<container>>   │   │  <<container>>   │   │
  │  │  SPA             │──→│  State Mgmt      │   │
  │  │  [Vue 3, TS]     │   │  [Pinia]         │   │
  │  │  Single-page app │   │  App state       │   │
  │  └──────────────────┘   └────────┬─────────┘   │
  │                                  │              │
  │                        Persists ─┘              │
  │                        [Dexie ORM]              │
  │                                  │              │
  │                                  ▼              │
  │                         ┌──────────────────┐    │
  │                         │  <<database>>    │    │
  │                         │  IndexedDB       │    │
  │                         │  [Dexie]         │    │
  │                         │  Local workout   │    │
  │                         │  storage         │    │
  │                         └──────────────────┘    │
  └─────────────────────────────────────────────────┘
```

### Component Diagram (Level 3)

```
  ┌──────────────────┐
  │  <<container>>   │
  │  Views           │
  │  [Vue Router]    │
  └────────┬─────────┘
           │
     Uses ─┘
           │
           ▼
  ┌───────────────────────────────────────────────┐
  │  [Workout Feature]                            │
  │                                               │
  │  ┌──────────────────┐  ┌──────────────────┐  │
  │  │  <<component>>   │  │  <<component>>   │  │
  │  │  useWorkout      │─→│  useTimer        │  │
  │  │  [Composable]    │  │  [Composable]    │  │
  │  │  Workout exec.   │  │  Timer state     │  │
  │  │  state           │  │  machine         │  │
  │  └────────┬─────────┘  └──────────────────┘  │
  │           │                                   │
  │  Saves ───┘                                   │
  │  to                                           │
  │           │                                   │
  │           ▼                                   │
  │  ┌──────────────────┐                         │
  │  │  <<component>>   │                         │
  │  │  WorkoutRepo     │                         │
  │  │  [Dexie]         │                         │
  │  │  Workout persist.│                         │
  │  └──────────────────┘                         │
  └───────────────────────────────────────────────┘
```

### Deployment Diagram

```
  ╭───────────────────────────────────────╮
  │  <<node>> Customer Browser            │
  │  [Chrome/Firefox]                     │
  │                                       │
  │  ┌──────────────────┐                 │
  │  │  <<container>>   │                 │
  │  │  SPA             │                 │
  │  │  [React]         │                 │
  │  │  Web application │                 │
  │  └────────┬─────────┘                 │
  ╰───────────┼───────────────────────────╯
              │
    API calls ┘
    [HTTPS]
              │
              ▼
  ╭───────────────────────────────────────────────────╮
  │  <<node>> AWS Cloud [us-east-1]                   │
  │                                                   │
  │  ╭─────────────────────╮  ╭─────────────────────╮│
  │  │ <<node>> ECS Cluster│  │ <<node>> RDS        ││
  │  │ [Fargate]           │  │ [db.r5.large]       ││
  │  │                     │  │                     ││
  │  │ ┌──────────────────┐│  │ ┌──────────────────┐││
  │  │ │ <<container>>    ││  │ │ <<database>>     │││
  │  │ │ API Service      ││─→│ │ Database         │││
  │  │ │ [Node.js]        ││  │ │ [PostgreSQL]     │││
  │  │ │ REST API         ││  │ │ Application data │││
  │  │ └──────────────────┘│  │ └──────────────────┘││
  │  ╰─────────────────────╯  ╰─────────────────────╯│
  ╰───────────────────────────────────────────────────╯
```

---

## C4 Dynamic Diagram (Interface Communication)

### Purpose

C4 Dynamic Diagrams show the **runtime interactions** between elements (persons, systems,
containers, components) for a specific use case or business process. Interactions are
**numbered** to visualize temporal sequence — similar to UML Sequence Diagrams, but in
C4 style and at the desired abstraction level.

### Target Audience

- **Integration Architects**: Interface communication, protocols, data flows between systems
- **Solution Architects**: End-to-end flow of a use case across system boundaries

### When to Use

Use Dynamic Diagrams when:
- The **temporal sequence** of interactions between systems or components must be described
- **Interface communication** needs detailed documentation (which system calls what, when?)
- A specific **use case / business process** across multiple systems must be visualized
- **Integration scenarios** are analyzed or documented (e.g., onboarding flow, order process, data synchronization)
- The question is: "How do the systems communicate?" (not just "with whom?")

### Abstraction Levels

| Level | Elements | Typical Use |
|-------|----------|-------------|
| **System Context** | Persons ↔ Systems | Overview: Which systems participate in a process? |
| **Container** | Containers within systems (Web-App, API, DB, Queue) | Detail: How do calls flow within and between systems? |
| **Component** | Components within a container (Controller, Service, Repository) | Fine detail: How is a call processed within a container? |

### Interactive Dialog

When creating a Dynamic Diagram, follow this structured process:

#### Step 1: Identify Use Case / Scenario

Ask:
- Which use case or business process should be depicted?
  (e.g., "User signs in", "Order is placed", "Master data is synchronized")
- What is the **triggering event** (trigger)? (e.g., user action, timer, incoming message)
- What is the **expected outcome** at the end of the flow?

#### Step 2: Determine Abstraction Level

Ask:
- At which level should the diagram be created?
  - **System Context**: Interactions between whole systems (overview)
  - **Container**: Interactions between containers like web-app, API, database (recommended for interface documentation)
  - **Component**: Interactions between components within a container (fine detail)

If a C4 System Context Diagram has already been created in the conversation, reference
the identified systems and suggest the Container level as the next detail step.

#### Step 3: Identify Participating Elements

Ask (adapted to chosen level):

Collect elements in a table:

```
| # | Element         | Type                 | Belongs to     | Description              |
|---|-----------------|----------------------|----------------|--------------------------|
| 1 | Sachbearbeiter  | Actor                | —              | Triggers the process     |
| 2 | Web-Frontend    | Container (SPA)      | Portal-System  | Angular-based UI         |
| 3 | API-Gateway     | Container (Service)  | Portal-System  | Kong Gateway, Routing    |
| 4 | Fachservice     | Container (Service)  | Backend-System | Spring Boot REST-API     |
| 5 | PostgreSQL      | Container (Database) | Backend-System | Business data            |
| 6 | SAP ERP         | External System      | —              | Financial accounting     |
```

Confirm the table with the user before proceeding.

#### Step 4: Capture Interaction Steps

Ask:
- Describe the flow step by step:
  - Who calls whom?
  - What is transmitted/requested?
  - Which protocol/technology is used? (REST/JSON, gRPC, AMQP, SQL, JDBC, GraphQL, SOAP, SFTP, ...)
  - Is the call synchronous or asynchronous?
  - Is there a response/return? (e.g., "returns order confirmation")

Collect steps in a numbered table:

```
| Step | From           | To             | Action                       | Protocol   | Sync/Async | Response                |
|------|----------------|----------------|------------------------------|------------|------------|-------------------------|
| 1    | Sachbearbeiter | Web-Frontend   | Opens order form             | HTTPS      | Sync       | —                       |
| 2    | Web-Frontend   | API-Gateway    | POST /api/orders             | REST/JSON  | Sync       | 202 Accepted            |
| 3    | API-Gateway    | Fachservice    | Forward POST /orders         | REST/JSON  | Sync       | 202 Accepted            |
| 4    | Fachservice    | PostgreSQL     | INSERT INTO orders           | JDBC/SQL   | Sync       | OK                      |
| 5    | Fachservice    | SAP ERP        | Create booking               | SOAP/XML   | Async      | —                       |
| 6    | SAP ERP        | Fachservice    | Booking confirmation (CB)    | REST/JSON  | Async      | Booking number          |
| 7    | Fachservice    | PostgreSQL     | UPDATE orders SET status=... | JDBC/SQL   | Sync       | OK                      |
```

Confirm with user before proceeding.

#### Step 5: Error Cases and Alternative Paths (optional)

Ask:
- Are there error cases to be shown? (e.g., "What happens if SAP is unreachable?")
- Are there alternative paths? (e.g., "If customer already exists, step X is skipped")

If yes, capture as additional steps with marking (e.g., "5a" for alternative to step 5).

#### Step 6: Generate Diagram

### Dynamic Diagram Notation

```
Participating elements as columns (similar to Sequence Diagram):

  ┌──────────┐    ┌──────────────┐    ┌ ─ ─ ─ ─ ─ ─┐
  │  ☺ Name  │    │ <<container>> │   │ <<external>> │
  │  [Rolle] │    │  Servicename  │   │  Systemname  │
  └────┬─────┘    └──────┬────────┘   └ ─ ─ ─┬─ ─ ─ ┘
       │                 │                     │
       │                 │                     │

Synchronous call (numbered):
       │── 1. Description ──→│
       │       [Protocol]     │
       │←── Response ────────│

Asynchronous call (numbered):
       │─ ─ 2. Description ─ ─→│
       │        [Protocol]       │

Asynchronous response:
       │←─ ─ ─ Response ─ ─ ─ ─│

Self-call:
       │──┐ 3. Validation
       │  │    [internal]
       │←─┘

Grouping (optional, for loops/conditions):
       ╔══[loop: for each item]════════════════════╗
       ║  │── 4. Check item ──→│                   ║
       ║  │←── Stock level ───│                   ║
       ╚═══════════════════════════════════════════╝

       ╔══[alt: customer exists]═══════════════════╗
       ║  │── 5a. Load customer data ──→│          ║
       ╠══[else]═══════════════════════════════════╣
       ║  │── 5b. Create customer ─────→│          ║
       ╚═══════════════════════════════════════════╝
```

### System Boundaries in Dynamic Diagrams

```
       │ Portal-System                │ Backend-System              │ External
       │                              │                             │
  ┌─────────┐  ┌──────────────┐  ┌──────────┐  ┌──────────┐  ┌ ─ ─ ─ ─ ─┐
  │ Web-     │  │ API-Gateway  │  │ Fach-    │  │ Postgres │  │  SAP ERP  │
  │ Frontend │  │              │  │ service  │  │          │  │           │
  └────┬─────┘  └──────┬───────┘  └────┬─────┘  └────┬─────┘  └ ─ ─┬─ ─ ─┘
       │               │               │              │              │
```

### Dynamic Diagram Example: User Sign In Flow

```
  ┌──────────────┐  ┌──────────────────────────────────────────┐  ┌──────────────┐
  │ <<container>> │  │ [API Application]                        │  │ <<database>> │
  │ Single-Page  │  │                                          │  │ Database     │
  │ App          │  │  ┌───────────────┐  ┌─────────────────┐  │  │ [PostgreSQL] │
  │ [Angular]    │  │  │ <<component>> │  │  <<component>>  │  │  │ User         │
  │ Banking UI   │  │  │ Sign In       │  │  Security       │  │  │ credentials  │
  │              │  │  │ Controller    │  │  Service         │  │  │              │
  └──────┬───────┘  │  │ [Spring MVC]  │  │  [JWT]          │  │  └──────┬───────┘
         │          │  └──────┬────────┘  └────────┬────────┘  │         │
         │          └─────────┼────────────────────┼───────────┘         │
         │                    │                    │                     │
         │── 1. Submit ──────→│                    │                     │
         │   credentials      │                    │                     │
         │   [JSON/HTTPS]     │                    │                     │
         │                    │── 2. Validate ────→│                     │
         │                    │                    │                     │
         │                    │                    │── 3. Query user ──→│
         │                    │                    │   [JDBC]            │
         │                    │                    │                     │
         │                    │                    │←── User data ──────│
         │                    │←── Auth result ───│                     │
         │←── JWT Token ─────│                    │                     │
         │   [JSON/HTTPS]     │                    │                     │
```

### Dynamic Diagram Example: Order Processing (Event-Driven)

```
  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
  │ <<container>> │  │ <<container>> │  │ <<container>> │  │ <<container>> │
  │ Order        │  │ Inventory    │  │ Payment      │  │ Shipping     │
  │ Service      │  │ Service      │  │ Service      │  │ Service      │
  │ [Java]       │  │ [Go]         │  │ [Node.js]    │  │ [Python]     │
  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘
         │                 │                  │                  │
         │─ ─ 1. Publish ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─→
         │   order.created                    │                  │
         │   [Kafka/Avro]  │                  │                  │
         │                 │                  │                  │
         │          2. Consume ←─ ─ ─ ─ ─ ─ ─┘                  │
         │          order.created              │                  │
         │          [Kafka/Avro]               │                  │
         │                 │                  │                  │
         │                 │─ ─ 3. Publish ─ ─ ─ ─ ─ ─ ─ ─ ─ ─→│
         │                 │   inventory.reserved                │
         │                 │   [Kafka/Avro]   │                  │
         │                 │                  │                  │
         │                 │           4. Consume ←─ ─ ─ ─ ─ ─ ─┘
         │                 │           inventory.reserved         │
         │                 │           [Kafka/Avro]               │
         │                 │                  │                  │
         │                 │                  │─ ─ 5. Publish ─→│
         │                 │                  │   payment.done   │
         │                 │                  │   [Kafka/Avro]   │
         │                 │                  │                  │
         │                 │                  │           6. Consume
         │                 │                  │           payment.done
         │                 │                  │           [Kafka/Avro]
```

### Dynamic Diagram Example: OAuth2 Authorization Code Flow

```
  ┌──────────────┐  ┌──────────────┐  ┌ ─ ─ ─ ─ ─ ─ ─┐  ┌──────────────┐
  │ <<container>> │  │ <<container>> │  │ <<external>>  │  │ <<database>> │
  │ SPA          │  │ API          │  │ Auth0          │  │ User DB      │
  │ [React]      │  │ [Node.js]    │  │ [AuthZ Server] │  │ [PostgreSQL] │
  └──────┬───────┘  └──────┬───────┘  └ ─ ─ ─┬─ ─ ─ ─┘  └──────┬───────┘
         │                 │                  │                   │
         │── 1. Redirect ─ ─ ─ ─ ─ ─ ─ ─ ─→│                   │
         │   to /authorize                    │                   │
         │                 │                  │                   │
         │←─ 2. Redirect ─ ─ ─ ─ ─ ─ ─ ─ ─│                   │
         │   with auth code                   │                   │
         │                 │                  │                   │
         │── 3. Exchange code ──→│            │                   │
         │   for tokens          │            │                   │
         │   [HTTPS]             │            │                   │
         │                       │── 4. POST ─ ─ ─ ─ ─ ─ ─ ─ ─→│
         │                       │   /oauth/token                │
         │                       │   [HTTPS]  │                   │
         │                       │            │                   │
         │                       │←─ tokens ─ ─ ─ ─ ─ ─ ─ ─ ─ ─│
         │                       │            │                   │
         │←── 5. Access + ──────│            │                   │
         │   refresh tokens      │            │                   │
         │                 │                  │                   │
         │── 6. API request ────→│            │                   │
         │   with access token   │            │                   │
         │   [HTTPS]             │            │                   │
         │                       │── 7. Fetch ──────────────────→│
         │                       │   user data                    │
         │                       │   [SQL]    │                   │
         │                       │            │                   │
         │                       │←── user data ─────────────────│
         │←── response ─────────│            │                   │
```

---

## Heuristics (MUST)

### General Rules

1. **Every element must have**: Name, Type, Technology (where applicable), and Description
2. **Use unidirectional arrows** - Bidirectional arrows create ambiguity; show call and response separately
3. **Label arrows with action verbs** - "Sends email using", "Reads from", not just "uses"
4. **Include technology labels** - "JSON/HTTPS", "JDBC", "gRPC"
5. **Stay under 20 elements per diagram** - Split complex systems into multiple diagrams

### Actor Positioning Rules

1. **Actors MUST be placed on the sides (left/right) or at the top** — never in the center of a diagram.
2. **Triggering actors** go on the **left side** or **top-left**.
3. **Consuming/receiving actors** go on the **right side** or **top-right**.
4. In System Context diagrams: place actors on the **left and/or right edges**, with systems flowing horizontally between them. Alternatively, place actors **above** the system boundary, left- or right-aligned.
5. In Container diagrams: place actors **above** the system boundary, left- or right-aligned.
6. Rationale: lateral/top positioning keeps the system landscape in the center and clearly separates human interaction from technical integration.

### Extended System Context Rules

1. **Horizontal layout**: Systems flow left-to-right, actors on the edges.
2. **Team boundaries** are mandatory when multiple teams are involved: every system must belong to a team/responsibility area (dashed boundary).
3. **System status** must be indicated: mark systems as `[bestehend]` (existing) or `[neu]` (new).
4. **Data stores** are shown directly below their owning system using the `<<data>>` notation.
5. **Technical interfaces** (REST API, SOAP, SFTP, etc.) are labeled on arrows between systems.
6. **User interactions** use dashed arrows (`─ ─ ─→`) from actors to systems.
7. **A legend is mandatory** explaining all visual elements (system status, boundary styles, arrow types).

### Dynamic Diagram Rules

1. **Numbering is mandatory**: Every interaction step **must** have a sequential number showing temporal order.
2. **One use case per diagram**: A Dynamic Diagram describes **exactly one** use case or business process.
3. **Protocol mandatory**: Every call **must** specify the protocol/technology used.
4. **Sync/Async marking**: Synchronous calls as solid arrows (`───`), asynchronous as dashed arrows (`─ ─ ─`).
5. **Direction mandatory**: Every arrow **must** have a clear direction.
6. **Responses explicit**: If a call has a relevant response (data, confirmation), show it as a return arrow.
7. **Consistent abstraction level**: All elements **must** be at the same C4 abstraction level.
8. **Trigger recognizable**: The triggering actor/event must be clearly recognizable (leftmost position).
9. **Layout**: Elements from left (trigger) to right (target systems). Frequently interacting elements side by side.
10. **Compactness**: Maximum 7±2 elements per diagram. With more elements, switch to a higher abstraction level or split the use case.

### Clarity Guidelines

1. **Start at Level 1** - Context diagrams help frame system scope
2. **One diagram per file** - Keep diagrams focused on a single abstraction level
3. **Meaningful names** - Use descriptive names (e.g., "Order Service" not "Svc1")
4. **Concise descriptions** - Keep descriptions under 50 characters when possible
5. **Always include a title** - "System Context diagram for [System Name]"

### What to Avoid

See [references/common-mistakes.md](references/common-mistakes.md) for detailed anti-patterns:
- Confusing containers (deployable) vs components (non-deployable)
- Modeling shared libraries as containers
- Showing message brokers as single containers instead of individual topics
- Adding undefined abstraction levels like "subcomponents"
- Removing type labels to "simplify" diagrams

---

## Legend

Always add a legend below every diagram:

```
╔══════════════════════════════════════════════════════════╗
║  LEGEND                                                  ║
╠══════════════════════════════════════════════════════════╣
║  ☺        = Actor / Person                               ║
║  ╔═╗      = Central System (scope)                       ║
║  ┌─┐      = Internal Element (System/Container/Comp.)    ║
║  ┌ ┐      = External System                              ║
║  ───→     = Synchronous call                             ║
║  ─ ─→     = Asynchronous call                            ║
║  ←───     = Synchronous response                         ║
║  ←─ ─     = Asynchronous response / Callback             ║
║  [n]      = Step number (temporal order)                  ║
║  ╔══[x]═╗ = Grouping (loop/alt/opt)                      ║
║  ┄┄┄     = Trust Boundary                                ║
╚══════════════════════════════════════════════════════════╝
```

---

## Microservices Guidelines

### Single Team Ownership

Model each microservice as a **container** within a single system:

```
  ┌──────────────────┐
  │  ☺ Customer      │
  │  [Online shopper]│
  └────────┬─────────┘
           │
  Uses ────┘
  [HTTPS]
           │
           ▼
  ┌──────────────────────────────────────────────────────────────────────┐
  │  [E-commerce Platform]                                              │
  │                                                                     │
  │  ┌──────────────────┐                                               │
  │  │  <<container>>   │                                               │
  │  │  API Gateway     │                                               │
  │  │  [Kong]          │                                               │
  │  │  Routing, auth,  │                                               │
  │  │  rate limiting   │                                               │
  │  └────┬──────┬──────┘                                               │
  │       │      │      ──────────────────────────────────────          │
  │       │      │      │                    │                │         │
  │       ▼      ▼      ▼                    │                │         │
  │  ┌──────────┐ ┌──────────┐ ┌──────────┐  │                │         │
  │  │ Order    │ │ Product  │ │ User     │  │                │         │
  │  │ Service  │ │ Service  │ │ Service  │  │                │         │
  │  │ [Node.js]│ │ [Go]     │ │ [Java]   │  │                │         │
  │  └────┬─────┘ └────┬─────┘ └──┬───┬──┘  │                │         │
  │       │            │          │   │      │                │         │
  │       ▼            ▼          ▼   ▼      │                │         │
  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐     │         │
  │  │<<database>>││<<database>>││<<database>>││<<database>>│  │         │
  │  │ Order DB │ │ Product  │ │ User DB  │ │ Cache    │     │         │
  │  │[Postgres]│ │ DB       │ │[Postgres]│ │ [Redis]  │     │         │
  │  └──────────┘ │[MongoDB] │ └──────────┘ │ Sessions │     │         │
  │               └──────────┘              └──────────┘     │         │
  └──────────────────────────────────────────────────────────────────────┘
```

### Multi-Team Ownership

Promote microservices to **software systems** when owned by separate teams:

```
  ┌──────────────────┐                      ┌──────────────────┐
  │  ☺ Customer      │                      │  ☺ Admin         │
  │  [Online shopper]│                      │  [Store manager] │
  └────────┬─────────┘                      └────────┬─────────┘
           │                                         │
           ├──── Places orders ─────→ ╔══════════════╧══════════╗
           │                          ║  <<system>>             ║
           │                          ║  Order System           ║
           │                          ║  [Team Alpha]           ║
           │                          ╚═══════╤═════════════════╝
           │                                  │
           │                    Checks stock ─┘    Processes payment ─┐
           │                                  │                       │
           │                                  ▼                       ▼
           │                    ┌──────────────────┐  ┌ ─ ─ ─ ─ ─ ─ ─ ─┐
           │                    │  <<system>>      │  │ <<external>>     │
           │                    │  Inventory System│  │ Stripe           │
           │                    │  [Team Beta]     │  │ [Payment proc.]  │
           │                    └──────────────────┘  └ ─ ─ ─ ─ ─ ─ ─ ─┘
           │
           └──── Browses products ──→ ┌──────────────────┐
                                      │  <<system>>      │
                                      │  Product System  │
                                      │  [Team Beta]     │
                                      └──────────────────┘
```

### Event-Driven Architecture

Show individual topics/queues as containers, NOT a single "Kafka" box:

```
  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
  │ <<container>> │  │ <<container>> │  │ <<container>> │
  │ Order        │  │ Inventory    │  │ Payment      │
  │ Service      │  │ Service      │  │ Service      │
  │ [Java]       │  │ [Java]       │  │ [Java]       │
  └──┬───────┬───┘  └──┬───────┬───┘  └──┬───────────┘
     │       │         │       │         │
     │       │         ▲       │         ▲
     │    Publishes    │    Publishes    │
     │    [Avro]       │    [Avro]       │
     │       │     Consumes    │     Consumes
     │       │     [Avro]      │     [Avro]
     │       ▼         │       ▼         │
     │  ┌──────────────┴──┐  ┌┴──────────────┐
     │  │  <<queue>>      │  │  <<queue>>     │
     │  │  order.created  │  │  stock.reserved│
     │  │  [Kafka]        │  │  [Kafka]       │
     │  └─────────────────┘  └────────────────┘
     │
     │  Consumes payment.complete [Avro]
     │         │
     │         ▼
     │  ┌─────────────────┐
     │  │  <<queue>>      │
     │  │  payment.       │
     │  │  complete       │
     │  │  [Kafka]        │
     │  └─────────────────┘
     │         ▲
     │         │ Publishes [Avro]
     │         │
     └─────────┘ (from Payment Service)
```

---

## Cross-References Between Diagram Types

Nach Abschluss jedes Diagramms oder jeder Analyse IMMER die **Follow-Up-Optionen**
aus dem Entry-Point Dialog (oben) anbieten. Zusätzlich gelten folgende inhaltliche
Querverweise:

- **Context → Dynamic**: Wenn im System Context Diagram Schnittstellen identifiziert wurden,
  ein Dynamic Diagram als Detaillierung für einen konkreten Use Case vorschlagen.
- **Context → Container**: Wenn ein System im Kontext-Diagramm technisch vertieft werden soll,
  ein Container Diagram vorschlagen.
- **Dynamic → ADR**: Wenn im Dynamic Diagram komplexe Integrationsmuster auftauchen
  (z. B. Orchestration vs. Choreography), einen ADR für die Pattern-Entscheidung vorschlagen.
- **Dynamic → NFR**: Aus dem Dynamic Diagram Performance-Anforderungen ableiten
  (z. B. „Step 3→4 muss in < 100ms abgeschlossen sein").

---

## Output Location

Write architecture documentation to `docs/architecture/` with this naming convention:

- `c4-context.md` - System Context diagram (extended, with team boundaries, system status, data stores)
- `c4-containers.md` - Container diagram (optional)
- `c4-components-{feature}.md` - Component diagrams per feature (optional)
- `c4-deployment.md` - Deployment diagram (optional)
- `c4-dynamic-{flow}.md` - Dynamic diagrams for specific flows

## Audience-Appropriate Detail

| Audience | Recommended Diagrams |
|----------|---------------------|
| Enterprise Architects | System Context (Extended) + Dynamic |
| Executives | System Context only |
| Product Managers | System Context (Extended) |
| Integration Architects | System Context (Extended) + Dynamic |
| Solution Architects | System Context (Extended) + Dynamic + Container |
| Developers | All levels as needed |
| DevOps | Container + Deployment |

## References

- [references/c4-syntax.md](references/c4-syntax.md) - Complete ASCII C4 notation reference
- [references/common-mistakes.md](references/common-mistakes.md) - Anti-patterns to avoid
- [references/advanced-patterns.md](references/advanced-patterns.md) - Microservices, event-driven, deployment, dynamic patterns
