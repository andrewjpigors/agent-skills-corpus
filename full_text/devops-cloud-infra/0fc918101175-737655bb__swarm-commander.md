---
name: swarm-commander
description: Use this skill when asked to lead large projects, trigger massive parallel compute, or deploy multi-agent swarms.
---

# Swarm Automation & Commander Directives

You have the ability to spawn background instances of yourself (ClawBot agents) to tackle multiple parts of a complicated problem SIMULTaneously. 

## 1. When to use a Swarm?
- If the user asks to build an entire SaaS platform, deploy 3 workers: 
  - Worker 1 builds the Frontend
  - Worker 2 builds the Backend
  - Worker 3 researches documentation or design patterns
- If you need to write 5 articles at once, unleash 5 workers!

## 2. How to Dispatch the Swarm?
Instead of doing everything yourself linearly, construct your JSON response with the `dispatch_swarm` action:

```json
{
  "thought": "This project is huge. I will deploy a Frontend and Backend worker to build concurrently.",
  "action": "dispatch_swarm",
  "tasks": [
     "Build the frontend react UI for the saas app in the 'saas-frontend' folder.",
     "Build the python fast-api backend in the 'saas-backend' folder."
  ]
}
```

## 3. Post-Dispatch
Once dispatched, the Child Agents will open in their own separate terminal windows and begin executing automatically using the `gemini-2.5-flash` model. You (the commander) can then `done` out of your loop or continue monitoring. DO NOT attempt to write the code yourself if you have delegated it to the swarm.
