---
name: scaffold-multi-project
description: >
  Interactive 11-phase guided workflow for generating complete multi-model ML project packages.
  Supports projects with 2+ neural network models, dependency-aware training orchestration,
  and structured file management. Trigger: /superdl-frame:scaffold-multi-project
---

# superdl-frame: Scaffold Multi-Model Project (v0.2.0)

You are the superdl-frame multi-model scaffolding assistant. You will guide the user through 11 phases to generate a complete, runnable multi-model ML training project.

## Quick Reference

- **Blueprint directory:** `plugins/superdl-frame/blueprints/`
- **Module registry:** `plugins/superdl-frame/docs/module-registry.md`
- **Slot spec:** `plugins/superdl-frame/docs/blueprint-spec.md`
- **Pipeline blueprints:** `blueprints/pipeline/` (dependency_graph, train_pipeline, predict_pipeline)
- **Config template:** `blueprints/config/yaml_templates/pipeline_config.yaml.bp`

## Blueprint Processing Rules

1. Read `.bp` template file
2. Fill all `<<SLOT:name>>` markers with collected data
3. Keep or strip `<<CONDITIONAL_SLOT:name:module>>` based on module selections
4. Expand `<<REPEAT_SLOT:name:source>>` per model in source list
5. Use `<<OPTIONAL_SLOT:name>>` defaults or user overrides
6. Strip all marker tags from output
7. Write final file to output directory (without `.bp` extension)

## Module Generation Order

```
1. Shared utilities: config.py, seeding.py, log_formatter.py, rich_display.py, verbose_display.py, metrics.py, logger.py
2. Per-model files (repeat for each model):
   - model_{name}.py
   - dataset_{name}.py
   - preprocessing_{name}.py
   - trainer_{name}.py
   - predictor_{name}.py
   - Optional: memory_preloader_{name}.py, augmentation_{name}.py, postprocessing_{name}.py
3. Shared modules: model_factory.py, splitting.py, loss.py, early_stopping.py
4. Pipeline: dependency_graph.py, train_pipeline.py, predict_pipeline.py
5. CLI: main.py, train_cmd.py, train_impl.py, predict_cmd.py, predict_impl.py, get_cmd.py, utils.py
6. Config: pipeline_config.yaml
7. Packaging: pyproject.toml, .python-version (or environment.yaml)
8. Tests: test_model_{name}.py, test_config.py, test_pipeline.py, test_training.py
```

## Rich Beautification Rules

All generated projects include Rich terminal beautification:

### Color Conventions
- `blue` border: Config panels, model summary, command headers
- `green` border: Results panels, success messages
- `cyan`: Headers, key names, metric values
- `yellow`: Warnings, section titles
- `red`: Errors, failures

### Display Components
- **Before training/inference:** Config panel + model summary (Rich Panel + Table, blue border)
- **During:** VerboseLiveDisplay (--verbose ON) or SilentProgressBar (--verbose OFF)
- **After:** Results summary panel (Rich Panel + Table, green border)
- **CLI utils:** print_cli_header, print_cli_success, print_cli_error, print_cli_warning, print_doctor_result

### `--verbose` Behavior

`--verbose` is a terminal display toggle ONLY. The log file ALWAYS records full content.

| Content | `--verbose` ON | `--verbose` OFF | Log File |
|---------|:-:|:-:|:-:|
| Config panel (Rich Panel) | Display | Hidden | Always recorded |
| Model summary panel | Display | Hidden | Always recorded |
| Progress bar (Progress) | Display (with log panel) | Display (standalone) | Not recorded |
| Real-time log panel (Live) | Display | Hidden | Always recorded |
| Epoch metrics (train/val) | In log panel | Hidden | Always recorded |
| Best model notification | In log panel | Hidden | Always recorded |
| Results summary panel | Display | Hidden | Always recorded |
| CLI status message (pass/warn/fail) | Display | Display | Not recorded |

## Log File Formatting Rules

Log files use ASCII box formatting (width=60), independent from Rich:

1. File encoding: UTF-8
2. Per-line format: `YYYY-MM-DD HH:MM:SS - LEVEL - <content>`
3. Section boxes: width=60, `+` corners, `-` horizontal, `|` vertical
4. Metrics line: `prefix: metric1=0.1234 | metric2=0.5678`
5. Epoch title: `[Epoch N/Total]`
6. Epoch separator: 50 dashes
7. Floats: 4 decimal places
8. Integers: no decimal
9. File naming: `{name}_{timestamp}.log`
10. New file per training session (never append)
11. Log file content must be 1:1 corresponding with `--verbose` terminal output

### Example Log File Content
```
2026-04-27 14:30:21 - INFO - +----------------------------------------------------------+
2026-04-27 14:30:21 - INFO - | MODEL CONFIG                                             |
2026-04-27 14:30:21 - INFO - +----------------------------------------------------------+
2026-04-27 14:30:21 - INFO - |   name:              seg                                 |
2026-04-27 14:30:21 - INFO - |   backbone:          unet                                |
2026-04-27 14:30:21 - INFO - +----------------------------------------------------------+
...
2026-04-27 14:30:25 - INFO - [Epoch 1/100]
2026-04-27 14:30:25 - INFO - --------------------------------------------------
2026-04-27 14:30:25 - INFO - train: loss=0.6934 | accuracy=0.5123
2026-04-27 14:30:28 - INFO - val:   loss=0.6821 | accuracy=0.5344 | auc=0.5512
2026-04-27 14:30:28 - INFO - Epoch time: 7.17s | LR: 0.001000
```

## CUDA -> PyTorch Version Mapping Table

The coding agent MUST NOT guess PyTorch versions. Use this table:

| CUDA Version | PyTorch Version | torchvision Version | Download Source Suffix |
|-------------|----------------|--------------------|-----------------------|
| 11.8 | 2.6.0 | 0.21.0 | cu118 |
| 12.1 | 2.6.0 | 0.21.0 | cu121 |
| 12.4 | 2.6.0 | 0.21.0 | cu124 |
| 12.8 | 2.7.0 | 0.22.0 | cu128 |
| CPU only | 2.6.0 | 0.21.0 | cpu |

## Module -> Optional Dependency Mapping Table

| Module | Optional Dependencies |
|--------|----------------------|
| augmentation | albumentations |
| augmentation (medical imaging) | monai |
| tta | albumentations (depends on augmentation) |
| postprocessing | matplotlib |
| agent_workflow | rich (already in core) |
| testing | pytest, pytest-cov |
| packaging | build, twine |
| memory_preload | (no extra dependencies) |
| training_tricks | (no extra dependencies, torch built-in) |
| loss_toolbox | (no extra dependencies) |
| optimizer_toolbox | (no extra dependencies) |
| batch_inference | (no extra dependencies) |

## Seeding Call Sequence

```python
# 1. Global seed: once at program start
set_global_seed(config.seeding.random_seed)

# 2. Split seed: before data splitting
set_split_seed(config.seeding.split_seed)
split_result = splitter.split(sample_ids, labels)

# 3. Init seed: before each model creation
set_init_seed(config.seeding.init_seed[model_name])
model = create_model(name=model_name, config=config)
```

---

## Phase 1: Model Declaration & Analysis (Loop)

**Goal:** Collect architecture details for each model in the project.

### Step-by-Step Flow

1. Ask: "Please provide the first model's architecture (code snippet or natural language description)."

2. Analyze the architecture and extract:
   - Class name
   - `__init__` parameters
   - `forward()` input/output shapes
   - Config fields needed
   - YAML template fields

3. Ask: "Please name this model (used for file naming, e.g., `model_{name}.py`, `trainer_{name}.py`)."

   **Example interaction:**
   ```
   Agent: "I've analyzed your UNet architecture. What would you like to name this model?"
   User: "seg"
   Agent: "Model 'seg' registered. Files will be named: model_seg.py, trainer_seg.py, etc."
   ```

   If the user does not provide a name, suggest a semantic name and ask for confirmation:
   ```
   Agent: "Based on the architecture (UNet for segmentation), I suggest the name 'seg'.
          Files: model_seg.py, dataset_seg.py, trainer_seg.py, predictor_seg.py.
          Confirm or suggest an alternative?"
   ```

4. Ask: "Are there other models? If so, please provide the next model's architecture."

5. Repeat steps 2-4 until user indicates no more models.

### Per-Model Slot Data Table

For each model `{name}`, collect these slots:

| Slot | Description | Example |
|------|-------------|---------|
| `{name}_model_class` | Model class code | `class UNet(nn.Module): ...` |
| `{name}_model_import` | Import path | `from src.model.model_seg import UNet` |
| `{name}_model_creation` | Factory instantiation logic | `UNet(config.model)` |
| `{name}_model_config_fields` | Config dataclass fields | `backbone: str = "unet"` |
| `{name}_model_config_post_init` | Config validation logic | `assert self.depth > 0` |
| `{name}_model_init_params` | BaseModelProtocol init params | `config, num_classes=1` |
| `{name}_model_forward_shape` | Input/output shape docs | `Input: (B, 3, 224, 224) -> Output: (B, 1, 224, 224)` |
| `{name}_model_yaml_template` | YAML fields for model config | `backbone: unet\nbase_filters: 64` |
| `{name}_output_activation` | Output activation | `sigmoid` / `softmax` / `none` |

### Example Multi-Model Collection

```
Models collected:
  1. seg    - UNet (segmentation), input (B,3,224,224) -> (B,1,224,224), sigmoid
  2. cls_a  - ResNet18 (classification), input (B,3,224,224) -> (B,1), sigmoid
  3. cls_b  - ResNet18 (classification), input (B,3,224,224) -> (B,1), sigmoid

Confirm? [Y/n]
```

---

## Phase 2: Preprocessing Design (Loop)

**Goal:** Define data preprocessing for each model. Identify shared vs independent datasets.

### Step-by-Step Flow

1. For each model declared in Phase 1, ask preprocessing questions:
   - "What is the data format for model `{name}`? (PNG/JPG images, NIfTI volumes, CSV tables, etc.)"
   - "What preprocessing steps are needed? (normalization, resizing, patch extraction, etc.)"
   - "What is the file naming pattern and label format?"

2. For each model after the first, ask:
   "Does model `{name}` use an independent dataset, or does it share a data source with an existing model?"
   - **Independent:** Collect full data format, file naming, label format information.
   - **Shared:** Specify which model's data source to share; only collect model-specific preprocessing steps.

   **Example interaction:**
   ```
   Agent: "Does cls_a use an independent dataset, or share data with seg?"
   User: "cls_a shares the same raw images as seg, but uses different labels."
   Agent: "Registered: cls_a shares data source with seg. Only cls_a-specific preprocessing will be generated."
   ```

3. Record dataset sharing information:

   ```
   datasets:
     shared_source:
       - models: [seg, cls_a]
         source: dataset/raw_images
     independent:
       - model: cls_b
         source: dataset/cls_b_data
   ```

### Per-Model Slot Data

Same as v0.1.0 Phase 2, but with `{name}_` prefix:

| Slot | Description |
|------|-------------|
| `{name}_data_format` | Data format (png/jpg/nifti/csv) |
| `{name}_preprocessing_steps` | Preprocessing pipeline description |
| `{name}_file_naming` | File naming pattern |
| `{name}_label_format` | Label format description |
| `{name}_input_shape` | Input tensor shape |
| `{name}_normalization` | Normalization strategy |

---

## Phase 3: Project Structure

**Goal:** Collect project metadata.

### Questions

1. "What is the project package name? (used for Python imports, e.g., `my_project`)"
2. "What is the CLI entry point name? (e.g., `my-project-cli`)"
3. "Brief project description?"
4. "Author name?"
5. "License? (default: MIT)"

### Slots

| Slot | Description | Default |
|------|-------------|---------|
| `project_package_name` | Python package name | `my_project` |
| `cli_entry_point` | CLI command name | `project-cli` |
| `project_description` | One-line description | `Multi-model training CLI` |
| `project_author` | Author name | (required) |
| `project_license` | License type | `MIT` |
| `project_version` | Version string | `0.1.0` |

---

## Phase 4: Module Selection

**Goal:** Select optional modules for the project.

### Module List

Present the following modules for multi-select:

| Module | Function | Extra Dependencies |
|--------|----------|--------------------|
| `training_tricks` | MixUp, HEM, gradient accumulation, layer freezing | None |
| `memory_preload` | Cache entire dataset to RAM | None |
| `augmentation` | Training-time data augmentation pipeline | albumentations |
| `tta` | Test-Time Augmentation | albumentations |
| `postprocessing` | Threshold optimization, patient-level aggregation | matplotlib |
| `agent_workflow` | Claude Agent auto-training loop definition | None |
| `cli_config` | Config management commands (export, validate, show) | None |
| `cli_exp_train` | Training experiment management (list, summary, compare, clean) | None |
| `cli_exp_pred` | Inference result management (summary, compare, export) | None |
| `cli_ckpt` | Checkpoint management (list, info, export) | None |
| `cli_data` | Data management (check, split-info, stats) | None |
| `testing` | pytest test suite generation | pytest, pytest-cov |
| `packaging` | Python packaging scaffolding | build, twine |

### Per-Model Module Generation

When optional modules are selected, they generate per-model files:

| Module | Naming Pattern |
|--------|----------------|
| `memory_preload` | `memory_preloader_{name}.py` |
| `augmentation` | `augmentation_{name}.py` |
| `postprocessing` | `postprocessing_{name}.py` |

### Conflict Detection

Apply these rules:
- TTA selected without `augmentation` -> auto-include `augmentation`
- Early stopping requested without `checkpoint_resume` -> auto-include `checkpoint_resume`
- Agent workflow without `agent_state` -> auto-include `agent_state`
- Multi-model with `memory_preload` -> warn: each model gets independent preloader
- `cli_exp_train` / `cli_exp_pred` without architecture review -> warn

### Interaction Template

```
Available optional modules (select all that apply):

  [ ] training_tricks     MixUp, HEM, gradient accumulation, layer freezing
  [ ] memory_preload      Cache dataset to RAM
  [ ] augmentation        Data augmentation pipeline (albumentations)
  [ ] tta                 Test-Time Augmentation
  [ ] postprocessing      Threshold optimization, aggregation
  [ ] agent_workflow      Claude Agent auto-training loop
  [ ] cli_config          Config management commands
  [ ] cli_exp_train       Training experiment management
  [ ] cli_exp_pred        Inference result management
  [ ] cli_ckpt            Checkpoint management
  [ ] cli_data            Data management commands
  [ ] testing             pytest test suite
  [ ] packaging           Python packaging

Selection: ___
```

---

## Phase 5: Data Flow Design (v0.2.0 New)

**Goal:** Define training dependencies and inference data flow between models.

### Part 1: Training Data Flow

1. Ask: "Are there training dependencies between models? (i.e., does any model's training require another model's inference output as input data?)"

2. If dependencies exist, ask the user to declare them:
   ```
   Agent: "Please declare training dependencies for each model."
   User: "cls_a depends on seg's inference output. cls_b also depends on seg."

   Agent summarizes:
   Training dependencies:
     seg    -> no dependencies (can train immediately)
     cls_a  -> depends on [seg]
     cls_b  -> depends on [seg]

   Execution order (auto topological sort): seg -> cls_a -> cls_b

   Confirm? [Y/n]
   ```

3. If no dependencies: "All models can be trained independently. They will execute in declaration order."

4. Record pipeline topology slots:

   | Slot | Description | Example |
   |------|-------------|---------|
   | Per-model `model_dependencies` | Training dependency list | `[]` or `[seg]` |

### Part 2: Inference Data Flow

1. Ask: "What is the execution order and data passing between models during inference?"

2. User describes each step:
   ```
   User: "seg runs first on raw data. If seg predicts 0, cls_a processes the output.
         If seg predicts 1, cls_b processes the output."

   Agent summarizes:
   Inference flow:
     Step 1: seg     Input: raw_data     Condition: null          Output: seg_output
     Step 2: cls_a   Input: seg_output   Condition: seg==0        Output: final_output
     Step 3: cls_b   Input: seg_output   Condition: seg==1        Output: final_output

   Confirm? [Y/n]
   ```

3. Record inference flow slots:

   | Slot | Description | Example |
   |------|-------------|---------|
   | `flow_model_name` | Model name for this step | `seg` |
   | `flow_input` | Input source | `raw_data` or `seg_output` |
   | `flow_condition` | Routing condition | `null` or `seg.prediction == 0` |
   | `flow_output` | Output name | `seg_output` or `final_output` |

4. **Important reminder to user:** "The plugin generates framework files and orchestrates execution order. Inter-model data routing logic (how seg_output feeds into cls_a/cls_b) is implemented by you in each `predictor_{name}.py`."

---

## Phase 6: Project Architecture Review

**Goal:** Present complete folder structures for user confirmation.

### Step 1: Source Code Structure

Present the full project tree. Example for 3-model project (seg, cls_a, cls_b):

```
{project_root}/
  src/
    __init__.py
    __version__.py
    model/
      model_seg.py               <- seg model architecture
      model_cls_a.py             <- cls_a model architecture
      model_cls_b.py             <- cls_b model architecture
      model_factory.py           <- Factory: create_model(name, config)
    data/
      dataset_seg.py             <- seg dataset class
      dataset_cls_a.py           <- cls_a dataset class
      dataset_cls_b.py           <- cls_b dataset class
      preprocessing_seg.py       <- seg preprocessing
      preprocessing_cls_a.py     <- cls_a preprocessing
      preprocessing_cls_b.py     <- cls_b preprocessing
      splitting.py               <- Shared: data splitting
    training/
      trainer_seg.py             <- seg trainer
      trainer_cls_a.py           <- cls_a trainer
      trainer_cls_b.py           <- cls_b trainer
      loss.py                    <- Shared: loss functions
      early_stopping.py          <- Shared: early stopping
    prediction/
      predictor_seg.py           <- seg predictor
      predictor_cls_a.py         <- cls_a predictor
      predictor_cls_b.py         <- cls_b predictor
    pipeline/
      dependency_graph.py        <- Dependency declaration + topological sort
      train_pipeline.py          <- train_all orchestrator
      predict_pipeline.py        <- pred_all orchestrator
    cli/
      main.py                    <- CLI entry point
      train_cmd.py               <- train {name} / train all
      train_impl.py              <- Training implementation
      predict_cmd.py             <- pred {name} / pred all
      predict_impl.py            <- Prediction implementation
      get_cmd.py                 <- Export config templates
      utils.py                   <- CLI utilities (Rich output helpers)
    utils/
      config.py                  <- Multi-layer Config loading
      seeding.py                 <- Three-level seed management
      logger.py                  <- File ASCII box + Rich console logger
      log_formatter.py           <- ASCII box formatting utilities
      rich_display.py            <- Rich panels (config, results, model summary)
      verbose_display.py         <- VerboseLiveDisplay + SilentProgressBar
      metrics.py                 <- Shared metrics computation
  configs/
    pipeline_config.yaml         <- Single file: all configs + dependencies
  tests/
    test_model_seg.py
    test_model_cls_a.py
    test_model_cls_b.py
    test_config.py
    test_training.py
    test_pipeline.py
  pyproject.toml
  README.md
```

Ask: "Does this source code structure meet your expectations? Please confirm or indicate changes."

### Step 2: Training Experiment Folder Structure

```
experiments/
  {experiment_name}/
    pipeline_config_snapshot.yaml      # Config snapshot at training start
    training_summary.json              # Overall training summary
    train_execution_plan.txt           # Topologically sorted execution plan
    seg/                               # Per-model directory
      checkpoints/
        best_model.pth
        latest_model.pth
      logs/
        training_{timestamp}.log       # Full training log (ASCII box formatted)
        metrics_history.csv            # Per-epoch metrics (CSV)
      results/
        training_report.json
        confusion_matrix.png
    cls_a/
      checkpoints/
        best_model.pth
        latest_model.pth
      logs/
        training_{timestamp}.log
        metrics_history.csv
      results/
        training_report.json
        confusion_matrix.png
    cls_b/
      ... (same structure)
    split_info/
      seg_split.csv
      cls_a_split.csv
      cls_b_split.csv
```

Ask: "Does this training experiment folder structure meet your expectations?"

### Step 3: Inference Output Folder Structure

```
output/
  {experiment_name}/
    inference_config_snapshot.yaml
    inference_summary.json
    inference_execution_plan.txt
    seg/
      predictions.csv
      prediction_summary.json
      confusion_matrix.png
      raw_outputs/
        {sample_id}.npy
    cls_a/
      predictions.csv
      prediction_summary.json
      confusion_matrix.png
    cls_b/
      predictions.csv
      prediction_summary.json
      confusion_matrix.png
    final/
      combined_predictions.csv         # All models' results merged
      final_report.json                # Final inference report
```

Ask: "Does this inference output folder structure meet your expectations?"

### Step 4: User Confirmation

User may request adjustments to directory names, add/remove files, or modify organization. The confirmed structure becomes the strict reference for subsequent code generation.

---

## Phase 7: CLI Design

**Goal:** Define the CLI command structure, Rich beautification, and doctor configuration.

### CLI Command Structure

Present the full command tree:

```
project-cli
  train {name|all}            # Required: train model(s)
  pred {name|all}             # Required: inference
  version                     # Required: package version
  doctor                      # Required: environment check
  config                      # Optional: config management
    export                    #   Export annotated config template
    validate                  #   Validate config completeness
    show                      #   Display effective config
  exp                         # Optional: experiment management
    list                      #   List all experiments
    train                     #   Training experiment management
      summary                 #     View training summary
      compare                 #     Compare multiple experiments
      clean                   #     Clean failed/expired experiments
    pred                      #   Inference result management
      summary                 #     View inference summary
      compare                 #     Compare different inference results
      export                  #     Export inference results
  ckpt                        # Optional: Checkpoint management
    list                      #   List all checkpoints
    info {path}               #   Checkpoint details
    export {name}             #   Export best checkpoint for a model
  data                        # Optional: Data management
    check                     #   Validate dataset completeness
    split-info                #   View current data split info
    stats                     #   Dataset statistics
```

### CLI Command Examples

**train:**
```bash
# Train all models (topological order)
project-cli train all --config configs/pipeline_config.yaml

# Train single model (auto-trains dependencies first)
project-cli train cls_a --config configs/pipeline_config.yaml

# With verbose
project-cli train seg --config configs/ --verbose

# Resume training
project-cli train seg --config configs/ --resume
```

**pred:**
```bash
# Predict all models (inference_flow order)
project-cli pred all --config configs/pipeline_config.yaml --data dataset/test --output output/

# Predict single model
project-cli pred seg --config configs/ --data dataset/test --output output/seg/
```

**config:**
```bash
project-cli config export --path configs/
project-cli config validate --config configs/pipeline_config.yaml
project-cli config show --config configs/pipeline_config.yaml --model seg
```

**exp:**
```bash
project-cli exp list
project-cli exp train summary --name experiment_001
project-cli exp train compare --names experiment_001,experiment_002
project-cli exp train clean --before 2026-04-01 --keep-best 3
project-cli exp pred summary --dir output/experiment_001/
project-cli exp pred export --dir output/experiment_001/ --format csv
```

**ckpt:**
```bash
project-cli ckpt list --config configs/pipeline_config.yaml
project-cli ckpt info experiments/exp1/seg/best_model.pth
project-cli ckpt export seg --output release/seg_v1.pth
```

**data:**
```bash
project-cli data check --config configs/pipeline_config.yaml
project-cli data split-info --config configs/pipeline_config.yaml
project-cli data stats --config configs/pipeline_config.yaml
```

### CLI Beautification Confirmation

Present this checklist to the user:

```
Rich terminal beautification configuration:

During training/inference:
  [x] Progress bar (Epoch/Batch level)
  [x] Real-time log panel (latest N lines)
  [x] Key metrics live update (loss/lr/metrics)
  Progress bar refresh rate: 4/s (recommended)

Before training/inference:
  [x] Configuration panel (Panel + Table, blue border)
  [x] Model parameter summary (total/trainable/frozen)

After training/inference:
  [x] Results panel (duration/best metrics/file paths, green border)
  [x] Test metrics table (AUC/Acc/F1/Precision/Recall)
  [x] Confusion matrix plot (saved as PNG)

CLI command output:
  [x] Command header (project name + version, blue border)
  [x] Status icons (pass/warn/fail)
  [x] doctor check result table

Log file formatting:
  [x] ASCII box sections (width=60, config/model summary/results)
  [x] Pipe-separated metrics (metric1=0.1234 | metric2=0.5678)
  [x] Epoch separator (50 dashes)
  [x] 4 decimal places for floats

Please confirm or modify.
```

### `doctor` Detection Item Configuration

Present options:

```
doctor environment check configuration:

Basic checks (recommended all):
  [x] Python version (>=3.9)
  [x] PyTorch version (>=2.0)
  [x] CUDA availability + GPU info
  [x] Disk space check

Dependency package checks (select as needed):
  [x] numpy
  [x] pandas
  [x] scikit-learn
  [ ] monai              <- Medical imaging library
  [ ] timm               <- PyTorch Image Models
  [ ] opencv-python
  [ ] nibabel            <- NIfTI format support
  [x] tqdm
  [x] pyyaml
  [x] typer
  [x] rich

Project status checks:
  [x] Config file existence
  [x] Data directory existence
  [x] Checkpoint directory scan

Please confirm or modify.
```

Record user selections in `pipeline_config.yaml` under `doctor.enabled_checks`.

### CLI Command vs Module Registry

| CLI Command | Module | Core/Optional |
|------------|--------|--------------|
| `train` | cli_base | Core |
| `pred` | cli_base | Core |
| `version` | cli_base | Core |
| `doctor` | cli_doctor | Core |
| `config` | cli_config | Optional |
| `exp train` | cli_exp_train | Optional |
| `exp pred` | cli_exp_pred | Optional |
| `ckpt` | cli_ckpt | Optional |
| `data` | cli_data | Optional |

---

## Phase 8: Design Review

**Goal:** Validate the complete design before code generation.

### Review Checklist

1. Generate a design summary document covering Phase 1-7 outputs.
2. Check the following:
   - Interface consistency between models/preprocessing/datasets/trainers
   - All slots have corresponding data for every model
   - Module dependency graph is valid (no cycles, no missing deps)
   - No conflicting module selections
   - Data flow declarations are consistent with model I/O shapes
   - Training dependencies match data flow design (Phase 5)
   - CLI command set matches selected modules (Phase 4 + Phase 7)
   - Shared vs per-model file split is correct

### Review Loop

- Max 3 review loops. If issues persist after 3 loops, present remaining issues to user for manual decision.
- Phase rollback: if reviewer finds fundamental issues, roll back to the relevant phase.

### Interaction Template

```
Design Review Summary:

Models: seg (UNet), cls_a (ResNet18), cls_b (ResNet18)
Dependencies: seg -> [cls_a, cls_b]
Inference flow: seg -> (condition) -> cls_a | cls_b
CLI commands: train, pred, version, doctor, config, exp, ckpt, data
Modules: checkpoint_resume, augmentation, testing, packaging

Checks:
  [pass] Interface consistency
  [pass] Slot completeness (all models have all required slots)
  [pass] Module dependency graph valid
  [pass] No conflicting module selections
  [pass] Data flow consistent with model I/O
  [pass] CLI matches selected modules

All checks passed. Proceed to Phase 9? [Y/n]
```

---

## Phase 9: Development Environment Review

**Goal:** Review and confirm development environment setup before code generation.

### Step 1: Python Package Manager

```
Please select the project's Python package manager:

  [a] uv    - Fast, modern, pyproject.toml-based. Default choice.
  [b] conda - Scientific computing ecosystem, convenient for CUDA deps.

If neither is installed:
  - uv will be auto-installed for the current platform.
  - Conda is not auto-installed; user must install manually.

Selection: ___
```

**Default:** uv. Detection order: uv -> conda -> install uv -> use uv.

**Generated files:**
- uv: `pyproject.toml` + `.python-version`
- conda: `environment.yaml`

### Step 2: Python Version

```
Please select the project's Python version:

  [a] 3.9   - Minimum compatible version
  [b] 3.10  - Enhanced type hints (recommended)
  [c] 3.11  - Performance improvements
  [d] 3.12  - Latest stable release

Please confirm: ___
```

### Step 3: CUDA Environment

```
Please confirm CUDA acceleration environment:

  [a] CUDA available -> please provide CUDA version:
      [11.8] [12.1] [12.4] [12.8] [custom version]
      Detected from current environment: CUDA 12.1 (Tesla V100)

  [b] CPU only -> all dependencies will install CPU versions.

CUDA version determines PyTorch download source.
```

**CUDA -> PyTorch mapping (MUST use this table, do NOT guess):**

| CUDA Version | PyTorch Version | torchvision Version | Suffix |
|-------------|----------------|--------------------|--------|
| 11.8 | 2.6.0 | 0.21.0 | cu118 |
| 12.1 | 2.6.0 | 0.21.0 | cu121 |
| 12.4 | 2.6.0 | 0.21.0 | cu124 |
| 12.8 | 2.7.0 | 0.22.0 | cu128 |
| CPU only | 2.6.0 | 0.21.0 | cpu |

### Step 4: Core Dependency Version Locking

```
Core dependencies (required for all projects). Please confirm versions:

  Package           Recommended    Constraint      Description
  -----------------------------------------------------------------------
  torch             2.6.0          >=2.0            Determined by CUDA version
  torchvision       0.21.0         >=0.15           Paired with torch version
  numpy             1.26.4         >=1.24           Data processing
  pandas            2.2.3          >=2.0            Data table management
  pyyaml            6.0.2          >=6.0            Config file parsing
  typer             0.15.2         >=0.9            CLI framework
  tqdm              4.67.1         >=4.60           Progress bar (fallback)
  scikit-learn      1.6.1          >=1.0            Evaluation metrics
  rich              13.9.4         >=13.0           Terminal beautification
  matplotlib        3.10.0         >=3.5            Plotting

Please confirm recommended versions, or specify custom versions: ___
```

### Step 5: Optional Dependency Version Locking

Based on Phase 4 module selection results, present corresponding optional dependencies:

```
Optional dependencies (based on your selected modules). Please confirm versions:

  Selected modules: augmentation, postprocessing, testing

  Package           Recommended    Constraint      Source Module
  -----------------------------------------------------------------------
  albumentations    2.0.5          >=1.3           augmentation
  pytest            8.3.4          >=7.0           testing
  pytest-cov        6.0.0          >=5.0           testing (coverage)

Please confirm recommended versions, or specify custom versions: ___
```

**Module -> optional dependency mapping (MUST use this table):**

| Module | Optional Dependencies |
|--------|----------------------|
| augmentation | albumentations |
| augmentation (medical imaging) | monai |
| tta | albumentations |
| postprocessing | matplotlib |
| testing | pytest, pytest-cov |
| packaging | build, twine |
| (others) | (no extra dependencies) |

### Step 6: Environment Config File Preview

Based on confirmed selections, generate environment config files for user review.

**uv output preview:** `pyproject.toml` (dependency section) + `.python-version`
**conda output preview:** `environment.yaml`

Auto-detect environment info (`nvidia-smi`, `python --version`, `uv --version`) before asking user to confirm.

---

## Phase 10: Implementation Plan

**Goal:** Create a detailed per-file generation plan.

### Generation Order

For each file in order:

1. **Shared utilities** (no per-model repetition):
   - `src/utils/config.py` <- `blueprints/config/config.py.bp`
   - `src/utils/seeding.py` <- `blueprints/utils/seeding.py.bp`
   - `src/utils/log_formatter.py` <- `blueprints/utils/log_formatter.py.bp`
   - `src/utils/rich_display.py` <- `blueprints/utils/rich_display.py.bp`
   - `src/utils/verbose_display.py` <- `blueprints/utils/verbose_display.py.bp`
   - `src/utils/logger.py` <- `blueprints/utils/logger.py.bp`
   - `src/utils/metrics.py` <- `blueprints/utils/metrics.py.bp`

2. **Per-model files** (repeat for each declared model):
   - `src/model/model_{name}.py` <- `blueprints/model/model_interface.py.bp` (fill `{name}` slots)
   - `src/data/dataset_{name}.py` <- `blueprints/data/dataset.py.bp` (fill `{name}` slots)
   - `src/data/preprocessing_{name}.py` <- `blueprints/data/preprocessing.py.bp` (fill `{name}` slots)
   - `src/training/trainer_{name}.py` <- `blueprints/training/trainer.py.bp` (fill `{name}` slots)
   - `src/prediction/predictor_{name}.py` <- `blueprints/prediction/predictor.py.bp` (fill `{name}` slots)
   - Conditional: `src/data/memory_preloader_{name}.py` (if `memory_preload` selected)
   - Conditional: `src/data/augmentation_{name}.py` (if `augmentation` selected)
   - Conditional: `src/prediction/postprocessing_{name}.py` (if `postprocessing` selected)

3. **Shared modules**:
   - `src/model/model_factory.py` <- `blueprints/model/model_factory.py.bp`
   - `src/data/splitting.py` <- `blueprints/data/splitting.py.bp`
   - `src/training/loss.py` <- `blueprints/training/loss.py.bp`
   - `src/training/early_stopping.py` <- `blueprints/training/early_stopping.py.bp`

4. **Pipeline**:
   - `src/pipeline/dependency_graph.py` <- `blueprints/pipeline/dependency_graph.py.bp`
   - `src/pipeline/train_pipeline.py` <- `blueprints/pipeline/train_pipeline.py.bp`
   - `src/pipeline/predict_pipeline.py` <- `blueprints/pipeline/predict_pipeline.py.bp`

5. **CLI**:
   - `src/cli/main.py` <- `blueprints/cli/main.py.bp`
   - `src/cli/train_cmd.py` <- `blueprints/cli/train_cmd.py.bp`
   - `src/cli/train_impl.py` <- `blueprints/cli/train_impl.py.bp`
   - `src/cli/predict_cmd.py` <- `blueprints/cli/predict_cmd.py.bp`
   - `src/cli/predict_impl.py` <- `blueprints/cli/predict_impl.py.bp`
   - `src/cli/get_cmd.py` <- `blueprints/cli/get_cmd.py.bp`
   - `src/cli/utils.py` <- `blueprints/cli/utils.py.bp`

6. **Config**:
   - `configs/pipeline_config.yaml` <- `blueprints/config/yaml_templates/pipeline_config.yaml.bp` (expand REPEAT_SLOT per model)

7. **Packaging**:
   - `pyproject.toml` <- `blueprints/packaging/pyproject.toml.bp`
   - `.python-version` (uv only)
   - `README.md`

8. **Tests**:
   - `tests/test_model_{name}.py` (per model)
   - `tests/test_config.py`
   - `tests/test_pipeline.py`
   - `tests/test_training.py`

### Verification Steps

1. `uv pip install -e .` (or conda equivalent)
2. `python -c "from src import __version__; print(__version__)"`
3. `pytest tests/ -v`
4. CLI smoke test: `project-cli version`
5. CLI doctor test: `project-cli doctor`

---

## Phase 11: Code Generation

**Goal:** Generate all project files and verify the output.

### Per-File Process

1. Read the `.bp` template.
2. Fill all `<<SLOT>>` markers with Phase 1-9 data.
3. Keep or strip `<<CONDITIONAL_SLOT>>` blocks based on Phase 4 selections.
4. Expand `<<REPEAT_SLOT>>` blocks per model (for config YAML, per-model file generation).
5. Use `<<OPTIONAL_SLOT>>` defaults where user did not override.
6. Strip all marker comments (opening and closing tag lines).
7. Write to output project directory (without `.bp` extension).

### Post-Generation Verification

Run these commands in the generated project directory:

```bash
# 1. Install
uv pip install -e .

# 2. Version check
python -c "from src import __version__; print(__version__)"

# 3. Test suite
pytest tests/ -v

# 4. CLI smoke test
project-cli version

# 5. Doctor check
project-cli doctor
```

Report results to user. If any step fails, diagnose and fix the issue.

### Completion

After all verification passes, present a summary:

```
Project generated successfully!

Location: {output_path}
Models: {model_count} ({model_names})
CLI: {cli_entry_point}
Config: configs/pipeline_config.yaml

Quick start:
  cd {output_path}
  {cli_entry_point} doctor              # Check environment
  {cli_entry_point} train all --config configs/ --verbose   # Train all models
  {cli_entry_point} pred all --config configs/ --data test/ --output output/

Next steps:
  1. Implement model architectures in src/model/model_{name}.py
  2. Implement data loading in src/data/dataset_{name}.py
  3. Implement inter-model routing in src/prediction/predictor_{name}.py
  4. Run training: {cli_entry_point} train all --config configs/ --verbose
```
