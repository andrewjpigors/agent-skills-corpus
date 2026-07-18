---
name: structural-io-research
description: Methodology guide for structural IO demand estimation research, with integrated humanizer for natural academic writing. Covers BLP, nested logit, GMM, IV, DiD, RDD, merger simulation, counterfactual analysis, and paper writing. Includes a 29-pattern anti-AI writing check adapted from the humanizer skill. Triggers on demand estimation, nested logit, Berry, BLP, GMM, IV, RDD, DiD, nesting structure, search costs, Monte Carlo, Hansen J, merger simulation, counterfactual, welfare, market definition, outside good, instruments, weak identification, bootstrap, pre-testing, replication, referee, writing, paper, humanize.
user-invocable: true
argument-hint: "topic or question"
---

# Structural IO Research Methodology Guide

Built from two things: learning the hard way on actual research projects, and reading the papers that would have saved time if read earlier. Covers BLP estimation, nested logit, instruments, causal inference, and how to write the paper without sounding like a chatbot. References include Conlon & Gortmaker (2020), Berry & Haile (2014), Gandhi & Houde (2020), Cattaneo et al. (2020/2024), Roth et al. (2023), and about 60 others.

---

## TABLE OF CONTENTS

1. BLP/Random Coefficients Demand Estimation Best Practices
2. Nested Logit Estimation Pitfalls
3. GMM Estimation for Nonlinear Models
4. Instrumental Variables in Demand Estimation
5. Monte Carlo Validation
6. Weak Instruments in Demand Estimation
7. Identification in Differentiated Products Markets
8. How to Write an Empirical IO Paper
9. Consumer Search Models Estimation
10. Difference-in-Differences Best Practices
11. Regression Discontinuity Design Best Practices
12. Market Definition in Demand Estimation
13. Outside Option and Market Size
14. Counterfactual Analysis and Merger Simulation
15. Nesting Structure Choice
16. Bootstrap Inference for GMM
17. Pre-Testing Bias and Specification Search
18. Replication, Transparency, and Credibility
19. What Referees Look For in IO Papers
20. Workflow Checklists
21. Writing Like a Human: Integrated Humanizer for IO Research

---

## 1. BLP/RANDOM COEFFICIENTS DEMAND ESTIMATION BEST PRACTICES

### Key Principle
BLP (Berry, Levinsohn & Pakes 1995) is the standard model for differentiated products demand. Most estimation problems trace to sloppy numerics, not deep econometric issues. Conlon & Gortmaker (2020) is the best practical reference.

### Do This
- **Use PyBLP** (Conlon & Gortmaker) as the reference implementation. It encodes best practices and is extensible.
- **Set tight contraction mapping tolerance:** Use 1e-14 for the inner loop (Berry inversion). Loose tolerances (1e-6 or worse) introduce numerical error that contaminates the GMM objective, creating spurious local optima. This is the single most important numerical recommendation.
- **Use enough simulation draws:** At minimum 1,000-2,000 Halton draws or scrambled Halton sequences. Pseudo-random draws require far more (10,000+). Sparse grids are an alternative.
- **Draw simulation shocks OUTSIDE the optimization loop.** Fix the draws once and reuse them across all evaluations. Drawing inside creates artificial noise in the objective.
- **Use a two-step procedure:** (1) Estimate with 2SLS weight matrix and differentiation IVs of Gandhi & Houde. (2) Compute feasible optimal instruments from step-1 estimates and re-estimate. This dramatically improves finite-sample performance.
- **Try multiple starting values** for the nonlinear parameters (sigma). Conlon & Gortmaker's Monte Carlo evidence suggests local optima are rare in well-identified problems, but verify by running from 5-10 random starts and checking convergence.
- **Include supply-side moments** when cost data or margins are available. Adding supply restrictions greatly sharpens identification of price coefficients and random coefficients.
- **Use a warm start** for the contraction mapping: initialize delta_t from the previous parameter guess rather than from scratch.

### Don't Do That
- **Don't use loose contraction tolerance.** This is the #1 source of computational problems in BLP. Knittel & Metaxoglou (2014) documented widespread problems from this.
- **Don't use too few simulation draws.** This introduces simulation bias that does not vanish with more data.
- **Don't over-parameterize random coefficients** relative to data richness. Too many RCs with limited data yields imprecise estimates. Focus on characteristics where heterogeneity materially affects substitution patterns.
- **Don't rely on pseudo-random draws.** Use quasi-random sequences (Halton, Sobol) for better coverage with fewer draws.
- **Don't ignore the gradient.** Supply analytic gradients to the optimizer. Numerical gradients are slow and less accurate. PyBLP provides analytic gradients.

### Key References
- Berry, S., Levinsohn, J. & Pakes, A. (1995). "Automobile Prices in Market Equilibrium." Econometrica.
- Conlon, C. & Gortmaker, J. (2020). "Best Practices for Differentiated Products Demand Estimation with PyBLP." RAND Journal of Economics, 51(4), 1108-1161.
- Nevo, A. (2000). "A Practitioner's Guide to Estimation of Random-Coefficients Logit Models of Demand." JEMS, 9(4), 513-548.
- Conlon, C. & Gortmaker, J. (2023). "Incorporating Micro Data into Differentiated Products Demand Estimation with PyBLP." NBER WP 31605.
- Knittel, C. & Metaxoglou, K. (2014). "Estimation of Random-Coefficient Demand Models: Two Empiricists' Perspective." Review of Economics and Statistics.

---

## 2. NESTED LOGIT ESTIMATION PITFALLS

### Key Principle
The nested logit is simple to estimate but easy to get wrong. Sigma must stay in [0,1], the nest structure matters more than people think, and the within-group share is endogenous even when prices are not.

### Do This
- **Check that the nesting parameter sigma (or 1-sigma, depending on parameterization) lies in [0,1].** Values outside this range violate random utility maximization (McFadden 1978). If your estimate hits 0, the model collapses to logit (no within-nest correlation). If it exceeds 1 or is negative, the nesting structure is likely wrong.
- **Treat the within-group share ln(s_j|g) as endogenous.** Even with exogenous prices, the within-group share depends on xi_j (unobserved product quality). Instrument for it with counts of competing products in the nest, characteristics of other products in the nest, etc.
- **Use the correct normalization.** The McFadden-consistent nested logit (NNNL vs. RU1 vs. RU2 forms) differs from alternative parameterizations. Using the wrong form changes coefficient interpretation and can produce incorrect welfare calculations. Use the RU1 (utility-maximizing) form.
- **Test multiple nesting structures.** Report results for at least 2-3 plausible nest definitions. If sigma is small (close to 0), the nesting choice matters little. If large, you must justify your choice carefully.
- **Use Berry's (1994) linear inversion** for estimation when possible: the nested logit admits a closed-form inversion ln(s_j) - ln(s_0) = x_j*beta - alpha*p_j + sigma*ln(s_j|g) + xi_j. This is a linear IV regression once you instrument for price and the within-group share.

### Don't Do That
- **Don't choose nests for convenience** (e.g., nesting by a variable that happens to be in the data). Nests should reflect substitution patterns: products in the same nest should be closer substitutes.
- **Don't ignore the endogeneity of the within-group share.** OLS on the Berry inversion equation produces biased sigma estimates because ln(s_j|g) is correlated with xi_j.
- **Don't use the non-normalized nested logit (NNNL)** without understanding how it differs from the McFadden model. The NNNL excludes the inverse logsum parameter from utility, producing dramatically different substitution patterns and welfare implications.
- **Don't assume that a passing Hansen J test validates your nest structure.** The J test checks moment validity, not nest correctness. A wrong nest structure with valid instruments can still pass.

### Key References
- Berry, S. (1994). "Estimating Discrete-Choice Models of Product Differentiation." RAND Journal of Economics.
- Cardell, N.S. (1997). "Variance Components Structures for the Extreme-Value and Logistic Distributions." Econometric Theory.
- McFadden, D. (1978). "Modeling the Choice of Residential Location." In Spatial Interaction Theory and Planning Models.
- Heiss, F. (2002). "Structural Choice Analysis with Nested Logit Models." Stata Journal.
- Train, K. (2009). Discrete Choice Methods with Simulation. Cambridge University Press. Ch. 4.

---

## 3. GMM ESTIMATION FOR NONLINEAR MODELS

### Key Principle
Nonlinear GMM looks scary because people worry about local optima. Conlon & Gortmaker (2020) show that with tight contraction tolerance, local optima are rare. Most "non-convexity" problems are really numerical sloppiness.

### Do This
- **Use the two-step efficient GMM procedure.** Step 1: estimate with the identity or 2SLS weight matrix. Step 2: update the weight matrix using step-1 residuals, then re-estimate. The continuously-updated GMM (CU-GMM) is an alternative but can be numerically less stable.
- **Supply analytic gradients and Hessians** to the optimizer whenever possible. This makes optimization faster and more reliable.
- **Use robust optimizers.** For BLP-type problems, quasi-Newton methods (L-BFGS) work well. For more difficult problems, consider hybrid approaches: start with a derivative-free method (Nelder-Mead) or grid search, then switch to a gradient-based method for refinement.
- **Run from multiple starting values** (5-10 minimum). If all converge to the same point (within numerical tolerance), you likely have the global minimum. Report the starting values and convergence diagnostics.
- **Monitor the GMM objective function value** across starting values. If different starts yield very different objective values, you have a non-convexity problem.
- **Use the Conlon & Gortmaker recommendation:** tight inner-loop tolerance (1e-14) eliminates most apparent non-convexity, which is actually numerical artifact from sloppy contraction mapping.

### Don't Do That
- **Don't use the efficient weight matrix in the first step.** The efficient weight matrix depends on consistent first-step estimates, which you don't have yet. Use identity or 2SLS weights first.
- **Don't declare convergence based on a single starting value.** This is the most common source of local-optima problems in applied work.
- **Don't use numerical gradients if analytic gradients are available.** Numerical gradients are O(k) times slower and introduce finite-difference error.
- **Don't blindly trust the Hansen J test in nonlinear settings.** Non-convexity can cause you to evaluate J at a local minimum that appears to "pass." Verify with multiple starts.
- **Don't use gradient descent** for BLP-type problems. It converges very slowly. Gauss-Newton or quasi-Newton methods are strongly preferred.

### Key References
- Hansen, L.P. (1982). "Large Sample Properties of Generalized Method of Moments Estimators." Econometrica.
- Newey, W. & McFadden, D. (1994). "Large Sample Estimation and Hypothesis Testing." Handbook of Econometrics, Vol. 4.
- Conlon, C. & Gortmaker, J. (2020). "Best Practices for Differentiated Products Demand Estimation with PyBLP." RAND Journal of Economics.
- Chernozhukov, V. & Hong, H. (2003). "An MCMC Approach to Classical Estimation." Journal of Econometrics.
- Dube, J.-P., Fox, J. & Su, C.-L. (2012). "Improving the Numerical Performance of Static and Dynamic Aggregate Discrete Choice Random Coefficients Demand Estimation." Econometrica.

---

## 4. INSTRUMENTAL VARIABLES IN DEMAND ESTIMATION

### Key Principle
Instruments matter more than anything else in demand estimation except maybe the model itself. Bad instruments produce bad estimates, and no amount of robustness checking can fix that. The field has moved from BLP-style sums of competitor characteristics to differentiation IVs (Gandhi & Houde 2020) to recentered instruments (Borusyak et al. 2025).

### Do This
- **Start with Differentiation IVs (Gandhi & Houde 2020).** These measure the distance between a product's characteristics and those of its competitors (e.g., |x_j - x_k| for each characteristic, summed over competitors). They substantially outperform traditional BLP instruments (sums of competitor characteristics) because they isolate the variation that matters for identification: how differentiated a product is from its rivals.
- **Compute optimal instruments in a second step** (Chamberlain 1987, Berry, Levinsohn & Pakes 1999). After a first-step estimate, compute the expected Jacobian of the moments with respect to parameters, and use these as instruments. Conlon & Gortmaker (2020) show this dramatically improves efficiency.
- **Include cost shifters when available.** Input prices, tariffs, exchange rates, and regulatory costs that shift marginal cost but do not directly affect demand are the gold standard. But they are often unavailable.
- **Consider Hausman instruments** (prices of the same product in other markets) when the identifying assumption is plausible: common cost shocks across markets but independent demand shocks. This fails if demand shocks are correlated across markets (e.g., national advertising).
- **Consider recentered instruments (Borusyak et al. 2025)** when you have exogenous supply-side shocks (cost shifters) but endogenous product characteristics. These construct model-predicted responses to cost shocks, recentered to remove bias from endogenous characteristics. They work even with product fixed effects.
- **Always report the effective first-stage F-statistic** (or Cragg-Donald statistic for multiple endogenous regressors). F < 10 signals weak instruments. For nonlinear models, the equivalent diagnostic is harder but essential.

### Don't Do That
- **Don't use sums of competitor characteristics as your only instruments** (the naive BLP instrument). Gandhi & Houde (2020) show these become weak as the number of products grows, because summing washes out the relevant variation in competitive proximity.
- **Don't ignore the endogeneity of within-group shares in nested logit.** The log within-group share ln(s_j|g) is endogenous and needs instrumenting, not just price.
- **Don't assume exogeneity of product characteristics without argument.** If firms choose characteristics in response to demand conditions, characteristics are endogenous. This is a serious concern in many settings.
- **Don't use weak instruments and hope for the best.** Weak instruments produce biased estimates, incorrect standard errors, and misleading J tests. If your instruments are weak, either find better ones or acknowledge the limitation explicitly.

### Key References
- Berry, S., Levinsohn, J. & Pakes, A. (1995). BLP instruments (original formulation).
- Gandhi, A. & Houde, J.-F. (2020). "Measuring Substitution Patterns in Differentiated Products Industries." NBER WP 26375.
- Borusyak, K., Hull, P. & Jaravel, X. (2025). "Estimating Demand with Recentered Instruments." arXiv:2504.04056.
- Chamberlain, G. (1987). "Asymptotic Efficiency in Estimation with Conditional Moment Restrictions." Journal of Econometrics.
- Reynaert, M. & Verboven, F. (2014). "Improving the Performance of Random Coefficients Demand Models." Journal of Econometrics.

---

## 5. MONTE CARLO VALIDATION

### Key Principle
Before trusting any structural estimate, simulate data where you know the truth and check that your estimator can recover it. This is not optional. If the estimator fails on simulated data, it will fail on real data too.

### Do This
1. **Fix true parameters** at values close to your real estimates (or at several different configurations to test sensitivity).
2. **Simulate data from the exact DGP** you assume in your model. Include the same: number of markets, products per market, endogeneity structure (e.g., price correlated with xi), instrument structure, and sample size.
3. **Estimate the model** using the exact same procedure (same instruments, same GMM weighting, same optimizer settings, same contraction tolerance).
4. **Repeat 200-500 times.** 200 is a minimum; 500 is better for precise coverage estimates.
5. **Report these:** (a) Mean bias of each parameter. (b) RMSE. (c) 95% CI coverage rate (should be near 0.95). (d) Median bias (more robust than mean to outliers from non-convergence). (e) Rejection rate of specification tests under the true model (should be near nominal size).
6. **Vary the DGP systematically:** test with different numbers of products, different instrument strength, different degrees of endogeneity. This reveals where your estimator breaks down.
7. **Present results in tables and histograms** showing the sampling distribution of each parameter estimate.

### Don't Do That
- **Don't use a DGP that is too simple** relative to your actual model. If your real model has 50 products per market and correlated heterogeneity, don't simulate with 5 products and iid errors.
- **Don't calibrate the MC to make your estimator look good.** Use realistic parameter values and sample sizes. Advani, Kitagawa & Sloczynski (2019) show that empirical Monte Carlo studies designed to select estimators are often worse than random at reducing bias.
- **Don't skip the MC because it's computationally expensive.** If you can't afford to run the MC, you likely can't afford to trust the estimates. Budget computation time for this.
- **Don't treat a single MC configuration as proof.** Test robustness of the MC findings to the DGP specification.

### Key References
- Conlon, C. & Gortmaker, J. (2020). Monte Carlo exercises in the PyBLP best practices paper.
- Advani, A., Kitagawa, T. & Sloczynski, T. (2019). "Mostly Harmless Simulations? Using Monte Carlo Studies for Estimator Selection." Journal of Applied Econometrics.
- Paxton, P., Curran, P., Bollen, K., Kirby, J. & Chen, F. (2001). "Monte Carlo Experiments: Design and Implementation." Structural Equation Modeling.

---

## 6. WEAK INSTRUMENTS IN DEMAND ESTIMATION

### Key Principle
Weak instruments mess up everything: biased point estimates, wrong confidence intervals, misleading specification tests. F > 10 is a rough screen, not a guarantee. With many instruments or heteroskedastic errors, you need more than just looking at F.

### Do This
- **Report the first-stage F-statistic** (or effective F for multiple endogenous regressors). Compare to Stock & Yogo (2005) critical values for your desired maximal bias (e.g., 10% relative bias of IV to OLS) or maximal size distortion (e.g., actual size of 10% when nominal is 5%).
- **Use the Anderson-Rubin (AR) test** for inference when instruments may be weak. AR confidence sets are valid regardless of instrument strength. They invert the test statistic H0: beta = beta_0 for each candidate value. The AR test is the most robust weak-instrument-robust procedure.
- **Use the tF procedure (Lee et al. 2022)** as a simple correction: adjust the t-statistic critical value based on the first-stage F. This is easy to implement and provides valid inference under weak instruments.
- **Improve instrument strength** before resorting to weak-instrument-robust inference. Switch from BLP instruments to differentiation IVs. Add supply-side moments. Use optimal instruments. These are more productive than statistical fixes.
- **For nonlinear GMM (BLP):** weak identification manifests as a flat GMM objective function. Diagnose by plotting the objective function along each parameter dimension. If flat, identification is weak for that parameter.
- **Consider the Olea & Pflueger (2013) effective F-statistic** for settings with heteroskedasticity and clustering, where the standard Cragg-Donald F may be misleading.

### Don't Do That
- **Don't rely solely on F > 10 as a pass/fail.** This is a rough screen, not a guarantee. With many instruments, the F can be high even when instruments are collectively weak. With heteroskedastic errors, the standard F is too optimistic.
- **Don't ignore weak instruments and report 2SLS standard errors.** If instruments are weak, 2SLS confidence intervals can have coverage far below 95%. The bias can be nearly as bad as OLS.
- **Don't add more (weak) instruments to boost the F-statistic.** Many weak instruments create their own bias problem (Bekker 1994). Quality matters more than quantity.
- **Don't confuse a high F-statistic with instrument validity (exogeneity).** F measures relevance only. You still need to argue for the exclusion restriction.

### Key References
- Stock, J. & Yogo, M. (2005). "Testing for Weak Instruments in Linear IV Regression." In Identification and Inference for Econometric Models.
- Anderson, T.W. & Rubin, H. (1949). "Estimation of the Parameters of a Single Equation in a Complete System of Stochastic Equations." Annals of Mathematical Statistics.
- Andrews, I., Stock, J. & Sun, L. (2019). "Weak Instruments in Instrumental Variables Regression: Theory and Practice." Annual Review of Economics.
- Olea, J.L.M. & Pflueger, C. (2013). "A Robust Test for Weak Instruments." Journal of Business & Economic Statistics.
- Lee, D., McCrary, J., Moreira, M. & Porter, J. (2022). "Valid t-Ratio Inference for IV." American Economic Review.

---

## 7. IDENTIFICATION IN DIFFERENTIATED PRODUCTS MARKETS

### Key Principle
Berry & Haile (2014) answer the question "what can you actually learn from market share data?" The answer: a lot, provided you have instruments and variation across markets. The Berry (1994) inversion maps observed shares to unique mean utilities -- that's where identification starts.

### Do This
- **Start from the Berry inversion.** Under mild regularity conditions, any vector of observed market shares is rationalized by a unique vector of mean utilities (delta). This is the first identification result and holds for any model in the BLP class.
- **Identify linear parameters (beta)** from the exclusion restriction: instruments Z are uncorrelated with the structural demand error xi. This is standard IV identification. The number of instruments must equal or exceed the number of endogenous variables.
- **Identify nonlinear parameters (sigma, random coefficients)** from cross-market variation in how shares respond to characteristics of competing products. A single market's shares cannot identify sigma because the inversion absorbs it. You need variation across markets with different product menus.
- **For the price coefficient (alpha):** identification requires instruments that shift price but not demand. Standard supply-side cost shifters or demand shifters in other markets.
- **For conduct parameters or marginal costs:** use supply-side first-order conditions combined with demand estimates. Berry & Haile (2014) show this is nonparametrically identified under exclusion restrictions (demand shifters excluded from cost).
- **Welfare and consumer surplus** are identified once the demand function is identified, without additional assumptions.

### Don't Do That
- **Don't confuse the inversion (computational) with identification (econometric).** The inversion tells you delta exists uniquely for any sigma. Identification tells you which sigma is the true one, and that requires instruments.
- **Don't think you can identify substitution patterns from a single cross-section of shares.** You need exogenous variation in the competitive environment (instruments, market variation).
- **Don't omit the discussion of identification from your paper.** Referees expect a clear statement of what identifies each parameter, what assumptions are needed, and how those assumptions are tested.

### Key References
- Berry, S. & Haile, P. (2014). "Identification in Differentiated Products Markets Using Market Level Data." Econometrica, 82(5), 1749-1797.
- Berry, S. & Haile, P. (2024). "Nonparametric Identification of Differentiated Products Demand Using Micro Data." Econometrica.
- Berry, S. (1994). "Estimating Discrete-Choice Models of Product Differentiation." RAND Journal of Economics.
- Berry, S. & Haile, P. (2021). "Foundations of Demand Estimation." NBER WP 29305. Handbook of Industrial Organization, Vol. 4.

---

## 8. HOW TO WRITE AN EMPIRICAL IO PAPER

### Key Principle
The structure of an IO paper is pretty standard. What separates publishable from unpublishable is whether the identification is credible and whether the economic question actually matters. Nobody cares about a technically perfect paper on a boring market.

### Paper Structure (following Bellemare 2020 and standard IO conventions)

**Title:** Brief, informative, under 15 words if possible. State the topic and sometimes the main finding.

**Abstract:** 4-5 sentences, ~150 words. Context, question, method, key result, contribution. Write last.

**Introduction (3-5 pages):**
1. Hook: Why should anyone care about this market/question? Policy relevance or economic significance.
2. Research question: One clear sentence.
3. What you do: Brief summary of model, data, and identification.
4. What you find: Main results in 2-3 sentences with magnitudes.
5. Contribution: How this advances on the existing literature. Be specific and honest.
6. Roadmap: Brief outline of paper sections.

**Institutional Background / Industry Description (1-3 pages):**
- Describe the market structure, key players, regulatory environment
- This is where IO papers differ from generic applied micro: the institutional detail matters for model specification

**Model (3-8 pages for structural papers):**
- Demand model: utility specification, distributional assumptions, timing
- Supply model: cost structure, conduct assumption, equilibrium concept
- Clearly state all assumptions and discuss which are testable

**Data (2-4 pages):**
- Sources, sample construction, variable definitions
- Summary statistics table(s)
- Market definition: justify carefully (see Section 12)
- Discuss data limitations honestly

**Estimation / Identification Strategy (3-5 pages):**
- Estimation method (GMM, MLE, 2SLS)
- Instruments: what they are, why they are valid (relevance AND exclusion)
- How you test the identifying assumptions (first-stage F, J test, placebo tests)

**Results (3-5 pages):**
- Main parameter estimates with standard errors
- Emphasize economic magnitudes, not just statistical significance
- Own-price elasticities, cross-price elasticities, markups
- Robustness checks

**Counterfactuals / Policy Exercises (3-5 pages for structural papers):**
- Merger simulation, welfare analysis, policy counterfactuals
- Discuss sensitivity of counterfactuals to model assumptions
- This is where structural IO earns its keep: reduced-form cannot do this

**Conclusion (1-2 pages):**
- Restate question and findings
- Policy implications
- Limitations and future directions
- No new results

### Do This
- **Lead with the economics, not the econometrics.** Referees want to know why the question matters before they see your model.
- **Make tables and figures self-contained.** A reader should understand each table without reading the text. Label everything clearly.
- **Report economic magnitudes:** elasticities, dollar values of welfare changes, percentage markup changes. Not just coefficients and t-statistics.
- **Discuss what drives your identification** in plain language before the formal model. The reader should understand the intuition.
- **Anticipate objections** and address them in robustness checks. Show that results survive alternative specifications, instruments, samples, and functional forms.

### Don't Do That
- **Don't bury the economic question under technical detail.** The most common referee complaint is "I don't understand what this paper contributes."
- **Don't present 50 robustness tables without a main result.** Have a clear baseline specification and test robustness to specific, motivated alternatives.
- **Don't oversell counterfactuals.** If your model is a nested logit, say so and acknowledge the restrictive substitution patterns. Don't claim you've perfectly predicted a merger outcome.
- **Don't hide unfavorable results.** Transparency builds credibility. If some specifications give different answers, discuss why.

### Key References
- Bellemare, M. (2020). "How to Write Applied Papers in Economics." Working paper (widely circulated).
- Levin, J. (2011). "Empirical Industrial Organization: A Progress Report." Journal of Economic Perspectives.
- Angrist, J. & Pischke, J.-S. (2010). "The Credibility Revolution in Empirical Economics." Journal of Economic Perspectives.

---

## 9. CONSUMER SEARCH MODELS ESTIMATION

### Key Principle
In search models, consumers don't see everything -- they pay a cost (time, clicks) to discover products. The hard part is telling apart "didn't search" from "searched and didn't like it." You usually can't observe search behavior directly, which makes identification tricky.

### Do This
- **Distinguish sequential vs. simultaneous search.** Sequential search (Weitzman 1979): consumers search one option at a time, stopping when the expected gain falls below the search cost. Simultaneous search (Stigler 1961): consumers choose how many options to sample upfront. The data requirements and identification differ.
- **Use search order data when available** (e.g., clickstream data, browsing sequences). Ursu (2018) exploits experimental variation in rankings on Expedia to identify position effects and search costs separately.
- **Account for position bias.** On platforms, items shown first are searched more, conditional on quality. Ursu (2018) finds average position effects of $1.92 per position on Expedia. Failing to account for this biases search cost estimates.
- **Use exclusion restrictions for identification.** Search cost shifters (variables that affect the cost of acquiring information but not preferences for the product) are the ideal instruments. Examples: page position, UI design changes, number of search results.
- **Pool data across markets** with common search technology but varying product characteristics to increase precision (Moraga-Gonzalez, Sandor & Wildenbeest 2013).
- **Be honest about weak identification of search-cost parameters.** If search-cost shifters hit boundary values or are imprecise, report this and show that core demand parameters are robust to the search specification.

### Don't Do That
- **Don't assume consumers observe all products.** In most online markets, the typical consumer sees a small fraction of available options. Ignoring search biases demand estimates.
- **Don't conflate position effects with preference effects.** A product appearing first gets more clicks, but this does not mean consumers prefer it. You need exogenous variation in position to separate these.
- **Don't over-parameterize the search cost distribution** relative to available data. The search cost distribution is often weakly identified. Start with a simple specification (homogeneous search costs, or a two-point distribution) and add complexity only if the data support it.

### Key References
- Moraga-Gonzalez, J.-L., Sandor, Z. & Wildenbeest, M. (2013). "Semi-Nonparametric Estimation of Consumer Search Costs." Journal of Applied Econometrics.
- Moraga-Gonzalez, J.-L., Sandor, Z. & Wildenbeest, M. (2023). "Consumer Search and Prices in the Automobile Market."
- Ursu, R. (2018). "The Power of Rankings: Quantifying the Effect of Rankings on Online Consumer Search and Purchase Decisions." Marketing Science.
- Ursu, R., Seiler, S. & Honka, E. (2023). "The Sequential Search Model: A Framework for Empirical Research." CESifo WP 10264.
- Dinerstein, M., Einav, L., Levin, J. & Sundaresan, N. (2018). "Consumer Price Search and Platform Design in Internet Commerce." American Economic Review.
- Weitzman, M. (1979). "Optimal Search for the Best Alternative." Econometrica.

---

## 10. DIFFERENCE-IN-DIFFERENCES BEST PRACTICES

### Key Principle
DiD changed a lot since 2019. The old two-way fixed effects estimator can be badly biased with staggered treatment and heterogeneous effects -- it uses already-treated units as controls, which makes no sense. Callaway & Sant'Anna (2021) and Sun & Abraham (2021) fix this. Read Baker et al. (2025) for the full picture.

### Do This
- **Start by diagnosing your TWFE:** Run the Goodman-Bacon (2021) decomposition to understand which 2x2 comparisons are driving the TWFE estimate. If already-treated units receive substantial weight as controls, the TWFE is likely biased.
- **Use a heterogeneity-robust estimator.** Callaway & Sant'Anna (2021) is the most widely used. It estimates group-time average treatment effects (ATT(g,t)) using only clean controls (never-treated or not-yet-treated units). Sun & Abraham (2021) provide an interaction-weighted estimator that is robust to heterogeneous effects.
- **Choose your control group carefully.** "Never-treated" units are safest if available. "Not-yet-treated" units expand the control group but assume that treatment does not affect outcomes before its onset (no anticipation). Document your choice and test sensitivity.
- **Test for pre-trends carefully but do not over-interpret.** Roth (2022) shows that failing to reject the null of parallel pre-trends does not validate the parallel trends assumption -- it may simply reflect low power. Roth et al. (2023) recommend also reporting sensitivity analyses (e.g., Rambachan & Roth 2023 honest confidence intervals) that allow for modest violations of parallel trends.
- **Report event study plots** with confidence intervals. Pre-treatment coefficients should be approximately zero. Post-treatment coefficients show the dynamic treatment effect.
- **Use proper inference:** cluster standard errors at the treatment unit level. With few clusters (<50), use wild cluster bootstrap (Cameron, Gelbach & Miller 2008).

### Don't Do That
- **Don't naively use TWFE with staggered treatment timing** without checking for heterogeneous effects. This is the single most important lesson from the modern DiD literature.
- **Don't test for pre-trends and then claim parallel trends is "validated."** The pre-trend test has low power. A non-significant pre-trend coefficient is consistent with both zero and substantial violations.
- **Don't use previously-treated units as controls.** This is the source of the "negative weight" problem in TWFE. Their outcomes reflect treatment effects, not counterfactual untreated outcomes.
- **Don't ignore anticipation effects.** If units change behavior before the official treatment date, the parallel trends assumption is violated.

### Key References
- Baker, A., Callaway, B., Cunningham, S., Goodman-Bacon, A. & Sant'Anna, P. (2025). "Difference-in-Differences Designs: A Practitioner's Guide." Forthcoming, Journal of Economic Literature.
- Callaway, B. & Sant'Anna, P. (2021). "Difference-in-Differences with Multiple Time Periods." Journal of Econometrics.
- Sun, L. & Abraham, S. (2021). "Estimating Dynamic Treatment Effects in Event Studies with Heterogeneous Treatment Effects." Journal of Econometrics.
- Goodman-Bacon, A. (2021). "Difference-in-Differences with Variation in Treatment Timing." Journal of Econometrics.
- Roth, J., Sant'Anna, P., Bilinski, A. & Poe, J. (2023). "What's Trending in Difference-in-Differences? A Synthesis of the Recent Econometrics Literature." Journal of Econometrics.
- de Chaisemartin, C. & D'Haultfoeuille, X. (2020). "Two-Way Fixed Effects Estimators with Heterogeneous Treatment Effects." American Economic Review.
- Rambachan, A. & Roth, J. (2023). "A More Credible Approach to Parallel Trends." Review of Economic Studies.

---

## 11. REGRESSION DISCONTINUITY DESIGN BEST PRACTICES

### Key Principle
RDD uses a cutoff in a running variable to estimate treatment effects right at the threshold. It only tells you what happens at the cutoff, not away from it. Main references: Cattaneo, Idrobo & Titiunik (2020, 2024). Main threats: people gaming the cutoff, and fitting the wrong functional form.

### Do This
- **Always show the RDD plot.** Binned scatter plot of the outcome vs. the running variable, with fitted local polynomial curves on each side of the cutoff. The visual should make the treatment effect (or lack thereof) obvious.
- **Use local polynomial estimation** (Calonico, Cattaneo & Titiunik 2014) rather than global polynomial fits. Global polynomials (high-order) are sensitive to data far from the cutoff and can generate spurious effects.
- **Use MSE-optimal bandwidth selection** (Calonico, Cattaneo & Titiunik 2014 -- the CCT method). This balances bias and variance optimally. Then use **robust bias-corrected (RBC) inference** for confidence intervals, because the MSE-optimal bandwidth is by construction invalid for standard inference.
- **Test for manipulation** of the running variable using the density test of Cattaneo, Jansson & Ma (2020) -- implemented in the rddensity package. If agents can precisely manipulate the running variable to be just above or below the cutoff, the RDD is invalid.
- **Run placebo tests:** (a) Test for discontinuities in pre-determined covariates at the cutoff (there should be none). (b) Test for effects at placebo cutoffs away from the true cutoff (there should be no effect).
- **Show robustness to bandwidth choice.** Present results for the MSE-optimal bandwidth and for bandwidths 50% and 200% of optimal. If the effect is sensitive to bandwidth, the result is fragile.
- **For Fuzzy RDD:** when the cutoff induces a jump in treatment probability (not a sharp change from 0 to 1), use the ratio of the jump in the outcome to the jump in treatment probability. This is a local Wald estimator.

### Don't Do That
- **Don't use global high-order polynomials** (e.g., 4th or 5th order on the full sample). Gelman & Imbens (2019) show these are unreliable: sensitive to data far from the cutoff and capable of generating spurious discontinuities.
- **Don't skip the manipulation test.** If agents sort precisely around the cutoff, the whole design is invalid.
- **Don't extrapolate.** RDD identifies effects only at the cutoff. Do not claim the effect applies far from the threshold.
- **Don't use arbitrary bandwidth choices.** Always use data-driven bandwidth selection (CCT or IK) and show sensitivity.
- **Don't forget to test for covariate balance at the cutoff.** Discontinuities in covariates suggest manipulation or confounding.

### Key References
- Cattaneo, M., Idrobo, N. & Titiunik, R. (2020). "A Practical Introduction to Regression Discontinuity Designs: Foundations." Cambridge Elements.
- Cattaneo, M., Idrobo, N. & Titiunik, R. (2024). "A Practical Introduction to Regression Discontinuity Designs: Extensions." Cambridge Elements.
- Calonico, S., Cattaneo, M. & Titiunik, R. (2014). "Robust Nonparametric Confidence Intervals for Regression-Discontinuity Designs." Econometrica.
- Cattaneo, M., Jansson, M. & Ma, X. (2020). "Simple Local Polynomial Density Estimators." JASA.
- Gelman, A. & Imbens, G. (2019). "Why High-Order Polynomials Should Not Be Used in Regression Discontinuity Designs." JBES.
- Lee, D. & Lemieux, T. (2010). "Regression Discontinuity Designs in Economics." Journal of Economic Literature.
- Software: rdrobust, rddensity, rdlocrand packages (R/Stata/Python) at rdpackages.github.io.

---

## 12. MARKET DEFINITION IN DEMAND ESTIMATION

### Key Principle
Market definition decides which products are in the choice set and how big the total market is. Get it wrong and your elasticities, substitution patterns, and welfare numbers are all off. Most people don't think about this enough.

### Do This
- **Define markets based on economic substitutability,** not data convenience. Products are in the same market if consumers view them as substitutes. The Hypothetical Monopolist Test (SSNIP test -- Small but Significant Non-transitory Increase in Price) from antitrust provides the conceptual framework: could a monopolist of the candidate market profitably raise price by 5-10%?
- **Be explicit about geographic and temporal market boundaries.** A "market" typically has a geographic scope (city, state, national) and a time period (week, month, quarter). Justify both.
- **Consider the product space carefully.** In BLP-type models, the set of products J in market t determines the choice set. Including too many irrelevant products adds noise; excluding close substitutes biases elasticities.
- **Report sensitivity to market definition.** Estimate with broader and narrower product sets and show that results are robust (or discuss why they change).
- **When in doubt, err on the side of a broader market** and let the substitution parameters sort out which products actually compete. The BLP model's strength is that it estimates flexible substitution patterns within the defined market.

### Don't Do That
- **Don't define markets based on SIC/NAICS codes alone.** These are administrative classifications, not economic market definitions. Two products with different SIC codes can be close substitutes.
- **Don't use price correlations to define markets.** FTC research (Werden & Froeb) shows price correlations contain little information about substitutability and can mislead.
- **Don't ignore the market definition choice.** Many papers present estimates as if the market definition is obvious. Acknowledge it as an assumption and test sensitivity.

### Key References
- DOJ/FTC Horizontal Merger Guidelines (2023 revision). Section on Market Definition.
- Werden, G. (1993). "Market Delineation Under the Merger Guidelines: Monopoly Cases and Alternative Approaches."
- Berry, S. & Haile, P. (2014). Discusses identification given a market definition.
- Bresnahan, T. (1989). "Empirical Studies of Industries with Market Power." Handbook of IO.

---

## 13. OUTSIDE OPTION AND MARKET SIZE

### Key Principle
The outside option (not buying anything) anchors the whole demand model. How big you assume the total market is determines the outside share, which in turn determines every elasticity and welfare number. Bugni & Ura (2025) checked: 24 of 29 BLP papers in top journals use an ad hoc market size, and only 5 test sensitivity. That's a problem.

### Do This
- **Think carefully about what the outside option represents.** For cereals, it might be not eating cereal (or eating oatmeal, toast, etc.). For cars, it might be not buying a car (using public transit, keeping the old car).
- **Justify your market size assumption.** Common approaches: (a) Total population in the geographic market. (b) Total category sales from a broader data source. (c) Number of potential buyers (e.g., households for consumer products). Document the source and reasoning.
- **Test sensitivity to market size.** Vary the assumed market size by +/- 50% and re-estimate. If your key results (elasticities, counterfactuals) are sensitive to this choice, you have a problem. Report this sensitivity analysis.
- **Consider partial identification** when the outside good share is genuinely unknown. Bugni & Ura (2025) derive sharp identified sets for structural parameters when market size is not observed, and show that informative bounds on elasticities, markups, and diversion ratios are often achievable without pinning down market size exactly.
- **If using the standard normalization** (u_i0 = epsilon_i0), understand that all utility parameters are measured relative to the outside option. A large outside option share means most consumers prefer not buying, which affects the level and slope of demand.

### Don't Do That
- **Don't set market size = observed total sales** (i.e., assuming no outside option). This drives the outside good share to zero, producing infinite own-price elasticities at the logit level and nonsensical substitution patterns.
- **Don't set market size to an arbitrary multiple of inside sales** without justification. Using 2x or 5x observed sales is common but ad hoc.
- **Don't assume the outside option is irrelevant to your results.** It affects every elasticity and counterfactual through the denominator of the logit share formula.
- **Don't hide the market size assumption in a footnote.** It should be prominently stated, justified, and sensitivity-tested.

### Key References
- Bugni, F. & Ura, T. (2025). "Demand Estimation Without Outside Good Shares." arXiv:2602.19154.
- Berry, S., Levinsohn, J. & Pakes, A. (1995). Original BLP framework with outside good normalization.
- Nevo, A. (2001). "Measuring Market Power in the Ready-to-Eat Cereal Industry." Econometrica. (Uses population-based market size.)

---

## 14. COUNTERFACTUAL ANALYSIS AND MERGER SIMULATION

### Key Principle
The whole point of structural estimation is that you can run counterfactuals: what happens if two firms merge? What if a product exits? What's the welfare effect of a price change? But the counterfactuals are only as good as the model. Change the demand specification a little and the merger prediction can flip sign.

### Do This
- **Solve for the new equilibrium** after the counterfactual change (e.g., merger changes the ownership matrix, causing internalization of cross-price effects). Do not just compute partial effects holding other prices fixed.
- **Report counterfactual sensitivity.** Show how predictions change under: (a) different demand specifications (logit vs. nested logit vs. random coefficients), (b) different conduct assumptions (Bertrand vs. Cournot), (c) different cost specifications, (d) different market size assumptions.
- **Compute welfare measures** (compensating variation, consumer surplus change) when relevant. For discrete choice models, the log-sum formula (Small & Rosen 1981) provides exact welfare calculations under logit.
- **Validate counterfactual predictions** when possible. Head & Mayer (2026) compare IO-style merger simulations with trade-style CES models and find that for aggregate outcomes, incorporating non-unitary pass-through matters more than fixing over-simplified substitution patterns.
- **Be transparent about what is held fixed** in the counterfactual. Standard merger simulation holds fixed: product characteristics, the set of products, demand shocks, cost functions. If any of these would plausibly change post-merger (e.g., product repositioning, cost synergies), discuss the implications.

### Don't Do That
- **Don't treat counterfactual predictions as precise forecasts.** They are conditional on the model being correctly specified. Present ranges or sensitivity analyses, not point predictions.
- **Don't use logit for merger simulation** if your market has many products with diverse characteristics. The logit's IIA property produces unrealistic substitution patterns: the merged firm's customers are predicted to substitute proportionally to all competitors' market shares, regardless of product similarity.
- **Don't assume zero cost synergies** (or any specific synergy level) without justification. The welfare effects of a merger depend critically on whether and how costs change.
- **Don't ignore entry/exit responses.** Standard short-run merger simulation holds the product set fixed. In the long run, competitors may enter or reposition.

### Key References
- Nevo, A. (2000). "Mergers with Differentiated Products: The Case of the Ready-to-Eat Cereal Industry." RAND Journal of Economics.
- Werden, G. & Froeb, L. (1994). "The Effects of Mergers in Differentiated Products Industries: Logit Demand and Merger Policy." Journal of Law, Economics, and Organization.
- Small, K. & Rosen, H. (1981). "Applied Welfare Economics with Discrete Choice Models." Econometrica.
- Head, K. & Mayer, T. (2026). "Poor Substitutes? Counterfactual Methods in IO and Trade Compared." Review of Economics and Statistics.
- Miller, N. & Weinberg, M. (2017). "Understanding the Price Effects of the MillerCoors Joint Venture." Econometrica.

---

## 15. NESTING STRUCTURE CHOICE

### Key Principle
Which products go in which nest is a choice you have to make, and getting it wrong biases everything (Fosgerau et al. 2024). For a long time there was no systematic way to pick nests. Almagro et al. (2025) now offer a data-driven approach: cluster products by their demand patterns and let the data decide.

### Do This
- **Motivate nests economically.** Products in the same nest should be closer substitutes than products in different nests. Ask: "When a consumer switches away from product A, which products do they switch to?" Those products should be in the same nest.
- **Consider data-driven nests (Almagro & Ciscato 2025).** Two-step approach: (1) Use clustering methods (k-means on demand response patterns) to classify products into nests. (2) Estimate the structural model conditional on the discovered nests. This uses the panel structure of consumer choice data.
- **Test multiple nesting structures.** Estimate with at least 2-3 alternative nest definitions and compare: (a) economic plausibility, (b) fit (log-likelihood or GMM objective), (c) stability of key parameters across specifications.
- **Validate nests with exogenous shocks** when possible. If a shock removes a product, do within-nest substitutes gain more share than cross-nest substitutes? (Almagro et al. use the Bud Light boycott for this.)
- **If sigma is small (close to 0), nests matter less.** The model approaches logit regardless of nest structure. But report the comparison anyway.
- **Consider the Generalized Nested Logit (GNL)** of Wen & Koppelman (2001) or Fosgerau & de Palma (2016) if products might belong to multiple nests. The GNL allows partial nest membership and more flexible substitution.

### Don't Do That
- **Don't choose nests by maximizing fit** alone. This is a form of specification search that invalidates inference (see Section 17 on pre-testing bias).
- **Don't assume the "obvious" nest structure is correct.** In our Hugging Face research, nesting by license type seemed natural but produced economically small sigma (0.046), suggesting license may not be the main dimension of substitution.
- **Don't ignore the Fosgerau, Monardo & De Palma (2024) warning:** misspecified nests create bias in ALL parameters, not just sigma. The bias can be substantial and is not detectable from the data alone.

### Key References
- Almagro, M. & Ciscato, E. (2025). "Data-Driven Nests." Working paper.
- Fosgerau, M., Monardo, J. & de Palma, A. (2024). Misspecification bias from wrong nests.
- McFadden, D. (1978). Nested logit original formulation.
- Wen, C.-H. & Koppelman, F. (2001). "The Generalized Nested Logit Model." Transportation Research B.
- Train, K. (2009). Discrete Choice Methods with Simulation. Ch. 4.

---

## 16. BOOTSTRAP INFERENCE FOR GMM

### Key Principle
Asymptotic standard errors from nonlinear GMM can be way off in finite samples. The bootstrap gives you a better sense of the actual sampling distribution, but you have to do it right -- resample at the cluster level, not individual observations.

### Do This
- **Resample at the cluster level** (market-time period, not individual observations) to preserve the within-cluster correlation structure. If your data has markets as the unit of analysis, resample markets with replacement.
- **Re-estimate the full model for each bootstrap draw.** No shortcuts: each draw must go through the complete estimation procedure (contraction mapping, optimization, etc.).
- **Use at least 200 draws** for standard errors and percentile confidence intervals. Use 500+ for bias-corrected confidence intervals or if computational budget allows. For publication, 1000 is a safe target.
- **Report: bootstrap mean, bootstrap SE, percentile-based 95% CI** (2.5th and 97.5th percentiles). The percentile CI is preferred over the normal-approximation CI (estimate +/- 1.96*SE) because it accounts for asymmetry in the sampling distribution.
- **Check that the point estimate falls within the bootstrap distribution.** If it is in the tail, there may be a convergence or boundary problem.
- **For block bootstrap in time series settings:** use the moving block bootstrap (MBB) with block length proportional to T^(1/3). The block preserves temporal dependence within blocks.
- **Consider the wild bootstrap** for heteroskedasticity-robust inference with few clusters. The standard pairs bootstrap can be unreliable with fewer than ~30 clusters.

### Don't Do That
- **Don't resample individual observations** when the data has a panel or cluster structure. This destroys the within-cluster dependence and produces incorrect standard errors.
- **Don't use the bootstrap to "fix" a fundamentally unidentified parameter.** If the parameter hits a boundary in many bootstrap draws (e.g., search costs going to zero), this signals weak identification, not a standard error problem.
- **Don't report only asymptotic standard errors** for nonlinear structural models. At minimum, present bootstrap SEs alongside asymptotic ones. If they differ substantially, the asymptotic approximation is poor.
- **Don't ignore non-convergence in bootstrap draws.** If a substantial fraction of draws fail to converge, your model may be fragile. Report the fraction of successful draws and investigate the failures.

### Key References
- Hall, P. (1994). "Methodology and Theory for the Bootstrap." Handbook of Econometrics.
- Cameron, A.C., Gelbach, J. & Miller, D. (2008). "Bootstrap-Based Improvements for Inference with Clustered Errors." Review of Economics and Statistics.
- Horowitz, J. (2001). "The Bootstrap." Handbook of Econometrics, Vol. 5.
- Higgins, A. (2024). "Bootstrap Inference for Fixed-Effect Models." Econometrica.

---

## 17. PRE-TESTING BIAS AND SPECIFICATION SEARCH

### Key Principle
You use the data to pick the specification, then do inference pretending you knew the specification all along. The confidence intervals are wrong because they don't account for the search. Everyone does this; almost nobody adjusts for it.

### Do This
- **Pre-commit to your main specification** before looking at results. Ideally, write the estimation section (instruments, functional form, controls) before running the final analysis. If your project has a pre-analysis plan, follow it.
- **Separate exploration from confirmation.** Use a holdout sample or split-sample approach: explore specifications on one half, confirm on the other. Report both.
- **Report all specifications you estimated,** not just the one that gives the desired result. If you estimated 10 nesting structures and 3 instrument sets, the reader needs to see (at least summarized) all 30 combinations.
- **If you test whether to include a variable and then re-estimate:** the standard errors of the surviving model are wrong (too small). The actual uncertainty includes the model selection step. Use post-model-selection inference (Berk et al. 2013, Andrews et al. 2025) or honest confidence intervals that account for the search.
- **Apply the Armstrong, Kline & Sun (2025) framework** for adapting to potential misspecification. They propose shrinkage estimators that optimally trade off robustness and efficiency, and are valid even when the restricted model may be misspecified.

### Don't Do That
- **Don't try all 50 specifications and report only the one with a significant result.** This is p-hacking and produces false discoveries at a rate far above the nominal 5%.
- **Don't use the Hansen J test to select among specifications** and then report inference from the selected specification as if no selection occurred. The Hansen test does not dictate model choice.
- **Don't present your final specification as if it were your first and only attempt.** Referees are sophisticated and will be suspicious of a single specification with perfectly clean results.
- **Don't let the data tell you the "right" nest structure and then do inference as if you knew it all along.** If nests are data-driven (Almagro et al. 2025), the two-step procedure must account for first-step estimation error in the second step.

### Key References
- Leamer, E. (1983). "Let's Take the Con Out of Econometrics." American Economic Review.
- Armstrong, T.B., Kline, P. & Sun, L. (2025). "Adapting to Misspecification." Econometrica.
- Prallon, B. (2026). "How Robust Are Robustness Checks?" arXiv:2602.19384.
- Andrews, I., Kitagawa, T. & McCloskey, A. (2025). Sensitivity to model specification.

---

## 18. REPLICATION, TRANSPARENCY, AND CREDIBILITY

### Key Principle
A lot of published results don't replicate (Christensen & Miguel 2018). The fix is boring but effective: share your code, share your data, make it possible for someone else to reproduce your numbers in one afternoon.

### Do This
- **Share your code and data** (or synthetic/simulated data if the real data are proprietary). Top journals now require this. Make it possible for someone to replicate your results in one click.
- **Write replication-ready code.** Document all data cleaning steps, all parameter choices, and all random seeds. Use version control (git). Create a master script that runs everything from raw data to final tables.
- **Consider pre-registration** for natural experiment analyses (DiD, RDD). While less common for structural estimation, pre-registering the model specification and counterfactual exercises before seeing data is increasingly valued.
- **Use open-source tools when possible.** PyBLP is open-source and replicable. Proprietary Matlab code that depends on specific toolbox versions is a replication hazard.
- **Report exact standard error methods,** clustering levels, and any corrections applied. A surprising number of replication failures stem from undocumented standard error adjustments.
- **Archive your code and data** at the journal's repository or a platform like Zenodo/Dataverse at the time of submission.

### Don't Do That
- **Don't make replication contingent on contacting the authors.** If the code is available only "upon request," it is effectively unavailable.
- **Don't round or truncate results selectively.** Report the precision your estimation delivers, not the precision that makes results look clean.
- **Don't hide negative results.** If your model fits poorly for some subsamples or specifications, report this. Selective reporting undermines the entire literature.

### Key References
- Christensen, G. & Miguel, E. (2018). "Transparency, Reproducibility, and the Credibility of Economics Research." Journal of Economic Literature.
- Camerer, C. et al. (2016). "Evaluating Replicability of Laboratory Experiments in Economics." Science.
- Angrist, J. & Pischke, J.-S. (2010). "The Credibility Revolution in Empirical Economics." Journal of Economic Perspectives.

---

## 19. WHAT REFEREES LOOK FOR IN IO PAPERS

### Key Principle
Knowing what referees care about saves you from writing a paper that's dead on arrival. IO referees check four things: does the question matter, is the identification believable, is the execution clean, and does it teach us something we didn't already know.

### What Referees Evaluate (Berk 2015, Econometric Society Guidelines)

1. **Is the question important?** Does this market/question matter for policy, theory, or the profession? A technically perfect paper on an unimportant question will be rejected.

2. **Is the identification credible?** What is the source of exogenous variation? Are the instruments plausible? Are the identifying assumptions testable, and have they been tested? This is the make-or-break criterion for empirical IO papers.

3. **Is the model appropriate for the question?** Is the structural model rich enough to answer the economic question but not so complex that it is uninterpretable or unestimable? Does the model impose assumptions that are clearly counterfactual?

4. **Are the results robust?** Do key findings survive alternative specifications, instruments, samples, and functional forms? A result that depends on one specific instrument or one specific nesting structure is fragile.

5. **Are the counterfactuals informative?** For structural papers, the counterfactual exercises should teach us something beyond what reduced-form evidence already tells us. If the counterfactuals are obvious given the estimates, they add little.

6. **Is the paper well-written?** Can a referee understand the contribution from the introduction? Are tables and figures clear and self-contained? Is the paper the right length (not padded)?

### Do This
- **Frontload the contribution.** The referee decides in the first 5 pages whether the paper is worth careful reading. Make the question, contribution, and main result crystal clear.
- **Anticipate the "so what?" question.** For every result, the referee will ask: what do we learn from this that we didn't know before? Have an answer ready.
- **Compare honestly to the closest existing paper.** If someone has estimated demand for a similar market, explain precisely what is new: better data, better identification, new counterfactual, different economic question.
- **Respond constructively to referee reports.** Address every point, even minor ones. When you disagree, explain why respectfully and provide evidence.

### Don't Do That
- **Don't pad the paper with unnecessary robustness checks.** Focus on checks that address genuine concerns about identification or specification.
- **Don't oversell.** Claiming your paper "overturns" the conventional wisdom, when it really provides a modest extension, will alienate referees.
- **Don't submit to a journal above your paper's level.** This wastes referee time and delays your publication.

### Key References
- Berk, J. (2015). "Preparing a Referee Report: Guidelines and Perspectives." AEA Conference.
- Berk, J., Harvey, C. & Hirshleifer, D. (2017). "How to Write an Effective Referee Report and Improve the Scientific Review Process." Journal of Economic Perspectives.
- Econometric Society Reviewer Guidelines: https://www.econometricsociety.org/publications/econometrica/guidelines-referees

---

## 20. WORKFLOW CHECKLISTS

### A. Before Starting Estimation

- [ ] **Economic question clear?** Can you state in one sentence why this analysis matters?
- [ ] **Market definition justified?** Geographic, temporal, and product boundaries documented and sensitivity-tested?
- [ ] **Outside option defined?** Market size assumption documented with source? Sensitivity analysis planned?
- [ ] **Nesting structure motivated?** If using nested logit, nests reflect economic substitution patterns?
- [ ] **Data cleaned and documented?** Summary statistics, sample construction, and variable definitions complete?

### B. Estimation Phase

- [ ] **Monte Carlo validation complete?** Estimation strategy recovers known parameters on simulated data?
- [ ] **Instruments justified?** Both relevance (F > 10, preferably >> 10) and exclusion (economic argument) established?
- [ ] **Instrument quality established?** Using differentiation IVs or optimal instruments, not just BLP sums?
- [ ] **Contraction tolerance tight?** Using 1e-14 for BLP inner loop?
- [ ] **Sufficient simulation draws?** At least 1,000 Halton draws for BLP?
- [ ] **Multiple starting values?** At least 5-10 random starts with convergence comparison?
- [ ] **Two-step GMM implemented?** Optimal instruments computed in second step?
- [ ] **Supply side included?** If cost data available, adding supply moments?
- [ ] **Bootstrap implemented?** Market-level resampling with 200+ draws?

### C. Results and Counterfactuals

- [ ] **All specifications reported?** Not just the best-looking one?
- [ ] **Economic magnitudes emphasized?** Elasticities, dollar welfare changes, markup changes?
- [ ] **Counterfactual sensitivity shown?** Results under alternative demand specs, conduct assumptions, market sizes?
- [ ] **Plots provided?** RDD binned scatters, event study coefficients, elasticity distributions?
- [ ] **Robustness documented?** Alternative instruments, samples, functional forms, nesting structures?
- [ ] **Weakly identified parameters flagged?** Boundary hits in bootstrap reported honestly?

### D. Reduced-Form Complements (if applicable)

- [ ] **Natural experiment motivated economically?** Clear statement of what it identifies beyond the structural model?
- [ ] **DiD design validated?** Pre-trends tested (but not over-interpreted), heterogeneity-robust estimator used, proper inference?
- [ ] **RDD design validated?** Manipulation test, covariate balance, bandwidth sensitivity, RDD plot?
- [ ] **Event study plotted?** Pre-period flat, confidence intervals shown?
- [ ] **Test at multiple aggregation levels?** Cross-category, cross-market consistency checked?

### E. Paper and Replication

- [ ] **Introduction compelling?** Question, contribution, and main result in first 3 pages?
- [ ] **Identification clearly explained?** Source of variation, assumptions, and tests for each parameter?
- [ ] **Code and data packaged for replication?** Master script, documented, version-controlled?
- [ ] **Pre-testing bias avoided?** Specification not chosen to maximize significance?
- [ ] **Hansen J not dictating model choice?** Model compared on economic grounds, not just J statistic?

---

## 21. WRITING LIKE A HUMAN: INTEGRATED HUMANIZER FOR IO RESEARCH

This section integrates the [humanizer skill](https://github.com/shoal-rat/humanizer) into the IO research workflow. Academic economics writing has its own version of AI-slop: vague significance claims, padded prose, and mechanical structure. Good IO papers read like a person is thinking on the page, not like a template got filled in.

### When writing or editing any text for this research, apply the humanizer skill

The full humanizer rules (29 patterns to avoid) live in the companion skill at `~/.claude/skills/humanizer/SKILL.md`. Here is how they apply specifically to IO research writing:

### IO-Specific AI Writing Traps

**1. Inflated significance claims.** "This paper makes a pivotal contribution to our understanding of platform markets" -- no. Say what you found and let the reader decide if it matters. "We estimate that a 1% increase in trending score raises downloads by 13.4%" is the finding. The reader will see it's big.

**2. Mechanical structure signposting.** "The remainder of this paper is organized as follows. Section 2 reviews the related literature. Section 3 describes the institutional background." -- This is fine in a 50-page paper. In a 30-page paper it wastes half a page. Just write "Section 2 reviews related work" and move on. Or skip the roadmap entirely if the paper is short.

**3. Vague hedging that hides the ball.** "The results suggest that visibility may play a role in shaping demand outcomes" -- what does this mean? Say "Visibility is the strongest predictor of downloads. The elasticity is 13.4." If you're uncertain, say why you're uncertain, don't just hedge everything.

**4. Synonym cycling in variable descriptions.** "The trending score, which we also refer to as the visibility proxy, platform-assigned prominence metric, and algorithmic ranking signal..." -- pick one name and stick with it.

**5. Rule-of-three in contributions.** "This paper makes three contributions. First... Second... Third..." -- Three is fine if you genuinely have three contributions. But don't pad to reach three. Two is fine. Four is fine. The number doesn't matter.

**6. Copula avoidance.** "The market serves as an arena for competition" -- just say "The market is competitive." Use "is" and "has" freely. They're not weak verbs; they're clear ones.

**7. Formulaic robustness intros.** "We subject our results to a battery of robustness checks" -- don't announce the robustness checks, just do them. "Table 5 re-estimates with base-model nests instead of license nests" is better.

### The Anti-AI Audit for Research Papers

Before submitting any draft, run this two-step check (adapted from the humanizer skill):

**Step 1:** Read your abstract and introduction aloud. Ask: "Does this sound like a person talking to another economist at a seminar, or does it sound like a press release?" If the latter, rewrite.

**Step 2:** Search the document for these high-frequency AI words and replace or cut them:
- "delve" -> cut or replace with "examine" / "study"
- "crucial" / "pivotal" -> cut; if something is important, the reader will see it from the numbers
- "landscape" (abstract noun) -> cut entirely
- "tapestry" / "interplay" / "synergy" -> cut
- "underscores" / "highlights" -> "shows" or just state the fact
- "fosters" / "cultivates" -> say what actually happens
- "robust" (when describing your own results) -> show the robustness table and let the reader judge
- "comprehensive" / "holistic" -> almost always padding

**Step 3:** Check every sentence that starts with a participle (-ing). "Leveraging the exogenous variation from the reform, we estimate..." -> "We estimate ... using the reform as an exogenous shock." Active voice, subject first.

**Step 4:** Search for em dashes (--). Replace most with periods or commas. One or two per page is fine. Five per page is AI-coded.

**Step 5:** Do a final pass asking: "If I remove this sentence, does the paper lose anything?" If no, remove it.

### Voice for Economics

Economics papers should sound like one careful thinker explaining their work to another. Not promotional, not self-deprecating, not breathless.

Good models to imitate:
- Angrist & Pischke: casual but precise, every sentence earns its place
- Nevo (2000, 2001): clear notation, honest about limitations, no padding
- Dinerstein et al. (2018): clean structure, the economic question leads every section
- Berry & Haile (2014): technical but readable, no unnecessary hedging

Bad patterns to avoid:
- "This is the first paper to..." (probably not true, and referees will check)
- "Our results have important implications for policy" (show, don't tell)
- "In this rapidly evolving landscape..." (kill it)
- "The rest of this paper is structured as follows..." (usually unnecessary)

### Integration with humanizer skill

When generating or editing paper text, reports, or email drafts:
1. Write the content first using the IO methodology sections above
2. Then apply `/humanizer` to the output for a de-AI pass
3. The humanizer will catch patterns that the IO-specific rules above miss (emojis, bold overuse, sycophantic tone, etc.)

For the full 29-pattern humanizer reference, see the companion skill at `~/.claude/skills/humanizer/SKILL.md` or https://github.com/shoal-rat/humanizer

---

## COMPLETE REFERENCE LIST

### Core Demand Estimation
- Berry, S. (1994). "Estimating Discrete-Choice Models of Product Differentiation." RAND Journal of Economics.
- Berry, S., Levinsohn, J. & Pakes, A. (1995). "Automobile Prices in Market Equilibrium." Econometrica.
- Berry, S. & Haile, P. (2014). "Identification in Differentiated Products Markets Using Market Level Data." Econometrica.
- Berry, S. & Haile, P. (2021). "Foundations of Demand Estimation." NBER WP 29305 / Handbook of IO, Vol. 4.
- Berry, S. & Haile, P. (2024). "Nonparametric Identification of Differentiated Products Demand Using Micro Data." Econometrica.
- Nevo, A. (2000). "A Practitioner's Guide to Estimation of Random-Coefficients Logit Models of Demand." JEMS.
- Nevo, A. (2001). "Measuring Market Power in the Ready-to-Eat Cereal Industry." Econometrica.
- Conlon, C. & Gortmaker, J. (2020). "Best Practices for Differentiated Products Demand Estimation with PyBLP." RAND Journal of Economics.
- Conlon, C. & Gortmaker, J. (2023). "Incorporating Micro Data into Differentiated Products Demand Estimation with PyBLP." NBER WP 31605.

### Instruments
- Gandhi, A. & Houde, J.-F. (2020). "Measuring Substitution Patterns in Differentiated Products Industries." NBER WP 26375.
- Borusyak, K., Hull, P. & Jaravel, X. (2025). "Estimating Demand with Recentered Instruments." arXiv:2504.04056.
- Reynaert, M. & Verboven, F. (2014). "Improving the Performance of Random Coefficients Demand Models." Journal of Econometrics.
- Chamberlain, G. (1987). "Asymptotic Efficiency in Estimation with Conditional Moment Restrictions." Journal of Econometrics.

### Nested Logit and Nesting
- Cardell, N.S. (1997). "Variance Components Structures for the Extreme-Value and Logistic Distributions." Econometric Theory.
- McFadden, D. (1978). "Modeling the Choice of Residential Location." In Spatial Interaction Theory and Planning Models.
- Almagro, M. & Ciscato, E. (2025). "Data-Driven Nests." Working paper.
- Fosgerau, M., Monardo, J. & de Palma, A. (2024). Misspecification bias from wrong nests.
- Train, K. (2009). Discrete Choice Methods with Simulation. Cambridge University Press.

### GMM and Econometrics
- Hansen, L.P. (1982). "Large Sample Properties of Generalized Method of Moments Estimators." Econometrica.
- Newey, W. & McFadden, D. (1994). "Large Sample Estimation and Hypothesis Testing." Handbook of Econometrics.
- Dube, J.-P., Fox, J. & Su, C.-L. (2012). "Improving the Numerical Performance of BLP." Econometrica.
- Knittel, C. & Metaxoglou, K. (2014). "Estimation of Random-Coefficient Demand Models." Review of Economics and Statistics.

### Weak Instruments
- Stock, J. & Yogo, M. (2005). "Testing for Weak Instruments in Linear IV Regression."
- Anderson, T.W. & Rubin, H. (1949). "Estimation of the Parameters of a Single Equation."
- Andrews, I., Stock, J. & Sun, L. (2019). "Weak Instruments in IV Regression." Annual Review of Economics.
- Olea, J.L.M. & Pflueger, C. (2013). "A Robust Test for Weak Instruments." JBES.
- Lee, D., McCrary, J., Moreira, M. & Porter, J. (2022). "Valid t-Ratio Inference for IV." AER.

### Outside Good and Market Size
- Bugni, F. & Ura, T. (2025). "Demand Estimation Without Outside Good Shares." arXiv:2602.19154.

### Consumer Search
- Moraga-Gonzalez, J.-L., Sandor, Z. & Wildenbeest, M. (2013). "Semi-Nonparametric Estimation of Consumer Search Costs." JAE.
- Ursu, R. (2018). "The Power of Rankings." Marketing Science.
- Ursu, R., Seiler, S. & Honka, E. (2023). "The Sequential Search Model: A Framework for Empirical Research."
- Dinerstein, M., Einav, L., Levin, J. & Sundaresan, N. (2018). "Consumer Price Search and Platform Design." AER.
- Weitzman, M. (1979). "Optimal Search for the Best Alternative." Econometrica.

### Counterfactuals and Mergers
- Head, K. & Mayer, T. (2026). "Poor Substitutes? Counterfactual Methods in IO and Trade Compared." Review of Economics and Statistics.
- Small, K. & Rosen, H. (1981). "Applied Welfare Economics with Discrete Choice Models." Econometrica.
- Miller, N. & Weinberg, M. (2017). "Understanding the Price Effects of the MillerCoors Joint Venture." Econometrica.
- Werden, G. & Froeb, L. (1994). "The Effects of Mergers in Differentiated Products Industries." JLEO.

### Difference-in-Differences
- Baker, A., Callaway, B., Cunningham, S., Goodman-Bacon, A. & Sant'Anna, P. (2025). "DiD Designs: A Practitioner's Guide." JEL.
- Callaway, B. & Sant'Anna, P. (2021). "Difference-in-Differences with Multiple Time Periods." Journal of Econometrics.
- Sun, L. & Abraham, S. (2021). "Estimating Dynamic Treatment Effects in Event Studies." Journal of Econometrics.
- Goodman-Bacon, A. (2021). "Difference-in-Differences with Variation in Treatment Timing." Journal of Econometrics.
- Roth, J., Sant'Anna, P., Bilinski, A. & Poe, J. (2023). "What's Trending in Difference-in-Differences?" Journal of Econometrics.
- de Chaisemartin, C. & D'Haultfoeuille, X. (2020). "Two-Way Fixed Effects Estimators with Heterogeneous Treatment Effects." AER.
- Rambachan, A. & Roth, J. (2023). "A More Credible Approach to Parallel Trends." REStud.

### Regression Discontinuity
- Cattaneo, M., Idrobo, N. & Titiunik, R. (2020). "A Practical Introduction to RDD: Foundations." Cambridge Elements.
- Cattaneo, M., Idrobo, N. & Titiunik, R. (2024). "A Practical Introduction to RDD: Extensions." Cambridge Elements.
- Calonico, S., Cattaneo, M. & Titiunik, R. (2014). "Robust Nonparametric Confidence Intervals for RDD." Econometrica.
- Cattaneo, M., Jansson, M. & Ma, X. (2020). "Simple Local Polynomial Density Estimators." JASA.
- Gelman, A. & Imbens, G. (2019). "Why High-Order Polynomials Should Not Be Used in RDD." JBES.
- Lee, D. & Lemieux, T. (2010). "Regression Discontinuity Designs in Economics." JEL.

### Specification and Misspecification
- Armstrong, T.B., Kline, P. & Sun, L. (2025). "Adapting to Misspecification." Econometrica.
- Leamer, E. (1983). "Let's Take the Con Out of Econometrics." AER.

### Transparency and Replication
- Christensen, G. & Miguel, E. (2018). "Transparency, Reproducibility, and the Credibility of Economics Research." JEL.

### Writing and Refereeing
- Bellemare, M. (2020). "How to Write Applied Papers in Economics." Working paper.
- Berk, J., Harvey, C. & Hirshleifer, D. (2017). "How to Write an Effective Referee Report." JEP.
- Levin, J. (2011). "Empirical Industrial Organization: A Progress Report." JEP.

### Monte Carlo Methods
- Advani, A., Kitagawa, T. & Sloczynski, T. (2019). "Mostly Harmless Simulations?" JAE.
- Paxton, P. et al. (2001). "Monte Carlo Experiments: Design and Implementation." SEM.
- Koehler, E., Brown, E. & Haneuse, S. (2009). "On the Assessment of Monte Carlo Error in Simulation-Based Statistical Analyses." The American Statistician.

### Data-Driven Nests
- Almagro, M., Lai, K. & Manresa, E. (2025). "Data-Driven Nests." Working paper, Chicago Booth.
- Bonhomme, S. & Manresa, E. (2015). "Grouped Patterns of Heterogeneity in Panel Models." Econometrica.
- Fosgerau, M., Monardo, J. & de Palma, A. (2024). Misspecification bias from wrong nests.

---

## 21. LESSONS FROM PRACTICE: DATA-DRIVEN NESTING IN PLATFORM MARKETS

### Key Principle
When applying the Almagro et al. (2025) data-driven nesting approach to new settings, the requirement that matters most is that nest assignments must preserve the exclusion restriction for the instruments. In markets without time-varying exogenous product characteristics (like AI model platforms where the main "price" is an endogenous trending score), demand-side clustering violates instrument validity even though it produces descriptively interesting groups.

### Do This
- **Check corr(n_in_nest, outcome) before running structural estimation.** If popular products cluster into small nests and unpopular products into large nests, the count instruments will have the WRONG sign in the first stage. This correlation should be approximately zero.
- **Prefer supply-side-informed data-driven nests.** Instead of pure demand-side clustering, merge supply-side categories (e.g., license types, brand families) using demand-pattern similarity. This preserves the exclusion restriction while letting the data optimize the grouping.
- **Use enough nests for IV variation.** With K=4, n_in_nest barely varies. With K=48, there is rich variation. The sweet spot is typically K=8-15 for platforms with 50K+ products.
- **Compute nest-specific sigma_k.** A single sigma can hide substantial heterogeneity. Report sigma_k as a separate empirical finding about market segmentation.
- **Run the full pipeline for EVERY specification.** When comparing nesting structures, ensure all diagnostics are computed for each spec. Do not leave blank cells in comparison tables.
- **Validate with Monte Carlo FIRST (500+ reps per Paxton et al. 2001; 1,000 most common in published work).** Only after MC confirms the estimation strategy is sound should you compare specifications.
- **Do not use the Hansen J test to choose among nesting structures.** Use economic plausibility, placebo lead tests, parameter reasonableness (validated via MC), and parsimony.

### Don't Do That
- **Don't cluster on endogenous demand outcomes and then use count instruments.** Count instruments require supply-side nest definitions. Demand-side clustering creates negative corr(n_in_nest, log_dl), inverting the first stage.
- **Don't use too few nests (K=4-6) with count instruments on large markets.** Each nest will contain 10K-40K products, making n_in_nest nearly constant.
- **Don't assume the Almagro method works out-of-the-box in every setting.** It requires time-varying exogenous product characteristics for identification.

---

## 22. SUPERVISOR FEEDBACK PATTERNS AND HOW TO RESPOND

### Common Patterns

**"Ignore the Hansen J test."** Model selection should use economic reasoning, MC validation, placebo tests, and parsimony, not J. With millions of observations, J rejects any slightly misspecified model. In nonlinear GMM, J at a local minimum may not reflect global J.

**"Try running a Monte Carlo."** Non-negotiable for structural papers. Use 500+ reps (Paxton et al. 2001). Match the DGP to your real data structure. Report bias, RMSE, and CI coverage.

**"I don't understand what your natural experiment teaches us."** In a structural paper, the structural model already has a causal interpretation through IV. Frame the natural experiment as out-of-sample model validation and policy quantification, not as "proving causality."

**"What is [technical test]?"** If the supervisor doesn't understand it, neither will referees. Add 2-3 sentences of intuitive explanation right after introducing any test.

**"Run these tests at the [broader] level."** Test generalizability across subsamples. Present results in a single figure showing all subsamples together.

### The Completeness Principle
Every diagnostic should be computed for ALL specifications. Blank cells signal cherry-picking. If a test is not applicable, explain why in a footnote.

---

## 23. RESEARCH RIGOR RULES

### The Verification Principle
**Every number, method, threshold, and parameter choice must be grounded in published literature.** Before using any specific value (e.g., number of MC replications, bootstrap draws, bandwidth, significance level, number of nests), search the literature to find what authoritative sources recommend, then use the **strictest practicable** value:
- Monte Carlo replications: 1,000 (most common in published econometrics per Koehler et al. 2009; Paxton et al. 2001 recommend minimum 500; use 1,000 as the strict-but-practicable standard)
- Bootstrap draws: 200 minimum (Hall 1994; Cameron, Gelbach & Miller 2008), 500+ preferred
- RDD bandwidth: MSE-optimal via Calonico, Cattaneo & Titiunik (2014), not arbitrary
- BLP contraction tolerance: 1e-14 (Conlon & Gortmaker 2020)
- Simulation draws for BLP: 1,000-2,000 Halton minimum (Conlon & Gortmaker 2020)
- Number of starting values for nonlinear GMM: 5-10 minimum
- Pre-trend test: do NOT over-interpret (Roth 2022; Rambachan & Roth 2023)

**Do not guess or use round numbers without justification.** If you choose N=100, you must cite why 100 is sufficient. If the literature says 1,000, use 1,000.

### The Universality Principle
**When you introduce a new test, diagnostic, parameter, or analysis, it must be applied to ALL specifications/models/subsamples in the paper.** Concretely:
- If you add a placebo lead test → run it for License NL, Base-Model NL, Data-Driven NL, and No-Search. Report all results.
- If you add a Monte Carlo study → calibrate the DGP to match each major specification (or at minimum the preferred spec and document why).
- If you add pipeline-level RDD → run for all pipeline types, not just text-to-image.
- If you compute nest-specific sigma_k → compute for all nesting structures that have nests (License, Base-Model, Data-Driven). Note that No-Search has sigma=0 and explain why sigma_k is not applicable.
- If you add a causal analysis (DiD, event study, placebo) → run under every specification where the outcome data is available.

**The logic:** A referee seeing sigma_k reported for one nesting but not another will ask "why?" If the answer is "we didn't compute it," that signals incomplete analysis. If the answer is "it's not applicable because sigma=0," say so explicitly.

### The Iteration Principle
**When iterating on a method (e.g., data-driven nesting v1→v2→v3→v4), document the full iteration log.** Each failed version teaches something. Report:
1. What you tried
2. What went wrong (specific diagnostic: sigma hit boundary, correlation was negative, etc.)
3. What theoretical insight led to the fix
4. The final working version and why it works

This is not just for transparency — it demonstrates deep understanding of the method and its assumptions. Referees and supervisors value this.
