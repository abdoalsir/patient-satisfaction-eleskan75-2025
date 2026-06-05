* Encoding: UTF-8.
* Patient Satisfaction in Primary Healthcare Settings During the War
* in Sudan, Eleskan75 Center, Karary Locality, Khartoum State, 2025.
* Data analyst: Abdulrahman Sirelkhatim.
* Input: cleaned_data.xlsx (output of cleaning.py).

* NOTE: Update the FILE path below before running.
GET DATA
  /TYPE=XLSX
  /FILE="1_data/cleaned/cleaned_data.xlsx"
  /SHEET=name "Sheet1"
  /CELLRANGE=full
  /READNAMES=on.
EXECUTE.

* Age group: already coded as string (≤20, 21–30, 31–40, 41+).
* Create numeric version for parametric tests.
NUMERIC age_grp_n (F1).
DO IF (age_grp = "≤20").
  COMPUTE age_grp_n = 1.
ELSE IF (age_grp = "21–30").
  COMPUTE age_grp_n = 2.
ELSE IF (age_grp = "31–40").
  COMPUTE age_grp_n = 3.
ELSE IF (age_grp = "41+").
  COMPUTE age_grp_n = 4.
ELSE.
  COMPUTE age_grp_n = $SYSMIS.
END IF.
EXECUTE.

VARIABLE LABELS age_grp_n "Age group (numeric)".
VALUE LABELS age_grp_n 1 "≤20" 2 "21–30" 3 "31–40" 4 "41+".
VARIABLE LEVEL age_grp_n (ORDINAL).

* Value labels for existing numeric variables.
VALUE LABELS Gender 1 "Male" 2 "Female".
VALUE LABELS MaritalStatus 1 "Single" 2 "Married" 3 "Widowed" 4 "Divorced".
VALUE LABELS displaced 0 "Resident" 1 "Displaced".
VALUE LABELS overall_sat 1 "Very Dissatisfied" 2 "Dissatisfied" 3 "Neutral"
  4 "Satisfied" 5 "Very Satisfied".
VALUE LABELS sat_bin 0 "Dissatisfied/Neutral" 1 "Satisfied".
EXECUTE.

VARIABLE LABELS
  Age "Age (years)"
  Gender "Gender"
  MaritalStatus "Marital status"
  Occupation "Occupation (grouped)"
  displaced "Displacement status (0=Resident, 1=Displaced)"
  care_expect "Q7: Medical care met expectations"
  staff_comp "Q8: Staff were competent and professional"
  info_clarity "Q9: Health condition and treatment clearly explained"
  respect "Q10: Treated with respect and dignity"
  doc_listen "Q11: Doctor listened and understood"
  staff_concern "Q12: Staff showed emotional concern"
  hygiene "Q13: Health center clean and hygienic"
  safe "Q14: Felt physically and emotionally safe"
  wait_time "Q15: Waiting time was acceptable"
  meds_avail "Q16: Medications and treatments were available"
  conflict_affect "Q17: Health condition affected by conflict"
  displacement "Q18: Staff addressed displacement issues"
  overall_sat "Q19: Overall satisfaction with care"
  quality_mean "Domain mean: Quality of Medical Care (Q7–Q9)"
  provider_mean "Domain mean: Patient–Provider Interaction (Q10–Q12)"
  env_mean "Domain mean: Health Center Environment (Q13–Q16)"
  conflict_mean "Domain mean: Conflict-Related Circumstances (Q17–Q18)"
  overall_index "Overall Satisfaction Index (mean Q7–Q18)"
  sat_bin "Overall satisfaction (binary: 0=Dissatisfied/Neutral, 1=Satisfied)".
EXECUTE.

VALUE LABELS care_expect staff_comp info_clarity respect doc_listen
  staff_concern hygiene safe wait_time meds_avail conflict_affect displacement
  1 "Strongly Disagree" 2 "Disagree" 3 "Neutral" 4 "Agree" 5 "Strongly Agree".
VARIABLE LEVEL care_expect staff_comp info_clarity respect doc_listen
  staff_concern hygiene safe wait_time meds_avail conflict_affect displacement (ORDINAL).
EXECUTE.

* 1. Reliability.
RELIABILITY
  /VARIABLES = care_expect staff_comp info_clarity
  /SCALE("Quality_of_Care") ALL
  /MODEL=ALPHA.

RELIABILITY
  /VARIABLES = respect doc_listen staff_concern
  /SCALE("Provider_Interaction") ALL
  /MODEL=ALPHA.

RELIABILITY
  /VARIABLES = hygiene safe wait_time meds_avail
  /SCALE("Environment") ALL
  /MODEL=ALPHA.

RELIABILITY
  /VARIABLES = conflict_affect displacement
  /SCALE("Conflict") ALL
  /MODEL=ALPHA.

RELIABILITY
  /VARIABLES = care_expect staff_comp info_clarity respect doc_listen
    staff_concern hygiene safe wait_time meds_avail conflict_affect displacement
  /SCALE("Overall_Index") ALL
  /MODEL=ALPHA.
EXECUTE.

* 2. Descriptive statistics.
FREQUENCIES VARIABLES = Gender MaritalStatus displaced age_grp_n sat_bin
  /FORMAT=DFREQ
  /STATISTICS=MODE.

FREQUENCIES VARIABLES = Occupation
  /FORMAT=DFREQ
  /STATISTICS=MODE.

DESCRIPTIVES VARIABLES = Age quality_mean provider_mean env_mean
    conflict_mean overall_index overall_sat
  /STATISTICS=MEAN STDDEV MIN MAX.

FREQUENCIES VARIABLES = overall_index overall_sat
  /STATISTICS=MEDIAN SKEWNESS.

* Item-level frequencies for all Likert items.
FREQUENCIES VARIABLES = care_expect staff_comp info_clarity respect doc_listen
    staff_concern hygiene safe wait_time meds_avail conflict_affect displacement overall_sat
  /FORMAT=DFREQ.
EXECUTE.

* 3. Correlation analysis.
* Spearman correlations for individual items with overall satisfaction.
NONPAR CORR
  /VARIABLES = care_expect staff_comp info_clarity respect doc_listen
    staff_concern hygiene safe wait_time meds_avail conflict_affect displacement overall_sat
  /PRINT=TWOTAIL SPEARMAN
  /MISSING=PAIRWISE.
EXECUTE.

* Pearson and Spearman correlations for domain means.
CORRELATIONS
  /VARIABLES = quality_mean provider_mean env_mean conflict_mean overall_index
  /PRINT=TWOTAIL
  /MISSING=PAIRWISE.

NONPAR CORR
  /VARIABLES = quality_mean provider_mean env_mean conflict_mean overall_index
  /PRINT=TWOTAIL SPEARMAN
  /MISSING=PAIRWISE.
EXECUTE.

* 4. Bivariate tests.
* Independent samples t-tests by gender.
T-TEST GROUPS = Gender(1 2)
  /VARIABLES = quality_mean provider_mean env_mean conflict_mean overall_index
  /MISSING=ANALYSIS.
EXECUTE.

* One-way ANOVA: overall index by marital status.
ONEWAY overall_index BY MaritalStatus
  /STATISTICS DESCRIPTIVES HOMOGENEITY
  /POSTHOC=Tukey.
EXECUTE.

* One-way ANOVA: overall index by age group.
ONEWAY overall_index BY age_grp_n
  /STATISTICS DESCRIPTIVES HOMOGENEITY
  /POSTHOC=Tukey.
EXECUTE.

* Chi-square tests: demographics vs binary satisfaction.
CROSSTABS /TABLES = Gender BY sat_bin /STATISTICS=CHISQ /CELLS=COUNT ROW COLUMN.
CROSSTABS /TABLES = MaritalStatus BY sat_bin /STATISTICS=CHISQ /CELLS=COUNT ROW COLUMN.
CROSSTABS /TABLES = displaced BY sat_bin /STATISTICS=CHISQ /CELLS=COUNT ROW COLUMN.
CROSSTABS /TABLES = age_grp_n BY sat_bin /STATISTICS=CHISQ /CELLS=COUNT ROW COLUMN.
EXECUTE.

* 5. Multivariate analysis.
* Multiple linear regression: predictors of overall satisfaction (Q19).
REGRESSION
  /STATISTICS COEFF R ANOVA COLLIN TOL
  /DEPENDENT overall_sat
  /METHOD=ENTER Age Gender MaritalStatus displaced
    quality_mean provider_mean env_mean conflict_mean
  /MISSING LISTWISE.
EXECUTE.

* Ordinal logistic regression: demographic predictors of Q19 (ordered 1–5).
PLUM overall_sat
  WITH Age Gender MaritalStatus displaced
  /LINK=logit
  /PRINT=PARAMETER SUMMARY FIT
  /CRITERIA=MXITER(100) MXSTEP(10) LCONVERGE(0.001) SINGULAR(0.000001).
EXECUTE.

* NOTE: Update the OUTFILE path below before running.
SAVE OUTFILE="1_data/cleaned/pt_sat_recoded.sav"
  /COMPRESSED.
EXECUTE.
