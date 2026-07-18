---
name: portals-building-guide
description: Complete guide for building interactive 3D spaces in Portals. Use when creating spaces, configuring triggers/effects, writing function expressions, setting up NPCs, quests, token trading, iframes, or any Portals development task. Covers Interactive Studio, Function Effects, building tools, and all game mechanics.
---

# Portals Building Guide - Complete Reference

## Overview

Portals is a platform for creating interactive 3D virtual spaces. This guide covers all building tools, the Interactive Studio (no-code gamification), and advanced scripting with Function Effects.

---

# BUILDING BASICS

## Creating a Space

1. Sign in to Portals
2. Click profile icon → My Spaces
3. Click "Create New"
4. Choose a template
5. Name your space
6. Click "Create New Space"
7. You'll automatically load into your space

## Build Mode

1. Click the **wrench icon** to enter build mode
2. Select an item from inventory
3. Click in your space to place the item

---

# BUILDING TOOLS (20 Total)

| Tool | Description |
|------|-------------|
| **AI Item Generator** | Automated 3D object creation |
| **Image** | Place 2D images in 3D space |
| **Video** | Embed video players |
| **Build Block** | Basic structural elements |
| **Screenshare** | Display sharing |
| **Portal** | Teleportation between spaces/locations |
| **Custom GLB** | Import custom 3D models |
| **Light Source** | Static lighting |
| **Blink Light** | Animated/flashing lights |
| **Spotlight** | Directional lighting |
| **Spawn Point** | Player entry locations |
| **NPC** | Non-player characters with dialogue/AI |
| **Billboard** | Text/image display surfaces |
| **Jump Pad** | Launch players into air |
| **Trigger Cube** | Invisible interaction zones |
| **Collectible GLB** | Gatherable 3D objects |
| **Leaderboard** | Score tracking display |
| **Elemental** | Environmental effects |
| **Chart** | Live data visualization (crypto) |
| **World Text** | 3D text in space |

## Portal Tool

Creates teleportation between spaces or spawn points.

**Configuration:**
- **Destination**: Full space URL
- **Spawn Name**: Target spawn point (case-sensitive, leave blank for default)
- **Auto Teleport**: On = instant, Off = press X to activate
- **Custom Message**: Action prompt text (e.g., "teleport" shows "Press X to teleport")

## Trigger Cube

Invisible zone that activates events when players enter.

**Settings:**
- **Press X to Activate**: Toggle between auto-trigger or manual activation
- **Events**: Add actions (open doors, play sounds, teleport, etc.)
- **Custom Title**: Label for organization

**Important:** Trigger cubes only activate when a player **enters** the cube (crosses the boundary from outside). If a player spawns or loads into the game already inside a trigger cube, the trigger will NOT fire.

**Organization Tip:** Place related triggers on Build Blocks (which have a color selector), give them distinct colors, and add On Hover Text Display labels to organize your game logic.

## NPC (Non-Player Character)

Interactive characters with dialogue trees and AI.

**Setup:**
- Paste GLB avatar URL or choose preset
- Configure: Name, Auto Popup, Default Animation, AI Settings

**NPC-Specific Effects:**
- Turn To Player
- Walk to Position
- Record NPC Path
- Change Animation
- Change Avatar Mood
- Show/Hide NPC

**Requirement:** Must use rigged GLB avatars for animations.

---

# INTERACTIVE STUDIO

The no-code system for gamifying spaces. Three core components:

## Tasks

Tasks are progress trackers with **three states**:
- **NotActive** (default starting state)
- **Active**
- **Completed**

Tasks can transition between states in any order via triggers.

**Task Types:**
- Single Player Tasks
- Multiplayer Tasks
- Dependent Tasks (chains)
- Non-Persistent Tasks (reset on reload)
- Quests (visible in quest log)

## Task Debug Panel

Access via **Space Options > Task Debug Panel**

**Important:** Task system must be turned on BEFORE opening debug panel.

**State Indicators:**
- Red circle = NotActive
- Yellow circle = Active
- Green circle = Completed

**Features:**
- Change state of any task (single or multiplayer)
- View complete history log of all state changes
- Essential for testing effects and triggers

## Node View

Visual graph interface for analyzing game logic.

**Access:** Space Options > Tasks > Click 'Graph' button

**Node Colors:**
- Grey = Objects
- Green = Triggers
- Purple = Tasks
- Yellow = Effects

**Features:**
- View task dependencies (arrows show relationships)
- Create Tasks, Triggers, Effects directly in the graph
- Click any node to edit its configuration
- See which triggers fire which tasks

## Triggers (17 Types) - Detailed Guide

Triggers are events that cause tasks to change state. Understanding when each trigger fires is critical for building reliable game logic.

### Backpack Item Activated
**What it does:** Fires when a player uses an item from their backpack/inventory.

**Use cases:**
- Consumable items (health potions, power-ups)
- Tools that players can activate on demand
- Special abilities tied to inventory items

**Example:** Player clicks "Health Potion" in backpack → trigger fires → effect heals player

---

### Click
**What it does:** Fires when a player clicks on the object this trigger is attached to.

**Use cases:**
- Interactive buttons and switches
- Doors that open when clicked
- NPCs that respond to clicks
- Any "press to interact" mechanic

**Important:** The click must be on the specific object. For area-based interactions, use User Enter Trigger instead.

**Example:** Player clicks a lever → trigger fires → door opens

---

### Collision
**What it does:** Fires when the player's physics collider touches a trigger volume. This is for physics-based interactions.

**Use cases:**
- Detecting when player hits an obstacle
- Projectile impacts
- Physics puzzle elements

**Important:** For simply detecting when a player walks into an area, use "User Enter Trigger" instead. Collision is for physics interactions.

---

### Item Collected
**What it does:** Fires when a player picks up a Collectible GLB object.

**Use cases:**
- Coin/gem collection games
- Scavenger hunts
- Key items for puzzles
- Tracking collection progress

**Common pattern:** Item Collected → Update Value (+1) → check if all items collected

---

### Key Pressed
**What it does:** Fires when player presses a specific keyboard key.

**Configuration:** Select which key to listen for (E, F, numbers, etc.)

**Use cases:**
- Custom interaction keys beyond the default X
- Ability hotkeys (press 1 for sword, 2 for shield)
- Debug/admin commands
- Quick actions without clicking

**Important:** Only works when the Portals window has focus. If player clicks outside, key triggers won't fire.

---

### Key Released
**What it does:** Fires when player releases a keyboard key they were holding.

**Use cases:**
- Charged abilities (hold to charge, release to fire)
- Sprint mechanics (hold to run, release to walk)
- Any hold-and-release interaction

---

### Player Died
**What it does:** Fires when the player's health reaches zero.

**Use cases:**
- Respawn systems
- Death counters
- Game over screens
- Score penalties on death
- Team deathmatch kill tracking

**Critical for games:** This is how you detect kills. When Player A kills Player B, Player B's "Player Died" trigger fires. The killer is determined by which team the dead player was on (enemy team gets the point).

**Example pattern:**
```
Player Died →
  Check which team player was on →
  Award point to opposite team →
  Respawn player after delay
```

---

### Player Login
**What it does:** Fires once when a player enters/loads into the space.

**Use cases:**
- Initialize player variables (set team to 0, health to 100)
- Show welcome messages or tutorials
- Spawn HUD iframes
- Assign player to default state
- Start background music

**Critical:** This is your "on game start" trigger for each player. Use it to set up everything the player needs.

**Common pattern:**
```
Player Login →
  Set Player_Team = 0
  Set Player_Health = 100
  Show HUD iframe
```

---

### Player Started Moving
**What it does:** Fires when a stationary player begins moving (WASD or joystick).

**Use cases:**
- Tutorial prompts ("Great, you're moving!")
- Stealth games (movement breaks stealth)
- Idle detection systems
- Triggering ambient sounds when player moves

---

### Player Stopped Moving
**What it does:** Fires when a moving player comes to a stop.

**Use cases:**
- Idle animations or effects
- "Stand still to interact" mechanics
- AFK detection
- Meditation/rest mechanics

---

### Swap Volume
**What it does:** Fires when audio volume or track changes.

**Use cases:**
- Sync visual effects to music
- Trigger events on song changes
- Audio-reactive environments

---

### Timer Stopped
**What it does:** Fires when a countdown timer reaches zero.

**Use cases:**
- Race finish detection
- Time-limited challenges
- Round timers
- Bomb defusal countdown

**Note:** This is for the built-in Portals timer, not custom iframe timers.

**Timer Limitation:** Portals does not currently have a native shared timer system that can be synchronized across players and pulled into an iframe. For multiplayer timer displays, use local JavaScript timing in iframes triggered by game state changes. Timer values shown will be approximate and client-side.

---

### User Enter Trigger
**What it does:** Fires when a player walks into a Trigger Cube's volume.

**This is one of the most important triggers.** Use it for:
- Zone detection (player entered red base, blue base, danger zone)
- Automatic doors
- Checkpoint systems
- Team selection areas
- Teleport zones
- Any "walk here to do something" mechanic

**Configuration:**
- Attach to a Trigger Cube object
- Size the cube to cover the detection area
- Optional: "Press X to Activate" for manual activation instead of auto

**Important:** Trigger cubes only activate when a player **enters** the cube (crosses the boundary from outside). If a player spawns or loads into the game already inside a trigger cube, the trigger will NOT fire. Plan spawn point placement accordingly, or use Player Login trigger for logic that must run when players join.

**Example:** Player walks into red team zone → User Enter Trigger fires → Set Player_Team = 1

---

### User Exit Trigger
**What it does:** Fires when a player leaves a Trigger Cube's volume.

**Use cases:**
- Close doors after player leaves
- Remove buffs when leaving an area
- Stop area-specific music
- Hide contextual UI
- Boundary warnings ("You're leaving the play area!")

**Common pattern:** Enter shows something, Exit hides it
```
User Enter → Show Token Swap UI
User Exit → Hide Token Swap UI
```

---

### Value Updated
**What it does:** Fires whenever a specific variable changes value.

**Configuration:** Select which variable to watch

**Use cases:**
- React to score changes (update HUD when Red_Score changes)
- Threshold detection (when health drops below 20, show warning)
- Sync iframes with game state
- Chain reactions (when X changes, update Y)

**Critical for iframes:** Use this to automatically send updated values to iframes whenever variables change.

**Example pattern:**
```
Value Updated (Red_Score) →
  Send Message To Iframes: red_|Red_Score|
```

---

### Wearable Off
**What it does:** Fires when player unequips/removes a wearable item.

**Use cases:**
- Remove buffs when armor is removed
- Track equipment state
- Costume change effects

---

### Wearable On
**What it does:** Fires when player equips a wearable item.

**Use cases:**
- Apply buffs when equipping items
- Unlock abilities with equipment
- Costume-specific permissions
- Achievement tracking

## Effects (60+ Types) - Detailed Guide

Effects are actions that happen when a task changes state. They're the "do this" part of your game logic.

---

### MOVEMENT & CAMERA EFFECTS

#### Teleport
**What it does:** Instantly moves the player to a named spawn point.

**Configuration:** Enter the exact spawn point name (case-sensitive)

**Use cases:**
- Respawn systems (teleport to RedSpawn1 after death)
- Fast travel between areas
- Team base assignment
- Returning players to lobby after game ends
- Checkpoint systems

**Critical:** Spawn point names are CASE-SENSITIVE. "RedSpawn1" is different from "redspawn1".

**Example:** After player joins red team → Teleport to "RedSpawn1"

---

#### Apply Velocity To Player
**What it does:** Pushes the player in a direction with force.

**Use cases:**
- Jump pads (launch player upward)
- Knockback effects
- Wind zones
- Boost pads

---

#### Change Camera Filter/State/Zoom
**What it does:** Modifies how the player's camera behaves or looks.

**Use cases:**
- Cinematic moments (zoom in on important object)
- Drunk/dizzy effects (apply filter)
- Scope/aim mode (zoom in)
- Dramatic reveals

---

#### Lock/Unlock Camera
**What it does:** Prevents or allows player from rotating their camera view.

**Use cases:**
- Cutscenes (force player to look at something)
- Dialogue sequences
- Tutorial moments

---

#### Lock/Unlock Movement
**What it does:** Prevents or allows player from moving (WASD/joystick).

**Use cases:**
- Cutscenes
- Dialogue with NPCs
- Puzzle moments where player must stay still
- Pre-game countdown ("Game starts in 3... 2... 1...")

**Warning:** Always make sure to unlock movement eventually, or player gets stuck!

---

#### Toggle Free Camera
**What it does:** Switches between normal third-person and free-flying camera.

**Use cases:**
- Spectator mode
- Photo mode
- Building/editing mode

---

### VISUAL & ENVIRONMENT EFFECTS

#### Hide/Show Object
**What it does:** Makes an object invisible or visible.

**Configuration:** Select which object to hide/show

**Use cases:**
- Doors that disappear when opened
- Hidden passages revealed
- Removing obstacles after puzzle solved
- Showing/hiding visual indicators

**Example:** Player collects all keys → Show Object (exit door)

---

#### Change Fog
**What it does:** Adjusts the fog density/color in the scene.

**Use cases:**
- Spooky atmosphere
- Weather changes
- Zone-specific ambiance
- Revealing hidden areas (clear the fog)

---

#### Change Time of Day
**What it does:** Changes lighting to simulate different times.

**Use cases:**
- Day/night cycles
- Dramatic mood shifts
- Puzzle mechanics (things only visible at night)

---

#### Change Bloom
**What it does:** Adjusts the glow/bloom post-processing effect.

**Use cases:**
- Dreamy/magical areas
- Power-up visual feedback
- Environmental storytelling

---

### PLAYER EFFECTS

#### Change Player Health
**What it does:** Sets or modifies the player's health value.

**Configuration:**
- **Set:** Sets health to exact value (e.g., Set to 100)
- **Add:** Adds to current health (e.g., Add 25 for healing)
- **Subtract:** Removes health (e.g., Subtract 10 for damage)

**Use cases:**
- Healing items/zones
- Damage zones (lava, spikes)
- Respawn (Set to 100 after death)
- Poison/DOT effects

**Critical for combat games:** Use "Set → 100" after respawning to fully heal the player.

**Example pattern:**
```
RespawnRed task (on Active):
  1. Teleport → RedSpawn1
  2. Change Player Health → Set → 100
  3. Reset task
```

---

#### Change Avatar
**What it does:** Changes the player's 3D avatar/character model.

**Use cases:**
- Team uniforms (red team gets red armor)
- Power-ups that transform player
- Costume unlocks

---

#### Lock/Unlock Avatar Change
**What it does:** Prevents or allows player from changing their avatar.

**Use cases:**
- Enforce team uniforms during gameplay
- Lock cosmetics during competitive matches

---

#### Change Movement Profile
**What it does:** Modifies player movement speed, jump height, etc.

**Use cases:**
- Speed boost power-ups
- Slow zones (mud, water)
- Character classes with different mobility

---

#### Play Emote
**What it does:** Makes the player's avatar perform an animation.

**Use cases:**
- Celebration after winning
- Dance floors
- Social interactions

---

### AUDIO EFFECTS

#### Play Sound Once
**What it does:** Plays an audio file one time.

**Use cases:**
- Door opening sounds
- Pickup sounds
- Victory/defeat fanfares
- Button click feedback
- Death sounds

---

#### Play Sound In Loop
**What it does:** Continuously plays audio until stopped.

**Use cases:**
- Background music
- Ambient sounds (rain, wind)
- Alarm sounds

---

#### Toggle Mute
**What it does:** Mutes or unmutes audio.

**Use cases:**
- Audio settings
- Cutscene audio control

---

### UI & DISPLAY EFFECTS

#### Notification Pill
**What it does:** Shows a brief popup message to the player.

**Configuration:** Enter the message text

**Use cases:**
- "Joined Red Team!"
- "RED TEAM WINS!"
- "+10 Points"
- Tutorial hints
- Achievement unlocked messages

**Best practice:** Keep messages short and clear. Players only see them briefly.

---

#### Display Value
**What it does:** Shows a variable's value on screen.

**Configuration:** Select which variable to display

**Use cases:**
- Score displays
- Health bars
- Coin counters
- Timer displays

**Note:** For more control over display, use iframes instead.

---

#### Hide Value
**What it does:** Removes a displayed variable from screen.

---

#### Iframe
**What it does:** Opens an external webpage inside the Portals window.

**This is extremely powerful.** Iframes let you:
- Create custom HUDs with HTML/CSS/JavaScript
- Build complex UI that Portals can't do natively
- Display external content (leaderboards, guides)
- Create interactive menus

**See the IFRAMES section for complete documentation.**

---

#### Close Iframe
**What it does:** Closes an open iframe.

**Use cases:**
- Dismiss popups
- Clean up HUDs on game end

---

#### Send Message To Iframes
**What it does:** Sends data from Portals to all open iframes.

**Configuration:** Enter the message string. Use `|variableName|` to include variable values.

**Built-in variables:**
- `|username|` - player's Portals ID or name as a quoted string
- `|position|` - all players' positions as an array keyed by username, e.g. `{"buster"="(-32.49, 22.21, -99.82)"}`

**CRITICAL:** Do NOT use JSON with colons. Colons break the parser. Use underscore format instead.

**Correct:** `score_|Red_Score|` → sends "score_25"
**Wrong:** `{"score": |Red_Score|}` → BREAKS

**Use cases:**
- Update HUD with current scores
- Send timer values
- Sync game state to iframe displays

---

### GAME LOGIC EFFECTS

#### Update Value
**What it does:** Creates or modifies a variable.

**Configuration:**
- Variable name
- Operation (Set, Add, Subtract, Multiply, Divide)
- Value

**Use cases:**
- Score tracking (Add 1 to Red_Score)
- Health management
- Progress counters
- Any numeric game state

**Note:** For complex logic, use Function Effect instead.

---

#### Function Effect
**What it does:** Executes NCalc expressions for advanced logic.

**This is the most powerful effect.** It lets you:
- Read task states and variables
- Conditional logic (if/else)
- Set multiple values
- Complex calculations
- Delayed actions

**See the FUNCTION EFFECT section for complete documentation.**

---

#### Post Score to Leaderboard
**What it does:** Submits a player's score to a leaderboard.

**Configuration:** Value Label must match the leaderboard's score label exactly.

**Use cases:**
- High score submission
- Race time recording
- Competition rankings

---

#### Reset All Tasks
**What it does:** Sets all tasks back to NotActive.

**Use cases:**
- Full game reset
- New round starting
- Debug/testing

**Warning:** This resets EVERYTHING. Use carefully.

---

#### Run Trigger From Effector
**What it does:** Manually fires another trigger.

**Use cases:**
- Chain reactions
- Reusing trigger logic from multiple places

---

### OBJECT EFFECTS

#### Move Item
**What it does:** Moves an object to a new position.

**Use cases:**
- Sliding doors
- Moving platforms
- Puzzle pieces

---

#### Duplicate Item
**What it does:** Creates a copy of an object.

**Use cases:**
- Spawning collectibles
- Particle effects
- Dynamic content generation

---

#### Portals Animation
**What it does:** Plays a built-in Portals animation on an object.

---

### NPC EFFECTS

These effects only work on NPC objects, not regular 3D models.

#### Turn To Player
**What it does:** Rotates the NPC to face the player.

**Use cases:**
- NPCs that acknowledge player presence
- Shopkeepers looking at customers
- Guards tracking player movement

---

#### Walk to Position
**What it does:** Makes NPC walk to a specified location.

**Use cases:**
- NPC patrols
- Characters moving during cutscenes
- Quest givers walking to quest locations

---

#### Change Animation
**What it does:** Changes which animation the NPC is playing.

**Configuration:** Animation name (must match GLB file exactly, case-sensitive)

**Use cases:**
- NPC reactions (wave, point, scared)
- State changes (idle → talking)
- Combat animations

---

#### Show/Hide NPC
**What it does:** Makes NPC visible or invisible.

**Use cases:**
- NPCs appearing for quests
- Characters leaving after conversation
- Dramatic reveals

---

#### Message to NPC
**What it does:** Sends a command to an NPC's AI system.

**Use cases:**
- AI conversation prompts
- Behavior changes

---

# GAME BUILDING METHODOLOGY

## How to Approach Building Any Game

Before writing a single task or effect, spend 10-15 minutes planning. This prevents 90% of debugging headaches.

### Step 1: Define Your Core Loop

Every game has a core loop. Write it in plain English first:

**Example - Team Deathmatch:**
```
1. Player joins a team (Red or Blue)
2. Player spawns at team base
3. Player kills enemy players
4. Team scores points for kills
5. First to 50 points OR time runs out → winner declared
6. Everyone returns to lobby
```

**Example - Collectible Hunt:**
```
1. Player enters the game area
2. Player finds and collects hidden items
3. Each item adds to their score
4. When all items collected → show victory
```

### Step 2: Identify Your Variables

List every piece of data your game needs to track:

| Variable | Multiplayer? | Persistent? | Purpose |
|----------|--------------|-------------|---------|
| `Player_Team` | No | No | Which team this player is on (0=none, 1=red, 2=blue) |
| `Red_Score` | Yes | No | Red team's total points |
| `Blue_Score` | Yes | No | Blue team's total points |
| `Elapsed_Seconds` | Yes | No | Game timer |

**Key questions:**
- Does everyone need to see the same value? → Multiplayer = Yes
- Should it survive page refresh? → Persistent = Yes
- Is it per-player or global? → Per-player = Multiplayer No

### Step 3: Identify Your Tasks

Tasks are your game's state machine. List the major "events" or "states":

| Task | Type | What triggers it? | What does it do? |
|------|------|-------------------|------------------|
| `JoinRed` | Single Player | Player enters red zone | Set team=1, teleport to red spawn |
| `JoinBlue` | Single Player | Player enters blue zone | Set team=2, teleport to blue spawn |
| `KillHandler` | Single Player | Player dies | Award point to enemy team, respawn |
| `RedWins` | Multiplayer | Red reaches 50 OR time runs out | Show victory, reset game |
| `BlueWins` | Multiplayer | Blue reaches 50 OR time runs out | Show victory, reset game |

**Key insight:** Single Player tasks = actions that affect only one player. Multiplayer tasks = state changes everyone sees.

### Step 4: Build in Order

Always build in this order:

1. **Variables first** - Create all variables in Variable Manager
2. **Spawn points** - Place all teleport destinations
3. **Core triggers** - The main "what starts things" (Player Login, User Enter Trigger)
4. **Core tasks** - One at a time, test each before moving on
5. **Win conditions** - What ends the game
6. **Polish** - HUDs, sounds, effects

### Step 5: Test Each Piece Individually

**DO NOT** build everything then test. Build ONE task, test it works, then move to the next.

**Testing checklist for each task:**
1. Open Task Debug Panel
2. Manually set the task to each state
3. Verify effects fire correctly
4. Verify task resets properly
5. Check Variable Manager for correct values

---

## Complete Game Example: Team Deathmatch

Here's the complete implementation of a TDM game, step by step.

### Phase 1: Setup Variables

Create these in Variable Manager:

| Variable | Multiplayer | Persistent | Initial |
|----------|-------------|------------|---------|
| `Player_Team` | No | No | 0 |
| `Red_Score` | Yes | No | 0 |
| `Blue_Score` | Yes | No | 0 |

### Phase 2: Create Spawn Points

Place and name these spawn points:
- `LobbySpawn` - Where players start
- `RedSpawn1`, `RedSpawn2`, `RedSpawn3` - Red team spawns
- `BlueSpawn1`, `BlueSpawn2`, `BlueSpawn3` - Blue team spawns

### Phase 3: Team Selection

**Task: JoinRed**
- Type: Single Player
- Trigger: User Enter Trigger (red zone cube)

Effects (on Active):
```
1. Function Effect - Set team (only if not already on a team):
   if($N{Player_Team} == 0.0,
      SetVariable('Player_Team', 1.0, 0.0),
      0.0
   )

2. Teleport → RedSpawn1

3. Notification Pill → "Joined Red Team"

4. Function Effect - Reset task:
   SetTask('JoinRed', 'NotActive', 0.1)
```

**Task: JoinBlue** - Same pattern with Player_Team = 2.0 and BlueSpawn1

**Test:** Walk into red zone. Check:
- Variable Manager shows Player_Team = 1
- You teleported to RedSpawn1
- Notification appeared
- Task reset to NotActive

### Phase 4: Kill Handler

**Task: KillHandler**
- Type: Single Player
- Trigger: Player Died

Effects (on Active):
```
1. Function Effect - Award point to enemy team:
   if($N{Player_Team} == 1.0,
      SetVariable('Blue_Score', $N{Blue_Score} + 1.0, 0.0),
      if($N{Player_Team} == 2.0,
         SetVariable('Red_Score', $N{Red_Score} + 1.0, 0.0),
         0.0
      )
   )

2. Function Effect - Respawn after 3 seconds:
   if($N{Player_Team} == 1.0,
      SetTask('RespawnRed', 'Active', 3.0),
      if($N{Player_Team} == 2.0,
         SetTask('RespawnBlue', 'Active', 3.0),
         0.0
      )
   )

3. Function Effect - Check for winner:
   SetTask('CheckWinner', 'Active', 0.1)

4. Function Effect - Reset:
   SetTask('KillHandler', 'NotActive', 0.1)
```

**Task: RespawnRed**
- Type: Single Player
- Trigger: None (activated by KillHandler)

Effects (on Active):
```
1. Teleport → RedSpawn1
2. Change Player Health → Set → 100
3. Function Effect - Reset:
   SetTask('RespawnRed', 'NotActive', 0.1)
```

### Phase 5: Win Condition

**Task: CheckWinner**
- Type: Multiplayer
- Trigger: None (activated by KillHandler)

Effects (on Active):
```
1. Function Effect - Check scores:
   if($N{Red_Score} >= 50.0,
      SetTask('RedWins', 'Active', 0.0),
      if($N{Blue_Score} >= 50.0,
         SetTask('BlueWins', 'Active', 0.0),
         0.0
      )
   )

2. Function Effect - Reset:
   SetTask('CheckWinner', 'NotActive', 0.1)
```

**Task: RedWins**
- Type: Multiplayer
- Trigger: None

Effects (on Active):
```
1. Notification Pill → "RED TEAM WINS!"

2. Function Effect - Reset scores (2 sec delay):
   SetVariable('Red_Score', 0.0, 2.0)
   SetVariable('Blue_Score', 0.0, 2.0)

3. Function Effect - Reset player teams:
   SetVariable('Player_Team', 0.0, 2.0)

4. Function Effect - Return to lobby:
   SetTask('ReturnToLobby', 'Active', 2.0)

5. Function Effect - Reset self:
   SetTask('RedWins', 'NotActive', 3.0)
```

---

## Complete Game Example: Collectible Hunt

### Variables
| Variable | Multiplayer | Purpose |
|----------|-------------|---------|
| `Items_Collected` | No | How many items this player found |
| `Total_Items` | No | Total items to find (set on login) |

### Task: InitGame
- Trigger: Player Login

Effects:
```
1. SetVariable('Items_Collected', 0.0, 0.0)
2. SetVariable('Total_Items', 10.0, 0.0)
3. Notification Pill → "Find all 10 items!"
```

### Task: ItemCollected
- Trigger: Item Collected (on each collectible)

Effects:
```
1. Function Effect:
   SetVariable('Items_Collected', $N{Items_Collected} + 1.0, 0.0)

2. Notification Pill → "+1 Item Found!"

3. Function Effect - Check if all found:
   if($N{Items_Collected} >= $N{Total_Items},
      SetTask('Victory', 'Active', 0.0),
      0.0
   )
```

---

# DEBUGGING GUIDE

## Systematic Debugging Approach

When something doesn't work, follow this exact process:

### Step 1: Identify the Symptom

Be precise about what's wrong:
- ❌ "It doesn't work"
- ✅ "The door doesn't open when I click it"
- ✅ "The score updates but the HUD doesn't show it"
- ✅ "Red team gets points when red players die (should be blue)"

### Step 2: Trace the Flow

Write out what SHOULD happen:
```
1. Player clicks door → Click trigger fires
2. Click trigger → DoorOpen task becomes Active
3. DoorOpen Active → Hide Object effect runs
4. Door becomes invisible
```

Then identify WHERE it breaks:
- Does the trigger fire? (Check Task Debug Panel)
- Does the task change state? (Check Task Debug Panel)
- Does the effect run? (Check if object changes)

### Step 3: Use Task Debug Panel

**This is your most important debugging tool.**

Access: Space Options > Task Debug Panel

**What to check:**
1. Is the task in the expected state?
2. Does clicking the trigger change the state?
3. Look at the history log - what events fired?

**Pro tip:** Keep Task Debug Panel open while testing. Watch task states change in real-time.

### Step 4: Check Common Causes

| Symptom | Likely Cause |
|---------|--------------|
| Trigger doesn't fire | Wrong trigger type, object not selected, trigger cube too small |
| Task changes but no effect | Effect not added, wrong "on state" setting |
| Effect runs for wrong player | Task is Multiplayer when it should be Single Player |
| Variable not updating | Wrong variable name (case-sensitive), using wrong syntax |
| Function Effect does nothing | Missing "Trigger on Task Change" checkbox |
| Numbers look weird | Not using decimal notation (use 1.0 not 1) |

### Step 5: Isolate and Test

If you can't find the bug:
1. Create a NEW simple task that does just one thing
2. Test if that works
3. Add complexity one step at a time
4. Find exactly which addition breaks it

---

## Common Bugs and Fixes

### Bug: "Task fires but effects don't run"

**Causes:**
1. Effects attached to wrong state (e.g., effects on "Completed" but task goes to "Active")
2. Missing "Trigger on Task Change" checkbox for Function Effects
3. Condition in Function Effect always evaluates false

**Fix:** Check which state triggers your effects. Open the task, look at "On Active", "On Completed", etc.

---

### Bug: "Variable shows wrong value"

**Causes:**
1. Case mismatch (`Red_Score` vs `red_score`)
2. Using $T instead of $N (task state vs variable)
3. Not using decimal notation
4. Multiple places updating the same variable

**Fix:**
1. Check exact spelling in Variable Manager
2. Use $N{variableName} for variables
3. Use 1.0 not 1

---

### Bug: "Multiplayer task runs effects for all players"

**Cause:** That's what Multiplayer tasks do! When the task state changes, ALL players run the effects.

**Fix:** If only one player should be affected, use Single Player task instead.

---

### Bug: "Timer speeds up when second player joins"

**Cause:** Each player is running their own timer loop, all incrementing the same variable.

**Fix:** Use Single Player tasks for timer loops. Multiplayer tasks cause all players to run the loop simultaneously.

**Note:** Portals does not have a native shared timer system. For multiplayer timer displays, use local JavaScript timing in iframes triggered by game state changes.

---

### Bug: "Iframe not receiving messages"

**Causes:**
1. JSON with colons (`:`) breaks the parser
2. Wrong variable syntax (using $N instead of |pipes|)
3. Iframe not loaded yet when message sent

**Fix:**
1. Use underscore format: `score_|Red_Score|` not `{"score": |Red_Score|}`
2. Use pipe syntax in Send Message To Iframes
3. Use ready handshake pattern for timing

---

### Bug: "Player can join both teams"

**Cause:** No check to prevent re-joining if already on a team.

**Fix:** Add condition before setting team:
```
if($N{Player_Team} == 0.0,
   SetVariable('Player_Team', 1.0, 0.0),
   0.0
)
```

---

### Bug: "Task doesn't reset, only fires once"

**Cause:** Tasks don't auto-reset. Once they reach a state, they stay there.

**Fix:** Always add a reset effect:
```
SetTask('MyTask', 'NotActive', 0.1)
```

---

### Bug: "Function Effect condition never true"

**Causes:**
1. Comparing wrong types (string vs number)
2. Not using decimal notation
3. Logic error in condition

**Debug approach:**
1. Simplify to just `SetVariable('debug', 1.0, 0.0)` - does it run at all?
2. Add debug variables to see what values actually are
3. Check if condition should use == or >= or !=

---

### Bug: "Effects fire in wrong order"

**Cause:** Effects on the same task run in order, but there's no guarantee of timing between different tasks.

**Fix:** Use delays to enforce order:
```
SetTask('Step1', 'Active', 0.0)
SetTask('Step2', 'Active', 0.5)  // Runs 0.5 sec after Step1
SetTask('Step3', 'Active', 1.0)  // Runs 1 sec after Step1
```

---

### Bug: "Multiplayer variables not syncing"

**Cause:** Multiplayer variables take 2-3 seconds to sync across all players.

**Fix:** Add delays before checking multiplayer variables:
```
// On Player Login, wait 3 seconds before checking shared state
SetTask('DelayedCheck', 'Active', 3.0)
```

---

## Debugging Iframes

### Enable Browser Console

When testing iframes:
1. Open browser developer tools (F12)
2. Go to Console tab
3. Look for errors and your console.log() messages

### Add Debug Logging

Add console.log() statements to track what's happening:
```javascript
PortalsSdk.setMessageListener(function(message) {
  console.log('[Iframe] Received:', message);  // See what Portals sends

  // Your parsing code...

  console.log('[Iframe] Parsed value:', parsedValue);  // See what you extracted
});
```

### Test Iframe Standalone

Open your iframe URL directly in a browser to test:
1. Does the page load without errors?
2. Are there any console errors?
3. Does the UI render correctly?

Then test the Portals integration separately.

### Debug Display

Add a visible debug element to your iframe:
```html
<div id="debug" style="position:fixed;bottom:10px;left:10px;background:black;color:lime;padding:5px;font-family:monospace;font-size:12px;z-index:9999;">
  Waiting for messages...
</div>

<script>
function debug(msg) {
  document.getElementById('debug').textContent = msg;
  console.log('[Debug]', msg);
}

PortalsSdk.setMessageListener(function(message) {
  debug('Received: ' + JSON.stringify(message).substring(0, 50));
  // ... rest of handler
});
</script>
```

Remove this before publishing!

---

# IFRAME BEST PRACTICES

## The Golden Rules of Portals Iframes

### Rule 1: Different Syntax for Each Direction

This is the #1 source of iframe bugs. The syntax is DIFFERENT depending on direction:

**Portals → Iframe (Send Message To Iframes effect):**
```
score_|Red_Score|_|Blue_Score|
```
- Use pipe syntax `|variableName|` for variables
- Built-in variables: `|username|` (player ID/name), `|position|` (all players' positions)
- Do NOT use `$N{variableName}` - that's for Function Effects only
- Do NOT use JSON with colons - it breaks the parser

**Iframe → Portals (JavaScript):**
```javascript
PortalsSdk.sendMessageToUnity(JSON.stringify({
  TaskName: 'myTask',
  TaskTargetState: 'SetNotActiveToActive'
}));
```
- MUST use JSON.stringify()
- MUST use exact TaskTargetState values
- Raw objects cause "[object Object] is not supported" error

### Rule 2: Iframes Load Asynchronously

**The Problem:** When you activate an iframe AND send a message in the same task, the message arrives BEFORE the iframe finishes loading. The iframe never receives it.

**Console log showing this bug:**
```
[12:00:01] Sending message to iframes: scores_50_32
[12:00:01] Activating Iframe Event https://example.com/game-over.html
[12:00:02] [Iframe] Initialized - waiting for messages  ← Too late!
```

**The Solution: Ready Handshake Pattern**

1. Pass static data in URL parameters (always available)
2. Iframe sends "ready" signal when loaded
3. Portals sends dynamic data AFTER ready signal

```
Task activates iframe with ?winner=red in URL
         ↓
Iframe loads, reads winner from URL
         ↓
Iframe sends: gameover_ready → Completed
         ↓
Portals function triggers on gameover_ready Completed
         ↓
Portals sends: scores_50_32
         ↓
Iframe receives scores message, displays result
```

### Rule 3: Always Bust the Cache

GitHub Pages and browsers cache aggressively. Your changes won't appear without cache busting.

**Add version parameter to ALL iframe URLs:**
```
https://example.github.io/my-hud/index.html?v=1
```

**Every time you update the iframe:**
1. Push to GitHub
2. Wait 1-2 minutes for GitHub Pages to update
3. Increment version: `?v=2`, `?v=3`, etc.
4. Update the URL in Portals

**Pro tip:** Use a high random number during development (`?v=99847`) so you don't have to track versions.

### Rule 4: Handle Message Parsing Defensively

Messages from Portals can arrive in different formats. Your parsing code must handle all cases:

```javascript
PortalsSdk.setMessageListener(function(message) {
  console.log('[Iframe] Raw message:', message, typeof message);

  let msg = message;

  // Step 1: If it's a string, try to parse as JSON
  if (typeof message === 'string') {
    try {
      msg = JSON.parse(message);
    } catch (e) {
      // Not JSON - that's OK, keep as string
      // DO NOT RETURN HERE - underscore format won't be JSON
      msg = message;
    }
  }

  // Step 2: Convert to string for pattern matching
  const msgStr = typeof msg === 'string' ? msg : JSON.stringify(msg);

  // Step 3: Handle your message patterns
  if (msgStr.startsWith('score_')) {
    const value = parseFloat(msgStr.substring(6));
    if (!isNaN(value)) {
      updateScore(value);
    }
  } else if (msgStr.startsWith('time_')) {
    const value = parseFloat(msgStr.substring(5));
    if (!isNaN(value)) {
      updateTimer(value);
    }
  }
  // Add more patterns as needed
});
```

**Critical mistakes to avoid:**
- Don't `return` after JSON.parse fails - underscore format isn't JSON
- Don't assume message type - always check
- Don't forget `!isNaN()` check after parseFloat

### Rule 5: Design for Late Joiners

In multiplayer, players can join mid-game. Your iframe needs to handle this:

**Problem:** Player joins when score is 25-18 and timer is at 5:32. Their iframe shows 0-0 and 10:00.

**Solution: Sync on Load**

Option A: Request current state
```javascript
// Iframe requests sync when loaded
PortalsSdk.sendMessageToUnity(JSON.stringify({
  TaskName: 'request_sync',
  TaskTargetState: 'SetNotActiveToActive'
}));

// Portals responds with full state: sync_332_25_18
```

Option B: Continuous updates
```javascript
// Portals sends updates every second via Value Updated triggers
// Late joiner receives next update within 1 second
```

### Rule 6: Keep Iframes Stateless When Possible

Iframes can be closed and reopened. They can refresh. Don't rely on iframe state.

**Bad:** Iframe tracks score internally, only receives increments
```javascript
let score = 0;
// If iframe refreshes, score resets to 0 but game score is 25
```

**Good:** Iframe receives absolute values, displays what it's told
```javascript
// Portals always sends current total: score_25
// Iframe just displays 25, no internal tracking needed
```

### Rule 7: Transparent Backgrounds for HUDs

For HUD overlays, you want only your UI visible, not a white/colored background:

```css
html, body {
  background: transparent;  /* Critical! */
  margin: 0;
  padding: 0;
  overflow: hidden;
}

.hud-container {
  /* Apply visible background only to your content */
  background: rgba(0, 0, 0, 0.8);
  border-radius: 8px;
  padding: 10px;
}
```

**The key:** Keep html/body transparent, apply backgrounds only to content containers.

### Rule 8: Size Iframes Correctly

**For HUDs:** Size to match your content exactly
- If your HUD bar is 600x80px, set iframe to 600x80
- Extra space will be transparent but may block clicks

**For Popups/Modals:** Size to fit with padding
- Leave room for close button if visible
- Consider different screen sizes

**Position fields:** Only fill in what you need, leave others BLANK (not 0)
- Top-centered: Only set `Top Position: 0`
- Bottom-right: Only set `Bottom Position` and `Right Position`

---

# INTERPRETING PORTALS CONSOLE LOGS

## How to Read the Console

Access: Open browser developer tools (F12) → Console tab while in Portals

The console shows everything happening in your space. Learning to read it is essential for debugging.

## Log Types and What They Mean

### Task State Changes

```
[TaskSystem] Task 'JoinRed' state changed: NotActive → Active
[TaskSystem] Trigger: User Enter Trigger on TriggerCube_RedZone
```

**What this tells you:**
- Which task changed
- What state it changed to
- What trigger caused it

**Debugging use:** Verify triggers are firing and tasks are changing state.

---

### Effect Execution

```
[EffectSystem] Executing effects for 'JoinRed' on Active
[EffectSystem] → Teleport to 'RedSpawn1'
[EffectSystem] → Notification: "Joined Red Team"
[EffectSystem] → Function Effect executed
```

**What this tells you:**
- Which effects ran
- In what order
- Whether they completed

**Debugging use:** Verify effects are attached to the right state and running.

---

### Function Effect Details

```
[FunctionEffect] Evaluating: if($N{Player_Team} == 0.0, SetVariable('Player_Team', 1.0, 0.0), 0.0)
[FunctionEffect] $N{Player_Team} = 0
[FunctionEffect] Condition true, executing: SetVariable('Player_Team', 1.0, 0.0)
[FunctionEffect] Result: Variable 'Player_Team' set to 1
```

**What this tells you:**
- The exact expression being evaluated
- Current variable values
- Which branch executed
- The result

**Debugging use:** See why conditions pass or fail, verify variable values.

---

### Variable Updates

```
[VariableManager] Variable 'Red_Score' updated: 24 → 25
[VariableManager] Source: Function Effect in task 'KillHandler'
```

**What this tells you:**
- Which variable changed
- Old and new values
- What caused the change

**Debugging use:** Track variable changes, find unexpected modifications.

---

### Iframe Messages

```
[IframeManager] Sending message to iframes: score_25
[IframeManager] Activating Iframe: https://example.com/hud.html?v=5
[IframeManager] Received from iframe: {"TaskName":"gameover_ready","TaskTargetState":"SetNotActiveToCompleted"}
```

**What this tells you:**
- Messages being sent to iframes
- When iframes are activated/deactivated
- Messages received from iframes

**Debugging use:** Verify message flow, check timing issues.

---

### Error Messages

```
[ERROR] NCalc parse error in Function Effect: Unexpected token ':' at position 15
[ERROR] Task 'InvalidTask' not found
[ERROR] Spawn point 'RedSpawn1' not found (check case sensitivity)
[ERROR] Variable 'score' is undefined
```

**What this tells you:**
- Syntax errors in expressions
- Missing references
- Typos in names

**Debugging use:** Direct pointer to what's broken.

---

## Common Log Patterns and What They Mean

### Pattern: Message Sent Before Iframe Activated

```
[12:00:01.100] Sending message to iframes: gameover_red_50_32
[12:00:01.150] Activating Iframe: game-over.html
```

**Problem:** Message sent 50ms BEFORE iframe activated. Iframe won't receive it.

**Fix:** Use ready handshake pattern. Iframe signals when loaded, then receives message.

---

### Pattern: Rapid Task State Cycling

```
[12:00:01.000] Task 'GameTimer' state: NotActive → Active
[12:00:01.010] Task 'GameTimer' state: Active → NotActive
[12:00:01.020] Task 'GameTimer' state: NotActive → Active
[12:00:01.030] Task 'GameTimer' state: Active → NotActive
... (hundreds more)
```

**Problem:** Task is looping too fast, probably missing delay or wrong timing.

**Fix:** Check your reset and loop delays. Should be:
```
SetTask('GameTimer', 'NotActive', 0.9)  // Reset
SetTask('GameTimer', 'Active', 1.0)    // Loop (must be > reset delay)
```

---

### Pattern: Variable Shows NaN or Undefined

```
[FunctionEffect] $N{Red_Score} = NaN
[FunctionEffect] Evaluating: $N{Red_Score} + 1.0
[FunctionEffect] Result: NaN
```

**Problem:** Variable was never initialized or was set to non-numeric value.

**Fix:** Initialize variables on Player Login:
```
SetVariable('Red_Score', 0.0, 0.0)
```

---

### Pattern: Effect Runs for All Players

```
[Player1] KillHandler Active - awarding point to Blue
[Player2] KillHandler Active - awarding point to Blue
[Player3] KillHandler Active - awarding point to Blue
```

**Problem:** Multiplayer task running effects for everyone when only one player died.

**Fix:** KillHandler should be Single Player task, not Multiplayer.

---

### Pattern: Condition Always False

```
[FunctionEffect] Evaluating: if($N{Player_Team} == 1, ...)
[FunctionEffect] $N{Player_Team} = 1.0
[FunctionEffect] Condition false
```

**Problem:** Comparing `1.0` to `1` (different types in some cases).

**Fix:** Always use decimal notation:
```
if($N{Player_Team} == 1.0, ...)
```

---

## Debug Logging Strategy

### Add Strategic Console Logs

When debugging, add console.log() at key decision points:

```javascript
PortalsSdk.setMessageListener(function(message) {
  console.log('[RECV] Raw:', message);
  console.log('[RECV] Type:', typeof message);

  // ... parsing ...

  console.log('[RECV] Parsed:', parsedValue);
  console.log('[RECV] Action:', whatWeWillDo);
});
```

### Use Descriptive Prefixes

Make logs easy to filter:
- `[HUD]` - HUD iframe logs
- `[GameOver]` - Game over screen logs
- `[Timer]` - Timer-related logs
- `[RECV]` - Received messages
- `[SEND]` - Sent messages
- `[ERROR]` - Error conditions

### Log State Changes

```javascript
function updateScore(team, newScore) {
  console.log(`[HUD] Score update: ${team} = ${newScore}`);
  // ... update display ...
  console.log(`[HUD] Display updated`);
}
```

### Remove Debug Logs for Production

Before publishing:
1. Remove or comment out console.log statements
2. Remove visible debug displays
3. Test one more time to make sure nothing broke

---

# QUESTS

Turn any task into a trackable quest:

1. Go to **Space Options > Tasks**
2. Select the task
3. Toggle **Visibility On**

**Quest States:**
- NotActive → Not visible in log
- Active → Visible, incomplete
- Completed → Visible, marked complete

**Quest Groups:** Assign same group name to organize tasks together.

**Rewards:** Add wearables/collectibles granted on completion (requires Portals team assistance for item setup).

---

# VARIABLE MANAGER

Manage all variables created with Update Value effect.

**Location:** Space Options → Variable Manager

**Settings:**
- **Persistent**: Value saved across sessions (survives refresh/logout)
- **Multiplayer**: All players share the same value

**Defaults:** Non-persistent, single-player

**Initializing Variables:** Variables do not have a built-in "default value" setting. To initialize variables, use a Player Login trigger with SetVariable effects:
```
SetVariable('Player_Score', 0.0, 0.0)
SetVariable('Player_Team', 0.0, 0.0)
```

---

# ADVANCED TOOLING: FUNCTION EFFECT

Scripting system based on NCalc expression language.

## Reading Values

| Syntax | Returns | Example |
|--------|---------|---------|
| `$T{taskName}` | Task state as text | `$T{door}` → 'Active' |
| `$TN{taskName}` | Task state as number | `$TN{door}` → 1 |
| `$N{variableName}` | Variable value | `$N{coins}` → 50 |
| `$N{timerName}` | Timer elapsed time (seconds) | `$N{RaceTimer}` → 45.5 |

**Task State Numbers:** 0=NotActive, 1=Active, 2=Completed

**Timer Values:** You can read any running timer's elapsed time using `$N{timerName}`. The timer must be started first using the Start Timer effect.

## Setting Values

```
SetTask(taskName, 'TaskState', delaySeconds)
SetTaskState(taskName, 'TaskState')
SetVariable(variableName, value, delaySeconds)
```

**Examples:**
```
SetTask('door', 'Active', 0.0)           // Immediate
SetTask('alarm', 'NotActive', 5.0)       // 5-second delay
SetTaskState('door', 'NotActive')        // No delay parameter
SetVariable('coins', $N{coins} + 10, 0.0)
```

**SetTask vs SetTaskState:**
- `SetTask()` - Has delay parameter, use for timed actions
- `SetTaskState()` - No delay, use in reset functions triggered by task status changes

## Math Operators

| Operator | Example |
|----------|---------|
| `+` | `$N{coins} + 10` |
| `-` | `$N{health} - 1` |
| `*` | `$N{score} * 2` |
| `/` | `$N{time} / 2` |
| `%` | `$N{coins} % 2` (remainder) |
| `**` | `2 ** 3` (exponent = 8) |

## Comparison Operators

| Operator | Example |
|----------|---------|
| `==` | `$N{coins} == 10` |
| `!=` | `$T{quest} != 'NotActive'` |
| `>` | `$N{coins} > 10` |
| `<` | `$N{health} < 5` |
| `>=` | `$N{coins} >= 10` |
| `<=` | `$N{health} <= 0` |

## Logic Operators

| Operator | Name | Example |
|----------|------|---------|
| `&&` | AND | `$T{task1} == 'Active' && $T{task2} == 'Completed'` |
| `\|\|` | OR | `$T{task1} == 'Completed' \|\| $T{task2} == 'Completed'` |
| `!` | NOT | `!($T{alarm} == 'Active')` |

## Conditions

**if() - Single condition:**
```
if(condition, whenTrue, whenFalse)

if($N{coins} >= 10,
   SetVariable('doorUnlocked', 1, 0.0),
   0
)
```

**ifs() - Multiple conditions (first match wins):**
```
ifs(
  $N{health} <= 0, SetVariable('warning', 3, 0.0),
  $N{health} <= 3, SetVariable('warning', 2, 0.0),
  $N{health} <= 6, SetVariable('warning', 1, 0.0),
                   SetVariable('warning', 0, 0.0)
)
```

## OnChange Triggers

```
OnChange('taskName', 'TaskState')     // Specific state
OnChange('taskName')                   // Any state change
OnChange('variableName', '>= 10')     // Variable condition
```

**Task completion triggers variable:**
```
if(OnChange('puzzle1', 'Completed'),
   SetVariable('doorUnlocked', 1.0, 0.0),
   0.0)
```

**Variable threshold completes task:**
```
if(OnChange('coins', >= 10.0),
   SetTask('buyDoor', 'Completed', 0.0),
   0.0)
```

**Multiple conditions with current state check:**
```
(OnChange('task1', 'Active') || OnChange('task2', 'Completed'))
&& $T{task1} == 'Active'
&& $T{task2} == 'Completed'
```

**State change with conditional actions:**
```
if(OnChange('questStep'),
   ifs($T{questStep} == 'NotActive', SetVariable('hintText', 0.0, 0.0),
       $T{questStep} == 'Active', SetVariable('hintText', 1.0, 0.0),
       SetVariable('hintText', 2.0, 0.0)),
   0.0)
```

## SelectRandom

```
SelectRandom(item1, item2, item3, ...)
```

**Random number reward:**
```
SetVariable('coins', $N{coins} + SelectRandom(1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0), 0.0)
```

**50/50 chance:**
```
SelectRandom(true, false)
```

**Random task state:**
```
SetTask('alarm', SelectRandom('NotActive', 'Active', 'Completed'), 0.0)
```

## Math Functions

| Function | Description | Example |
|----------|-------------|---------|
| `Min(a, b)` | Returns smaller of two numbers | `Min($N{coins}, 100.0)` → cap at 100 |
| `Max(a, b)` | Returns larger of two numbers | `Max($N{health}, 0.0)` → prevent negative |
| `Round(number)` | Rounds to nearest whole | `Round(3.6)` → 4 |
| `Abs(number)` | Absolute value | `Abs(-5)` → 5 |
| `Floor(number)` | Rounds down | `Floor(3.9)` → 3 |
| `Ceiling(number)` | Rounds up | `Ceiling(3.1)` → 4 |
| `Sqrt(number)` | Square root | `Sqrt(9.0)` → 3 |

**Nesting functions:**
```
Min(Max($N{health}, 0.0), 100.0)   // Clamp health between 0-100
```

## Multiplayer Functions

Functions for working with multiple players simultaneously. Essential for team games, role assignment, and any logic affecting multiple players.

### Player Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `[Players]` | List | All players currently in the room |

**Built-in player properties:**
- `playerName` - The player's username
- `health` - The player's health (default: 100, no max limit)

### SelectRandomPlayers([Players], count)

Picks random players from a list. Selection is **deterministic** (all clients get same result) and **persistent** (survives reconnects).

```
SelectRandomPlayers([Players], 2)   // Pick 2 random players
```

### SelectPlayersParameters([Players], 'parameterName')

Gets a parameter value from each player in a list.

```
SelectPlayersParameters([Players], 'health')   // Returns [100, 85, 100, 50]
SelectPlayersParameters(SelectRandomPlayers([Players], 3), 'playerName')   // Names of 3 random players
```

### SetPlayersParameters([Players], 'parameterName', value)

Sets a parameter on all players in a list. Changes sync to all clients automatically.

```
SetPlayersParameters([Players], 'canMove', true)   // Enable movement for everyone
```

### PrintString(value)

Prints a value to the browser console for debugging.

```
PrintString(SelectPlayersParameters([Players], 'playerName'))   // Debug: list all player names
```

### Multiplayer Function Examples

**Impostor Assignment (Among Us style):**
```
SetPlayersParameters([Players], 'impostor', false) +
SetPlayersParameters(SelectRandomPlayers([Players], 2), 'impostor', true)
```
Sets everyone to non-impostor, then picks 2 random impostors. Use on game start trigger.

**Team Assignment (Red vs Blue):**

First track player count with a multiplayer variable incremented when players enter a "ready" zone.

```
SetPlayersParameters([Players], 'team', 'blue') +
SetPlayersParameters(SelectRandomPlayers([Players], Floor($N{PlayerCount} / 2.0)), 'team', 'red')
```
Sets everyone to blue, then switches half to red. Guarantees all players are assigned and teams are balanced.

**One Hunter, Everyone Else Hides:**
```
SetPlayersParameters([Players], 'role', 'hider') +
SetPlayersParameters(SelectRandomPlayers([Players], 1), 'role', 'hunter')
```

**Damage All Players:**
```
SetPlayersParameters([Players], 'health', 50)   // Set everyone's health to 50
```

### Multiplayer Function Notes

- **One trigger, all clients:** When one player triggers a multiplayer function, the result propagates to everyone
- **Order matters:** In chained expressions using `+`, later operations can override earlier ones
- **Custom parameters:** Use any variable name from the Variable system, not just built-in ones
- **Nesting works:** Use output of one function as input to another

## Timer Variables

You can read timer values as variables and manipulate them in calculations.

**Reading timer values:**
```
$N{RaceTimer}              // Returns elapsed seconds (e.g., 45.5)
$N{RaceTimer} >= 60.0      // Check if timer is 60+ seconds
```

**Manipulating timer values:**
```
SetVariable('HalfTime', $N{RaceTimer} / 2.0, 0.0)           // Divide time by 2
SetVariable('BonusTime', $N{RaceTimer} + 30.0, 0.0)         // Add 30 seconds
SetVariable('TimeRemaining', 120.0 - $N{RaceTimer}, 0.0)    // Calculate remaining time
SetVariable('TimeScore', 1000.0 - ($N{RaceTimer} * 10.0), 0.0)  // Time-based scoring
```

**Common patterns:**

Checkpoint time storage:
```
SetVariable('Checkpoint1Time', $N{RaceTimer}, 0.0)
```

Time-based scoring (faster = more points):
```
SetVariable('Score', Max(1000.0 - ($N{RaceTimer} * 5.0), 0.0), 0.0)
```

Time penalty on death:
```
SetVariable('PenaltyTime', $N{GameTimer} + 10.0, 0.0)
```

**Note:** Timer must be started (Start Timer effect) before reading. Unstarted timers return 0.

## Important Notes

- **Always use decimal notation:** `0.0`, `1.0`, `50.0` (not `0`, `1`, `50`) to avoid type errors
- **Use nested if(), NOT ifs()** - ifs() may have bugs in some cases
- **Tasks don't auto-reset** - always add reset function effects
- **Enable "Trigger on Task Change"** checkbox for Function Effects

---

# MULTIPLAYER CONSIDERATIONS

## Single Player vs Multiplayer Tasks

| Task Type | Behavior |
|-----------|----------|
| **Single Player** | Effects run only for the player who triggered it |
| **Multiplayer** | When task state changes, effects run for ALL players |

**Critical:** For looping tasks (timers, game loops), use **Single Player** tasks. Multiplayer tasks will cause all players to run the loop, causing acceleration/duplication bugs.

## Multiplayer Variable Sync Delay

Multiplayer variables take **2-3 seconds** to sync across all players. This causes race conditions when:
- Checking if another player already set a value
- Coordinating actions between players

**Solution:** Add delays before checking multiplayer variables:
```
// On Player Login, delay 3 seconds before checking shared state
SetTask('DelayedCheck', 'Active', 3.0)
```

## Self-Looping Task Pattern

For continuous updates (use Single Player tasks to prevent acceleration):

```
// GameLoop task (Single Player, on Active):

// Effect 1: Your game logic here
SetVariable('SomeValue', $N{SomeValue} + 1.0, 0.0)

// Effect 2: Reset for next loop
SetTask('GameLoop', 'NotActive', 0.9)

// Effect 3: Loop
SetTask('GameLoop', 'Active', 1.0)
```

**Note on Timers:** Portals does not have a native shared timer system that syncs across players. For multiplayer timer displays, use local JavaScript timing in iframes triggered by game state changes.

---

# LEADERBOARDS

## Post Score to Leaderboard

| Setting | Description |
|---------|-------------|
| **Value Label** | Must match the Leaderboard Score Label (e.g., "score", "coins") |

**Compatibility:**
- Works with: Trigger Cube, Building Cube, Nine Cube, Custom Import
- Does NOT work with: NPC

**Note:** For time-based leaderboards, the timer auto-posts when it ends.

---

# USING IFRAMES

Embed external web pages with bidirectional communication.

## Important: Iframe is an Effect, Not a Tool

Iframe is an **effect**, not a building tool. To display an iframe:
1. Create a task with a trigger (e.g., Player Login)
2. Add the Iframe effect to that task
3. The iframe appears when the task activates

## Iframe Effect Settings

| Setting | Description |
|---------|-------------|
| **Iframe URL** | URL to the web page |
| **Layer Order** | Z-index for stacking (higher = on top) |
| **Left Position (px)** | Distance from left edge |
| **Right Position (px)** | Distance from right edge |
| **Top Position (px)** | Distance from top edge |
| **Bottom Position (px)** | Distance from bottom edge |
| **Width (px)** | Iframe width in pixels |
| **Height (px)** | Iframe height in pixels |
| **NPC will animate** | Toggle mouth animation for NPC dialogues |

## Positioning Tips

**Important:** Only fill in position/size values you want to change. **Leave other fields blank** - don't enter zeros for fields you don't need.

**For top-centered HUD:**
- Set **only** `Top Position: 0`
- Leave Left, Right, Width, Height **blank**
- The iframe content will auto-center if CSS uses `justify-content: center`

**For bottom-right popup:**
- Set only `Bottom Position` and `Right Position`
- Leave other fields blank

**For fixed-size centered iframe:**
- Calculate Left: `(screen width - iframe width) / 2`
- Example: 1920px screen, 400px iframe → Left Position = 760
- Note: Fixed positioning doesn't adapt to different screen sizes

## Creating Transparent HUD Iframes

For HUD overlays where only the content should be visible (no background):

```css
body {
  background: transparent;
}

/* Wrap content in a container with the visible background */
.hud-container {
  display: flex;
  background: rgba(0,0,0,0.9);
  border-radius: 8px;
}
```

**Key principle:** Keep body/html transparent, apply backgrounds only to content containers. Size the iframe to match content exactly.

## SDK Setup

Add to your HTML:
```html
<script src="https://portals-labs.github.io/portals-sdk/portals-sdk.js?v=10005456"></script>
```

## Sending Messages to Unity (Iframe → Portals)

```javascript
// MUST stringify the JSON object
PortalsSdk.sendMessageToUnity(JSON.stringify({
  TaskName: "level1_intro",
  TaskTargetState: "SetNotActiveToActive"
}));
```

**Valid TaskTargetState values:**
- `ToNotActive`
- `SetNotActiveToActive`
- `SetActiveToCompleted`
- `SetCompletedToActive`
- `SetAnyToCompleted`
- `SetAnyToActive`
- `SetActiveToNotActive`
- `SetCompletedToNotActive`
- `SetNotActiveToCompleted`

## Receiving Messages from Unity (Portals → Iframe)

Use the SDK's message listener to receive commands from Portals:

```javascript
// Register the listener
PortalsSdk.setMessageListener(function(message) {
  console.log('Received:', message);

  let data = message;

  // Parse if string - but DON'T return on failure (might be underscore format)
  if (typeof message === 'string') {
    try {
      data = JSON.parse(message);
    } catch (e) {
      // Not JSON - keep as string for underscore format parsing
      data = message;
    }
  }

  const msg = typeof data === 'string' ? data : JSON.stringify(data);

  // Handle underscore format (recommended)
  if (msg.startsWith('score_')) {
    const score = parseFloat(msg.substring(6));
    if (!isNaN(score)) updateScore(score);
  } else if (msg.startsWith('time_')) {
    const elapsed = parseFloat(msg.substring(5));
    if (!isNaN(elapsed)) updateTimer(elapsed);
  }
});
```

**Sending from Portals:**

**CRITICAL:** JSON with colons (`:`) breaks Portals' NCalc parser. Use underscore format instead:

| Data | Message Format | Effect Setting |
|------|----------------|----------------|
| Score | `score_25` | `score_\|Score\|` |
| Time | `time_120` | `time_\|Elapsed_Seconds\|` |
| Team scores | `sync_120_25_30` | `sync_\|Time\|_\|Red\|_\|Blue\|` |

**Note:** In "Send Message To Iframes" effect, use `|variableName|` (pipe syntax), NOT `$N{variableName}`.

**Tip:** Use `Value Updated` trigger on variables to automatically send iframe updates when values change.

## Close Iframe

```javascript
// Must be inside user event handler (onclick)
PortalsSdk.closeIframe();
```

## Game Over / Result Screen Pattern

For screens that display results (winner, scores), use a **two-step handshake** to ensure the iframe is loaded before receiving data:

**Problem:** Portals sends messages before iframe finishes loading, so data is lost.

**Solution:**
1. Pass static data (winner) in URL parameters
2. Have iframe signal "ready" when loaded
3. Portals sends dynamic data (scores) after ready signal

**Step 1: Create iframe URLs with winner in params**
```
game-over.html?winner=red&v=1
game-over.html?winner=blue&v=1
game-over.html?winner=tie&v=1
```

**Step 2: Iframe signals ready on load**
```javascript
// In iframe, after DOM loaded:
PortalsSdk.sendMessageToUnity(JSON.stringify({
  TaskName: 'gameover_ready',
  TaskTargetState: 'SetNotActiveToCompleted'
}));
```

**Step 3: Portals function sends scores on ready**
- Trigger: `gameover_ready` status is `Completed`
- Action: Send Message To Iframes → `scores_|Red_Score|_|Blue_Score|`

**Step 4: Iframe reads URL params + listens for scores**
```javascript
// Read winner from URL (available immediately)
const params = new URLSearchParams(window.location.search);
const winner = params.get('winner');

// Listen for scores message
PortalsSdk.setMessageListener(function(msg) {
  if (msg.startsWith('scores_')) {
    const parts = msg.split('_');
    const redScore = parts[1];
    const blueScore = parts[2];
    displayGameOver(winner, redScore, blueScore);
  }
});
```

**Note:** Bump the `v=` version number when updating iframe to bust cache.

## URL Parameters

| Parameter | Effect |
|-----------|--------|
| `?noCloseBtn=true` | Hide close button |
| `?hideMaximizeButton=true` | Hide maximize |
| `?hideRefreshButton=true` | Hide refresh |
| `?maximized=true` | Open fullscreen |
| `?forceClose=true` | X closes instead of minimize |

**Example:**
```
https://example.com/page.html?noCloseBtn=true&maximized=true
```

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| "[object Object] is not supported" | Sending raw object | Use `JSON.stringify()` |
| "Failed to launch uniwebview" | Testing in browser | Test in Unity WebView |
| "User gesture required" | closeIframe outside click | Wrap in onclick handler |
| Iframe not receiving messages | JSON with colons | Use underscore format: `score_\|Score\|` |
| Timer not updating display | Early return in JS | Don't `return` after JSON.parse failure |
| Timer accelerates with 2+ players | All players incrementing | Use Single Player task for loops |
| Variables not syncing | Race condition | Add 3-second delay before checking |
| Iframe misses initial message | Message sent before load | Use ready handshake pattern (see Game Over Pattern) |
| URL params show literal \|Var\| | Portals doesn't interpolate URL params | Pass static values in URL, dynamic via message |

---

# HOW TO: TOKEN TRADING SPACE

## Part 1: Buy/Sell Zones

**Buy Zone Setup:**
1. Place Trigger Cube
2. Add User Enter Trigger → Show Token Swap effect
3. Configure: Buy=On, Sell=Off, Token Address, Wallet Address
4. Add User Exit Trigger → Hide Token Swap effect

**Sell Zone:** Same setup with Buy=Off, Sell=On

## Part 2: 3D Candlestick Chart

1. Copy token contract address
2. Open inventory → Select Chart item
3. Paste contract address
4. Click "Spawn Chart"
5. Position in space

---

# QUICK REFERENCE

## Task State Transitions

```
NotActive → Active → Completed
     ↑         ↓         ↓
     ←─────────←─────────←
```
(Any state can transition to any other)

## Common Patterns

**Door that opens on click, closes after exit:**
- Click Trigger → Set task Active (plays open animation)
- Exit Trigger with delay → Set task NotActive (plays close animation)

**Collectible counter:**
- Item Collected Trigger → Update Value effect (+1)
- Display Value effect to show count

**Multi-step quest:**
- Create dependent tasks
- Each task completion triggers next task to Active
- Toggle visibility for quest log tracking

**Auto-reset task (resets immediately after firing):**
Create a separate reset function for each task:
- Trigger: Task status is `Active` (or `Completed`)
- Action: `SetTaskState('taskName', 'NotActive')`

This pattern is useful for:
- Win condition tasks that need to fire again next game
- Iframe-triggered tasks (gameover_ready, etc.)
- Any task that should be reusable without manual reset

**Example reset functions:**
```
// Function: reset_red_wins
// Trigger: timer_red_wins status is Active
// Action: SetTaskState('timer_red_wins', 'NotActive')

// Function: reset_gameover_ready
// Trigger: gameover_ready status is Completed
// Action: SetTaskState('gameover_ready', 'NotActive')
```

---

# GAME DESIGN PATTERNS

## Core Loop
All games follow: **Player Action → Feedback → Reward → Repeat**

Spend 10-15 minutes designing before building to prevent confusion and edge cases.

## Pattern Types

| Pattern | Best For | Complexity |
|---------|----------|------------|
| **Collectible** | Treasure hunts, coin collection, exploration | Beginner |
| **Puzzle** | Escape rooms, logic challenges, hidden objects | Intermediate |
| **Quest/RPG** | Story-driven, NPC interactions, progression | Intermediate |
| **Racing** | Time trials, obstacle courses, leaderboards | Beginner |

---

# COMMON GOTCHAS

## Function Effects
- **Decimal notation required:** Use `10.0` not `10`
- **Case-sensitive task names:** `$T{Open Door}` works, `$T{open door}` doesn't
- **Single quotes for strings:** Use `'Active'` not `"Active"`
- **Enable "Trigger on Task Change":** Effects won't execute without this checkbox
- **Avoid ifs():** Use nested `if()` instead due to known bugs

## Tasks
- **No auto-reset:** Manually reset completed tasks if you want repeatable actions
- **Non-persistent tasks reset:** Check Space Options if progress vanishes after refresh
- **Multiplayer tasks are shared:** All players see same state; use single-player for individual progress
- **Dependent tasks:** Parent must reach "Completed" state, not just "Active"

## Triggers
- **Collision vs User Enter:** Collision handles physics; use "User Enter Trigger" for zone entry
- **Trigger cubes invisible during play:** Use build mode to verify placement
- **Key triggers need focus:** Won't work if Portals window loses focus

## NPCs
- **Rigged GLB avatars required:** Standard 3D models won't animate
- **NPC-specific effects:** "Turn To Player" and "Walk to Position" only work on NPC objects
- **Case-sensitive animations:** Names must match exactly what's in the GLB file

## Leaderboards
- **Value Label must match:** Effect label must correspond to Leaderboard label
- **Timer auto-posts:** Racing timer leaderboards post automatically when stopped
- **NPCs can't post scores:** Use Trigger Cubes instead

## Variables
- **Created on first use:** No pre-declaration needed
- **Check persistence settings:** Verify persistent and multiplayer settings in Variable Manager
- **Unset variables are undefined:** Initialize variables when players enter

## Portals/Teleportation
- **Spawn Name is case-sensitive:** Leave blank for default spawn
- **Auto Teleport:** ON = immediate on contact; OFF = requires X key
- **Cross-space teleports reset data:** Non-persistent tasks and variables reset when switching spaces

## Quick Debug Checklist
1. Open Task Debug Panel to verify triggers fire
2. Check exact names (case and space-sensitive)
3. Verify effect configuration settings
4. Use decimal notation (0.0, not 0)
5. Enable required checkboxes
6. Test simple cases first
7. Review Variable Manager values
8. Check browser console for iframe errors

---

# RESOURCES

- **Official Docs:** https://prtls.gitbook.io/portals-building-guide
- **Video Tutorials:** Available in Building Basics section
- **Portals SDK:** https://portals-labs.github.io/portals-sdk/portals-sdk.js
- **Discord:** Community help and discussions
