"""
Project  : Patient Satisfaction in Primary Healthcare Settings During the War
           in Sudan, Eleskan75 Center, Karary Locality, Khartoum State – 2025
Script   : Figure Generation (all figures)
Author   : Abdulrahman Sirelkhatim
Date     : May 2026
Input    : 1_data/cleaned/cleaned_data.xlsx
Output   : 5_figures/ directory (PNG, 300 DPI)

Figures produced:
    fig01_gender_distribution.png
    fig02_age_group_distribution.png
    fig03_marital_status_distribution.png
    fig04_displacement_status_distribution.png
    fig05_occupation_distribution.png
    fig06_overall_satisfaction_distribution.png
    fig07_domain_mean_scores.png
    fig08_likert_item_diverging.png
    fig09_overall_index_by_gender.png
    fig10_domain_scores_by_gender.png
    fig11_overall_index_by_marital_status.png
    fig12_correlation_heatmap.png
"""

import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

warnings.filterwarnings("ignore")

DATA_PATH = "1_data/cleaned/cleaned_data.xlsx"
FIGURES_DIR = "5_figures/"

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 11
plt.rcParams["figure.dpi"] = 200

BLUE = sns.color_palette("Blues_r", 6)
PALETTE = sns.color_palette("Set2")
CONTRAST = [BLUE[1], BLUE[3], BLUE[5]]

LIKERT_COLS = [
    "care_expect",
    "staff_comp",
    "info_clarity",
    "respect",
    "doc_listen",
    "staff_concern",
    "hygiene",
    "safe",
    "wait_time",
    "meds_avail",
    "conflict_affect",
    "displacement",
]

ITEM_LABELS = [
    "Q7: Care met expectations",
    "Q8: Staff competent",
    "Q9: Treatment explained",
    "Q10: Treated with respect",
    "Q11: Doctor listened",
    "Q12: Emotional concern",
    "Q13: Clean/hygienic",
    "Q14: Felt safe",
    "Q15: Waiting time acceptable",
    "Q16: Medication available",
    "Q17: Health affected by conflict",
    "Q18: Staff addressed displacement",
]

DOMAIN_COLS = ["quality_mean", "provider_mean", "env_mean", "conflict_mean"]
DOMAIN_LABELS = [
    "Quality of\nMedical Care",
    "Patient–Provider\nInteraction",
    "Health Center\nEnvironment",
    "Conflict-Related\nCircumstances",
]


def save_fig(fig, filename):
    fig.savefig(FIGURES_DIR + filename, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {filename}")


def remove_spines(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


df = pd.read_excel(DATA_PATH)
n = len(df)

gender_labels = {1: "Male", 2: "Female"}
marital_labels = {1: "Single", 2: "Married", 3: "Widowed", 4: "Divorced"}

fig, ax = plt.subplots(figsize=(5, 5))
gender_counts = df["Gender"].map(gender_labels).value_counts()
ax.pie(
    gender_counts,
    labels=gender_counts.index,
    autopct="%1.1f%%",
    colors=[BLUE[1], PALETTE[1]],
    wedgeprops={"width": 0.6, "edgecolor": "white"},
    pctdistance=0.75,
    labeldistance=1.05,
)
ax.set_title(f"Gender Distribution (N={n})", pad=12)
save_fig(fig, "fig01_gender_distribution.png")


age_order = ["≤20", "21–30", "31–40", "41+"]
fig, ax = plt.subplots(figsize=(6, 4))
age_counts = df["age_grp"].value_counts().reindex(age_order)
pcts = age_counts / n * 100
bars = ax.bar(age_order, pcts, color=BLUE[:4])
for bar, v in zip(bars, pcts):
    ax.text(
        bar.get_x() + bar.get_width() / 2, v + 0.5, f"{v:.1f}%", ha="center", fontsize=9
    )
ax.set_ylabel("Percentage (%)")
ax.set_xlabel("Age Group")
ax.set_title(f"Age Group Distribution (N={n})\nMean age = 30.1 ± 9.3 years")
ax.set_ylim(0, 75)
remove_spines(ax)
plt.tight_layout()
save_fig(fig, "fig02_age_group_distribution.png")


fig, ax = plt.subplots(figsize=(5, 5))
marital_counts = df["MaritalStatus"].map(marital_labels).value_counts()
ax.pie(
    marital_counts,
    labels=marital_counts.index,
    autopct="%1.1f%%",
    colors=CONTRAST + [PALETTE[3]],
    wedgeprops={"width": 0.6, "edgecolor": "white"},
    pctdistance=0.75,
    labeldistance=1.05,
)
ax.set_title(f"Marital Status Distribution (N={n})", pad=12)
save_fig(fig, "fig03_marital_status_distribution.png")


fig, ax = plt.subplots(figsize=(5, 5))
disp_counts = df["displaced"].map({0: "Resident", 1: "Displaced"}).value_counts()
ax.pie(
    disp_counts,
    labels=disp_counts.index,
    autopct="%1.1f%%",
    colors=[BLUE[1], BLUE[4]],
    wedgeprops={"width": 0.6, "edgecolor": "white"},
    pctdistance=0.75,
    labeldistance=1.05,
)
ax.set_title(f"Displacement Status (N={n})", pad=12)
save_fig(fig, "fig04_displacement_status_distribution.png")


fig, ax = plt.subplots(figsize=(7, 4))
occ_counts = df["Occupation"].value_counts().sort_values()
pcts = occ_counts / n * 100
bars = ax.barh(occ_counts.index, pcts, color=BLUE[1])
for bar, v in zip(bars, pcts):
    ax.text(
        v + 0.3,
        bar.get_y() + bar.get_height() / 2,
        f"{v:.1f}%",
        va="center",
        fontsize=9,
    )
ax.set_xlabel("Percentage (%)")
ax.set_title(f"Occupation Distribution (N={n})")
ax.set_xlim(0, 80)
remove_spines(ax)
plt.tight_layout()
save_fig(fig, "fig05_occupation_distribution.png")


sat_order = [
    "Very Dissatisfied",
    "Dissatisfied",
    "Neutral",
    "Satisfied",
    "Very Satisfied",
]
sat_map = {
    1: "Very Dissatisfied",
    2: "Dissatisfied",
    3: "Neutral",
    4: "Satisfied",
    5: "Very Satisfied",
}
fig, ax = plt.subplots(figsize=(7, 4))
sat_counts = df["overall_sat"].map(sat_map).value_counts().reindex(sat_order)
pcts = sat_counts / n * 100
bars = ax.bar(sat_order, pcts, color=CONTRAST + [BLUE[0], BLUE[2]])
for bar, v in zip(bars, pcts):
    ax.text(
        bar.get_x() + bar.get_width() / 2, v + 0.5, f"{v:.1f}%", ha="center", fontsize=9
    )
ax.set_ylabel("Percentage (%)")
ax.set_xlabel("Overall Satisfaction (Q19)")
ax.set_title(
    f"Overall Satisfaction Distribution (N={n})\n75.6% Satisfied or Very Satisfied"
)
ax.set_ylim(0, 55)
ax.tick_params(axis="x", labelsize=9)
remove_spines(ax)
plt.tight_layout()
save_fig(fig, "fig06_overall_satisfaction_distribution.png")


domain_means = [df[col].mean() for col in DOMAIN_COLS]
domain_sds = [df[col].std() for col in DOMAIN_COLS]
fig, ax = plt.subplots(figsize=(7, 4.5))
x = np.arange(len(DOMAIN_LABELS))
bars = ax.bar(
    x, domain_means, yerr=domain_sds, capsize=5, color=CONTRAST + [PALETTE[3]]
)
for bar, v in zip(bars, domain_means):
    ax.text(
        bar.get_x() + bar.get_width() / 2, v + 0.05, f"{v:.2f}", ha="center", fontsize=9
    )
ax.axhline(
    3.0, color="gray", linestyle="--", linewidth=0.8, alpha=0.7, label="Neutral (3.0)"
)
ax.set_xticks(x)
ax.set_xticklabels(DOMAIN_LABELS, fontsize=9)
ax.set_ylabel("Mean Score (1–5 scale)")
ax.set_ylim(0, 5)
ax.set_title(f"Mean Scores Across Satisfaction Domains (N={n})")
ax.legend(fontsize=9)
remove_spines(ax)
plt.tight_layout()
save_fig(fig, "fig07_domain_mean_scores.png")


likert_colors = ["#d73027", "#fc8d59", "#cccccc", "#91bfdb", "#4575b4"]
likert_response_labels = [
    "Strongly Disagree",
    "Disagree",
    "Neutral",
    "Agree",
    "Strongly Agree",
]

rows = []
for col, label in zip(LIKERT_COLS, ITEM_LABELS):
    vc = df[col].value_counts(normalize=True).mul(100)
    rows.append(
        {
            "item": label,
            "SD": vc.get(1, 0),
            "D": vc.get(2, 0),
            "N": vc.get(3, 0),
            "A": vc.get(4, 0),
            "SA": vc.get(5, 0),
        }
    )
df_lik = pd.DataFrame(rows).set_index("item")

df_lik["n_right"] = df_lik["N"] / 2
df_lik["n_left"] = -df_lik["N"] / 2
df_lik["left_d"] = df_lik["n_left"]
df_lik["left_sd"] = df_lik["n_left"] - df_lik["D"]
df_lik["left_a"] = df_lik["n_right"]
df_lik["left_sa"] = df_lik["n_right"] + df_lik["A"]

fig, ax = plt.subplots(figsize=(12, 7))
ax.barh(df_lik.index, df_lik["n_right"], color=likert_colors[2])
ax.barh(df_lik.index, df_lik["n_left"], color=likert_colors[2])
ax.barh(
    df_lik.index,
    df_lik["D"],
    left=df_lik["left_d"],
    color=likert_colors[1],
    label="Disagree",
)
ax.barh(
    df_lik.index,
    -df_lik["SD"],
    left=df_lik["left_sd"],
    color=likert_colors[0],
    label="Strongly Disagree",
)
ax.barh(
    df_lik.index,
    df_lik["A"],
    left=df_lik["left_a"],
    color=likert_colors[3],
    label="Agree",
)
ax.barh(
    df_lik.index,
    df_lik["SA"],
    left=df_lik["left_sa"],
    color=likert_colors[4],
    label="Strongly Agree",
)
ax.axvline(0, color="black", linewidth=0.8)
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{abs(x):.0f}%"))
ax.set_xlabel("Percentage of Respondents")
ax.set_title(f"Item-Level Patient Satisfaction Responses (N={n})")
ax.legend(
    loc="upper center", bbox_to_anchor=(0.5, 1.07), ncol=5, frameon=False, fontsize=9
)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.tick_params(axis="y", length=0, labelsize=9)
ax.invert_yaxis()
plt.tight_layout(rect=[0, 0, 1, 0.97])
save_fig(fig, "fig08_likert_item_diverging.png")


fig, ax = plt.subplots(figsize=(5, 4))
gender_index = (
    df.groupby("Gender")["overall_index"]
    .agg(["mean", "std"])
    .rename(index={1: "Male\n(n=49)", 2: "Female\n(n=308)"})
)
x = np.arange(len(gender_index))
bars = ax.bar(
    x,
    gender_index["mean"],
    yerr=gender_index["std"],
    capsize=5,
    color=[BLUE[1], PALETTE[1]],
    width=0.5,
)
for bar, v in zip(bars, gender_index["mean"]):
    ax.text(
        bar.get_x() + bar.get_width() / 2, v + 0.05, f"{v:.2f}", ha="center", fontsize=9
    )
ax.set_xticks(x)
ax.set_xticklabels(gender_index.index)
ax.set_ylabel("Overall Satisfaction Index (mean)")
ax.set_ylim(0, 5)
ax.set_title(f"Overall Satisfaction Index by Gender (N={n})\nt-test p = 0.001")
remove_spines(ax)
plt.tight_layout()
save_fig(fig, "fig09_overall_index_by_gender.png")


fig, ax = plt.subplots(figsize=(9, 5))
width = 0.35
x = np.arange(len(DOMAIN_LABELS))
male_means = [df[df["Gender"] == 1][col].mean() for col in DOMAIN_COLS]
female_means = [df[df["Gender"] == 2][col].mean() for col in DOMAIN_COLS]
male_sds = [df[df["Gender"] == 1][col].std() for col in DOMAIN_COLS]
female_sds = [df[df["Gender"] == 2][col].std() for col in DOMAIN_COLS]
p_vals = [0.089, 0.001, 0.010, 0.009]

bars_m = ax.bar(
    x - width / 2,
    male_means,
    width,
    yerr=male_sds,
    capsize=4,
    label="Male (n=49)",
    color=BLUE[1],
)
bars_f = ax.bar(
    x + width / 2,
    female_means,
    width,
    yerr=female_sds,
    capsize=4,
    label="Female (n=308)",
    color=PALETTE[1],
)

for i, (p, fm, fsd) in enumerate(zip(p_vals, female_means, female_sds)):
    if p < 0.05:
        ax.text(x[i] + width / 2, fm + fsd + 0.12, "*", ha="center", fontsize=13)

ax.set_xticks(x)
ax.set_xticklabels(DOMAIN_LABELS, fontsize=9)
ax.set_ylabel("Mean Score (1–5 scale)")
ax.set_ylim(0, 5.2)
ax.set_title(f"Satisfaction Domain Scores by Gender (N={n})\n* p < 0.05")
ax.legend(fontsize=9)
remove_spines(ax)
plt.tight_layout()
save_fig(fig, "fig10_domain_scores_by_gender.png")


fig, ax = plt.subplots(figsize=(7, 4))
marital_order = [
    "Single\n(n=29)",
    "Married\n(n=293)",
    "Widowed\n(n=29)",
    "Divorced\n(n=6)",
]
marital_means = [
    df[df["MaritalStatus"] == 1]["overall_index"].mean(),
    df[df["MaritalStatus"] == 2]["overall_index"].mean(),
    df[df["MaritalStatus"] == 3]["overall_index"].mean(),
    df[df["MaritalStatus"] == 4]["overall_index"].mean(),
]
marital_sds = [
    df[df["MaritalStatus"] == 1]["overall_index"].std(),
    df[df["MaritalStatus"] == 2]["overall_index"].std(),
    df[df["MaritalStatus"] == 3]["overall_index"].std(),
    df[df["MaritalStatus"] == 4]["overall_index"].std(),
]
bars = ax.bar(
    marital_order,
    marital_means,
    yerr=marital_sds,
    capsize=5,
    color=[BLUE[0], BLUE[2], BLUE[4], PALETTE[2]],
)
for bar, v in zip(bars, marital_means):
    ax.text(
        bar.get_x() + bar.get_width() / 2, v + 0.05, f"{v:.2f}", ha="center", fontsize=9
    )
ax.set_ylabel("Overall Satisfaction Index (mean)")
ax.set_ylim(0, 5)
ax.set_title(
    f"Overall Satisfaction Index by Marital Status (N={n})\nOne-way ANOVA F(3,353) = 3.28, p = 0.021"
)
remove_spines(ax)
plt.tight_layout()
save_fig(fig, "fig11_overall_index_by_marital_status.png")


corr_vars = DOMAIN_COLS + ["overall_index"]
corr_labels = [
    "Quality of\nMedical Care",
    "Patient–Provider\nInteraction",
    "Health Center\nEnvironment",
    "Conflict-Related\nCircumstances",
    "Overall\nSat. Index",
]
corr_matrix = df[corr_vars].corr(method="pearson")
corr_matrix.index = corr_labels
corr_matrix.columns = corr_labels

fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(
    corr_matrix,
    annot=True,
    fmt=".3f",
    cmap="Blues",
    vmin=0.4,
    vmax=1.0,
    linewidths=0.5,
    linecolor="lightgray",
    cbar_kws={"label": "Pearson r"},
    ax=ax,
)
plt.xticks(rotation=30, ha="right", fontsize=9)
plt.yticks(rotation=0, fontsize=9)
ax.set_title(f"Pearson Correlation Heatmap — Satisfaction Domains (N={n})", pad=10)
plt.tight_layout()
save_fig(fig, "fig12_correlation_heatmap.png")

print(f"\nAll figures saved to: {FIGURES_DIR}")
