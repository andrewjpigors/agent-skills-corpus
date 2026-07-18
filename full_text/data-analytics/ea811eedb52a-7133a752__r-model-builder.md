---
name: r-model-builder
description: Build advanced R model-helper layers for clinical and statistical workflows, including Bayesian, causal, meta-analytic, SEM, tidymodels, and post-estimation helpers. Use when implementing or hardening reusable modeling code.
argument-hint: [modeling task or helper]
---

# R Model Builder

Implement advanced R modeling helpers as small, testable layers that separate variable selection, fitting, warning capture, and reporting.

## Quick start

1. Read `references/model-builder-patterns.md`.
2. If the helper must work with large or Parquet-backed data, also read `references/arrow-parquet-model-builders.md`.
3. If the helper must construct tidymodels model specs, recipes, workflows, tuned workflow helpers, or finalized workflow objects, also read `references/tidymodels-model-builders.md`.
4. If the helper must support multiple imputation or pooled fits, also read `references/multiple-imputation-model-builders.md`.
5. If the helper must return adjusted predictions, contrasts, slopes, or emmeans-style marginal means through `marginaleffects`, also read `references/marginal-effects-model-builders.md`.
6. If the helper must return model-output figures, post-estimation plots, or Shiny-facing interactive analytical figures, also read `references/model-output-figures-and-interactivity.md`.
7. If the helper must support pediatric oncology competing-risk/time-to-event work or pediatric asthma recurrent-event/longitudinal workflows, also read `references/specialized-clinical-endpoint-model-builders.md`.
8. If the helper must support complex survey designs, weighted descriptives, `svyglm()`, or `srvyr`/replicate-weight workflows, also read `references/survey-design-model-builders.md`.
9. If the helper must support Bayesian regression, `brms`, posterior draws, `tidybayes`, posterior predictive checks, or `loo()` comparison, also read `references/bayesian-model-builders.md`.
10. If the helper must support observational causal design through matching, weighting, balance diagnostics, trimming, or post-design effect estimation, also read `references/causal-design-model-builders.md`.
11. If the helper must support meta-analysis through `metafor`, effect-size construction, multilevel synthesis, forest-plot-ready outputs, or influence diagnostics, also read `references/meta-analysis-model-builders.md`.
12. If the helper must expose diagnostics, parameter tables, effect sizes, or easystats-driven summary layers through `performance`, `parameters`, `effectsize`, or `report`, also read `references/easystats-model-summary-adapters.md`.
13. If the helper must support GEE or repeated-measure population-averaged models through `geepack`, `geeglm()`, `geese()`, working-correlation comparison, or `QIC()`, also read `references/gee-model-builders.md`.
14. If the helper must support structural equation models, confirmatory factor analysis, growth curves, latent-variable regression, `lavaan`, `cfa()`, `sem()`, `growth()`, fit measures, standardized solutions, modification indices, or latent scores, also read `references/lavaan-model-builders.md`.
15. If the helper must support ROC/AUC, precision-recall evaluation, Brier score, calibration, threshold metrics, decision curves, `pROC`, `probably`, or `rmda`, also read `references/predictive-performance-model-builders.md`.
16. If the helper must support bootstrap or permutation inference, `boot::boot()`, `boot.ci()`, `rsample::bootstraps()`, `int_pctl()`, `int_t()`, `int_bca()`, or `infer` resampling pipelines, also read `references/bootstrap-and-permutation-adapters.md`.
17. If the helper must support nonlinear smooths, splines, `mgcv`, `gam()`, `bam()`, `s()`, `te()`, `ti()`, `t2()`, or `ns()`, also read `references/gam-model-builders.md`.
18. If the helper must produce deployable model artifacts, prediction endpoints, or remote scoring helpers through `vetiver`, also read `references/vetiver-deployment-surfaces.md`.
19. When the helper lives inside a package that must support a new model class for `marginaleffects`, also read `r-package-dev/references/marginaleffects-package-extension.md`.
20. Split the task into five layers:
   - recommendation/helper logic;
   - formula builder;
   - model-data slice/materialization helper;
   - fit wrapper;
   - reporting/tidy table or figure surface.
21. Keep recommendation helpers pure.
22. Keep the data-materialization boundary explicit: narrow first, then collect only the model-ready slice.
23. Keep the missing-data boundary explicit too: imputation planning, scientific model fitting, and pooled reporting should stay visible as separate layers.
24. Keep the post-estimation boundary explicit too: fitting the model and computing predictions/comparisons/slopes should remain separate layers.
25. Keep the figure boundary explicit too: plot-ready data, canonical ggplot output, and optional interactive wrapping should remain separate layers.
26. Keep the resampling-inference boundary explicit too: observed statistic or fit, resampling engine, interval or p-value summarizer, and reporting adapter should remain separate layers.
27. Capture warnings in the fit wrapper and surface them in the result object.
28. Add tests for both the pure helper and the calling module or script. In package repos, scaffold the `R/` and `tests/testthat/` pair with `usethis::use_r()` and `use_test()` when files are missing or drifting.

## Workflow

### 1. Define the estimand and family

Clarify whether the target is:
- mean difference,
- odds ratio,
- hazard ratio,
- rate ratio,
- mixed-model fixed effect,
- adjusted prediction,
- risk difference or risk ratio,
- derivative-style marginal effect,
- or a custom estimand such as adjusted RMST difference.

The displayed estimand should drive:
- family choice,
- exponentiation rules,
- post-estimation function choice,
- table labels,
- and formatting.

### 2. Build recommendation helpers separately

When defaults depend on metadata or a registry, score candidates in a pure function and return a simple list of recommended inputs.

### 3. Build formulas defensively

Construct the right-hand side from validated term vectors and append random effects only after checking the grouping variable.

### 4. Make the model-data boundary explicit

When the upstream data source is large, lazy, or Parquet-backed:
- select only the variables required by the model spec;
- push obvious filters upstream before materialization;
- collect only the model-ready slice;
- keep the data-read boundary out in the open instead of hiding it inside the fit wrapper.

The fit wrapper should receive a ready-to-fit in-memory frame plus enough metadata to report row counts, dropped rows, and any upstream dataset signature.

### 4b. Keep tidymodels stages explicit when that stack is in play

- Current `parsnip` documentation says `fit()` and `fit_xy()` take a model specification, translate the required code, and execute the fit routine. Keep that model-spec layer separate from preprocessing and resampling decisions.
- Current `parsnip::set_engine()` documentation says engine-specific arguments are captured and can be tuned. Keep engine choice and engine arguments explicit in the helper contract rather than burying them inside one opaque fit call.
- Current `workflows` documentation describes a workflow as the container that aggregates preprocessing and model information needed to fit and predict. When preprocessing is part of the public contract, keep the canonical helper surface as a workflow built from `add_model()` plus `add_recipe()` or another explicit preprocessor.
- Current `recipes` documentation says `prep()` estimates preprocessing parameters from training data and `bake()` applies the trained recipe to new data. Treat that as the leakage boundary: recipe estimation belongs inside the training/resampling process, not as a one-time global transform over the full dataset.
- Current `tune_grid()` documentation says tuning computes metrics for a set of model or recipe tuning parameters across resamples. Keep the resample object, tuning result, finalized workflow, and final fitted workflow as separate surfaces instead of collapsing them into one giant helper return.
- Current `finalize_*()` documentation says finalized parameter values can be spliced into models, recipes, and workflows. Keep the finalize step visible so downstream code can tell whether it is holding a tunable object or a locked workflow ready for final fitting.
- Team inference: for reusable model-helper layers, an unfitted workflow plus explicit resampling and finalize helpers is often a stronger contract than returning only an already fitted model object, because it keeps preprocessing, tuning, and final fitting inspectable and testable.

### 4c. Keep Bayesian posterior quantity surfaces explicit when using `brms`

- Current `brm()` documentation says the returned `brmsfit` object holds posterior draws together with rich model metadata. Keep the fit wrapper focused on producing a stable `brmsfit` plus explicit metadata about formula, family, priors, backend, and sampling posture.
- Current `posterior_epred()` documentation says expected-response draws and predictive draws answer different questions. Preserve separate helper surfaces for:
  - parameter summaries;
  - expected-response summaries (`posterior_epred()` / `add_epred_draws()`);
  - posterior predictive summaries (`posterior_predict()` / `add_predicted_draws()`).
- Current `posterior` documentation keeps `draws_df`, `rvar`, and `summarise_draws()` explicit. Normalize posterior draws through one adapter layer so downstream tables, plots, and Shiny surfaces share the same tidy contract.
- Current `conditional_effects()` documentation supports fitted values, predictive quantities, spaghetti overlays, and explicit resolution settings. Keep grid construction and posterior-quantity choice visible rather than hiding them deep inside a plotting helper.
- Current `pp_check()` documentation says model checks are routed through `bayesplot` PPC functions. Keep posterior predictive checking as a named helper surface alongside coefficient or curve helpers so model criticism stays inspectable.
- Current `loo` documentation keeps predictive-comparison outputs and Pareto-k diagnostics explicit. When helpers support model comparison, return the comparison object and diagnostics rather than collapsing them into a single selected label.
- Team doctrine: split Bayesian helper layers into fit, draw-extraction, expected-response, predictive-response, and model-check/comparison surfaces.

### 5. Make the imputation boundary explicit when missingness matters

- Keep the imputation plan separate from the scientific model helper.
- Reuse one validated model expression or formula across imputations.
- Pool fitted-model estimates rather than collapsing completed datasets into one analytic frame.
- Keep mixed-model pooling support and manual scalar pooling paths visible when tidiers are unavailable.

### 6. Fit with `data =` and warning capture

Wrap the fitting call so warnings are captured, deduplicated, and returned for UI or report display. Keep the `data =` contract explicit so the helper fits the already prepared model frame, not an opaque source path or lazy dataset object.

### 7. Add a post-estimation adapter when the estimand is not a raw coefficient

- Compute adjusted predictions with `predictions()` / `avg_predictions()`.
- Compute emmeans-style marginal means explicitly with `predictions()` on `newdata = "balanced"` or `datagrid(grid_type = "balanced")` when that reporting mode is required.
- Compute counterfactual contrasts with `comparisons()` / `avg_comparisons()`, including custom `comparison=` functions when the estimand is bespoke.
- Compute derivative-style marginal effects with `slopes()` / `avg_slopes()`, keeping `slope=` explicit for elasticity variants.
- Keep `hypotheses()` and, when warranted, `inferences()` available when helpers must own post-estimation testing or uncertainty.
- Keep the grid builder, `type=`, and averaging choice explicit so the downstream report surface receives a stable, interpretable object.

### 7b. Add a figure adapter when the output also needs a plot

- Current `marginaleffects` plot docs support `plot_predictions()`, `plot_comparisons()`, and `plot_slopes()` as reusable figure builders. Those docs also note that `plot_predictions()` can return the underlying data frame when `draw = FALSE`, which is a useful testing and Shiny-integration surface.
- Keep the figure helper separate from the fit helper: the fit/post-estimation layer should return the analytical result, and the figure layer should transform that result into either plot-ready data or one canonical ggplot object.
- Keep `condition` and `by` explicit because the docs map them directly to x-axis, color/shape, facets, and averaging semantics. If the figure is mixed-model-based, keep grouping-variable choices or model-specific prediction arguments visible in the helper interface.
- When the figure will appear in Shiny, wrap the canonical ggplot at the app boundary with `plotOutput()`, `ggplotly()`, or `girafe()` rather than baking widget-specific assumptions into the core model helper.
- Keep tooltip fields, key columns, and any linked-view identifiers explicit so the interactive layer does not have to guess how to reconnect the plotted estimate to the underlying analytical object.

### 8. Tidy once, then format for display

Generate one tidy result table and reuse it across:
- raw checks,
- Shiny tables,
- report output,
- and figure helpers that need the same estimates in plotted form.

For pooled multiple-imputation results, keep one adapter that converts the `mipo` summary or scalar-pooled results into the same tidy display contract.

For post-estimation results, keep one adapter that converts `marginaleffects` objects into the same display-ready contract used by downstream reporting wrappers and figure builders.

### 8b. Keep survey-design layers explicit when weighting is design-based

- Current `svydesign()` and `svrepdesign()` documentation keeps ordinary design weights and replicate-weight designs on separate constructor surfaces. Keep that distinction visible in helper APIs instead of hiding it behind one ambiguous weight argument.
- Current `srvyr::as_survey_design()` and `as_survey_rep()` documentation supports tidy-style constructors while still exposing `ids`, `strata`, `weights`, `repweights`, and `type`. Keep those survey inputs inspectable even when the surrounding workflow is dplyr-oriented.
- Current `subset.survey.design()` documentation says subsetting preserves the original design information. Keep subpopulation/domain helpers separate from raw row-filter helpers.
- Current `svyglm()` documentation keeps `formula`, `design`, and family choice explicit. Preserve that surface in the fit wrapper and return enough design metadata for downstream reporting.
- Team doctrine: keep design construction, domain restriction, formula building, fit wrapping, and reporting adapters as separate layers whenever weighted survey inference is part of the helper contract.

### 8c. Keep causal-design helper layers explicit in observational studies

- Current `matchit()` documentation says the returned object contains the design decisions and resulting matched sample information. Keep the matching specification helper separate from matched-data extraction and effect-estimation helpers.
- Current MatchIt guidance shows `match_data()` and `get_matches()` as downstream extraction surfaces carrying `weights`, `distance`, and often `subclass` or unit IDs. Preserve those fields in the model-ready output instead of rebuilding them ad hoc later.
- Current `weightit()` documentation keeps the weighting method, requested estimand, focal group, and optional M-estimation support explicit. Keep the weighting helper separate from the downstream weighted outcome-model helper.
- Current `glm_weightit()` documentation says it can fit outcome models with covariance matrices that account for weight estimation. Keep weighted effect-model helpers narrow enough that the uncertainty method remains inspectable.
- Current `cobalt` documentation positions `bal.tab()` as the cross-package balance surface. Keep balance-summary helpers separate from effect-estimation helpers so alternative designs can be compared before outcome modeling.
- Current `trim()` documentation supports trimming and dropping extreme weights on a `weightit` object. Keep trimming helpers and their metadata separate from the original design object so downstream code can still compare pre-trim and post-trim designs.
- Team doctrine: split observational-causal helpers into design specification, design object, balance diagnostics, optional trimming, analysis-ready extraction, and effect-model layers.

### 8d. Keep meta-analysis helper layers explicit in evidence-synthesis work

- Current `escalc()` documentation says the effect-size computation depends on study design, outcome type, and available data. Keep effect-size construction in its own helper surface so `yi`, `vi`, `slab`, and effect-measure metadata remain inspectable.
- Current `rma.uni()` documentation keeps equal-effects, fixed-effects, random-effects, and mixed-effects meta-regression within one family of fitted objects. Keep the meta-analytic model helper separate from effect-size construction so heterogeneity choices are visible.
- Current `rma.mv()` documentation keeps the variance-covariance matrix `V` and the random-effects structure explicit. When effect sizes are correlated, keep the covariance-construction helper separate from the fitting helper.
- Current `forest.rma()` documentation supports model-aware plotting features such as `addfit` and `addpred`. Keep plot-ready extraction or forest-plot helper layers separate from the fit object so reporting code can choose the right display without re-fitting.
- Current `leave1out()` and `influence()` documentation expose sensitivity surfaces tied to the fitted synthesis model. Keep sensitivity helpers separate from the main fit helper so they can be run selectively and reported independently.
- Team doctrine: split meta-analysis helpers into effect-size construction, synthesis-model fitting, moderator fitting, sensitivity diagnostics, and reporting/plot adapters.

### 8e. Keep easystats adapters separate from the fit wrapper

- Current `performance` documentation exposes both broad check surfaces such as `check_model()` and focused helpers such as `check_collinearity()` and `check_overdispersion()`. Keep diagnostic adapters separate from the fit wrapper so narrow checks can be reused without regenerating every reporting surface.
- Current `model_performance()` and `compare_performance()` documentation supports cross-model fit summaries. Keep performance-summary helpers separate from parameter extraction so downstream code can compare models without conflating fit metrics and coefficients.
- Current `parameters::model_parameters()` documentation provides a broad, tidy parameter table with options for standardization, exponentiation, grouping, and Bayesian extras. Treat that as a dedicated adapter layer rather than baking one bespoke coefficient tibble into every modeling helper.
- Current `effectsize` documentation exposes both generic and dedicated effect-size surfaces. Keep effect-size adapters separate from parameter adapters so the workflow can return coefficients, standardized effects, and design-specific effect sizes as different objects.
- Current `report` documentation provides narrative communication surfaces. Keep report-style helpers downstream of diagnostics and parameter adapters rather than letting a narrative helper become the only extractable summary contract.
- Team doctrine: split reusable helper layers into fit, diagnostic adapter, parameter adapter, effect-size adapter, and communication adapter whenever easystats is part of the workflow.

### 8f. Keep GEE helper layers explicit in correlated-data workflows

- Current `geeglm()` documentation says the cluster `id` should identify contiguous rows for each cluster and that `waves` can define the ordering of repeated measurements. Keep cluster-prep helpers separate from the fit wrapper so sorting and ordering assumptions are inspectable and testable.
- The same documentation says the function only works on complete data. Keep complete-case or other pre-fit handling in a distinct prep layer instead of letting the fit wrapper silently drop or reshape rows.
- Current `geeglm()` documentation keeps `corstr`, `zcor`, `std.err`, `scale.fix`, and `scale.value` explicit. Preserve those arguments in a narrow fit wrapper so working-correlation and standard-error choices remain visible in downstream tables and comparisons.
- Current `QIC()` documentation distinguishes working-correlation comparison from mean-model comparison through `QIC`, `CIC`, and `QICu`. Keep correlation-comparison helpers separate from the main fit helper so alternative structures can be compared cleanly.
- Current `geese()` documentation exposes separate mean, scale, and correlation-model surfaces. Keep a distinct advanced-fit helper for that path instead of overloading the simpler `geeglm()` wrapper.
- Team doctrine: split repeated-data helpers into cluster-prep, fit, working-correlation comparison, advanced covariance-structure, and reporting-adapter layers.

### 8g. Keep lavaan helper layers explicit in latent-variable workflows

- Current `lavaan` tutorial guidance centers the workflow on model syntax, fitting families such as `cfa()`, `sem()`, and `growth()`, and extractor functions. Keep the syntax builder separate from the fit wrapper so measurement and structural specifications stay inspectable.
- Current `sem()` documentation says it wraps `lavaan()` with common SEM defaults. Keep family-specific wrappers explicit so downstream code can tell whether the helper is fitting CFA, SEM, growth, or a more general `lavaan()` model.
- Current extractor documentation keeps `fitMeasures()`, `parameterEstimates()`, `standardizedSolution()`, `lavInspect()`, `modificationIndices()`, and `lavPredict()` on distinct surfaces. Preserve separate adapters for fit summaries, parameter tables, standardized solutions, local diagnostics, and latent-score outputs.
- Current `lavTestLRT()` documentation says nested comparisons can depend on the estimator and may require scaled difference tests. Keep model-comparison helpers separate from the main fit wrapper so comparison posture stays visible.
- When helpers expose multigroup, categorical-indicator, clustered, or weighted SEM options, keep those arguments visible in the helper contract instead of burying them inside a giant `...` surface.
- Team doctrine: split SEM helpers into syntax builder, fit wrapper, fit-summary adapter, parameter-summary adapter, diagnostic adapter, and latent-score adapter layers.

### 8h. Keep predictive-performance adapters separate from the fit wrapper

- Current `yardstick` documentation keeps `roc_auc()`, `pr_auc()`, and `brier_class()` as distinct probability-metric surfaces. Keep discrimination, precision-recall, and probability-error adapters separate so downstream code can request the right evaluation surface without unpacking one overloaded summary object.
- Current `pROC::roc()` documentation builds a reusable ROC object, while current `ci.auc()` and `coords()` documentation keep AUC uncertainty and threshold coordinates on dedicated surfaces. Preserve separate adapters for ROC construction, AUC intervals, and threshold extraction.
- Current `pROC::roc()` documentation keeps `levels` and `direction` explicit and warns about automatic direction when data are resampled or randomized. Keep score orientation visible in helper metadata so evaluation results remain comparable across splits and reruns.
- Current `probably::cal_plot_breaks()` and `threshold_perf()` documentation keep calibration and threshold-performance summaries on distinct surfaces. Build those from predicted probabilities rather than from already dichotomized predictions.
- Current `rmda::decision_curve()` and `plot_decision_curve()` documentation keep `policy`, threshold range, study design, and prevalence assumptions explicit. Keep decision-curve adapters separate from generic metric adapters so clinical utility stays inspectable.
- Team doctrine: split prediction-evaluation helpers into probability extractor, discrimination adapter, calibration adapter, threshold-performance adapter, and decision-curve adapter layers.

### 8i. Keep bootstrap and permutation adapters separate from fit wrappers

- Current `boot::boot()` documentation says the statistic function must accept the observed data plus indices, frequencies, or weights depending on `stype`, and that the returned object carries `t0`, `t`, `R`, `sim`, `stype`, and seed metadata. Keep the observed statistic function separate from the resampling engine so downstream code can inspect both the scientific statistic and the resampling scheme.
- The same documentation keeps `sim`, `strata`, `simple`, and parallel settings explicit. Preserve those choices in helper metadata rather than flattening every resampling workflow into one generic confidence-interval helper.
- Current `boot.ci()` documentation keeps interval family explicit through `type = c("norm", "basic", "stud", "perc", "bca")` and requires variance information for studentized intervals. Build interval adapters separately from the resampling engine so a helper can switch interval families without rewriting the statistic function.
- Current `rsample::bootstraps()` documentation returns `bootstraps` objects with analysis and assessment splits, while current `int_pctl()` documentation expects tidy bootstrap estimate columns and uses different requirements for percentile, student-t, and BCa intervals. Keep `rsample`-native interval adapters distinct from `boot`-object adapters.
- Current `infer::generate()` documentation keeps bootstrap, permutation, and theoretical-draw generation on separate `type` values, and current `get_confidence_interval()` plus `get_p_value()` documentation keeps interval and p-value summarization as separate downstream steps. Preserve separate adapters for null-distribution generation, confidence-interval summarization, and p-value summarization whenever `infer` is in play.
- Current `boot` parallel-operation documentation says reproducibility changes when random-number generation moves into worker processes. Keep seed choice, backend, and any Windows `snow` posture visible in helper metadata when the resampling path is parallelized.
- Team doctrine: split resampling-based helper stacks into observed-statistic builder, resampling engine, interval or p-value adapter, and reporting adapter layers.

### 8j. Keep GAM and spline helper layers explicit in nonlinear workflows

- Current `mgcv::gam()` documentation says smooth terms are added through the model formula and that smoothness is estimated during fitting. Keep smooth-spec construction separate from the fit wrapper so the chosen bases and tensor-product structure remain inspectable.
- Current `mgcv` documentation exposes `s()`, `te()`, `ti()`, and `t2()` as different smooth-building surfaces. Preserve those design choices in helper metadata instead of flattening every nonlinear term into one generic label.
- Current `mgcv::bam()` documentation positions `bam()` as the large-data GAM path. Keep `gam()` and `bam()` as distinct fit surfaces so memory, threading, and discretization choices remain visible.
- Current `predict.gam()` documentation keeps `type`, `se.fit`, and new-data prediction surfaces explicit. Keep prediction adapters separate from fit wrappers so downstream tables and plots can request link-scale, response-scale, or term-level outputs deliberately.
- Current `summary.gam()`, `gam.check()`, and `concurvity()` documentation expose separate summary and diagnostic surfaces. Keep smooth-term significance summaries, basis diagnostics, and concurvity checks on separate adapters instead of returning one overloaded fit summary.
- Team doctrine: split nonlinear helper stacks into smooth-spec builder, fit wrapper, prediction adapter, diagnostic adapter, and plotting adapter layers.

### 8k. Keep deployment-ready surfaces separate from training surfaces

- Current `vetiver_model()` documentation says a deployable object can carry a description, metadata, versioning posture, and an input data prototype. Keep the deployment wrapper separate from the fit helper so callers can tell when a model has crossed into a serving contract.
- Current `vetiver_pin_write()` documentation says deployable model objects can be written to a board and later read back at a specific version. Keep board choice and version lookup explicit so deployments are reproducible.
- Current `vetiver_api()` documentation says a POST prediction endpoint is added to a Plumber router with an explicit `path` and `check_prototype` behavior. Keep router assembly separate from fitting and pinning helpers.
- Current vetiver reference documentation lists `vetiver_endpoint()` plus `predict(<vetiver_endpoint>)` and `augment(<vetiver_endpoint>)` as the remote-client surface. Keep remote scoring helpers separate from local-fit helpers so the scoring boundary stays inspectable.
- Team doctrine: keep training helper, deployable `vetiver_model()` object, artifact pinning helper, router builder, and remote client as distinct layers whenever a model may be served.

### 9. Support custom estimands cleanly

For estimands that do not map cleanly to a model class, create a custom tidied coefficient table and pass it through `tbl_regression(tidy_fun = ...)` or a custom tibble-based reporting layer, depending on the shape of the result.

## Coordination notes

- Reach for `/r-eda` when the real work is building or refreshing the Arrow/Parquet working layer upstream of the modeling helper.
- Reach for `/r-package-dev` when the modeling helper lives inside an R package and `usethis`, `testthat`, or package release surfaces matter.
- Reach for `/r-stats` when the main uncertainty is method choice, missing-data strategy, or post-estimation doctrine rather than helper implementation.
- Reach for `/r-tables-reporting` when the main task is formatting adjusted predictions or marginal-effects output for publication.

## Resources

- Read `references/model-builder-patterns.md` for the evidence-backed family and reporting patterns.
- Read `references/arrow-parquet-model-builders.md` when model helpers must consume large or Parquet-backed analytical data without hiding the materialization boundary.
- Read `references/tidymodels-model-builders.md` when model helpers must expose `parsnip`, `recipes`, `workflows`, resampling, or tuned-workflow surfaces.
- Read `references/multiple-imputation-model-builders.md` when model helpers must wrap or consume `mice` workflows and pooled inferential output.
- Read `references/marginal-effects-model-builders.md` when model helpers must expose `marginaleffects`-based post-estimation output.
- Read `references/model-output-figures-and-interactivity.md` when model helpers must drive canonical plots, interactive model-output figures, or Shiny-facing post-estimation visualization surfaces.
- Read `references/specialized-clinical-endpoint-model-builders.md` when model helpers must support competing-risk/time-to-event or recurrent-event/longitudinal endpoint families.
- Read `references/survey-design-model-builders.md` when model helpers must own survey-design construction, domain restriction, weighted descriptives, or `svyglm()` fitting surfaces.
- Read `references/bayesian-model-builders.md` when model helpers must own `brms` fits, posterior draw extraction, `tidybayes` adapters, posterior predictive checks, or Bayesian model-comparison outputs.
- Read `references/causal-design-model-builders.md` when model helpers must own `MatchIt` or `WeightIt` design objects, balance diagnostics, trimming helpers, matched-data extraction, or weighted outcome-model surfaces.
- Read `references/meta-analysis-model-builders.md` when model helpers must own `metafor` effect-size construction, `rma.uni()` or `rma.mv()` fit wrappers, model-aware forest-plot adapters, or sensitivity-diagnostic helpers.
- Read `references/easystats-model-summary-adapters.md` when model helpers must expose reusable diagnostics, parameter tables, effect sizes, or report-ready easystats adapters.
- Read `references/gee-model-builders.md` when model helpers must own `geeglm()` or `geese()` fit wrappers, working-correlation comparison, cluster-ordering prep, or GEE reporting adapters.
- Read `references/lavaan-model-builders.md` when model helpers must own `lavaan` syntax builders, `cfa()`/`sem()`/`growth()` fit wrappers, fit-measure adapters, standardized-solution adapters, modification diagnostics, or latent-score outputs.
- Read `references/predictive-performance-model-builders.md` when model helpers must own probability extraction, ROC/AUC adapters, calibration adapters, threshold-performance helpers, or decision-curve evaluation surfaces.
- Read `references/bootstrap-and-permutation-adapters.md` when model helpers must own statistic functions, `boot`-object adapters, `rsample` bootstrap intervals, `infer` permutation workflows, or resampling-based uncertainty summaries.
- Read `references/gam-model-builders.md` when model helpers must own spline-spec builders, `gam()` or `bam()` fit wrappers, nonlinear prediction adapters, or GAM diagnostic and reporting surfaces.
- Read `references/vetiver-deployment-surfaces.md` when model helpers must create deployable artifacts, pinned model versions, prediction endpoints, or remote scoring surfaces.
