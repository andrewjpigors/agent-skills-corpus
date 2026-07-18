---
name: gdevelop-game
description: Specialist in GDevelop 5 game development for creating, structuring, organizing assets, implementing menus, levels, 2D platformers, 3D FPS, game bases with start/end screens, creative phase design, asset management from local folders, and best practices for full games
metadata:
  engine: gdevelop-5
  genres: platformer,3d-fps,arcade,puzzle,adventure
  platforms: web,mobile,desktop,html5
  no-code: true
---

## What I do
- Create complete GDevelop 5 games from concept to polished product
- Structure projects with external events, layouts, and organized assets
- Implement 2D platformers with player mechanics, enemies, collectibles, and level progression
- Build 3D first-person experiences with mouse look, WASD movement, and raycasting
- Design menus (main, pause, options) and end screens (win/lose, high scores)
- Architect creative level/phase design with unique mechanics per level
- Manage assets efficiently from local folders (sprites, audio, tilemaps, 3D models)
- Apply GDevelop 5 best practices for events, variables, behaviors, and performance
- Export and optimize for web (HTML5), mobile, and desktop platforms

## When to use me
Use this skill for any GDevelop 5 game project. Covers project initialization, asset management, scene setup, 2D platformer mechanics, 3D FPS mechanics, UI/menu systems, creative level design, event systems, variables/behaviors, saving/loading, and production export.

## Project Initialization & Structure

### New Project Setup
```
Project Resolution: 1920x1080 (desktop) / 1280x720 (mobile-friendly)
Default pixel rounding: Yes
Default scale mode: Linear
Scene order: MenuScene → GameScene(s) → EndScene
```

### Core Scene Architecture
- **MenuScene**: Title screen, play button, options, credits
- **GameScene(s)**: Per-level or procedural game scenes
- **PauseScene**: Overlay scene with resume/quit
- **EndScene**: Win/lose results, score display, high score, replay
- **OptionsScene**: Volume, controls, display settings

### Global Objects Setup
Create as global objects for reuse across scenes:
- UI buttons (play, pause, retry, menu)
- Text objects (score, health, timer)
- Player (if same across scenes, configure behaviors globally)
- Transition effects (fade in/out)

### External Layouts
Organize reusable level elements:
- `ExternalLayout_UI_HUD` — Health bar, score, coins, timer
- `ExternalLayout_Level_Platforms` — Common platform prefabs
- `ExternalLayout_Enemies` — Enemy templates
- `ExternalLayout_Collectibles` — Coins, power-ups, keys

### External Events
Modular event logic:
- `ExternalEvents_PlayerControls` — Movement, jump, attack
- `ExternalEvents_EnemyAI` — Patrol, chase, combat
- `ExternalEvents_Scoring` — Score calculation, combos
- `ExternalEvents_Audio` — Sound management
- `ExternalEvents_Camera` — Follow, bounds, zoom

## Asset Management

### Folder Structure
```
assets/
├── sprites/
│   ├── characters/
│   │   ├── player/
│   │   │   ├── idle_01.png
│   │   │   ├── run_01.png → run_08.png
│   │   │   ├── jump_01.png → jump_04.png
│   │   │   └── attack_01.png → attack_06.png
│   │   └── enemies/
│   │       ├── slime/
│   │       ├── bat/
│   │       └── boss/
│   ├── environment/
│   │   ├── tiles/
│   │   ├── backgrounds/
│   │   ├── platforms/
│   │   └── decorations/
│   ├── ui/
│   │   ├── buttons/
│   │   ├── icons/
│   │   ├── bars/
│   │   └── menus/
│   └── items/
│       ├── collectibles/
│       ├── powerups/
│       └── weapons/
├── audio/
│   ├── music/
│   │   ├── menu_theme.ogg
│   │   ├── level_01.ogg
│   │   └── boss_theme.ogg
│   └── sfx/
│       ├── jump.wav
│       ├── collect.wav
│       ├── hit.wav
│       └── explode.wav
├── fonts/
│   └── pixel_font.ttf
├── 3d/
│   ├── models/
│   └── textures/
└── particles/
```

### Asset Import Workflow
1. Scan local asset folder for images/audio
2. Drag & drop sprites into GDevelop's Resource manager
3. Assign animation frames following naming convention: `name_XX.png`
4. Configure collision masks (precise for characters, box for tiles)
5. Set origin points (bottom-center for characters, center for items)
6. Apply compression for audio (OGG for music, WAV for SFX)

### Sprite Animation Setup
| Animation | Speed | Loop | Frames |
|-----------|-------|------|--------|
| idle | 8 | Yes | idle_01 → idle_04 |
| run | 12 | Yes | run_01 → run_08 |
| jump_up | 8 | No | jump_01 → jump_02 |
| jump_fall | 8 | No | jump_03 → jump_04 |
| attack | 12 | No | attack_01 → attack_06 |
| hit | 10 | No | hit_01 → hit_03 |
| death | 6 | No | death_01 → death_04 |

### Tilemap Setup
- Import tileset as sprite first
- Create Tilemap object with tile size (16x16, 32x32, etc.)
- Define collision on specific tiles
- Layer multiple tilemaps for foreground/background
- Use Tilemap's built-in collision grid for performance

## Variables Strategy

### Global Variables
```
PlayerSpeed         = 300
PlayerJumpForce     = 800
PlayerGravity       = 1500
PlayerMaxHealth     = 5
PlayerHealth        = 5
PlayerLives         = 3
Score               = 0
Coins               = 0
CurrentLevel        = 0
UnlockedLevels      = 5 (JSON)
TotalTime           = 0
MusicVolume         = 80
SFXVolume           = 100
HighScore           = 0 (from Storage)
```

### Scene Variables
```
Scene_Coins          = 0        // Coins in current level
Scene_Enemies        = 5        // Remaining enemies
Scene_TimeLimit      = 180      // Seconds
Scene_CheckpointX    = 0        // Last checkpoint position
Scene_CheckpointY    = 0
Scene_IsComplete     = false
```

### Object Variables (on Player instance)
```
Health               = 5
IsGrounded           = false
IsJumping            = false
CanDoubleJump        = false
IsDashing            = false
AttackCooldown       = 0
Invincible           = false
InvincibleTimer      = 0
```

### JSON Variable for Save Data
```json
{
  "levels": {
    "unlocked": 5,
    "completed": [true, true, true, false, false],
    "coins": [45, 38, 50, 0, 0],
    "bestTime": [120, 95, 180, 0, 0],
    "stars": [3, 2, 3, 0, 0]
  },
  "settings": {
    "musicVolume": 80,
    "sfxVolume": 100,
    "fullscreen": false,
    "language": "en"
  },
  "stats": {
    "totalPlayTime": 3600,
    "totalDeaths": 12,
    "totalEnemiesKilled": 340
  }
}
```

## 2D Platformer Mechanics

### Player Setup
```
Object: Player
Behavior: Platformer character
  - Max speed: 300
  - Acceleration: 800
  - Deceleration: 1000
  - Jump speed: 700
  - Jump sustain time: 0.15s
  - Gravity: 1500
  - Max falling speed: 1200
  - Rotation offset: 0
Animations: idle, run, jump_up, jump_fall, attack, hit, death
```

### Advanced Player Mechanics
**Double Jump:**
```
Event: Player jumps
  Sub-event: Variable Player.IsJumping = true
    Set object variable CanDoubleJump = false
  Sub-event: (if Player.IsJumping AND Player.IsGrounded = false)
    Set object variable CanDoubleJump = true

Event: Player presses Jump key
  Sub-event: (if CanDoubleJump AND Player.IsGrounded = false)
    Simulate Jump key press
    Set object variable CanDoubleJump = false
    Trigger double jump animation/particles
```

**Wall Jump:**
```
Event: Player touches wall (collision with "Wall" group)
  And Player presses Jump
  And Player.IsGrounded = false
    Simulate Jump key press
    Add force opposite to wall direction
```

**Dash:**
```
Event: Player presses Dash key
  And IsDashing = false
    Set IsDashing = true
    Set platformer max speed to 800
    Wait 0.15 seconds
    Set platformer max speed to 300
    Set IsDashing = false
```

### Camera Setup
```
Object: Camera object (invisible)
Behavior: Camera
In events:
  Add Camera X to smooth scrolling:
    Set X = lerp(Camera.X(), Player.X(), 0.05)
    Set Y = lerp(Camera.Y(), Player.Y() - 50, 0.08)
  Camera Bounds:
    Center camera on Camera object
    Set camera bounds to level dimensions
  Parallax:
    Background layer: X = Camera.X() * 0.3
    Midground layer: X = Camera.X() * 0.6
```

### Enemy AI Patterns
**Patrol:**
```
Event: Every frame
  Enemy moves forward (Platformer behavior, direction variable)
  Sub-event: Enemy.X() >= patrolRightLimit
    Change direction to "left"
    Flip sprite horizontally
  Sub-event: Enemy.X() <= patrolLeftLimit
    Change direction to "right"
    Flip sprite horizontally
```

**Chase (Line of Sight):**
```
Event: Distance between Player.X() and Enemy.X() < 300
  And Distance between Player.Y() and Enemy.Y() < 50
    Change direction toward player
    Set platformer max speed to 350
  Otherwise:
    Set platformer max speed to 150 (patrol)
```

**Boss Phases:**
```
Event: At start of boss scene
  Trigger boss intro cutscene
  Boss variable phase = 0

Sub-event: Boss variable Health < 66%
  Set phase = 1
  Add new attack pattern

Sub-event: Boss variable Health < 33%
  Set phase = 2
  Activate rage mode, increase speed
```

### Collectibles System
```
Coin:
  Object variable value = 1
  Animation: spinning coin
  On collision with Player:
    Add Coin.value to Coins (global)
    Play sound "collect.wav"
    Add particles at Coin position
    Delete Coin

Checkpoint (Flag):
  Object variable activated = false
  On collision with Player AND activated = false:
    Set activated = true
    Change animation to "active"
    Set Scene_CheckpointX = Checkpoint.X()
    Set Scene_CheckpointY = Checkpoint.Y()
    Play sound "checkpoint.wav"

Respawn:
Event: Player.Lives > 0 AND Player animation death finished
  Subtract 1 from Player.Lives
  Change Player X/Y to (Scene_CheckpointX, Scene_CheckpointY)
  Set Player.Health = Player.MaxHealth
  Reset all enemies in scene
Event: Player.Lives = 0
  Change scene to EndScene
```

## 3D First-Person Mechanics

### 3D Scene Setup
```
Add 3D environment (Cube Map)
Add Directional Light (angle: 45°, intensity: 0.8, shadow: on)
Add Ambient Light (intensity: 0.3, color: slight blue tint)
Set Camera to First Person mode

3D Camera Settings:
  Field of View: 70°
  Near clip: 0.1
  Far clip: 1000
  Mouse sensitivity: 0.3
```

### 3D Player Controls
```
Event: Mouse movement (cursor locked)
  Rotate camera Y = MouseDX * sensitivity
  Rotate camera X = MouseDY * sensitivity * -1
  Clamp camera.X rotation between -89° and 89°

Event: WASD movement
  Forward (W): Move camera forward at speed 5 * DeltaTime
  Backward (S): Move camera backward at speed 5 * DeltaTime
  Strafe Left (A): Move camera left at speed 5 * DeltaTime
  Strafe Right (D): Move camera right at speed 5 * DeltaTime
  Apply gravity (constant Y -9.8 * DeltaTime)
  Ground check: raycast downward, length 2.0
```

### 3D Raycasting for Interaction
```
Event: Player presses Left Click
  Cast ray from camera center, max distance 200
  If ray hits object with tag "Interactable":
    Send message to hit object: "OnInteract"
  If ray hits object with tag "Enemy":
    Send message to hit object: "OnDamage"

Event: Crosshair HUD
  If ray hits "Interactable" object:
    Show "Press E to interact" text
    Change crosshair color to green
  Otherwise:
    Hide interaction text
    Crosshair color = white
```

## Menus and UI

### Main Menu Implementation
```
Scene: MenuScene
Background: Animated parallax or video
Logo: Animated sprite (scale up, fade in, floating)
Buttons (Sprite objects with mouse events):
  - Play: Change scene to level select or first GameScene
  - Continue: Load save data (if exists, else hidden)
  - Options: Change scene to OptionsScene
  - Credits: Show credits panel (external layout)
  - Quit: Exit game (web: close tab, desktop: close window)

Events:
  On Play hover: Scale button to 1.1, play hover SFX
  On Play click: Fade transition → Change to GameScene
  
Logo Animation:
  At scene start:
    Set logo opacity to 0, scale to 0.5
    Tween opacity to 255, scale to 1.0 (duration: 1.5s, ease: outBack)
```

### In-Game HUD (External Layout)
```
Layer: "HUD" (top-most, always visible)

Top-left:
  Health bar (Tiled Sprite or Progress Bar object)
  Lives display (text: "Lives: X" with heart sprite)

Top-center:
  Score (text: "Score: 000000")

Top-right:
  Coin counter (coin sprite + text)
  Timer (text: "Time: 00:00")

Events linked to HUD:
  Update health bar width = (Player.Health / Player.MaxHealth) * 200
  Update score text = "Score: " + ToString(Score)
  If health < 30%:
    Health bar tint = red
    Play low health pulse animation
```

### Pause Menu (Overlay Scene or External Layout)
```
Trigger: Esc key or P key or Pause button on screen

Actions on pause:
  Freeze all objects (Time scale = 0)
  Show pause panel (dark semi-transparent overlay)
  Show buttons:
    - Resume (unpause, hide panel)
    - Restart (reset scene variables, change scene to current)
    - Options
    - Main Menu (change scene to MenuScene)

Use "Pause and start a new scene" to prevent input passthrough
```

### End Screen
```
Scene: EndScene
Background: Dark gradient with particle effects
  
Events:
  At scene start:
    If Result = "win":
      Show "LEVEL COMPLETE!" text (large, animated, gold color)
      Show stars earned (1-3 based on score/coins/time)
      Display: Coins collected, Time taken, Score
      Check if new high score → Save to Storage
      Buttons: Next Level, Replay, Main Menu
    If Result = "lose":
      Show "GAME OVER" text (red, dramatic entrance)
      Show death count, progress percentage
      Buttons: Retry, Main Menu

Star Rating Calculation:
  Coins: > 80% = 1 star, > 90% = 2 stars, 100% = 3 stars
  Time: < target time = bonus star
  Final = min(coins stars + time bonus, 3)
```

### Options Menu
```
Scene: OptionsScene

Controls configuration:
  Use key press detection events to rebind keys
  Store key bindings in Global Variables or JSON
  Default keys: Arrow keys + Space for platformer

Volume sliders:
  Use Tiled Sprite or custom slider object
  Music Volume (0-100) → GlobalVariable(MusicVolume)
  SFX Volume (0-100) → GlobalVariable(SFXVolume)
  Apply to all audio via events

Display:
  Fullscreen toggle
  Resolution dropdown (if multiple export targets)
  V-Sync toggle

Language:
  Dropdown or flag buttons
  Store selection in JSON variable
  Use text formulas: choose by language index
```

## Event System Best Practices

### Event Organization
```
Root events → Groups → Sub-events → Actions/Conditions

Groups (collapsible):
  ☐ Player Controls
  ☐ Enemy AI
  ☐ Collectibles
  ☐ UI Updates
  ☐ Audio
  ☐ Camera
  ☐ Level Logic
  ☐ Save/Load

Within each group:
  Use comments to separate: Init, Update, Cleanup
  Use "Trigger Once" for initialization
  Use "Every frame" for continuous logic
```

### Event Optimization Patterns
```
AVOID (expensive):
  "Every frame" + "For each object" on the same event
  100+ conditions on a single event
  No collision masks on physics objects

PREFER:
  "Object near" for distance checks (more efficient than distance formula)
  Timer-based events instead of every-frame for non-critical updates
  Trigger Once when initializing objects
  Use object variables instead of scene variables for instance-specific data
  Object Groups for batch operations on similar objects

TRIGGER VS CONDITION:
  Trigger (top of event): Runs check every frame
  Condition (sub-event): Only runs when parent is true → cheaper
```

### Functions for Reusable Logic
```
Function Definition:
  Name: SpawnEnemy
  Parameters: enemyType (string), x (number), y (number)
  Actions:
    Create object "Enemy_" + enemyType at (x, y)
    Set enemy object variables based on type
    Add enemy to "Enemies" group

Function Definition:
  Name: DealDamage
  Parameters: target (object), damage (number)
  Actions:
    Subtract damage from target Health
    Play hit animation for target
    If target Health <= 0:
      Call function KillTarget(target)
```

## Creative Level & Phase Design

### Level Design Principles
- **Tutorial Level**: Introduce mechanics one at a time in safe environments
- **Rising Action**: Increase enemy count and complexity gradually
- **Peak Challenge**: Boss fights after skill mastery sections
- **Palate Cleanser**: Relaxed sections between intense moments
- **Fake Difficulty**: Use environmental storytelling, not unfair traps

### Unique Mechanics per Level (Examples)
**Gravity Flip Zone:**
  - Player enters trigger → gravity direction changes (up/down/left/right)
  - Visual indicator: screen edge tint or particles
  - Duration: Room/zone-based or timer

**Time Manipulation:**
  - Slow-mo zones using Time Scale variable
  - Player ability: Freeze time for 3 seconds on button press
  - Puzzle elements: Moving platforms that sync with time phase

**Morph/Transform:**
  - Player becomes different creature with unique abilities
  - Liquid form: Pass through grates, slow movement
  - Heavy form: Break walls, cannot jump

**Portal Mechanics:**
  - Shoot portals (like Portal game concept)
  - Enter one portal → exit the other
  - Visual: Warp effect, teleport particles

### Procedural Elements
```
Endless Runner Mode:
  Continuously spawn platform segments from a pool
  Use random number to select segment type
  Delete segments behind the player
  Gradually increase speed and difficulty

Wave-Based Spawning:
  Define wave patterns in JSON:
  [
    {"wave": 1, "enemies": ["slime", "slime", "bat"], "delay": 2},
    {"wave": 2, "enemies": ["slime", "bat", "bat", "slime"], "delay": 1.5},
    {"wave": 3, "enemies": ["boss_mini"], "delay": 5}
  ]
  Spawn enemies from array with delays between waves
```

## Saving and Loading

### SaveGame Function
```
Save (using Storage action):
  Create JSON structure with all persistent data
  Write to storage key "save_slot_1"
  
Example save JSON:
{
  "level": GlobalVariable(CurrentLevel),
  "coins": GlobalVariable(Coins),
  "score": GlobalVariable(Score),
  "lives": GlobalVariable(PlayerLives),
  "health": GlobalVariable(PlayerHealth),
  "completed": GlobalVariableString(LevelsCompleted),
  "setting_music": GlobalVariable(MusicVolume),
  "setting_sfx": GlobalVariable(SFXVolume),
  "timestamp": GlobalVariable(TotalTime)
}
```

### LoadGame Function
```
Load:
  Read JSON from storage key "save_slot_1"
  If exists:
    Set GlobalVariable(CurrentLevel) = JSON level value
    Set GlobalVariable(Coins) = JSON coins value
    ... (restore all values)
  Else:
    Initialize defaults (new game)
```

### High Score Persistence
```
Event: Level completed AND Score > HighScore
  Write Score to Storage key "highscore_level_" + ToString(CurrentLevel)
  Show "NEW HIGH SCORE!" text with celebration effect
```

## Audio Management

### Audio Channel Setup
```
Channel 0: Music (looping, controlled by MusicVolume)
Channel 1: SFX Primary (jump, collect, UI clicks)
Channel 2: SFX Secondary (enemy sounds, ambient)
Channel 3: Voice/Dialogue (if applicable)

Volume Control:
  Set channel 0 volume = GlobalVariable(MusicVolume)
  Set channels 1-3 volume = GlobalVariable(SFXVolume)
```

### Spatial Audio (3D)
```
For 3D games:
  Use 3D Sound objects
  Set position, attenuation, and max distance
  Sound volume scales with camera distance
```

### Audio Event Pattern
```
Group: Audio
  Sub-event: Jump SFX
    If player state changes to jumping:
      Play sound "jump.wav" on channel 1, volume 0.7, pitch random(0.95, 1.05)
  
  Sub-event: Music Transition
    If scene starts:
      Stop music channel 0
      Play music "level_" + ToString(CurrentLevel) + ".ogg" on channel 0
      
  Sub-event: Low Health Alert
    If Player.Health < 30% AND heartbeat timer > 1 sec:
      Play sound "heartbeat.wav" on channel 2
      Reset heartbeat timer
```

## Effects and Polish

### Particles
```
Particle Emitter Configs:
  Coin Collect: Gold sparks, burst 8-12 particles, gravity, fade out 0.5s
  Jump Dust: Brown/white dust, small burst, ground level
  Explosion: Orange fire, large burst 20-30, rotate, fade 1s
  Trail: Custom emitter on player while dashing
  Environment: Floating dust in air, leaves falling, rain
```

### Screen Effects
```
Layer: "Effects" (above game, below HUD)

Transition Effects:
  Fade to black: Tiled sprite (black) opacity tween 0 → 255 (0.5s)
  Wipe: Tiled sprite with custom mask/scaling animation
  Camera shake: On damage/explosion:
    Tween Camera X/Y offset rapidly, decay over 0.3s

Visual Feedback:
  Damage vignette: Red border overlay, flash 0.2s
  Speed lines: On dash, show motion blur particles
  Screen flash: White flash 0.1s on power-up pickup
```

### Shaders (GDevelop Effects)
```
Available effects to apply to layers/objects:
  Outline: Highlight interactable objects
  Glow: Power-ups, checkpoints
  CRT: Retro game aesthetic on menus
  Sepia/Desaturation: Flashback scenes, pause screen
  Bloom: On-layer for overall glow effect
```

## Performance Optimization

### Layer Management
```
Layer Ordering (back to front):
  1. Background (parallax layers, sky)
  2. Far Environment (distant platforms, decorations)
  3. Near Environment (main platforms, tiles)
  4. Interactive Objects (enemies, collectibles, items)
  5. Player
  6. Foreground (overlapping environment pieces)
  7. Particles
  8. UI / HUD
  9. Effects (transitions, overlays)

Disable layers not visible to camera:
  Check if layer objects are within camera bounds
  Hide/show layers accordingly
```

### Object Pooling (for frequently spawned objects)
```
Pool Setup:
  Create 20 Bullet objects at scene start, invisible, outside bounds
  Object variable "inUse" = false

Spawn from pool:
  Find Bullet with inUse = false
  Move to spawn position, set inUse = true, show

Despawn to pool:
  When Bullet leaves screen bounds:
    Set inUse = false, hide, move to offscreen (-1000, -1000)
```

### Performance Checklist
- Reuse objects instead of create/delete in rapid succession
- Limit "For each object" usage to necessary cases
- Use collision masks to reduce physics checks
- Static objects with "Platform" behavior are cheap
- Tilemap collisions are more efficient than individual platform objects
- Disable unused behaviors at runtime
- Keep particle count reasonable (< 200 simultaneous)
- Compress audio to OGG for music, short WAV for SFX
- Texture atlas: Combine small sprites into a single image

## Scene Transitions and Flow

### Transition Manager (External Events)
```
Function: TransitionToScene
  Parameters: sceneName (string), transitionType (string), duration (number)

  If transitionType = "fade":
    Create black overlay, tween opacity 0 → 255 over (duration/2)
    Wait (duration/2)
    Change scene to sceneName
    At new scene start: black overlay tween opacity 255 → 0 over (duration/2)

  If transitionType = "slide":
    Similar pattern with X/Y movement instead of opacity
  
  If transitionType = "instant":
    Change scene to sceneName immediately

Pass data between scenes via Global Variables
```

### Scene Data Passing Pattern
```
Before leaving GameScene:
  Set GlobalVariable(LastScore) = GlobalVariable(Score)
  Set GlobalVariable(LastTime) = GlobalVariable(TotalTime)
  Change scene to EndScene

In EndScene start:
  Read GlobalVariable(LastScore)
  Read GlobalVariable(LastTime)
  Display results using these values
```

## Export and Production

### Platform-Specific Export Settings
```
Web (HTML5):
  Compression: Maximum
  Include GDevelop watermark: No (with subscription)
  Embed resources: Bundle
  Resolution: Responsive (adapt to browser window)
  
Desktop (Windows/macOS/Linux):
  Via Electron export
  Window settings: 1920x1080, resizable, fullscreen option
  Icon: Custom .ico/.icns file
  
Mobile (Android):
  APK/AAB export options
  Virtual controls overlay for touch
  Adjust UI scaling for different screen sizes
  Battery optimization: Limit particle effects, reduce update frequency
```

### Pre-Export Checklist
1. All scenes have proper starting conditions
2. Save/Load functions tested across all scenarios
3. No debug objects or test logic remaining
4. All animations have correct frames and speeds
5. Collision masks properly defined
6. Audio balanced (music vs SFX levels)
7. Text fits within screen bounds at all resolutions
8. Touch/click targets are large enough (minimum 44x44px for mobile)
9. Game works from start to end without external resources
10. Performance target: 60 FPS on target platform

## Best Practices Reference

### Naming Conventions
```
Objects: PascalCase (Player, Enemy_Slime, Item_Coin)
Scenes: PascalCase with suffix (MenuScene, GameScene_Level01)
Variables: CamelCase (playerHealth, currentLevel)
Groups: PascalCase space-delimited (Enemy AI, Player Controls)
Functions: PascalCase verb-first (SpawnEnemy, DealDamage)
Animations: snake_case (idle_anim, run_anim, jump_up)
Resources: snake_case (player_idle_01.png, coin_collect.wav)
```

### Do's and Don'ts

✅ DO:
- Use External Events for reusable logic across scenes
- Group related events with collapsible groups
- Prefix object variables with object name for clarity in logs
- Use "Trigger once" for scene initialization
- Set up collision masks BEFORE adding many objects
- Use TimeDelta for smooth movement independent of framerate
- Test regularly on all target platforms
- Keep global variables under 100 for performance
- Use JSON for complex data structures

❌ DON'T:
- Don't use "Every frame" + "Create object" (creates infinite objects)
- Don't nest more than 5 levels of sub-events
- Don't ignore the return value of "Pick nearest object"
- Don't use "Always" as a condition (use "Every frame" with frequency)
- Don't mix physics behaviors (Platformer + Physics on same object)
- Don't store large strings in global variables (use JSON or storage)
- Don't create/destroy objects every frame (use object pooling)

### Common Issues & Solutions
| Issue | Solution |
|-------|----------|
| Objects fall through platforms | Increase "max falling speed" in platformer behavior |
| Animation glitches | Check animation speed and ensure stop/edit loop settings |
| Collision not detected | Verify collision masks and layer visibility |
| Can't click buttons in game | Ensure UI layer is above game layer |
| Jump feels floaty | Reduce "jump sustain time" and increase gravity |
| Camera stuttering | Use lerp with small factor, run camera events last |
| Audio distortion | Compress to OGG, keep WAV under 2 seconds |
| Game runs slow on mobile | Reduce active objects, disable effects, use Tilemap |

## GDevelop Reference

## Advanced Technical Reference

### Physics 2 Engine Configuration
```
Object: Physics2 behavior attached
Type: Static (immovable), Dynamic (full physics), Kinematic (forces only)
Shape: Box, Circle, Edge, Polygon

Properties:
  - Density: Weight according to size (default: 123)
  - Friction: Energy lost when objects slide (default: 0.3)
  - Restitution: Bounciness/energy conserved after collision (default: 0.1)
  - Linear Damping: Movement speed lost over time (default: 0.1)
  - Angular Damping: Rotation speed lost over time (default: 0.1)
  - Fixed Rotation: Prevents rotation (useful for characters)
  - Considered as Bullet: Accurate collision for fast objects
  - Can Sleep: Engine stops computing when not touched

Combined Friction = sqrt(bodyA.friction * bodyB.friction)
Combined Restitution = max(bodyA.restitution, bodyB.restitution)
```

### Pathfinding Behavior
```
Grid Configuration:
  - Cell Width/Height: Virtual grid resolution (smaller = more precise, slower)
  - Extra Border: Margin around obstacles
  - Grid Offset X/Y: Shift the grid

Obstacle Types:
  - Impassable: Objects must navigate around (cost = infinity)
  - Cost-based: Higher cost = objects prefer to avoid

Movement:
  - Acceleration: How quickly object speeds up on path
  - Max Speed: Maximum movement speed
  - Angular Max Speed: Rotation speed limit

Waypoint Access:
  Object.Pathfinding::NodeCount() → Total waypoints
  Object.Pathfinding::NextNodeX/Y() → Current target
  Object.Pathfinding::GetNodeX(index) → Any waypoint by index
```

### Tween Easing Functions
```
Linear: linear
Quadratic: easeInQuad, easeOutQuad, easeInOutQuad
Cubic: easeInCubic, easeOutCubic, easeInOutCubic
Quart: easeInQuart, easeOutQuart, easeInOutQuart
Quint: easeInQuint, easeOutQuint, easeInOutQuint
Sine: easeInSine, easeOutSine, easeInOutSine
Expo: easeInExpo, easeOutExpo, easeInOutExpo
Circ: easeInCirc, easeOutCirc, easeInOutCirc
Bounce: easeOutBounce, bounce, bouncePast
Back: easeInBack, easeOutBack, easeInOutBack
Elastic: elastic, swingFromTo, swingFrom, swingTo
Special: easeFromTo, easeFrom, easeTo

Usage: Tween position, opacity, scale, angle, color, or variables
DestroyOnFinish: Auto-remove object when tween completes
```

### Platformer Jump Physics
```
Jump Height Calculation:
  Height = (JumpSpeed²) / (2 × Gravity)
  
  Example: JumpSpeed=700, Gravity=1500
  Height = (700²) / (2 × 1500) = 163.3 pixels

Jump Sustain Time:
  - Time while holding jump that maintains initial velocity
  - Longer = higher jumps with held button
  - Default: 0.15s

Advanced Platformer Extension Properties:
  - JumpTimeFrame: Jump detection window (default: 0.125s)
  - SideSpeedSustainTime: Acceleration sustain (default: 0.2s)
  - SideAcceleration: Horizontal acceleration (default: 1500)
  - MinimalFallingSpeed: Minimum fall speed (default: 50)
  - ImpactSpeedAbsorption: Landing impact reduction (default: 350)
```

### Top-Down Movement Behavior
```
Movement Directions: 4 (cardinal) or 8 (cardinal + diagonal)
Acceleration/Deceleration: Smooth start/stop
Rotate Object: Face movement direction
Directions:
  - 4 directions: Up, Right, Down, Left
  - 8 directions: Adds Up-Right, Down-Right, Down-Left, Up-Left

Grid-based Movement:
  - Move on grid cells
  - Cell width/height configurable
```

### Custom Behaviors (Events-Based)
```
Create reusable logic attached to objects:
  - Define conditions and actions as behavior
  - Attach to any object type
  - Behavior can access object properties
  - Supports parameters for flexibility

Use cases:
  - Reusable enemy AI patterns
  - Shared player mechanics
  - Common interaction systems
```

### Linked Objects (Parent-Child)
```
Link Objects: Create persistent parent-child relationship
Unlink Objects: Remove relationship
Benefits:
  - Child follows parent position/rotation
  - Group operations on linked objects
  - Object hierarchies (player + weapons, characters + accessories)
```

### Spatial Sound (3D Audio)
```
Sound Position: X, Y, Z coordinates
Attenuation: Volume decrease over distance
Max Distance: Volume becomes zero beyond this
Reference Distance: Where volume starts decreasing

For 3D games:
  - Set sound position relative to player/camera
  - Sound volume scales with camera distance
  - Create immersive audio environments
```

### Input System
```
Keyboard:
  - Key pressed/released: One-frame detection
  - Key down: Continuous while held
  - Populate "Last Key Pressed" for input buffering

Mouse/Touch:
  - Button pressed/released: One-frame detection
  - Cursor/touch on object: Hover/click detection
  - Cursor position: X, Y coordinates
  - Mouse wheel: Scroll detection

Gamepad:
  - Button pressed/released
  - Axis values: Analog stick positions
  - Trigger values: L2/R2 pressure

Device Sensors (Mobile):
  - Accelerometer: Device tilt
  - Gyroscope: Device rotation
  - Magnetometer: Compass heading
```

### Object Types Deep Dive
```
Sprite: Image with animations, collision mask
Tiled Sprite: Repeating background texture
Panel Sprite (9-patch): Scalable UI backgrounds
Tilemap: Grid-based level from tileset
Text/Bitmap Text: Text display
BBText: Rich text with colors/styles
Button: Clickable UI element
Slider: Value selection UI
Toggle Switch: On/off UI element
Particle Emitter: Particle effects system
Shape Painter: Procedural 2D shapes
Video: Video playback
Spine: Skeletal animation (RPG Maker style)
Light: 2D lighting effects
3D Box/Model/Light: 3D scene elements
```

### Advanced Conditions
```
Trigger Once: Execute event only once per frame
For Each Object: Iterate all instances
Object is in collision with: Overlap detection
Object near: Optimized distance check (faster than Distance formula)
Timer: Time-based triggers
Value of object variable: Instance-specific state
Scene is loaded: Initialization hook
At the beginning/end of scene: Lifecycle events
```

### Core Features Reference

**Inventory System:**
```
Built-in inventory with items, quantities, equipment slots
Operations: Add/remove items, check quantity, equip/unequip
```

**Dialogue Tree:**
```
Visual conversation system for NPCs
Branching paths, conditions, text display
```

**Save State:**
```
Auto-save/load game state
Includes scene, objects, variables
```

**Firebase Integration:**
```
Authentication: Email/password, social login
Cloud Firestore: Database
Realtime Database: Real-time sync
Storage: File storage
Cloud Functions: Server-side logic
Analytics: Usage tracking
Remote Config: Dynamic settings
```

**Multiplayer/P2P:**
```
P2P networking for multiplayer games
Custom lobbies, peer connections
WebSocket client for server communication
Advanced HTTP for REST APIs
```

### Event System Reference

**Control Flow:**
```
Group: Organize related events
Else: Run when main condition is false
Repeat: Loop N times
While: Loop while condition true
For Each Object: Iterate instances
For Each Child Variable: Iterate structure/array
```

**Custom Functions:**
```
Parameters: Pass data to function
Return value: Get data back
Async functions: await operations (Storage, HTTP)
Extract Events: Convert to reusable function
```

**Advanced:**
```
JavaScript Code: Custom logic via JS
Async Events: Parallel execution
Callback Variables: Event communication
```

### Extensions for Advanced Gameplay
```
Fire Bullet: Projectile spawning with patterns
Advanced Projectile: Homing, bouncing, piercing
Homing Projectile: Track target
Boomerang: Return to sender
Boids Movement: Flocking/swarm behavior
Curved Movement: Bezier path movement
Ellipse Movement: Orbital paths
Orbiting Objects: Circular motion around center
Physics Car: Top-down vehicle with drift
Physics Character 3D Animator: 3D character locomotion
Platformer Character Animator: Animation state machine
Top-Down Movement Animator: 8-direction animation states
Bounce: Force-based bouncing
Explosion Force: Radial impulse
Face Forward: Rotate toward movement
Stick Objects: Attach objects together
Travel to Random Positions: Wander AI
Turret 2D: Auto-targeting weapon
```

### Movement Extensions Reference
```
Advanced Jump: Extended jump parameters (JumpTimeFrame, SideSpeedSustainTime, MinimalFallingSpeed)
Advanced Projectile: Homing, bouncing, piercing, guided missiles
Animated Back and Forth: Patrol with animation states
Boids Movement: Flocking AI (separation, alignment, cohesion)
Boomerang: Fire and return
Bounce: Force-based bouncing with decay
Curved Movement: Bezier curves, arcs, waves
Ellipse Movement: Elliptical orbits
Explosion Force: Radial impulse from point
Face Forward: Rotate to face movement direction
Homing Projectile: Target tracking with turn rate
Linear Movement: Constant velocity in direction
Orbiting Objects: Circular motion around center point
Physics Car: Top-down vehicle with acceleration, braking, drift
Platformer Trajectory: Predict landing position for aiming
Rectangular Movement: Square/rectangular patrol paths
Screen Wrap: Wrap around screen edges
Speed Restrictions: Min/max speed limits
Stay On Screen: Constrain to viewport
Stick Objects: Attach/detach objects with constraint
Timed Back and Forth: Auto-reverse after time
Top-Down Movement Animator: 8-direction sprite facing
Turret 2D: Auto-aim at target with fire rate
Travel to Random Positions: Wander AI
```

### Procedural Level Generation
```
Noise Generator Extension:
  - Perlin, Simplex noise for terrain generation
  - Use for: Terrain height, enemy spawns, item placement

Rectangular Flood Fill:
  - Cave generation, room detection
  - Connect spaces with corridors

Hexagonal Grid:
  - Strategy game tile movement
  - Axial coordinate conversions
```

### State Machine Pattern
```
Use object variables for FSM states:
  Player.State = "idle" | "running" | "jumping" | "attacking" | "hurt" | "dead"

Event-driven state transitions:
  State = "idle"
    Condition: Player is grounded → State = "running"
    Condition: Player jump key → State = "jumping"
  
  State = "jumping"
    Condition: Player on ground → State = "idle"
    Condition: Attack key → State = "attacking"

Animation tied to state:
  Change animation to Player.State when state changes
```

### External Layouts & Events
```
External Layouts:
  - Reusable scene fragments (UI panels, level pieces)
  - Instance multiple times with different positions
  - Good for: HUDs, enemy spawners, platform templates

External Events:
  - Reusable event logic
  - Include in any scene
  - Good for: Player controls, enemy AI, scoring
```

### Storage & Filesystem
```
Storage Actions:
  - Write/Read JSON to named keys
  - Check if key exists
  - Clear storage

Filesystem (when exported):
  - Read/write text files
  - Access app documents folder
  - Useful for: Custom save formats, level editors
```

### Performance Patterns
```
Object Pooling: Pre-create objects, reuse instead of create/delete
Collision Masks: Enable only on objects needing collision
Static Objects: Mark unmoving objects as static
Sleep Mode: Allow physics objects to sleep when idle
Layer Culling: Hide off-camera layers
Particle Limits: Cap simultaneous particles
Tilemap Collision: Use grid-based instead of object-based
```

---

## Key Behaviors
- **Platformer character**: Ground movement with gravity
- **Platform (simple)**: Static collider optimized for platformers
- **Physics Engine 2.0**: Full rigid body simulation (shapes, density, friction, restitution, damping, bullet collision)
- **Top-down movement**: 4/8-directional grid-based or free movement
- **Pathfinding**: A* navigation with obstacle costs, waypoint access
- **Tween**: Animate position, scale, opacity, angle, color, variables with 30+ easing functions
- **Tiled Sprite**: Repeating textures for backgrounds
- **Particle Emitter**: Burst and continuous particle effects
- **Text**: Display and format text
- **Tilemap**: Efficient tile-based level building with collision grid
- **Camera**: Follow object, apply bounds, smoothing, shake, zoom
- **Drag and drop**: Touch/mouse click movement
- **Anchor**: Pin objects to screen edges
- **Fade in/out**: Tween opacity transitions
- **Light (3D)**: Point, directional, spot lights for 3D scenes
- **3D Box**: Basic 3D collision box
- **3D Model**: Import external 3D models
- **3D Sound**: Spatial audio in 3D space
- **Custom behaviors**: Events-based reusable logic attached to objects
- **Linked objects**: Parent-child hierarchies

### Key Conditions
- **Mouse button pressed / released**: One-frame click detection
- **Cursor/touch on object**: Hover/click detection with drag support
- **Key pressed / released**: One-frame key detection
- **Key down**: Continuous input while held
- **Object is in collision with**: Physics overlap detection (rectangle, circle, points)
- **Distance between objects**: Proximity check (optimized vs manual calculation)
- **Object near**: More efficient than Distance() for collision checks
- **Variable value comparison**: Logic branching with operators
- **Timer**: Time-based triggers with pause/resume
- **Scene is loaded**: Initialization hook
- **At the beginning / end of the scene**: Lifecycle events
- **Trigger once**: One-time execution per frame
- **For each object**: Instance iteration (use sparingly)
- **Value of object variable**: Instance-specific state
- **Physics: Raycast hit**: Cast rays for shooting/visibility checks
- **Input: Gamepad button/axis**: Controller support

### Key Actions
- **Change the scene**: Scene transition with optional fade
- **Create / Delete object**: Lifecycle management
- **Change object variable**: State modification
- **Add / Subtract from variable**: Numeric operations
- **Play sound on channel**: Audio playback with volume/pitch/loop
- **Pause and start a new scene**: Modal overlay (blocks input)
- **Simulate key press**: Programmatic input for AI/demo
- **Tween**: Smooth interpolation (position, scale, opacity, angle, color, variables)
- **Flash**: Temporary visual effect (color + duration)
- **Link / Unlink objects**: Parent-child relationships
- **Change animation**: Animation state switching
- **Apply force**: Physics impulse (X, Y, torque)
- **Change layer**: Layer visibility and ordering
- **Read / Write Storage**: Persistent JSON data
- **Cast a ray**: 3D raycasting for shooting/visibility
- **Execute JavaScript**: Custom code (advanced)
- **Change time scale**: Slow-mo / pause effects (0.0 - 2.0)
- **Set physics properties**: Modify velocity, damping, gravity at runtime
