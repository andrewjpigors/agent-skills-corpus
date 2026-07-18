---
name: sourcepawn-l4d2
description: "SourcePawn scripting for Left 4 Dead 2 SourceMod plugins. Use when writing, editing, reviewing, or debugging .sp/.inc files; creating L4D2 plugins; working with Left4DHooks; dealing with SourceMod 1.11/1.12 compatibility; compiling SourcePawn; or looking up L4D2-specific constants, game events with their fields, DirectorOptions, netprops, datamaps, weapon/enemy IDs, or common plugin patterns."
---

# SourcePawn Development for Left 4 Dead 2

Complete reference for L4D2 SourceMod plugin development. All data sourced from the user's local include/ reference files.

## File Layout

```
sourcepawn-l4d2/                     ← Skill package root
├── SKILL.md                         ← This file (comprehensive reference)
└── references/
    ├── sm-1.11/include/             ← SM 1.11 full API (70 .inc files)
    ├── sm-1.12/include/             ← SM 1.12 full API (70 .inc files)
    ├── left4dhooks/include/         ← Left4DHooks (5 .inc files)
    ├── l4d2util/scripting/include/  ← l4d2util (8 .inc files)
    ├── multicolors/scripting/include/ ← multicolors + morecolors
    ├── smlib/scripting/include/     ← SMLib transitional syntax (27 .inc)
    ├── standalone/colors.inc        ← Standalone colored chat
    └── game-data/
        ├── DirectorOptions.txt      ← Full Director variables (1134 lines)
        ├── l4d2-events.txt          ← Complete event catalog (1837 lines)
        ├── netprop-dump.txt         ← All entity netprops (16581 lines)
        └── datamap-dump.txt         ← All class datamaps (15378 lines)
```

## Compilation

```bash
spcomp.exe myplugin.sp \
  -i"Desktop\sourcepawn\inc11\include" \
  -i"Desktop\sourcepawn\left4dhooks\include" \
  -i"Desktop\sourcepawn\l4d2util\scripting\include" \
  -o"myplugin.smx" -E
```

| Flag | Effect |
|------|--------|
| `-o<PATH>` | Output .smx path |
| `-i<PATH>` | Add include search path (repeatable) |
| `-E` | Warnings as errors |
| `-w<NUM>` | Suppress warning N |
| `--syntax-only` | Parse only, no .smx output |
| `-v2` | Verbose level 2 |
| `-;(--require-semicolons)` | Require semicolons |

**Rule: Recompile after every .sp edit. Fix ALL warnings.**

---

## SM 1.11 → 1.12 Complete Change Log

### Breaking Changes

| File | Change | Compat Code |
|------|--------|-------------|
| **clients.inc** | `MAXPLAYERS 65→101` | `MaxClients+1`; or `#if SOURCEMOD_V_MINOR>=12` guard |
| **core.inc** | `SOURCEMOD_PLUGINAPI_VERSION 5→7` | Plugins compiled for 1.12 may not load on 1.11 |
| **halflife.inc** | `EntRefToEntIndex` now validates entity alive; returns `INVALID_ENT_REFERENCE` (-2) if stale | Check `if(entity==INVALID_ENT_REFERENCE)return;` |
| **sdktools_sound.inc** | SND flags changed from sequential enum to bitmask (`1<<0` form) | Use enum names, never hardcode values |
| **entity_prop_stocks.inc** | `SetEntityHealth` internal impl changed from `GetEntityNetClass`+`FindSendPropInfo` to `FindDataMapInfo` | API unchanged; recompile only |

### New Natives (1.12 only — guard with `#if SOURCEMOD_V_MINOR >= 12`)

| Native | File | Description |
|--------|------|-------------|
| `ParseTime(dateTime, format)` | sourcemod.inc | Parse date/time string → Unix timestamp (UTC) |
| `LoadEntityFromHandleAddress(addr)` | entity.inc | Read entity from memory handle address |
| `StoreEntityToHandleAddress(addr, entity)` | entity.inc | Write entity to memory handle address |
| `GetPublicChatTriggers(buf, len)` | console.inc | Get public chat trigger characters |
| `GetSilentChatTriggers(buf, len)` | console.inc | Get silent chat trigger characters |
| `GetFilePermissions(path, &mode)` | files.inc | Get file/dir permissions |
| `GetClientOriginalLanguage(client)` | lang.inc | Get client's original language number |
| `TE_WriteEnt(prop, value)` | sdktools_tempents.inc | Write entity value in temp entity |
| `TE_ReadEnt(prop)` | sdktools_tempents.inc | Read entity value from temp entity |
| `FloatMod(a,b)` | float.inc | Float modulus (use `%` operator instead) |
| `CS_WeaponIDToLoadoutSlot(id)` | cstrike.inc | CS:GO weapon loadout slot |
| `File.Size()` | files.inc | Get file size in bytes |
| `TextParser.ParseString(str, &line, &col)` | textparse.inc | Parse raw UTF-8 as SMC file |
| `AssertArrayEq(text, val, exp, len)` | testing.inc | Array equality assertion |
| `AssertArray2DEq(text, val, exp, len, ilen)` | testing.inc | 2D array equality assertion |

### New Forwards (1.12 only)

```sourcepawn
// clients.inc
forward void OnServerEnterHibernation();  // Before server sleeps
forward void OnServerExitHibernation();   // After server wakes
```

### New Methodmaps & Types (1.12)

| Addition | File | Notes |
|----------|------|-------|
| `Handle` methodmap (Close/Clone) | handles.inc | Replaces `CloseHandle()` |
| `Cookie.SetInt(client, value)` | clientprefs.inc | Convenience method |
| `Cookie.SetFloat(client, value)` | clientprefs.inc | Convenience method |
| `TraceType` enum | sdktools_trace.inc | TRACE_EVERYTHING/WORLD_ONLY/ENTITIES_ONLY/FILTER_PROPS |
| `MenuHandler` typeset | menus.inc | void OR int return callbacks |
| `Timer` callback typeset | timers.inc | void OR int return callbacks |
| `Engine_PVKII=26`, `Engine_MCV` | halflife.inc | New engine enums |
| `SDKCall_Engine` type | sdktools.inc | CVEngineServer calls |
| `SND_IGNORE_PHONEMES` | sdktools_sound.inc | New flag `(1<<8)` |
| `SND_IGNORE_NAME` | sdktools_sound.inc | New flag `(1<<9)` |
| `SND_DO_NOT_OVERWRITE_EXISTING_ON_CHANNEL` | sdktools_sound.inc | New flag `(1<<10)` |

### New/Changed Parameters (1.12)

| Native | New Param | Default | File |
|--------|-----------|---------|------|
| `ForcePlayerSuicide` | `bool explode` | false | sdktools_functions.inc |
| `adt_array.GetString` | `int block` | 0 | adt_array.inc |
| `adt_array.SetString` | `int block` | 0 | adt_array.inc |
| `adt_array.GetArray` | `int block` | 0 | adt_array.inc |
| `adt_array.SetArray` | `int block` | 0 | adt_array.inc |
| `adt_stack.Top` | `int block, bool asChar` | 0,false | adt_stack.inc |
| `adt_stack.TopString` | *(entirely new method)* | — | adt_stack.inc |
| `adt_stack.TopArray` | *(entirely new method)* | — | adt_stack.inc |
| `KeyValues.SavePosition` | returns `bool` | — | keyvalues.inc |
| `KeyValues.Rewind` | `bool clearHistory` | true | keyvalues.inc |
| `TR_TraceRay/Filter/Entity` | `TraceType traceType` | TRACE_EVERYTHING | sdktools_trace.inc |
| `CreateDirectory` | `int mode` with default | FPERM_... | files.inc |

### SDKHooks Auto-Cleanup (1.12+)
All SDKHooks are automatically removed on entity destruction. No manual `SDKUnhook` needed in `OnEntityDestroyed`.

### L4D2-Specific Documentation Notes (1.12)
- `PrintHintText` / `PrintCenterText` display BROKEN on L4D2 clients
- Clients need `cl_showpluginmessages 1` (non-default) for some message funcs since ~2018
- SDKCall string returns: bytes written, or -1 for NULL

### Version Detection Pattern
```sourcepawn
#if !defined SOURCEMOD_V_MINOR
  #define SOURCEMOD_V_MINOR 11
#endif

#if SOURCEMOD_V_MINOR >= 12
  // 1.12+ path
#else
  // 1.11 fallback
#endif
```

---

## Left4DHooks Complete API

### Include Files
| File | Purpose |
|------|---------|
| `left4dhooks.inc` | Core: 100+ forwards, 200+ natives, constants, validators |
| `left4dhooks_stocks.inc` | Team/zombie class mgmt, weapons, visual effects, entity glow |
| `left4dhooks_silver.inc` | Engine detection, flow, doors, common CI spawn, SI-survivor interaction |
| `left4dhooks_lux_library.inc` | Particles, sounds, decals, physics, dynamic lights |
| `left4dhooks_anim.inc` | L4D1_ACT_* and L4D2_ACT_* animation constants |

### Include Order
```sourcepawn
#include <sourcemod>
#include <sdktools>
#include <sdkhooks>
#include <left4dhooks>
```

### Forward Categories (all in left4dhooks.inc)

**Hook Naming Convention:**
- `_Pre()` — Before event, can block with `Plugin_Handled`
- `_Post()` — After event, always fires
- `_PostHandled()` — Only fires if Pre was blocked
- `L4D_*` — Works on both L4D1 & L4D2
- `L4D2_*` — L4D2 only

```
// ── Survivor State ──
L4D_OnFirstSurvivorLeftSafeArea(client)          → Action (can block round start)
L4D_OnFirstSurvivorLeftSafeArea_Post(client)     → void
L4D_OnFirstSurvivorLeftSafeArea_PostHandled(c)   → void (if Pre blocked)
L4D_OnIncapacitated(client, attacker, inflictor) → Action
L4D_OnIncapacitated_Post(client, attacker, inflictor)
L4D_OnIncapacitated_PostHandled(client, attacker, inflictor)
L4D_OnIncapacitatedSurvivorKilled(victim, attacker, inflictor)
L4D_OnSurvivorDeathStart(victim, attacker, inflictor) → Action
L4D_OnSurvivorDeathFinish(victim, attacker, inflictor)
L4D_OnSurvivorHurt(victim, attacker, inflictor, &Float:damage, &int:type) → Action
L4D_OnLedgeGrabbed(client, &ledgetype)           → Action
L4D_OnCancelStagger(client, &result)             → Action
L4D_OnCancelStagger_Post(client, result)
L4D_OnCancelStagger_PostHandled(client, &result)
L4D_OnMotionControlledXY(client, &vecMotion[2], flFrameTime) → Action
L4D_OnShovedBySurvivor(victim, attacker, &result) → Action

// ── L4D2 Survivor Extras ──
L4D2_OnRevived(client, reviver)
L4D2_OnStagger(client, attacker, &result)        → Action
L4D2_OnStagger_Post(client, attacker, result)
L4D2_OnStagger_PostHandled(client, attacker, &result)
L4D2_OnPlayerFling(client, attacker, vecDir[3])  → Action
L4D2_OnPlayerFling_Post(client, attacker, vecDir[3])
L4D2_OnPounceOrLeapStumble(client, attacker, &result) → Action

// ── Charger ──
L4D_OnChargerCollide(charger, victim)            → Action
L4D_OnChargerGrab(charger, victim)               → Action
L4D_OnChargerReleased(charger, victim)
L4D_OnChargerPummel(charger, victim)             → Action
L4D2_OnStartCarryingVictim(charger, victim)      → Action
L4D2_OnStartCarryingVictim_Post(charger, victim)
L4D2_OnStartCarryingVictim_PostHandled(charger, victim)
L4D2_OnChargerImpact(client)
L4D2_OnPummelVictim(charger, victim)             → Action
L4D2_OnPummelVictim_Post(charger, victim)
L4D2_OnPummelVictim_PostHandled(charger, victim)
L4D2_OnSlammedSurvivor(charger, victim, vecDir[3], &wall, &ground) → Action
L4D2_OnSlammedSurvivor_Post(charger, victim, vecDir[3], wall, ground)
L4D2_OnSlammedSurvivor_PostHandled(charger, victim, vecDir[3], &wall, &ground)

// ── Jockey ──
L4D_OnJockeyMount(jockey, victim)                → Action
L4D_OnJockeyDismount(jockey, victim)
L4D2_OnJockeyRide(jockey, victim, &vecDir[3])    → Action
L4D2_OnJockeyRide_Post(jockey, victim, vecDir[3])
L4D2_OnJockeyRide_PostHandled(jockey, victim, &vecDir[3])

// ── Smoker ──
L4D_OnGrabWithTongue(smoker, victim, vecDir[3])  → Action
L4D_OnGrabWithTongue_Post(smoker, victim, vecDir[3])
L4D_OnGrabWithTongue_PostHandled(smoker, victim, vecDir[3])

// ── Spitter ──
L4D_OnSpitterSpit(spitter)                       → Action
L4D2_OnSpitSpread(spitter, spitEntity)

// ── Hunter / Pounce ──
L4D_OnPouncedOnSurvivor(pouncer, victim)         → Action
L4D_OnPouncedOnSurvivor_Post(pouncer, victim)
L4D_OnPouncedOnSurvivor_PostHandled(pouncer, victim)

// ── Boomer ──
L4D_OnVomitedUpon(victim, attacker)              → Action
L4D_OnVomitedUpon_Post(victim, attacker)
L4D_OnVomitedUpon_PostHandled(victim, attacker)

// ── Tank ──
L4D_OnSpawnTank(vecPos[3], vecAng[3])            → Action
L4D_OnSpawnTank_Post(client, vecPos[3], vecAng[3])
L4D_OnSpawnTank_PostHandled(client, vecPos[3], vecAng[3])
L4D_OnTankRockThrown(tank, &entity)              → Action
L4D_OnTankRockHit(tank, rock, hitEnt, &bool:allowDamage) → Action
L4D_OnTryOfferingTankBot(survivorCount, botCount) → Action
L4D_OnTryOfferingTankBot_Post(survivorCount, botCount, result)
L4D_OnReplaceTank(tank, replacement)             → Action
L4D2_OnSelectTankAttackPre(tank, &attackType)    → Action (L4D2 only)
L4D_TankClaw_DoSwing_Pre(tank, &result)          → Action
L4D_TankClaw_DoSwing_Post(tank, result)
L4D_TankClaw_OnPlayerHit_Pre(tank, victim, &retVal) → Action
L4D_TankClaw_OnPlayerHit_Post(tank, victim, retVal)
L4D_TankClaw_OnPlayerHit_PostHandled(tank, victim, &retVal)
L4D_TankRock_OnDetonate(rock, &result)           → Action
L4D_TankRock_OnRelease(tank, rock)
L4D_TankRock_BounceTouch(rock, entity, &result)  → Action
L4D_OnEnterStasis(tank)
L4D_OnLeaveStasis(tank)

// ── Witch ──
L4D_OnSpawnWitch(vecPos[3], vecAng[3])           → Action
L4D_OnSpawnWitch_Post(entity, vecPos[3], vecAng[3])
L4D_OnSpawnWitch_PostHandled(entity, vecPos[3], vecAng[3])
L4D2_OnSpawnWitchBride(vecPos[3], vecAng[3])     → Action (L4D2)
L4D2_OnSpawnWitchBride_Post(entity, vecPos[3], vecAng[3])
L4D2_OnSpawnWitchBride_PostHandled(entity, vecPos[3], vecAng[3])
L4D_OnWitchKilled(witch, killer, inflictor)
L4D_OnWitchAttack(witch, victim)                 → Action
L4D_OnWitchFlinch(witch, attacker, inflictor)    → Action
L4D_OnWitchIgnite(witch)
L4D_OnWitchRespawn(witch)
L4D_OnWitchStunned(witch)
L4D_OnWitchSetHarasser(witch, victim)

// ── Special Infected Spawn ──
L4D_OnSpawnSpecial(&zombieClass, vecPos[3], vecAng[3]) → Action
L4D_OnSpawnSpecial_Post(client, zombieClass, vecPos[3], vecAng[3])
L4D_OnSpawnSpecial_PostHandled(client, zombieClass, vecPos[3], vecAng[3])

// ── Infected State ──
L4D_OnEnterGhostStatePre(client)                 → Action
L4D_OnEnterGhostState(client)
L4D_OnEnterGhostState_PostHandled(client)
L4D_OnMaterializeFromGhostPre(client)            → Action
L4D_OnMaterializeFromGhost(client)
L4D_OnMaterializeFromGhost_PostHandled(client)
L4D_OnTakeOverBot(client)                        → Action
L4D_OnTakeOverBot_Post(client, success)
L4D_OnTakeOverBot_PostHandled(client, success)
L4D_OnIsDominatedBySpecialInfected(victim, dominator)
L4D2_OnChooseVictim(specialInfected, &victim)    → Action (L4D2)
L4D2_OnChooseVictim_Post(specialInfected, victim)
L4D2_OnChooseVictim_PostHandled(specialInfected, &victim)

// ── Mob / Horde ──
L4D_OnMobRushStart()                             → Action
L4D_OnMobRushStart_Post()
L4D_OnMobRushStart_PostHandled()
L4D_OnSpawnITMob(&amount)                        → Action
L4D_OnSpawnITMob_Post(amount)
L4D_OnSpawnITMob_PostHandled(amount)
L4D_OnSpawnMob(&amount)                          → Action
L4D_OnSpawnMob_Post(amount)
L4D_OnSpawnMob_PostHandled(amount)

// ── Items / Healing / Weapons ──
L4D_OnDeathDroppedWeapons(victim, bool:primary, bool:secondary)
L4D_PlayerExtinguish(client, attacker)
L4D2_OnUseHealingItems(client, target, &weapon)  → Action (L4D2)
L4D2_OnFindScavengeItem(client, item)            (L4D2)
L4D1_FirstAidKit_StartHealing(healer, patient)   → Action (L4D1)
L4D1_FirstAidKit_FinishedHealing(healer, patient)
L4D1_FirstAidKit_CancelHealing(healer, patient)
L4D2_BackpackItem_StartAction(client, item, ActionType) → Action (L4D2)
L4D2_BackpackItem_FinishedAction(client, item, ActionType)
L4D2_BackpackItem_CancelAction(client, item, ActionType)
L4D2_OnStartUseAction_PostHandled(client, entity, useType)

// ── Projectiles / Grenades ──
L4D_MolotovProjectile_Pre(&entity)               → Action
L4D_MolotovProjectile_Post(entity)
L4D_PipeBombProjectile_Pre(&entity)              → Action
L4D_PipeBombProjectile_Post(entity)
L4D2_VomitJarProjectile_Pre(&entity)             → Action (L4D2)
L4D2_VomitJarProjectile_Post(entity)
L4D2_GrenadeLauncherProjectile_Pre(&entity)      → Action (L4D2)
L4D2_GrenadeLauncherProjectile_Post(entity)
L4D_Molotov_Detonate(entity)                     → Action
L4D_Molotov_Detonate_Post(entity)
L4D_PipeBomb_Detonate(entity)                    → Action
L4D_PipeBomb_Detonate_Post(entity)
L4D2_VomitJar_Detonate(entity)                   → Action (L4D2)
L4D2_VomitJar_Detonate_Post(entity)
L4D2_GrenadeLauncher_Detonate(entity)            → Action (L4D2)

// ── Game State ──
L4D_OnGameFrame()
L4D_OnForceSurvivorPositions_Pre()
L4D_OnForceSurvivorPositions()
L4D_OnReleaseSurvivorPositions()
L4D_OnSpeakResponseConcept_Pre(entity)
L4D_OnSpeakResponseConcept_Post(entity)
L4D_OnGetCrouchTopSpeed(target, &retVal)         → Action
L4D_OnGetRunTopSpeed(target, &retVal)            → Action
L4D_OnGetWalkTopSpeed(target, &retVal)           → Action
L4D_OnGameModeChange(newMode)
L4D_OnServerHibernationUpdate(bool:inHibernation)
L4D_OnFinishIntro()
L4D_OnSavingEntities(info_changelevel)           → Action
L4D_OnSavingEntities_Post(info_changelevel)
L4D_OnSavingEntities_PostHandled(info_changelevel)
L4D2_OnSavingEntities(info_changelevel)          → Action (L4D2)
L4D2_OnSavingEntities_Post(info_changelevel)
L4D2_OnSavingEntities_PostHandled(info_changelevel)

// ── Script Values (L4D2) ──
L4D_OnGetScriptValueInt(key, &retVal)            → Action
L4D_OnGetScriptValueString(key, defaultVal, retVal[128]) → Action
L4D2_OnGetScriptValueVector(key, retVal[3], hScope) → Action
L4D_OnHasConfigurableDifficulty(&retVal)         → Action
L4D_OnHasConfigurableDifficulty_Post(retVal)
L4D_OnGetSurvivorSet(&retVal)                    → Action

// ── Finale / Versus ──
L4D2_OnChangeFinaleStage(stage, &newStage)       → Action (L4D2)
L4D2_OnEndVersusModeRound(&bWin, &bIsSurvivorTeam) → Action (L4D2)
L4D_OnGetMissionVSBossSpawning(...)              → Action
L4D_OnGetMissionVSBossSpawning_PostHandled(...)
L4D_OnClearTeamScores(newCampaign)               → Action
L4D_OnSetCampaignScores(&scoreA, &scoreB)        → Action
L4D_OnSetCampaignScores_Post(scoreA, scoreB)
L4D_OnRecalculateVersusScore(client)             → Action
L4D_OnIsTeamFull(team, &full)                    → Action

// ── Entity Shoved / Push (L4D2) ──
L4D2_OnEntityShoved(victim, attacker, &result)   → Action
L4D2_OnEntityShoved_Post(...)
L4D2_OnEntityShoved_PostHandled(...)

// ── Transition (L4D2) ──
L4D2_OnTransitionRestore(client)                 → Action
L4D2_OnTransitionRestore_Post(client, pkv)
L4D2_OnTransitionRestore_PostHandled(client, pkv)
L4D2_OnRestoreTransitionedSurvivorBots()         → Action
L4D2_OnRestoreTransitionedSurvivorBots_Post()
L4D2_OnRestoreTransitionedSurvivorBots_PostHandled()
L4D2_OnClientDisableAddons(SteamID)              → Action

// ── Misc ──
L4D_OnCThrowActivate(client, &weapon)            → Action
L4D_CBreakableProp_Break(prop, attacker, inflictor) → Action
L4D2_CGasCan_EventKilled(entity, attacker, inflictor, bool:aleardyDead) → Action
L4D2_CGasCan_EventKilled_Post(...)
L4D2_CGasCan_EventKilled_PostHandled(...)
L4D_OnPlayerCough_PostHandled(client)
L4D2_VomitJar_Detonate_Post(entity)
L4D2_OnSwingStart(client, weapon, &swingtype)    → Action
```

### Essential Natives

```sourcepawn
// ── Validation ──
bool IsValidSurvivor(int client);
bool IsValidInfected(int client);
bool IsValidSpecialInfected(int client);
bool IsValidTank(int client);
bool IsValidSurvivorBot(int client);
bool IsValidSpecialInfectedBot(int client);
bool IsPlayerInFirstPerson(int client);

// ── Survivor State ──
bool IsSurvivorIncapped(int client);
bool IsSurvivorPinned(int client);
bool IsSurvivorDead(int client);
bool IsSurvivorIncapacitated(int client);
bool IsSurvivorStaggered(int client);
bool L4D2_IsSurvivorGettingUp(int client);       // L4D2
bool L4D2_IsSurvivorOnLedge(int client);         // L4D2
bool IsSurvivorReviving(int client);
bool IsSurvivorReachable(int client);
bool L4D2_IsSurvivorInWater(int client);         // L4D2

// ── Counts ──
int L4D_GetSurvivorCount();
int L4D_GetInfectedCount();
int L4D_GetTankBossZombieCount();
int L4D_GetSpecialsBossZombieCount();
int L4D_GetTotalBossZombieCount();
int L4D2_GetTankCount();                          // L4D2
int L4D2_GetWitchCount();                         // L4D2
int L4D2_GetSpecialInfectedCount();               // L4D2

// ── Health / Ammo ──
float L4D_GetTempHealth(int client);
void L4D_SetTempHealth(int client, float health);
int L4D_GetReserveAmmo(int client, int weapon);
void L4D_SetReserveAmmo(int client, int weapon, int ammo);

// ── Game Mode ──
bool L4D_IsCoopMode();
bool L4D2_IsRealismMode();
bool L4D_IsVersusMode();
bool L4D_IsSurvivalMode();
bool L4D2_IsScavengeMode();
bool L4D2_IsGenericCooperativeMode();
int L4D_GetGameModeType();

// ── Flow / Checkpoints ──
bool L4D_HasAnySurvivorLeftSafeArea();
bool L4D_IsAnySurvivorInStartArea();
bool L4D_IsAnySurvivorInCheckpoint();
bool L4D_AreAllSurvivorsInFinaleArea();
bool L4D_IsInFirstCheckpoint(int client);
bool L4D_IsInLastCheckpoint(int client);
bool L4D_IsPositionInFirstCheckpoint(const float vecPos[3]);
bool L4D_IsPositionInLastCheckpoint(const float vecPos[3]);
int L4D_GetCheckpointFirst();
int L4D_GetCheckpointLast();
int L4D_GetHighestFlowSurvivor();
float L4D2_GetFurthestSurvivorFlow();

// ── Ghost / Spawn ──
bool L4D2_IsPlayerInGhostState(int client);
bool L4D_CanBecomeGhost(int client);
void L4D_SetBecomeGhostAt(int client, float time);
void L4D_MaterializeFromGhost(int client);
void L4D_BecomeGhost(int client);
void L4D_SetClass(int client, int zombieClass);
void L4D_State_Transition(int client, int state);

// ── SI Domination ──
int L4D2_GetSpecialInfectedDominatingMe(int victim);
bool L4D2_IsSpecialInfectedDominating(int client);

// ── Weapons (L4D2) ──
int L4D2_GetCurrentWeaponID(int client);
int L4D2_GetCurrentWeaponSlot(int client);
int L4D2_GetWeaponID(int weapon);
int L4D2_GetWeaponSlot(int weapon);
int L4D2_GetEquippedMelee(int client);
int L4D2_GetEquippedPrimary(int client);
int L4D2_GetEquippedSecondary(int client);

// ── Director / Script ──
void L4D_ResetMobTimer();
float L4D_GetPlayerSpawnTime(int player);
void L4D_SetPlayerSpawnTime(int player, float time, bool bReportToPlayer);
int L4D2_GetScriptValueInt(const char[] key, int value);
float L4D2_GetScriptValueFloat(const char[] key, float value);
int L4D2_GetFirstSpawnClass();
void L4D2_SetFirstSpawnClass(int zombieClass);
int L4D2_GetDirectorScriptScope(int level);
bool L4D2_IsScriptSpawnBlocked(const char[] scriptname);
void L4D2_BlockScriptSpawn(const char[] scriptname, bool block);

// ── Tank ──
void L4D_ReplaceTank(int tank, int newtank);
int L4D2_SpawnTank(const float vecPos[3], const float vecAng[3]);
int L4D2_SpawnSpecial(int zombieClass, const float vecPos[3], const float vecAng[3]);
int L4D2_SpawnWitch(const float vecPos[3], const float vecAng[3]);
int L4D2_SpawnWitchBride(const float vecPos[3], const float vecAng[3]);
bool L4D2_IsTankInPlay();

// ── Stagger / Fling ──
void L4D_StaggerPlayer(int target, int source_ent, const float vecSource[3]);
void L4D2_CTerrorPlayer_Fling(int client, int attacker, const float vecDir[3]);

// ── Revive ──
void L4D_ReviveSurvivor(int client);
void L4D_StopBeingRevived(int client, bool vocalize = false);
void L4D2_DefibByDeadBody(int client, int reviver, bool nopenalty);

// ── Misc ──
void L4D_RespawnPlayer(int client);
void L4D_SetHumanSpec(int bot, int client);
bool L4D_TakeOverBot(int client);
void L4D_Deafen(int client);
void L4D_RemoveEntityDelay(int entity, float time, int user);
int L4D_Dissolve(int entity);
void L4D_OnITExpired(int client);
float L4D_EstimateFallingDamage(int client);
bool L4D_GetRandomPZSpawnPosition(int client, int zombieClass, int attempts, float vecPos[3]);
void L4D_WarpToValidPositionIfStuck(int client);
void L4D2_UseAdrenaline(int client, float fTime, bool heal, bool event);
void L4D2_SendInRescueVehicle();
void L4D2_ChangeFinaleStage(int finaleType, const char[] arg);
bool L4D_HasPlayerControlledZombies();

// ── Force Interactions ──
void L4D_ForceHunterVictim(int victim, int attacker);
void L4D_ForceSmokerVictim(int victim, int attacker);
void L4D2_ForceJockeyVictim(int victim, int attacker);
void L4D2_Jockey_EndRide(int victim, int attacker);
void L4D2_Charger_ThrowImpactedSurvivor(int victim, int attacker);
void L4D2_Charger_StartCarryingVictim(int victim, int attacker);
void L4D2_Charger_PummelVictim(int victim, int attacker);
void L4D2_Charger_EndPummel(int victim, int attacker);
void L4D2_Charger_EndCarry(int victim, int attacker);
void L4D_Hunter_ReleaseVictim(int victim, int attacker);
void L4D_Smoker_ReleaseVictim(int victim, int attacker);

// ── Animation ──
bool AnimHookEnable(int client, AnimHookCallback cb, AnimHookCallback cbPost=INVALID_FUNCTION);
bool AnimHookDisable(int client, AnimHookCallback cb, AnimHookCallback cbPost=INVALID_FUNCTION);
bool AnimGetActivity(int sequence, char[] activity, int maxlength);
int AnimGetFromActivity(char[] activity);

// ── Memory ──
Address L4D_GetPointer(int ptr_type);
int L4D_GetClientFromAddress(Address addy);
int L4D_GetEntityFromAddress(Address addy);
int L4D_ReadMemoryString(Address addy, char[] buffer, int maxlength);
void L4D_WriteMemoryString(Address addy, const char[] buffer);
void L4D_PrecacheParticle(const char[] sEffectName);
int L4D_GetServerOS();  // 0=Windows, 1=Linux
int Left4DHooks_Version();
bool L4D_HasMapStarted();

// ── Projectile Creation ──
int L4D_TankRockPrj(int client, const float vp[3], const float va[3], const float vv[3]);
int L4D_PipeBombPrj(int client, const float vp[3], const float va[3], bool ef, const float vv[3], const float vr[3]);
int L4D_MolotovPrj(int client, const float vp[3], const float va[3], const float vv[3], const float vr[3]);
int L4D2_VomitJarPrj(int client, const float vp[3], const float va[3], const float vv[3], const float vr[3]);
int L4D2_GrenadeLauncherPrj(int client, const float vp[3], const float va[3], const float vv[3], const float vr[3], bool bIncendiary);
int L4D2_SpitterPrj(int client, const float vp[3], const float va[3], const float vv[3], const float vr[3]);

// ── Navigation ──
Address L4D_GetNearestNavArea(const float vecPos[3], float maxDist, bool anyZ, bool checkLOS, bool checkGround, int teamID);
Address L4D_GetLastKnownArea(int client);
bool L4D_IsTouchingTrigger(int trigger, int entity);
void L4D_FindRandomSpot(Address NavArea, float vecPos[3]);
bool L4D2_IsVisibleToPlayer(int client, const float vecPos[3], int team, int team_target, Address NavArea);
bool L4D2_IsReachable(int client, const float vecPos[3]);
float L4D2_NavAreaTravelDistance(const float s[3], const float e[3], bool ignoreNavBlockers = false);
bool L4D2_NavAreaBuildPath(Address ns, Address ne, float maxLen, int team, bool ignoreNavBlockers);
```

---

## l4d2util Constants

```sourcepawn
#include <l4d2util>

// ── Life States ──
#define LIFE_ALIVE      0
#define LIFE_DYING      1
#define LIFE_DEAD       2
#define LIFE_RESPAWNABLE 3
#define LIFE_DISCARDBODY 4

// ── Teams ──
#define TEAM_SPECTATOR  1
#define TEAM_SURVIVOR   2
#define TEAM_ZOMBIE     3
#define TEAM_L4D1_SURVIVOR  4
enum L4D2Team { L4D2Team_None=0, _Spectator, _Survivor, _Infected, _L4D1_Survivor, L4D2Team_Size=5 };

// ── Infected Types ──
#define ZC_SMOKER   1
#define ZC_BOOMER   2
#define ZC_HUNTER   3
#define ZC_SPITTER  4
#define ZC_JOCKEY   5
#define ZC_CHARGER  6
#define ZC_WITCH    7
#define ZC_TANK     8
enum L4D2Infected { L4D2Infected_Common=0, _Smoker=1, _Boomer, _Hunter, _Spitter, _Jockey, _Charger, _Witch, _Tank, L4D2Infected_Size=9 };

// ── Hit Groups ──
#define HITGROUP_GENERIC  0
#define HITGROUP_HEAD     1
#define HITGROUP_CHEST    2
#define HITGROUP_STOMACH  3
#define HITGROUP_LEFTARM  4
#define HITGROUP_RIGHTARM 5
#define HITGROUP_LEFTLEG  6
#define HITGROUP_RIGHTLEG 7
#define HITGROUP_GEAR     10

// ── Weapon Slots ──
enum L4D2WeaponSlot {
    L4D2WeaponSlot_Primary=0, _Secondary, _Throwable, _HeavyHealth, _Melee, _Carry
};
// Full WeaponId table (239 entries) in l4d2util_constants.inc
// Key IDs: WEPID_PISTOL=1, WEPID_SMG=2, WEPID_PUMPSHOTGUN=3, WEPID_AUTOSHOTGUN=4
//          WEPID_RIFLE=5, WEPID_HUNTING_RIFLE=6, WEPID_SMG_SILENCED=7
//          WEPID_SHOTGUN_CHROME=8, WEPID_RIFLE_DESERT=9, WEPID_SNIPER_MILITARY=10
//          WEPID_SHOTGUN_SPAS=11, WEPID_RIFLE_AK47=33, etc.

// ── Survivor Characters ──
enum SurvivorCharacterType { L4D2Survivor_Nick=0, _Rochelle, _Coach, _Ellis, _Bill, _Zoey, _Francis, _Louis, _Size };
stock const char g_sSurvivorName[][] = {"Nick","Rochelle","Coach","Ellis","Bill","Zoey","Francis","Louis"};

// ── Spawn Flags ──
#define SPAWNFLAG_DISABLED      (1<<0)
#define SPAWNFLAG_WAITFORSURVIVORS (1<<1)
#define SPAWNFLAG_WAITFORFINALE (1<<2)
#define SPAWNFLAG_WAITFORTANKTODIE (1<<3)
#define SPAWNFLAG_SURVIVORESCAPED (1<<4)
#define SPAWNFLAG_DIRECTORTIMEOUT (1<<5)
#define SPAWNFLAG_CANBESEEN     (1<<7)
#define SPAWNFLAG_TOOCLOSE      (1<<8)
#define SPAWNFLAG_RESTRICTEDAREA (1<<9)
#define SPAWNFLAG_BLOCKED       (1<<10)
```

---

## Colored Chat

### colors.inc API
```sourcepawn
#include <colors>
// L4D2 color profile: Green→Server(0), Blue→Surv(2), Red→Inf(3)
// Supported: {default} {green} {olive} {teamcolor} (SayText2=true)

C_PrintToChat(client, "msg", ...);
C_PrintToChatAll("msg", ...);
C_PrintToChatEx(client, author, "msg", ...);
C_PrintToChatAllEx(author, "msg", ...);
C_ReplyToCommand(client, "msg", ...);
C_ReplyToCommandEx(client, author, "msg", ...);
C_RemoveTags(char[] msg, int maxlen);
C_SkipNextClient(int client);
C_ShowActivity(int client, const char[] format, ...);
C_ShowActivity2(int client, const char[] tag, const char[] format, ...);
C_ShowActivityEx(int client, const char[] tag, const char[] format, ...);

// All color tags: {default}{darkred}{green}{lightgreen}{red}{blue}{olive}{lime}
// {lightred}{purple}{grey}{yellow}{orange}{bluegrey}{lightblue}{darkblue}{grey2}{orchid}{lightred2}
```

### multicolors.inc
```sourcepawn
#include <multicolors>           // or #include <multicolors/morecolors>
// Extended color sets; auto-detects engine version for correct profile.
```

---

## L4D2 Game Events (Full Catalog)

### player_death
```
short userid, long entityid, short attacker, string attackername, long attackerentid
string weapon, bool headshot, bool attackerisbot, string victimname, bool victimisbot
bool abort, long type, float victim_x, float victim_y, float victim_z
```

### player_hurt
```
local(not networked), short userid, short attacker, long attackerentid
short health, byte armor, string weapon, short dmg_health, byte dmg_armor
byte hitgroup, long type
```

### player_team
```
short userid, byte team, byte oldteam, bool disconnect, string name, bool isbot
```

### player_incapacitated
```
short userid, short attacker, long attackerentid, string weapon, long type
```

### player_spawn
```
short userid
```

### player_first_spawn
```
short userid, bool isbot (all 4 survivors spawned)
```

### player_left_safe_area
```
short userid
```

### player_left_start_area
```
short userid
```

### player_entered_checkpoint
```
short userid
```

### player_left_checkpoint
```
short userid
```

### player_ledge_grab
```
short userid (who grabbed), short causer (who caused it)
```

### player_ledge_release
```
short userid (who released)
```

### player_falldamage
```
short userid, float damage, short causer
```

### player_shoved
```
short userid (shover), short victimid
```

### entity_shoved
```
short userid, short victimid
```

### player_jump / player_jump_apex
```
short userid
```

### player_blocked
```
short userid, short blocker
```

### player_blind
```
short userid
```

### player_footstep
```
short userid
```

### player_bot_replace
```
short player (user ID), short bot (user ID)
```

### bot_player_replace
```
short bot, short player
```

### player_afk
```
short player
```

### player_now_it / player_no_longer_it
```
short userid, short attacker
```

### revive_begin
```
short userid, short subject
```

### revive_success / revive_end
```
short userid, short subject, bool ledge_hang (was hanging from ledge)
```

### heal_begin
```
short userid (healer), short subject
```

### heal_success
```
short userid, short subject, short health_restored
```

### heal_end / heal_interrupted
```
short userid, short subject
```

### defibrillator_begin
```
short userid, short subject
```

### defibrillator_used
```
short userid, short subject
```

### defibrillator_used_fail / defibrillator_interrupted
```
short userid, short subject
```

### pills_used
```
short userid, short subject
```

### pills_used_fail
```
short userid (failed to use pills)
```

### adrenaline_used
```
short userid
```

### ammo_pack_used
```
short userid, short subject
```

### upgrade_pack_begin / upgrade_pack_used
```
short userid
```

### weapon_fire
```
local, short userid, string weapon, short weaponid, short count
```

### weapon_fire_on_empty
```
local, short userid, string weapon, short count
```

### weapon_reload
```
short userid, bool manual
```

### weapon_zoom
```
short userid
```

### weapon_given
```
short userid (giver), short recipient, string weapon
```

### weapon_drop
```
short userid, long weaponid (entity), bool isdeath
```

### weapon_pickup
```
short userid, string weapon
```

### item_pickup
```
short userid, string item
```

### melee_kill
```
short userid, short weaponid
```

### ability_use
```
short userid, string ability (ability_tongue/ability_vomit/ability_lunge/ability_spit/ability_charge/ability_throw), short context
```

### ability_out_of_range
```
short userid
```

### tongue_grab
```
short userid (smoker), short victim
```

### tongue_release
```
short userid, short victim
```

### tongue_broke_bent / tongue_broke_victim_died
```
short userid, short victim
```

### choke_start / choke_end / choke_stopped / tongue_pull_stopped
```
short userid, short victim
```

### lunge_shove
```
short userid (hunter), short victim
```

### lunge_pounce
```
short userid, short victim
```

### pounce_end / pounce_stopped / pounce_attempt_stopped
```
short userid, short victim
```

### charger_charge_start
```
short userid
```

### charger_charge_end
```
short userid
```

### charger_carry_start
```
short userid (charger), short victim
```

### charger_carry_end / charger_pummel_start / charger_pummel_end
```
short userid, short victim
```

### charger_impact
```
short userid
```

### charger_killed
```
short userid, short attacker
```

### jockey_ride
```
short userid (jockey), short victim
```

### jockey_ride_end
```
short userid, short victim, float ride_length
```

### jockey_killed
```
short userid, short attacker
```

### spitter_killed
```
short userid, short attacker
```

### hunter_punched / hunter_headshot / jockey_punched / jockey_headshot
```
short userid, short attacker, bool dead
```

### tank_spawn
```
short userid
```

### tank_killed
```
short userid, short attacker, bool solo
```

### tank_frustrated
```
short userid
```

### tank_rock_killed
```
short userid, short attacker
```

### witch_spawn
```
short witchid
```

### witch_killed
```
short witchid, short userid (killer), bool oneshot
```

### witch_harasser_set
```
short userid, short witchid
```

### boomer_exploded / boomer_near
```
short userid
```

### zombie_ignited
```
short userid, short attacker
```

### infected_hurt (Witch + Common)
```
short entityid (entity index), short attacker, short health, byte hitgroup, long type, short amount
```

### infected_death (Witch + Common)
```
short entityid, short attacker
```

### infected_decapitated
```
short userid, short attacker
```

### fatal_vomit
```
short userid
```

### survivor_call_for_help
```
short userid, short subject (who needs rescuing)
```

### survivor_rescued
```
short userid (rescuer), short subject, short rescuee
```

### survivor_rescue_abandoned
```
short userid, short subject
```

### dead_survivor_visible
```
short userid, short subject
```

### ── Doors ──
```
door_open:       short userid, bool checkpoint, bool closed
door_close:      short userid, bool checkpoint
door_unlocked:   short userid, bool checkpoint
door_moving:     long entindex, short userid
rescue_door_open: short userid, long entindex
waiting_checkpoint_door_used: short userid, long entindex
```

### ── Round / Game Flow ──
```
round_start / round_end: byte winner, byte reason, string message, float time
round_start_pre_entity / round_start_post_nav / round_freeze_end: (no fields)
round_end_message: byte winner, byte reason, string message
map_transition: (no fields)
player_transitioned: short userid
nav_blocked: long area, bool blocked
nav_generate: (no fields)
```

### ── Finale ──
```
finale_start:         short userid
finale_rush:          short userid (panic event finisher)
finale_escape_start:  short userid
finale_vehicle_incoming: (no fields)
finale_vehicle_ready: (no fields)
finale_vehicle_leaving: (no fields)
finale_win:           byte winner, ...
mission_lost:         ...
finale_radio_start / finale_radio_damaged: ...
final_reportscreen:   ...
gauntlet_finale_start: ...
```

### ── Versus ──
```
versus_round_start: (no fields)
versus_match_finished: byte winners
versus_marker_reached: short userid, byte marker
```

### ── Scavenge ──
```
scavenge_round_start: (no fields)
scavenge_round_halftime: (no fields)
scavenge_round_finished: (no fields)
scavenge_match_finished: byte winners
scavenge_score_tied: (no fields)
begin_scavenge_overtime: (no fields)
scavenge_gas_can_destroyed: short userid
gascan_pour_blocked / gascan_pour_completed / gascan_dropped / gascan_pour_interrupted: short userid
```

### ── Misc ──
```
vote_started: string issue, string param1, string votedata, byte team, long initiator, reliable
vote_ended / vote_passed / vote_failed / vote_changed / vote_cast_yes / vote_cast_no
hostname_changed / difficulty_changed
achievement_earned: short player, int achievement
award_earned: short userid, byte award (survived/left4dead)
break_breakable: long entindex, short userid, byte material
create_panic_event: short userid (0 if not player-initiated)
ghost_spawn_time: short userid, float time
player_talking_state: short userid, bool talking
molotov_thrown: short userid
gas_can_forced_drop: short userid
mounted_gun_start / mounted_gun_overheated: short userid
chair_charged: short userid, short victim
m60_streak_ended: short userid
song_played: short userid, string song
foot_locker_opened: short userid
strongman_bell_knocked_off: short userid
stashwhacker_game_won: short userid
spit_burst / entered_spit: short userid
vomit_bomb_tank: short userid
triggered_car_alarm: short userid
area_cleared: ...
```

### ── Explain / Tutorial Events ──
```
explain_pills, explain_weapons, explain_pre_radio, started_pre_radio, explain_radio
explain_gas_truck, explain_panic_button, explain_elevator_button, explain_lift_button
explain_church_door, explain_emergency_door, explain_crane, explain_bridge
explain_gas_can_panic, explain_van_panic, explain_mainstreet, explain_train_lever
explain_disturbance, explain_scavenge_goal, explain_scavenge_leave_area
explain_pre_drawbridge, explain_drawbridge, explain_perimeter, explain_deactivate_alarm
explain_impound_lot, explain_decon, explain_mall_window, explain_mall_alarm
explain_coaster, explain_coaster_stop, explain_decon_wait, explain_float
explain_ferry_button, explain_hatch_button, explain_shack_button, explain_vehicle_arrival
explain_burger_sign, explain_carousel_button, explain_carousel_destination
explain_stage_lighting, explain_stage_finale_start, explain_stage_survival_start
explain_stage_pyrotechnics, explain_c3m4_radio1, explain_c3m4_radio2
explain_gates_are_open, explain_c2m4_ticketbooth, explain_c3m4_rescue
explain_hotel_elevator_doors, explain_gun_shop_tanker, explain_gun_shop
explain_store_alarm, explain_store_item, explain_store_item_stop
explain_survival_generic, explain_survival_alarm, explain_survival_radio
explain_survival_carousel, explain_return_item, explain_save_items
explain_need_gnome_to_continue, explain_survivor_glows_disabled
explain_item_glows_disabled, explain_rescue_disabled, explain_bodyshots_reduced
explain_witch_instant_kill, explain_sewer_gate, explain_sewer_run, explain_c6m3_finale
temp_c4m1_getgas, temp_c4m3_return_to_boat
```

### ── Survival ──
```
survival_round_start: (no fields)
survival_at_30min / survival_at_10min: short numplayers
```

---

## DirectorOptions (Full Reference)

### General Options
| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `AlwaysAllowWanderers` | bool | false | Allow wandering witches anywhere |
| `BuildUpMinInterval` | int | 15 | Min seconds BUILD_UP stage lasts |
| `ClearedWandererRespawnChance` | int | 0 (3 in Scavenge) | % chance cleared nav areas repopulate with wanderers |
| `DisallowThreatType` | int | — | Bitflag: ZOMBIE_WITCH, ZOMBIE_TANK |
| `FarAcquireRange` | float | 2500.0 | Max range CI can spot survivors |
| `NearAcquireRange` | float | 200.0 | Min range CI can instantly spot survivors |
| `FarAcquireTime` | float | 5.0 | Time to acquire at max range |
| `NearAcquireTime` | float | 0.5 | Time to acquire at min range |
| `GasCansOnBacks` | bool | false | Hard Rain diesel cans on backs |
| `IgnoreNavThreatAreas` | bool | false | Prevent bosses spawning along nav |
| `InfectedFlags` | int | 0 | Flags for new CI: INFECTED_FLAG_CANT_SEE/CANT_HEAR/CANT_FEEL_SURVIVORS |
| `IntensityRelaxAllowWanderersThreshold` | float | 0.8/0.5/0.3 | Below this survivor max intensity→wandering CI can spawn |
| `IntensityRelaxThreshold` | float | 0.9 | Survivors must be below this before Peak→Relax transition |
| `LockTempo` | bool | false (true in finales) | Lock Director in BUILD_UP phase |
| `MobRechargeRate` | float | 0.0025 | How fast mob CI spawn between each other |
| `MobSpawnMaxTime` | float | 180-240 | Max seconds between mob spawns (difficulty-dependent) |
| `MobSpawnMinTime` | float | 90-120 | Min seconds between mob spawns (difficulty-dependent) |
| `MusicDynamicMobScanStopSize` | int | 3 | Fewer than this many → mob music stops |
| `MusicDynamicMobSpawnSize` | int | 25 | Spawning mob this large → play mob music |
| `MusicDynamicMobStopSize` | int | 8 | Mob reaches this size → think about stopping music |
| `NumReservedWanderers` | int | 0 | Wandering CI that cannot be despawned for mobs |
| `PanicForever` | bool | false | Only in gauntlets |
| `PreferredMobDirection` | int | -1 | SPAWN_ABOVE/BEHIND/IN_FRONT/ANYWHERE/LARGE_VOLUME/NEAR_IT_VICTIM/NEAR_POSITION/NO_PREFERENCE/FAR_AWAY |
| `PreferredSpecialDirection` | int | -1 | Same values + SPAWN_SPECIALS_IN_FRONT/SPAWN_SPECIALS_ANYWHERE |
| `ProhibitBosses` | bool | false | Prohibit Tank+Witch in THREAT areas (campaign only) |
| `RelaxMaxFlowTravel` | float | 3000 | Flow advance before RELAX→BUILD_UP transition |
| `RelaxMaxInterval` | float | 45 | Max seconds in RELAX |
| `RelaxMinInterval` | float | 30 | Min seconds in RELAX |
| `ShouldAllowMobsWithTank` | bool | false | Allow mob spawns when tank active (campaign only) |
| `ShouldAllowSpecialsWithTank` | bool | false | Allow SI spawns when tank active (⚠ spawns by time, not tempo) |
| `SpecialInitialSpawnDelayMax` | float | 60.0 | SI can't spawn for this max time after leaving saferoom |
| `SpecialInitialSpawnDelayMin` | float | 30.0 | SI can't spawn for this min time after leaving saferoom |
| `SpecialRespawnInterval` | float | 45(Campaign)/10(Finale)/20(Versus) | Seconds before SI slot can respawn |
| `SurvivorMaxIncapacitatedCount` | int | 2 | Max incapacitations before death |
| `SustainPeakMaxTime` | float | 5 | Max SUSTAIN_PEAK (minutes) |
| `SustainPeakMinTime` | float | 3 | Min SUSTAIN_PEAK (minutes) |
| `TankHitDamageModifierCoop` | float | 1.0 | Tank damage multiplier (non-PvP) |
| `WanderingZombieDensityModifier` | float | 0.027(vs)/0.03(other) | Wandering CI density multiplier |
| `WaterSlowsMovement` | bool | true | Apply slowdown in water |
| `ZombieDiscardRange` | int | 2500 | Delete CI / suicide SI beyond this distance |
| `ZombieDontClear` | bool | false | Don't mark nav as cleared |
| `ZombieSpawnInFog` | bool | false | Allow spawning in LOS in fog |
| `ZombieSpawnRange` | float | 1500.0 | Max spawn distance from survivors |
| `ZombieTankHealth` | float | 4000.0 | Tank base health (×0.75 Easy, ×2 Advanced/Expert, ×1.5 Versus) |

### Spawning Limits
| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `BileMobSize` | int | — | CI count for bile/vomit mob |
| `BoomerLimit` | int | 1 | Max Boomers in play |
| `ChargerLimit` | int | 1 | Max Chargers in play |
| `CommonLimit` | int | 30 | Max CI in play |
| `DominatorLimit` | int | 2 | Max dominator types (Hunter/Smoker/Jockey/Charger) at their caps; extra capped at 1 |
| `HunterLimit` | int | 1 | Max Hunters in play |
| `JockeyLimit` | int | 1 | Max Jockeys in play |
| `MaxSpecials` | int | 2 | Max Director-spawned SI in play |
| `MegaMobSize` | int | 50 | Total infected during panic event |
| `MobMaxPending` | int | -1 | Pending infected when mob exceeds CommonLimit |
| `MobMaxSize` | int | 30 | Max infected per mob |
| `MobMinSize` | int | 10 | Min infected per mob |
| `MobSpawnSize` | int | — | Static mob size (overrides Min/Max) |
| `SmokerLimit` | int | 1 | Max Smokers in play |
| `SpitterLimit` | int | 1 | Max Spitters in play |
| `TankLimit` | int | -1 | Max Tanks in play (-1 = unlimited) |
| `WitchLimit` | int | -1 | Max Witches in play (-1 = unlimited) |

### EMS Stage Specific
| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `ScriptedStageType` | int | 9 (STAGE_NONE) | Next stage: STAGE_PANIC=0, STAGE_TANK=1, STAGE_DELAY=2, STAGE_CLEAROUT=4, STAGE_SETUP=5, STAGE_ESCAPE=7, STAGE_RESULTS=8, STAGE_NONE=9 |
| `ScriptedStageValue` | int | 1 | Depends on stage type |
| `SpawnSetRule` | int | 0 | SPAWN_FINALE=0, SPAWN_SURVIVORS=1, SPAWN_BATTLEFIELD=2, SPAWN_POSITIONAL=3 |
| `SpawnSetPosition` | Vector | — | Center of spawn area (when SPAWN_POSITIONAL) |
| `SpawnSetRadius` | float | 1000.0 | Spawn radius (when SPAWN_POSITIONAL) |
| `SpawnDirectionMask` | int | 0 | Bitmask: SPAWNDIR_N, _NE, _E, _SE, _S, _SW, _W, _NW |
| `TotalBoomers/Chargers/Hunters/Jockeys/Smokers/Spitters/Specials` | int | 0/varying | Per-wave SI counts |

### Finale Specific
| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `[A-E]_CustomFinale_StageCount` | int | — | Number of finale stages |
| `[A-E]_CustomFinaleX` | int | — | Stage X type: PANIC, SCRIPTED, DELAY, TANK |
| `[A-E]_CustomFinaleValueX` | any | — | Stage value |
| `[A-E]_CustomFinaleMusicX` | string | — | Soundscript entry |
| `HordeEscapeCommonLimit` | int | -1 | CI count in escape stage |
| `EscapeSpawnTanks` | bool | true | Spawn tanks in escape |
| `MinimumStageTime` | float | 1.0 | Min seconds for SCRIPTED stage |

### Gauntlet
| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `CustomTankKiteDistance` | float | 3000.0 | Flow distance to trigger Gauntlet Tank wave |
| `GauntletMovementThreshold` | float | 500.0 | Flow advance to reset Movement Bonus |
| `GauntletMovementTimerLength` | float | 5.0 | Seconds between Bonus increases |
| `GauntletMovementBonus` | float | 2.0 | Bonus increment per tick (seconds) |
| `GauntletMovementBonusMax` | float | 30.0 | Max Movement Bonus stored |

### Versus
| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `TankHitDamageModifierVersus` | float | 1.0 | Tank damage multiplier (PvP) |
| `ZombieGhostDelayMax` | float | 30.0 | Max respawn wait (seconds) |
| `ZombieGhostDelayMin` | float | 20.0 | Min respawn wait (seconds) |

### Scavenge
| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `ScavengeRoundInitialTime` | float | 90.0 | Timer length at round start |
| `ScavengeScoreBonusTime` | float | 15.0 | Time added per pour |

### Mutation (cm_*) Keys
| Key | Description |
|-----|-------------|
| `cm_CommonLimit` | Overrides `CommonLimit` |
| `cm_MaxSpecials` | Overrides `MaxSpecials` |
| `cm_ProhibitBosses` | Overrides `ProhibitBosses` |
| `cm_TankLimit` / `cm_WitchLimit` | Override Tank/Witch limits |
| `cm_SpecialRespawnInterval` | Override special respawn interval |
| `cm_WanderingZombieDensityModifier` | Override wanderer density |
| `cm_BaseSpecialLimit` | Default cap for all SI types |
| `cm_AggressiveSpecials` | bool — SI go straight after survivors |
| `cm_AllowPillConversion` | bool=true — Pills→health kits in non-Expert |
| `cm_AllowSurvivorRescue` | bool — Respawn in rescue closets |
| `cm_AutoReviveFromSpecialIncap` | bool — Instantly revive when incapped by SI |
| `cm_HeadshotOnly` | bool — Only headshots damage CI (Tanks excepted) |
| `cm_FirstManOut` | bool — First survivor reaching vehicle = escape end |
| `cm_HealingGnome` | bool — Temp health + gnome regen (Healing Gnome mutation) |
| `cm_InfiniteFuel` | bool — (Chainsaw Massacre mutation) |
| `cm_NoSurvivorBots` | bool — Kick survivor bots on round start |
| `cm_ShouldHurry` | bool — Bots rush like Versus |
| `cm_TankRun` | bool — Bypass c7m1 second train door (Tank Run mutations) |
| `cm_TempHealthOnly` | bool — Health decays, only temp health |
| `cm_VIPTarget` | bool — Spawn gnome that must be carried (Last Gnome on Earth) |
| `TempHealthDecayRate` | float=0.27 — Higher = faster decay; directly modifies `pain_pills_decay_rate` cvar |
| `NoMobSpawns` | bool=false — Prevent new mob spawns (pending still spawn) |

### Callback Functions
```
AllowFallenSurvivorItem(string classname) → bool
AllowWeaponSpawn(string classname) → bool
ConvertWeaponSpawn(string classname) → string
ConvertZombieClass(int zombieType) → int
EndScriptedMode() → int
GetDefaultItem(int index) → string
ShouldAvoidItem(string classname) → bool
ShouldPlayBossMusic(int index) → bool
```

### Enumerations
```
// AllowBash
ALLOW_BASH_ALL=0, ALLOW_BASH_PUSHONLY=1, ALLOW_BASH_NONE=2

// Bot Sense Flags (bitmask)
BOT_CANT_SEE=1, BOT_CANT_HEAR=2, BOT_CANT_FEEL=4

// CommandABot
BOT_CMD_ATTACK=0, BOT_CMD_MOVE=1, BOT_CMD_RETREAT=2, BOT_CMD_RESET=3

// DMG types (bitmask)
DMG_BULLET=2, DMG_BURN=8, DMG_BLAST=64(0x40), DMG_MELEE=2097152(0x200000)
DMG_STUMBLE=33554432(0x2000000), DMG_BLAST_SURFACE=134217728(0x8000000)
DMG_BUCKSHOT=536870912(0x20000000), DMG_HEADSHOT=1073741824(0x40000000)

// Finale stages
FINALE_GAUNTLET_1=0, FINALE_HORDE_ATTACK_1=1, FINALE_HALFTIME_BOSS=2
FINALE_GAUNTLET_2=3, FINALE_HORDE_ATTACK_2=4, FINALE_FINAL_BOSS=5
FINALE_HORDE_ESCAPE=6, FINALE_CUSTOM_PANIC=7, FINALE_CUSTOM_TANK=8
FINALE_CUSTOM_SCRIPTED=9, FINALE_CUSTOM_DELAY=10, FINALE_CUSTOM_CLEAROUT=11
FINALE_GAUNTLET_START=12, FINALE_GAUNTLET_HORDE=13, FINALE_GAUNTLET_HORDE_BONUSTIME=14
FINALE_GAUNTLET_BOSS_INCOMING=15, FINALE_GAUNTLET_BOSS=16, FINALE_GAUNTLET_ESCAPE=17

// HUD flags
HUD_FLAG_PRESTR=1, HUD_FLAG_POSTSTR=2, HUD_FLAG_BEEP=4, HUD_FLAG_BLINK=8
HUD_FLAG_AS_TIME=16, HUD_FLAG_COUNTDOWN_WARN=32, HUD_FLAG_NOBG=64
HUD_FLAG_ALLOWNEGTIMER=128, HUD_FLAG_ALIGN_LEFT=256, HUD_FLAG_ALIGN_CENTER=512
HUD_FLAG_ALIGN_RIGHT=768, HUD_FLAG_TEAM_SURVIVORS=1024, HUD_FLAG_TEAM_INFECTED=2048
HUD_FLAG_NOTVISIBLE=16384

// HUD slots
HUD_LEFT_TOP=0, HUD_LEFT_BOT=1, HUD_MID_TOP=2, HUD_MID_BOT=3
HUD_RIGHT_TOP=4, HUD_RIGHT_BOT=5, HUD_TICKER=6, HUD_FAR_LEFT=7
HUD_FAR_RIGHT=8, HUD_MID_BOX=9

// HUD Print
HUD_PRINTNOTIFY=1, HUD_PRINTCONSOLE=2, HUD_PRINTTALK=3, HUD_PRINTCENTER=4

// Input buttons (bitmask)
IN_ATTACK=1, IN_JUMP=2, IN_DUCK=4, IN_FORWARD=8, IN_BACK=16, IN_USE=32
IN_CANCEL=64, IN_LEFT=512, IN_RIGHT=1024, IN_ATTACK2=2048, IN_RELOAD=8192

// Nav directions
NAV_NORTH=0, NAV_EAST=1, NAV_SOUTH=2, NAV_WEST=3

// Spawn directions (bitmask)
SPAWNDIR_N=1, SPAWNDIR_NE=2, SPAWNDIR_E=4, SPAWNDIR_SE=8
SPAWNDIR_S=16, SPAWNDIR_SW=32, SPAWNDIR_W=64, SPAWNDIR_NW=128

// Preferred Spawn Directions
SPAWN_NO_PREFERENCE=-1, SPAWN_ANYWHERE=0, SPAWN_BEHIND_SURVIVORS=1
SPAWN_NEAR_IT_VICTIM=2, SPAWN_SPECIALS_IN_FRONT_OF_SURVIVORS=3
SPAWN_SPECIALS_ANYWHERE=4, SPAWN_FAR_AWAY_FROM_SURVIVORS=5
SPAWN_ABOVE_SURVIVORS=6, SPAWN_IN_FRONT_OF_SURVIVORS=7
SPAWN_VERSUS_FINALE_DISTANCE=8, SPAWN_LARGE_VOLUME=9, SPAWN_NEAR_POSITION=10

// Trace masks
TRACE_MASK_ALL=-1, TRACE_MASK_VISION=33579073, TRACE_MASK_VISIBLE_AND_NPCS=33579137
TRACE_MASK_PLAYER_SOLID=33636363, TRACE_MASK_NPC_SOLID=33701899, TRACE_MASK_SHOT=1174421507

// Upgrades
UPGRADE_INCENDIARY_AMMO=0, UPGRADE_EXPLOSIVE_AMMO=1, UPGRADE_LASER_SIGHT=2

// ZSpawn types
ZOMBIE_NORMAL=0, ZOMBIE_SMOKER=1, ZOMBIE_BOOMER=2, ZOMBIE_HUNTER=3
ZOMBIE_SPITTER=4, ZOMBIE_JOCKEY=5, ZOMBIE_CHARGER=6, ZOMBIE_WITCH=7
ZOMBIE_TANK=8, ZSPAWN_MOB=10, ZSPAWN_WITCHBRIDE=11, ZSPAWN_MUDMEN=12
```

---

## Common Netprops

```sourcepawn
// Survivor
GetEntProp(client, Prop_Send, "m_isIncapacitated");       // bool
GetEntProp(client, Prop_Send, "m_isHangingFromLedge");    // bool
GetEntProp(client, Prop_Send, "m_isGhost");               // bool
GetEntProp(client, Prop_Send, "m_zombieClass");           // int
GetEntProp(client, Prop_Send, "m_iHealth");               // int
GetEntProp(client, Prop_Send, "m_currentReviveCount");    // int
GetEntProp(client, Prop_Send, "m_reviveOwner");           // entity
GetEntProp(client, Prop_Send, "m_reviveTarget");          // entity
GetEntPropFloat(client, Prop_Send, "m_healthBuffer");     // float (temp HP)
GetEntPropFloat(client, Prop_Send, "m_flFlowDistance");   // float
GetEntProp(client, Prop_Send, "m_isCalm");                // bool

// Tank
GetEntProp(client, Prop_Send, "m_frustration");           // int
GetEntProp(client, Prop_Send, "m_isInStasis");            // bool

// Weapon
GetEntPropEnt(client, Prop_Send, "m_hActiveWeapon");      // entity
GetEntProp(weapon, Prop_Send, "m_iClip1");                // int
GetEntProp(weapon, Prop_Send, "m_iPrimaryAmmoType");      // int
GetEntProp(weapon, Prop_Send, "m_upgradeBitVec");         // int

// Full dumps at:
// Desktop\sourcepawn\Left 4 Dead 2 netprop dump.txt    (16581 lines)
// Desktop\sourcepawn\Left 4 Dead 2 datamap dump.txt    (15378 lines)
```

---

## Plugin Template

```sourcepawn
#include <sourcemod>
#include <sdktools>
#include <sdkhooks>
#include <left4dhooks>
#include <l4d2util>
#include <colors>

#define PLUGIN_VERSION "1.0.0"
public Plugin myinfo = {
    name = "My Plugin", author = "...", description = "...",
    version = PLUGIN_VERSION, url = ""
};

ConVar g_cvEnable; bool g_bLate;

public APLRes AskPluginLoad2(Handle me, bool late, char[] err, int m) {
    g_bLate = late; return APLRes_Success;
}

public void OnPluginStart() {
    g_cvEnable = CreateConVar("sm_myplugin_enable", "1", "Enable plugin");
    AutoExecConfig(true, "myplugin");
    HookEvent("round_start", OnRoundStart);
}

public void OnConfigsExecuted() {
    if (!g_cvEnable.BoolValue) return;
}

public void OnMapStart() { /* Precache models/sounds here */ }
public void OnPluginEnd() { /* Kill timers, close handles */ }

// Helpers
bool IsValidClient(int c) { return c>0 && c<=MaxClients && IsClientInGame(c); }
bool IsSurvivor(int c) { return IsValidClient(c) && GetClientTeam(c)==2 && IsPlayerAlive(c); }
bool IsInfected(int c) { return IsValidClient(c) && GetClientTeam(c)==3 && IsPlayerAlive(c); }
```

## Design Rules

1. **Recompile on every edit** — fix all warnings
2. **Validate all client indexes** — `IsValidClient()` before any use; `GetClientOfUserId()` for event userids
3. **Left4DHooks over raw SDKHooks** — game-specific, battle-tested
4. **Pre/Post/PostHandled hook model** — block in Pre, react in Post, cleanup in PostHandled
5. **Cleanup timers & handles** — `OnPluginEnd()`
6. **Handle late-load** — `g_bLate` flag
7. **AutoExecConfig** — generate `.cfg`
8. **Guard entity operations** — `IsValidEntity()` before Get/SetEntProp
9. **`MaxClients+1` over `MAXPLAYERS`** — runtime-accurate, 1.12-safe
10. **Version-guard 1.12-only APIs** — `#if SOURCEMOD_V_MINOR >= 12`

## Anti-Patterns

| Don't | Do |
|-------|----|
| Hardcode 65 clients | `MaxClients + 1` |
| Block Pre without PostHandled | Provide recovery path |
| 0.1s repeating timer for per-frame work | `OnGameFrame()` or Left4DHooks frame hook |
| Hardcode paths | `BuildPath(Path_SM, ...)` |
| Trust raw userid | `GetClientOfUserId()` + validate |
| `PrintToChat` with tags | `C_PrintToChat` |
| Ignore engine version | `GetEngineVersion()` and `Engine_Left4Dead2` |
| Blindly use 1.12 natives | `#if SOURCEMOD_V_MINOR >= 12` guard |
| Forget to `CloseHandle()` | Track handles; close on unload |

---

## L4D2 Netprop Tables (from full dump)

Source: `Left 4 Dead 2 netprop dump.txt` (16581 lines)

### CTerrorPlayer (DT_TerrorPlayer) — Core L4D2 player properties

```
m_isIncapacitated       (offset 11688)  integer  bits 1   Unsigned
m_isHangingFromLedge    (offset 14853)  integer  bits 1   Unsigned
m_isGhost               (offset 11449)  integer  bits 1   Unsigned
m_isGoingToDie          (offset 13072)  integer  bits 1   Unsigned
m_isCalm                (offset 11916)  integer  bits 1   Unsigned
m_hasVisibleThreats     (offset 12636)  integer  bits 1   Unsigned
m_zombieClass           (offset 11192)  integer  bits 8
m_zombieState           (offset 11932)  integer  bits 8
m_survivorCharacter     (offset 11188)  integer  bits 8
m_healthBuffer          (offset 13060)  float    bits 10
m_healthBufferTime      (offset 13064)  float    bits 0   NoScale
m_reviveOwner           (offset 11832)  integer  bits 21  Unsigned|NoScale
m_currentReviveCount    (via Resource)  integer  bits 8
m_frustration           (offset 14988)  integer  bits 8
m_isInStasis            (inherited)     integer  bits 1
m_staggerTimer          (offset 12804)  DT_CountdownTimer
m_staggerStart          (offset 12816)  vector   bits 0   CoordMP
m_staggerDir            (offset 12828)  vector   bits 0   CoordMP
m_staggerDist           (offset 12840)  float    bits 0   NoScale|CoordMP
m_carryVictim           (offset 10840)  integer  bits 21  Unsigned|NoScale
m_pounceVictim          (offset 15992)  integer  bits 21  Unsigned|NoScale
m_pounceAttacker        (offset 15996)  integer  bits 21  Unsigned|NoScale
m_jockeyVictim          (offset 16112)  integer  bits 21  Unsigned|NoScale
m_tongueVictim          (offset 13268)  integer  bits 21  Unsigned|NoScale
m_pummelVictim          (offset 15960)  integer  bits 21  Unsigned|NoScale
m_survivorsLineOfScrimmageDistance (offset 11312) float bits 0 NoScale
```

### CTerrorPlayerResource (DT_TerrorPlayerResource)
```
m_zombieClass           (offset 2888)  table     array
m_isGhost               (offset 2788)  table     array
m_tankTickets           (offset 3020)  table     array  (m_iTankTickets sub-table)
m_TeamSwitchRule        (offset 3188)  table
m_tankLotteryEntryRatio  (offset 3716) float    bits 0   NoScale
m_tankLotterySelectionRatio (offset 3720) float bits 0 NoScale
m_pendingTankPlayerIndex  (offset 3724) integer  bits 32
```

### Infected (DT_Infected) — Common Infected
```
Inherits CTerrorPlayer properties
Has DT_InfectedAnimationLayer x6 (layers 000-005)
m_nv_witchRage          (offset 392)   float    bits 8
```

### Tank (DT_Tank)
```
Inherits all CTerrorPlayer properties
```

### Witch (DT_Witch)
```
DT_Witch → baseclass DT_Infected → DT_InfectedAnimationLayer x6
m_nv_witchRage          (offset 392)   float    bits 8
```

### Weapon properties (CTerrorPlayer)
```
m_hActiveWeapon         (via CBaseCombatCharacter)
m_iAmmo                (via CBaseCombatCharacter)
```

### L4D2-Specific Entity Tables
```
CTerrorPlayer           DT_TerrorPlayer
Infected                DT_Infected
Tank                    DT_Tank
Witch                   DT_Witch
CTerrorPlayerResource   DT_TerrorPlayerResource
CTerrorGameRules        DT_TerrorGameRules
CSurvivorDeathModel     DT_SurvivorDeathModel
CSurvivorPosition       DT_SurvivorPosition
CSurvivorRescue         DT_SurvivorRescue
CTankClaw               DT_WeaponTankClaw
CFuncPlayerGhostInfectedClip  DT_FuncPlayerGhostInfectedClip
CFuncPlayerInfectedClip       DT_FuncPlayerInfectedClip
COxygenTank             DT_OxygenTank
CPropaneTank            DT_PropaneTank
CSurvivorBot            (shared DT_TerrorPlayer)
```

### Usage Pattern
```sourcepawn
// Read netprop
GetEntProp(client, Prop_Send, "m_isIncapacitated");
GetEntProp(client, Prop_Send, "m_zombieClass");
GetEntProp(client, Prop_Send, "m_isGhost");
GetEntPropFloat(client, Prop_Send, "m_healthBuffer");
GetEntProp(client, Prop_Send, "m_frustration");

// Resource-based (array properties)
int entity = GetPlayerResourceEntity();
GetEntProp(entity, Prop_Send, "m_pendingTankPlayerIndex");
GetEntProp(entity, Prop_Send, "m_tankLotteryEntryRatio");

// Use l4d2util constants for zombie class values:
// ZC_SMOKER=1, ZC_BOOMER=2, ZC_HUNTER=3, ZC_SPITTER=4,
// ZC_JOCKEY=5, ZC_CHARGER=6, ZC_WITCH=7, ZC_TANK=8
```

### Full Dump Search
```bash
# The full dumps are in references/game-data/
findstr /i "<propname>" "references/game-data/netprop-dump.txt"
findstr /i "<propname>" "references/game-data/datamap-dump.txt"
```

---

## SM Official Include API — Full Reference

### sourcemod.inc (Core Plugin API)
```sourcepawn
// ── Plugin Lifecycle ──
forward void OnPluginStart();
forward bool AskPluginLoad(Handle myself, bool late, char[] error, int err_max);
forward APLRes AskPluginLoad2(Handle myself, bool late, char[] error, int err_max);
forward void OnPluginEnd();
forward void OnPluginPauseChange(bool pause);
forward void OnGameFrame();
forward void OnMapInit(const char[] mapName);
forward void OnMapStart();
forward void OnMapEnd();
forward void OnConfigsExecuted();
forward void OnAutoConfigsBuffered();
forward void OnServerCfg();
forward void OnAllPluginsLoaded();

// ── Plugin Management ──
native Handle GetMyHandle();
native Handle GetPluginIterator();
native bool MorePlugins(Handle iter);
native Handle ReadPlugin(Handle iter);
native PluginStatus GetPluginStatus(Handle plugin);
native void GetPluginFilename(Handle plugin, char[] buffer, int maxlength);
native bool IsPluginDebugging(Handle plugin);
native bool GetPluginInfo(Handle plugin, PluginInfo info, char[] buffer, int maxlength);
native Handle FindPluginByNumber(int order_num);
native void SetFailState(const char[] string, any ...);
native void ThrowError(const char[] fmt, any ...);
native void LogStackTrace(const char[] fmt, any ...);

// ── Time ──
native int GetTime(int bigStamp[2]={0,0});
native void FormatTime(char[] buffer, int maxlength, const char[] format, int stamp=-1);
native int ParseTime(const char[] dateTime, const char[] format);  // 1.12+
native int GetSysTickCount();

// ── GameConfig / Memory ──
native GameData LoadGameConfigFile(const char[] file);
native int GameConfGetOffset(Handle gc, const char[] key);
native bool GameConfGetKeyValue(Handle gc, const char[] key, char[] buffer, int maxlen);
native Address GameConfGetAddress(Handle gameconf, const char[] name);
native any LoadFromAddress(Address addr, NumberType size);
native void StoreToAddress(Address addr, any data, NumberType size, bool updateMemAccess=true);

// ── Config ──
native void AutoExecConfig(bool autoCreate=true, const char[] name="", const char[] folder="sourcemod");

// ── Libraries ──
native void RegPluginLibrary(const char[] name);
native bool LibraryExists(const char[] name);
native int GetExtensionFileStatus(const char[] name, char[] error="", int maxlength=0);
forward void OnLibraryAdded(const char[] name);
forward void OnLibraryRemoved(const char[] name);
forward void OnNotifyPluginUnloaded(Handle plugin);

// ── Map Lists ──
native Handle ReadMapList(Handle array=INVALID_HANDLE, ...);
native void SetMapListCompatBind(const char[] name, const char[] file);

// ── Features ──
stock bool CanTestFeatures();
native FeatureStatus GetFeatureStatus(FeatureType type, const char[] name);
native void RequireFeature(FeatureType type, const char[] name, ...);

// ── Flood Check ──
forward bool OnClientFloodCheck(int client);
forward void OnClientFloodResult(int client, bool blocked);

// ── Version Constants ──
#define SOURCEMOD_V_MAJOR  1
#define SOURCEMOD_V_MINOR  12  // (11 in 1.11)
#define SOURCEMOD_VERSION  "1.12.0-manual"
```

### clients.inc (Client Management)
```sourcepawn
// ── Connection Lifecycle ──
forward bool OnClientConnect(int client, char[] rejectmsg, int maxlen);
forward void OnClientConnected(int client);
forward void OnClientPutInServer(int client);
forward void OnClientDisconnect(int client);
forward void OnClientDisconnect_Post(int client);
forward void OnClientSettingsChanged(int client);
forward void OnClientAuthorized(int client, const char[] auth);
forward Action OnClientPreAdminCheck(int client);
forward void OnClientPostAdminFilter(int client);
forward void OnClientPostAdminCheck(int client);
forward Action OnClientCommand(int client, int args);
forward Action OnClientCommandKeyValues(int client, KeyValues kv);
forward void OnClientCommandKeyValues_Post(int client, KeyValues kv);
forward void OnClientLanguageChanged(int client, int language);
forward void OnServerEnterHibernation();       // 1.12+
forward void OnServerExitHibernation();        // 1.12+

// ── Info ──
native int GetMaxClients();
native int GetMaxHumanPlayers();
native int GetClientCount(bool inGameOnly=true);
native bool GetClientName(int client, char[] name, int maxlen);
native bool GetClientIP(int client, char[] ip, int maxlen, bool remport=true);
native bool GetClientAuthString(int client, char[] auth, int maxlen, bool validate=true);
native bool GetClientAuthId(int client, AuthIdType authType, char[] auth, int maxlen, bool validate=true);
native int GetSteamAccountID(int client, bool validate=true);
native int GetClientUserId(int client);
native int GetClientOfUserId(int userid);
native int GetClientSerial(int client);
native int GetClientFromSerial(int serial);

// ── State Checks ──
native bool IsClientConnected(int client);
native bool IsClientInGame(int client);
native bool IsClientInKickQueue(int client);
native bool IsClientAuthorized(int client);
native bool IsFakeClient(int client);
native bool IsClientSourceTV(int client);
native bool IsClientReplay(int client);
native bool IsClientObserver(int client);
native bool IsPlayerAlive(int client);
native bool IsClientTimingOut(int client);
stock bool IsPlayerInGame(int client);

// ── Properties ──
native int GetClientTeam(int client);
native int GetClientHealth(int client);
native int GetClientArmor(int client);
native int GetClientDeaths(int client);
native int GetClientFrags(int client);
native int GetClientDataRate(int client);
native float GetClientTime(int client);
native void GetClientModel(int client, char[] model, int maxlen);
native void GetClientWeapon(int client, char[] weapon, int maxlen);
native void GetClientMaxs(int client, float vec[3]);
native void GetClientMins(int client, float vec[3]);
native void GetClientAbsAngles(int client, float ang[3]);
native void GetClientAbsOrigin(int client, float vec[3]);

// ── Network Stats ──
native float GetClientLatency(int client, NetFlow flow);
native float GetClientAvgLatency(int client, NetFlow flow);
native float GetClientAvgLoss(int client, NetFlow flow);
native float GetClientAvgChoke(int client, NetFlow flow);
native float GetClientAvgData(int client, NetFlow flow);
native float GetClientAvgPackets(int client, NetFlow flow);

// ── Actions ──
native void KickClient(int client, const char[] format="", any ...);
native void KickClientEx(int client, const char[] format="", any ...);
native void ChangeClientTeam(int client, int team);

// ── Admin ──
native void SetUserAdmin(int client, AdminId id, bool temp=false);
native AdminId GetUserAdmin(int client);
native void AddUserFlags(int client, AdminFlag ...);
native void RemoveUserFlags(int client, AdminFlag ...);
native void SetUserFlagBits(int client, int flags);
native int GetUserFlagBits(int client);
native bool CanUserTarget(int client, int target);
native bool RunAdminCacheChecks(int client);
native void NotifyPostAdminCheck(int client);

// ── Fake Clients ──
native int CreateFakeClient(const char[] name);
native void SetFakeClientConVar(int client, const char[] cvar, const char[] value);

// ── Constants ──
#define MAXPLAYERS  101   // 65 in SM 1.11
#define MAX_NAME_LENGTH 128
```

### entity.inc (Entity Management)
```sourcepawn
// ── Entity Info ──
native int GetMaxEntities();
native int GetEntityCount();
native bool IsValidEntity(int entity);
native bool IsValidEdict(int edict);
native bool IsEntNetworkable(int entity);
native bool GetEdictClassname(int edict, char[] clsname, int maxlength);
native bool GetEntityNetClass(int edict, char[] clsname, int maxlength);
stock bool GetEntityClassname(int entity, char[] clsname, int maxlength);

// ── Create / Destroy ──
native int CreateEdict();
native void RemoveEdict(int edict);
native void RemoveEntity(int entity);
native int GetEdictFlags(int edict);
native void SetEdictFlags(int edict, int flags);
native void ChangeEdictState(int edict, int offset=0);

// ── Raw EntData (offset-based) ──
native int GetEntData(int entity, int offset, int size=4);
native void SetEntData(int entity, int offset, any value, int size=4, bool changeState=false);
native float GetEntDataFloat(int entity, int offset);
native void SetEntDataFloat(int entity, int offset, float value, bool changeState=false);
native int GetEntDataEnt(int entity, int offset);
native void SetEntDataEnt(int entity, int offset, int other, bool changeState=false);
native int GetEntDataEnt2(int entity, int offset);
native void SetEntDataEnt2(int entity, int offset, int other, bool changeState=false);
native void GetEntDataVector(int entity, int offset, float vec[3]);
native void SetEntDataVector(int entity, int offset, const float vec[3], bool changeState=false);
native int GetEntDataString(int entity, int offset, char[] buffer, int maxlen);
native int SetEntDataString(int entity, int offset, const char[] buffer, int maxlen, bool changeState=false);
stock void GetEntDataArray(int entity, int offset, any[] array, int arraySize, int dataSize=4);
stock void SetEntDataArray(int entity, int offset, const any[] array, int arraySize, int dataSize=4, bool changeState=false);

// ── Named Property Access ──
native int FindSendPropOffs(const char[] cls, const char[] prop);
native int FindSendPropInfo(const char[] cls, ...);
native int FindDataMapOffs(int entity, ...);
native int FindDataMapInfo(int entity, ...);
stock int GetEntSendPropOffs(int ent, const char[] prop, bool actual=false);
stock bool HasEntProp(int entity, PropType type, const char[] prop);

native int GetEntProp(int entity, PropType type, const char[] prop, int size=4, int element=0);
native void SetEntProp(int entity, PropType type, const char[] prop, any value, int size=4, int element=0);
native float GetEntPropFloat(int entity, PropType type, const char[] prop, int element=0);
native void SetEntPropFloat(int entity, PropType type, const char[] prop, float value, int element=0);
native int GetEntPropEnt(int entity, PropType type, const char[] prop, int element=0);
native void SetEntPropEnt(int entity, PropType type, const char[] prop, int other, int element=0);
native void GetEntPropVector(int entity, PropType type, const char[] prop, float vec[3], int element=0);
native void SetEntPropVector(int entity, PropType type, const char[] prop, const float vec[3], int element=0);
native int GetEntPropString(int entity, PropType type, const char[] prop, char[] buffer, int maxlen, int element=0);
native int SetEntPropString(int entity, PropType type, const char[] prop, const char[] buffer, int element=0);
native int GetEntPropArraySize(int entity, PropType type, const char[] prop);
native Address GetEntityAddress(int entity);
native int LoadEntityFromHandleAddress(Address addr);       // 1.12+
native void StoreEntityToHandleAddress(Address addr, int entity);  // 1.12+
```

### halflife.inc (Engine / Game Functions)
```sourcepawn
// ── Engine ──
native void LogToGame(const char[] format, any ...);
native bool IsDedicatedServer();
native float GetEngineTime();
native float GetGameTime();
native int GetGameTickCount();
native float GetGameFrameTime();
native int GetGameDescription(char[] buffer, int maxlength, bool original=false);
native int GetGameFolderName(char[] buffer, int maxlength);
native int GetCurrentMap(char[] buffer, int maxlength);
native bool IsMapValid(const char[] map);
native FindMapResult FindMap(const char[] map, char[] foundmap, int maxlen);
native bool GetMapDisplayName(const char[] map, char[] displayName, int maxlen);
native int GuessSDKVersion();
native EngineVersion GetEngineVersion();

// ── Random ──
native void SetRandomSeed(int seed);
native float GetRandomFloat(float fMin=0.0, float fMax=1.0);
native int GetRandomInt(int nmin, int nmax);

// ── Precaching ──
native int PrecacheModel(const char[] model, bool preload=false);
native int PrecacheSentenceFile(const char[] file, bool preload=false);
native int PrecacheDecal(const char[] decal, bool preload=false);
native int PrecacheGeneric(const char[] generic, bool preload=false);
native bool PrecacheSound(const char[] sound, bool preload=false);
native bool IsModelPrecached(const char[] model);
native bool IsDecalPrecached(const char[] decal);
native bool IsGenericPrecached(const char[] generic);
native bool IsSoundPrecached(const char[] sound);

// ── User Messages (Chat/Hint/Center) ──
native void PrintToChat(int client, const char[] format, any ...);
stock void PrintToChatAll(const char[] format, any ...);
native void PrintCenterText(int client, const char[] format, any ...);
// Note: PrintHintText and PrintCenterText display BROKEN on L4D2 clients (1.12 doc)
// Note: cl_showpluginmessages 1 required on some games since ~2018 (1.12 doc)

// ── Dialogs ──
native void CreateDialog(int client, Handle kv, DialogType type);

// ── EntRefToEntIndex (behavior changed in 1.12) ──
// 1.11: just dereferences ref → entity index or -1
// 1.12: also validates entity is alive → entity index or INVALID_ENT_REFERENCE
```

### sdktools_functions.inc (Entity / Player Operations)
```sourcepawn
native bool RemovePlayerItem(int client, int item);
native int GivePlayerItem(int client, const char[] item, int iSubType=0);
native int GetPlayerWeaponSlot(int client, int slot);
native void IgniteEntity(int entity, float time, bool npc=false, float size=0.0, bool level=false);
native void ExtinguishEntity(int entity);
native void TeleportEntity(int entity, const float origin[3]=NULL_VECTOR, const float angles[3]=NULL_VECTOR, const float velocity[3]=NULL_VECTOR);
native void ForcePlayerSuicide(int client, bool explode=false);  // explode param new in 1.12
native void SlapPlayer(int client, int health=5, bool sound=true);
native int FindEntityByClassname(int startEnt, const char[] classname);
native bool GetClientEyeAngles(int client, float ang[3]);
native int CreateEntityByName(const char[] classname, int ForceEdictIndex=-1);
native bool DispatchSpawn(int entity);
native bool DispatchKeyValue(int entity, const char[] keyName, const char[] value);
stock bool DispatchKeyValueInt(int entity, const char[] keyName, int value);
native bool DispatchKeyValueFloat(int entity, const char[] keyName, float value);
native bool DispatchKeyValueVector(int entity, const char[] keyName, const float vec[3]);
native int GetClientAimTarget(int client, bool only_clients=true);
native int GetTeamCount();
native void GetTeamName(int index, char[] name, int maxlength);
native int GetTeamScore(int index);
native void SetTeamScore(int index, int value);
native int GetTeamClientCount(int index);
native int GetTeamEntity(int teamIndex);
native void SetEntityModel(int entity, const char[] model);
native bool GetPlayerDecalFile(int client, char[] hex, int maxlength);
native bool GetPlayerJingleFile(int client, char[] hex, int maxlength);
native void GetServerNetStats(float &inAmount, float &outAmout);
native void EquipPlayerWeapon(int client, int weapon);
native void ActivateEntity(int entity);
native void SetClientInfo(int client, const char[] key, const char[] value);
```

### events.inc (Game Events)
```sourcepawn
typeset EventHook {
    function Action(Event event, const char[] name, bool dontBroadcast);
    function void(Event event, const char[] name, bool dontBroadcast);
};
native void HookEvent(const char[] name, EventHook callback, EventHookMode mode=EventHookMode_Post);
native bool HookEventEx(const char[] name, EventHook callback, EventHookMode mode=EventHookMode_Post);
native void UnhookEvent(const char[] name, EventHook callback, EventHookMode mode=EventHookMode_Post);
native Event CreateEvent(const char[] name, bool force=false);
native void FireEvent(Handle event, bool dontBroadcast=false);
native void CancelCreatedEvent(Handle event);
native bool GetEventBool(Handle event, const char[] key, bool defValue=false);
native void SetEventBool(Handle event, const char[] key, bool value);
native int GetEventInt(Handle event, const char[] key, int defValue=0);
native void SetEventInt(Handle event, const char[] key, int value);
native float GetEventFloat(Handle event, const char[] key, float defValue=0.0);
native void SetEventFloat(Handle event, const char[] key, float value);
native void GetEventString(Handle event, const char[] key, char[] value, int maxlength, const char[] defvalue="");
native void SetEventString(Handle event, const char[] key, const char[] value);
native void GetEventName(Handle event, char[] name, int maxlength);
native void SetEventBroadcast(Handle event, bool dontBroadcast);
```

### console.inc (Server/Client Commands)
```sourcepawn
native void ServerCommand(const char[] format, any ...);
native void ServerCommandEx(char[] buffer, int maxlen, const char[] format, any ...);
native void InsertServerCommand(const char[] format, any ...);
native void ServerExecute();
native void ClientCommand(int client, const char[] fmt, any ...);
native void FakeClientCommand(int client, const char[] fmt, any ...);
native void FakeClientCommandEx(int client, const char[] fmt, any ...);
native void FakeClientCommandKeyValues(int client, KeyValues kv);
native void PrintToServer(const char[] format, any ...);
native void PrintToConsole(int client, const char[] format, any ...);
native void ReplyToCommand(int client, const char[] format, any ...);
native ReplySource GetCmdReplySource();
native ReplySource SetCmdReplySource(ReplySource source);
native bool IsChatTrigger();
native int GetPublicChatTriggers(char[] buffer, int maxlength);   // 1.12+
native int GetSilentChatTriggers(char[] buffer, int maxlength);   // 1.12+
native void ShowActivity2(int client, const char[] tag, const char[] format, any ...);
native void ShowActivity(int client, const char[] format, any ...);
native void ShowActivityEx(int client, const char[] tag, const char[] format, any ...);
native bool FormatActivitySource(int client, int target, const char[] namebuf, int maxlength);
```

### datapack.inc (DataPack)
```sourcepawn
native Handle CreateDataPack();
native void WritePackCell(Handle pack, int cell);
native void WritePackFloat(Handle pack, float val);
native void WritePackString(Handle pack, const char[] str);
native int ReadPackCell(Handle pack);
native float ReadPackFloat(Handle pack);
native void ReadPackString(Handle pack, char[] buffer, int maxlen);
native void ResetPack(Handle pack, bool clear=false);
native int GetPackPosition(Handle pack);
native void SetPackPosition(Handle pack, int position);
native bool IsPackReadable(Handle pack, int bytes);
```

### timers.inc (Timers)
```sourcepawn
native Handle CreateTimer(float interval, Timer callback, any data=INVALID_HANDLE, int flags=0);
native void KillTimer(Handle timer, bool autoRefire=false);
native void TriggerTimer(Handle timer, bool reset=false);
native float GetTickedTime();
native int GetProfileNum(int serial, char[] name, int maxlen);
```

### files.inc (File I/O)
```sourcepawn
native bool FileExists(const char[] path, bool use_valve_fs=false, const char[] valve_path_id="DEFAULT_READ_PATH");
native bool DirExists(const char[] path, bool use_valve_fs=false, const char[] valve_path_id="DEFAULT_READ_PATH");
native bool CreateDirectory(const char[] path, int mode=..., bool use_valve_fs=false, ...);  // mode default in 1.12
native bool GetFilePermissions(const char[] path, int &mode);  // 1.12+
native bool RenameFile(const char[] newpath, const char[] oldpath, ...);
native bool DeleteFile(const char[] path, ...);
native Handle OpenFile(const char[] file, const char[] mode, ...);
native Handle OpenDirectory(const char[] path, ...);
```

### convars.inc (Console Variables)
```sourcepawn
native ConVar CreateConVar(const char[] name, const char[] defaultValue, const char[] description="", int flags=0, bool hasMin=false, float min=0.0, bool hasMax=false, float max=0.0);
native ConVar FindConVar(const char[] name);
native void HookConVarChange(ConVar convar, ConVarChanged callback);
native void UnhookConVarChange(ConVar convar, ConVarChanged callback);
// ConVar methodmap: .BoolValue, .IntValue, .FloatValue, .SetString(), .GetString(), .SetInt(), .SetFloat(), .SetBool(), .RestoreDefault(), .GetDefault(), .AddChangeHook(), .RemoveChangeHook()
```

### sdktools_sound.inc (Sound) — 1.12 bitmask change
```sourcepawn
// 1.11: SND_CHANGEVOL=1, SND_CHANGEPITCH=2, SND_STOP=3 (sequential)
// 1.12: SND_CHANGEVOL=(1<<0), SND_CHANGEPITCH=(1<<1), SND_STOP=(1<<2) (bitmask)
// New in 1.12: SND_IGNORE_PHONEMES=(1<<8), SND_IGNORE_NAME=(1<<9),
//              SND_DO_NOT_OVERWRITE_EXISTING_ON_CHANNEL=(1<<10)
native void EmitSound(const char[] sample, int entity, int channel=SNDCHAN_AUTO, float level=SNDLEVEL_NORMAL, int flags=SND_NOFLAGS, float volume=SNDVOL_NORMAL, int pitch=SNDPITCH_NORMAL, ...);
native void EmitSoundToClient(int client, const char[] sample, int entity=SND_SELF, int channel=SNDCHAN_AUTO, float level=SNDLEVEL_NORMAL, int flags=SND_NOFLAGS, float volume=SNDVOL_NORMAL, int pitch=SNDPITCH_NORMAL, ...);
native void EmitSoundToAll(const char[] sample, int entity=SND_SELF, int channel=SNDCHAN_AUTO, float level=SNDLEVEL_NORMAL, int flags=SND_NOFLAGS, float volume=SNDVOL_NORMAL, int pitch=SNDPITCH_NORMAL, ...);
```

---

## L4D2 Datamap Reference

Source: `Left 4 Dead 2 datamap dump.txt` (15378 lines)

### CBaseEntity (base class)
```
m_iClassname             (Offset 116)   Save|Key   - classname
m_iGlobalname            (Offset 120)   Global|Save|Key - globalname
m_iParent                (Offset 124)   Save|Key   - parentname
m_iHammerID              (Offset 128)   Save|Key   - hammerid
m_flSpeed                (Offset 264)   Save|Key   - speed
m_nRenderFX              (Offset 268)   Save|Key   - renderfx
m_clrRender              (Offset 272)   Save|Key   - rendercolor
m_nModelIndex            (Offset 270)   Global|Save|Key - modelindex
m_iszVScripts            (Offset 972)   Save|Key   - vscripts
m_iszScriptThinkFunction (Offset 976)   Save|Key   - thinkfunction
m_nNextThinkTick         (Offset 200)   Save|Key   - nextthink
m_fEffects               (Offset 204)   Save|Key   - effects
m_lifeState              (Offset 240)   Save       - {LIFE_ALIVE=0,LIFE_DYING=1,LIFE_DEAD=2}
m_takedamage             (Offset 241)   Save       - damage flag
m_iMaxHealth             (Offset 232)   Save|Key   - max_health
m_iHealth                (Offset 236)   Save|Key   - health
m_target                 (Offset 228)   Save|Key   - target
m_iszDamageFilterName    (Offset 244)   Save|Key   - damagefilter
m_iEFlags                (Offset 312)   Save       - entity flags
m_MoveType               (Offset 370)   Save       - movetype
m_MoveCollide            (Offset 371)   Save       - movecollide
m_hOwnerEntity           (Offset 524)   Save       - owner
m_CollisionGroup         (Offset 544)   Save       - collision group
m_iInitialTeamNum        (Offset 564)   Save|Key|Input - TeamNum
m_iTeamNum               (Offset 568)   Save       - team number
m_bIsInStasis            (Offset 8)     Save       - stasis flag
m_hGroundEntity          (Offset 580)   Save       - ground entity
m_ModelName              (Offset 588)   Global|Save|Key - model
m_vecBaseVelocity        (Offset 596)   Save|Key   - basevelocity
m_vecAbsVelocity         (Offset 608)   Save       - absolute velocity
m_vecAngVelocity         (Offset 620)   Save|Key   - avelocity
m_nWaterLevel            (Offset 575)   Save|Key   - waterlevel
m_flGravity              (Offset 684)   Save|Key   - gravity
m_flFriction             (Offset 688)   Save|Key   - friction
m_vecAbsOrigin           (Offset 716)   Save       - absolute origin
m_vecVelocity            (Offset 728)   Save|Key   - velocity
m_spawnflags             (Offset 308)   Save|Key   - spawnflags
m_fFlags                 (Offset 316)   Save       - FL_* flags
m_fadeMinDist            (Offset 532)   Save|Key|Input - fademindist
m_fadeMaxDist            (Offset 536)   Save|Key|Input - fademaxdist
m_flFadeScale            (Offset 540)   Save|Key   - fadescale
m_flNavIgnoreUntilTime   (Offset 576)   Save       - nav ignore time
```
```
Inputs: SetTeam, Kill, KillHierarchy
```

### CTerrorPlayer Datamap (L4D2-specific)
The CTerrorPlayer datamap inherits all CBaseEntity + CBaseCombatCharacter properties plus:
```
m_zombieClass      (Offset 11192)  integer  8 bits
m_isGhost          (Offset 11449)  integer  1 bit  Unsigned
m_isIncapacitated  (Offset 11688)  integer  1 bit  Unsigned
m_isCalm           (Offset 11916)  integer  1 bit  Unsigned
m_isHangingFromLedge (Offset 14853) integer 1 bit Unsigned
m_isGoingToDie     (Offset 13072)  integer  1 bit  Unsigned
m_isOnThirdStrike  (related)
m_isGettingUp      (related)
m_hasVisibleThreats (Offset 12636)  integer 1 bit Unsigned
m_healthBuffer      (Offset 13060)  float   10 bits
m_healthBufferTime  (Offset 13064)  float   0 bits NoScale
m_frustration       (Offset 14988)  integer  8 bits
m_survivorCharacter (Offset 11188)  integer  8 bits
m_checkpointZombieKills  (Offset 14540) integer 16 bits InsideArray
m_missionZombieKills     (Offset 14576) integer 16 bits InsideArray
m_checkpointSurvivorDamage (Offset 12436) integer 16 bits
m_missionSurvivorDamage    (Offset 12440) integer 16 bits
m_checkpointDamageToTank   (Offset 14700) integer 32 bits
m_checkpointDamageToWitch  (Offset 14704) integer 32 bits
m_checkpointPZTankDamage   (Offset 14756) integer 32 bits
m_checkpointPZTankPunches  (Offset 14796) integer 32 bits
m_checkpointPZTankThrows   (Offset 14800) integer 32 bits
```

### Full Dump Structure
The full datamap dump is organized by class hierarchy:
```
CBaseEntity → CBaseAnimating → CBaseCombatCharacter → CTerrorPlayer
                                                      → Infected
                                                      → Tank
                                                      → Witch
```
Search with:
```bash
findstr /i "<propname>" "references/game-data/datamap-dump.txt"
```
