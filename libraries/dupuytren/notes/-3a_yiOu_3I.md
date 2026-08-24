---
id: -3a_yiOu_3I
title: "Guido Dolmans MD, \"A First Genome-Wide Association Study in Dupuytren's Disease\" 2010 Miami Dupuytren Symposium"
url: https://www.youtube.com/watch?v=-3a_yiOu_3I
upload_date: 2010-10-16
duration: "13:42"
subjects:
  - how a GWAS works, explained from first principles (SNPs, genotyping chips, linkage disequilibrium)
  - the multiple-testing problem and why genome-wide significance thresholds are so strict
  - the actual preliminary results — two significant loci, with odds ratios
  - the multicenter Dutch study design, including its well-matched biobank control group
management: []
anatomy: []
concepts:
  - genome-wide association study (GWAS) methodology
  - single nucleotide polymorphism (SNP)
  - linkage disequilibrium (correlated markers)
  - the Manhattan plot and QQ plot as GWAS result visualizations
  - odds ratio as a measure of a genetic marker's disease-risk effect
---

# Guido Dolmans MD, "A First Genome-Wide Association Study in Dupuytren's Disease" 2010 Miami Dupuytren Symposium

## Central claim

**This talk presents what appears to be the original, preliminary results of the genome-wide association
study later cited elsewhere in this library as identifying nine Dupuytren's susceptibility loci** — here,
still in progress, with **two highly significant chromosomal regions already identified: chromosome 7 and
chromosome 22.** Dolmans states the top chromosome 7 marker's significance directly: **a P-value of "10 to
the power of minus 15"** and **an odds ratio of "1.8, 1.9"** — meaning **"if you have this marker, you have
90% more chance of developing the disease"** `[11:20]`–`[12:23]`.

## Why GWAS, not family linkage studies

`[01:02]`–`[02:04]` — Dolmans distinguishes two research approaches by what kind of disease they're suited
to: **Mendelian disease** running in families, driven by **rare, high-effect mutations**, studied via
linkage analysis; versus **sporadic, non-familial disease**, potentially driven by **common genetic
variants** that everyone carries some combination of, studied via **genome-wide association studies (GWAS)**
— the approach chosen here specifically to study **non-familial (sporadic) Dupuytren's cases.**

## How a GWAS actually works

`[02:04]`–`[07:13]` — Explained step by step: a **SNP (single nucleotide polymorphism)** is a single-base-
pair variant at a specific genome location; genotyping hundreds of thousands of these across an individual
produces a genetic "fingerprint." A **case-control design** compares allele frequencies at each marker
between affected and unaffected people — a marker allele that's meaningfully more common in cases than
controls suggests a disease gene lies near that location. Results are visualized across all chromosomes to
find the markers with the strongest association signal. Two technical points Dolmans is careful to explain:

- **Multiple testing**: testing hundreds of thousands of markers across thousands of people means chance
  alone can produce a seemingly striking result (he gives the example of a P-value of 10⁻⁵ arising by chance)
  — so **the genome-wide significance threshold used is far stricter, at P < 10⁻⁸**, and any finding still
  requires **replication in an independent cohort** before being trusted.
- **Linkage disequilibrium**: you don't need to directly test all ~3 billion base pairs, because nearby
  markers are statistically correlated — testing ~300,000 well-chosen markers captures information about
  many more untested ones nearby. This also means a *significant* marker on the chip may not itself be the
  causal variant — it may simply be correlated with a nearby causal variant that isn't directly on the chip,
  requiring the whole surrounding region to be studied further.

## The study design

`[07:13]`–`[09:19]` — A **multicenter study across six major hospitals in the Netherlands**, recruiting every
Dupuytren's patient presenting to participating clinics, collecting blood, DNA, and questionnaires. At the
time of the talk: **864 cases analyzed, with 960 in progress.** The control group came from a **large,
same-region biobank** already tracking thousands of individuals prospectively for roughly 30 years for
unrelated epidemiological research — chosen specifically because these controls were genotyped **"with
exactly the same chip, in exactly the same lab"** as the cases, and drawn from the same geographic
population (northern Netherlands), minimizing population-structure confounds. Standard quality-control
steps are named: correcting genotyping errors, checking for ethnic outliers, and checking for undisclosed
relatives among participants, all before the case-control statistical comparison (a chi-squared test of
allele frequencies).

## The results

`[09:19]`–`[12:23]` — A **QQ plot** is used to show the observed association signal diverges meaningfully
from what chance alone would produce, before the **Manhattan plot** (his aside: "you could also call it the
Miami plot," a joke given the conference location) shows two regions clearing the strict genome-wide
significance threshold: **chromosome 7** and **chromosome 22**, each represented by multiple correlated
markers clustering at the same genomic position. The top chromosome 7 SNP reaches **P = 10⁻¹⁵** with an
**odds ratio around 1.8–1.9**; additional markers on both chromosomes showed somewhat lower but still
significant effect sizes (one example given at 1.6).

## Symptoms and body signals addressed

None directly — this is a genetics-methodology and results talk, not a discussion of clinical presentation.

## Glossary terms introduced

- **SNP (single nucleotide polymorphism)** — a single-base-pair genetic variant, the marker type used
  throughout GWAS genotyping `[02:04]`.
- **Genome-wide significance threshold (P < 10⁻⁸)** — the strict statistical cutoff required to call a GWAS
  finding significant, given the multiple-testing burden of scanning hundreds of thousands of markers
  `[05:12]`.
- **Linkage disequilibrium** — the statistical correlation between nearby genetic markers that lets a
  limited chip capture information about a much larger number of untested variants `[06:13]`.
- **Manhattan plot / QQ plot** — the two standard visualizations used to display and validate GWAS
  association results `[09:19]`–`[10:20]`.
- **Odds ratio (as a GWAS effect-size measure)** — here, roughly 1.8–1.9 for the strongest chromosome 7
  marker, interpreted directly as "90% more chance of developing the disease" per copy of the risk allele
  `[12:23]`.

## Analogies worth reusing

- **Genetic "fingerprint"** — hundreds of thousands of genotyped markers combining into an individual
  signature usable for case-control comparison `[03:08]`.

## Source-stated confidence

Unusually careful and pedagogical about what a GWAS finding does and doesn't establish: Dolmans explains the
multiple-testing problem before presenting any result, explicitly states that a significant marker may not
itself be the causal variant, and closes by stating plainly that **replication in an independent cohort is
still needed** before these preliminary findings can be trusted — **"the thing we have to do now is
replicate."** He frames the talk's title modestly too, opening by noting **"it says the first genome-wide
association study, but maybe we're not the first."**

## Conflicts with other sources

**Is very likely the primary, earlier-stage presentation of the same GWAS finding `-0JtjUrrU4o`** (Ophoff's
2015 genetics talk) cites as already-published, describing **"nine different loci... from fewer than 1,000
cases."** This talk shows that same study mid-analysis (864–960 cases) with its first two significant loci
(chromosome 7 and 22) identified — the two chromosome 7/22 findings here are plausibly among the nine loci
Ophoff references five years later as an established, if still only ~14–16%-heritability-explaining, result.
**Extends `g40N2M2C6qM`** (Bayat's 2010 genetics talk, delivered the same symposium) — that talk's
badly-degraded transcript could not confidently convey specific GWAS numbers; this talk supplies exactly the
methodology and preliminary results that talk was gesturing toward. **Relevant to `AbY1KVhTVAo`** (Eaton's
IDDB talk) — Eaton's proposed genetic/systemic versus exposure/benign disease-subset hypothesis remains
consistent with, but not yet directly confirmed by, the specific loci identified here. **`hRJZEQzxy4U`**
(Werker and Aartsen's 2015 introductory remarks) supplies the human backstory behind this collaboration —
Werker's own account of meeting Ophoff and the 2010 Miami symposium becoming the moment this work turned
international.
