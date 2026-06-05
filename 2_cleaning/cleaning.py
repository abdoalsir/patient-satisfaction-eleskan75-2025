"""
Project  : Patient Satisfaction in Primary Healthcare Settings During the War
           in Sudan, Eleskan75 Center, Karary Locality, Khartoum State – 2025
Script   : Data Cleaning & Recoding
Author   : Abdulrahman Sirelkhatim
Date     : May 2026
Input    : 1_data/raw/raw_data.xlsx  (Google Form export, Arabic)
Output   : 1_data/cleaned/cleaned_data.xlsx
"""

import numpy as np
import pandas as pd

RAW_PATH = "1_data/raw/raw_data.xlsx"
OUTPUT_PATH = "1_data/cleaned/cleaned_data.xlsx"

ARABIC_TRANSLATIONS = {
    "العمر:": "Age",
    "الجنس:\n\u202f\u202f": "Gender",
    "الحاله الاجتماعيه": "MaritalStatus",
    "  المهنة:  ": "Occupation",
    "الوضع المعيشي الحالي:": "CurrentLivingStatus",
    "  الرعاية الطبية المقدمة خلال زيارتك كانت تلبي توقعاتك.  ": "care_expect",
    "الطاقم الطبي كان كفؤا ومهنيا": "staff_comp",
    "تم شرح حالتي الصحية وخيارات العلاج بشكل واضح.": "info_clarity",
    "عاملني الطاقم الطبي باحترام وكرامة.": "respect",
    "شعرت بأن الطبيب استمع لي وفهمني جيدًا أثناء الاستشارة.": "doc_listen",
    "أبدى الطاقم اهتمامًا بمخاوفي النفسية والعاطفية.": "staff_concern",
    "المركز الصحي كان نظيفًا وملتزمًا بالنظافة العامة.": "hygiene",
    "شعرت بالأمان الجسدي والنفسي داخل المركز الصحي.": "safe",
    "كان وقت الانتظار لتلقي الرعاية مقبولًا.": "wait_time",
    "كانت الأدوية أو العلاجات التي أحتاجها متوفرة.": "meds_avail",
    "حالتي الصحية تأثرت بالنزاع الحالي.": "conflict_affect",
    "تعامل الطاقم الصحي مع القضايا المتعلقة بنزوحـي.": "displacement",
    "بشكل عام، أنا راضٍ عن الرعاية التي تلقيتها خلال هذه الزيارة.\n\n(مقياس خطي - ١ = غير راضٍ جدًا، ٥ = راضٍ جدًا)": "overall_sat",
}

ARABIC_VALUE_MAP = {
    "نعم": "Yes",
    "ذكر": "Male",
    "أنثى": "Female",
    "أعزب": "Single",
    "متزوج": "Married",
    "أرمل": "Widowed",
    "مطلق": "Divorced",
    "نازح بسبب النزاع": "Displaced due to the conflict",
    "مقيم بالقرب من المركز الصحي": "Resident living near the healthcare center",
    "أعارض بشدة": "Strongly Disagree",
    "أعارض": "Disagree",
    "محايد": "Neutral",
    "أوافق": "Agree",
    "أوافق بشدة": "Strongly Agree",
}

LIKERT_MAP = {
    "Strongly Disagree": 1,
    "Disagree": 2,
    "Neutral": 3,
    "Agree": 4,
    "Strongly Agree": 5,
}

OCCUPATION_KEYWORDS = {
    "housewife": "Housewife",
    "ربة منزل": "Housewife",
    "ربه منزل": "Housewife",
    "ربة منزا": "Housewife",
    "ربه منزا": "Housewife",
    "ربة ممزل": "Housewife",
    "طالب": "Student",
    "student": "Student",
    "معلم": "Teacher",
    "معلمة": "Teacher",
    "استاذ": "Teacher",
    "استاذة": "Teacher",
    "teacher": "Teacher",
    "ممرض": "Health Professional",
    "ممرضة": "Health Professional",
    "طبيب": "Health Professional",
    "ضابط صحة": "Health Professional",
    "ضابطة صحة": "Health Professional",
    "nurse": "Health Professional",
    "doctor": "Health Professional",
    "health officer": "Health Professional",
    "عامل": "Worker / Manual Labor / Driver",
    "سائق": "Worker / Manual Labor / Driver",
    "worker": "Worker / Manual Labor / Driver",
    "manual labor": "Worker / Manual Labor / Driver",
    "driver": "Worker / Manual Labor / Driver",
    "موظف": "Employee",
    "employee": "Employee",
    "عاطل": "Unemployed",
    "unemployed": "Unemployed",
    "لا يوجد": "Unemployed",
    "لايوجد": "Unemployed",
    "بدون مهنه": "Unemployed",
    "مهندس": "Other",
    "engineer": "Other",
    "الطب البديل": "Other",
    "traditional medicine": "Other",
    "اعمال حرة": "Other",
    "اعمال حره": "Other",
    "مخلص جمركي": "Other",
}

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


def recode_occupation(val) -> str:
    if not isinstance(val, str):
        return "Other"
    v = val.strip()
    for keyword, label in OCCUPATION_KEYWORDS.items():
        if keyword in v:
            return label
    return "Other"


def age_group(age) -> str:
    if pd.isna(age):
        return np.nan
    if age <= 20:
        return "≤20"
    if age <= 30:
        return "21–30"
    if age <= 40:
        return "31–40"
    return "41+"


df_raw = pd.read_excel(RAW_PATH)

df_raw.columns = [ARABIC_TRANSLATIONS.get(col, col) for col in df_raw.columns]

df_raw = df_raw.apply(
    lambda col: col.map(
        lambda x: ARABIC_VALUE_MAP.get(str(x).strip(), x) if isinstance(x, str) else x
    )
)

df = df_raw.drop(
    columns=["Timestamp", "consent", "Phone", "comments"], errors="ignore"
).copy()

df["Gender"] = df["Gender"].map({"Male": 1, "Female": 2})
df["MaritalStatus"] = df["MaritalStatus"].map(
    {"Single": 1, "Married": 2, "Widowed": 3, "Divorced": 4}
)
df["displaced"] = df["CurrentLivingStatus"].map(
    {
        "Displaced due to the conflict": 1,
        "Resident living near the healthcare center": 0,
    }
)
df.drop(columns=["CurrentLivingStatus"], inplace=True)

df["Occupation"] = df["Occupation"].apply(recode_occupation)
df["age_grp"] = df["Age"].apply(age_group)

for col in LIKERT_COLS:
    df[col] = df[col].map(LIKERT_MAP).astype("Int64")

df["quality_mean"] = df[["care_expect", "staff_comp", "info_clarity"]].mean(axis=1)
df["provider_mean"] = df[["respect", "doc_listen", "staff_concern"]].mean(axis=1)
df["env_mean"] = df[["hygiene", "safe", "wait_time", "meds_avail"]].mean(axis=1)
df["conflict_mean"] = df[["conflict_affect", "displacement"]].mean(axis=1)
df["overall_index"] = df[LIKERT_COLS].mean(axis=1)

df["sat_bin"] = df["overall_sat"].apply(
    lambda x: 1 if x >= 4 else (0 if pd.notna(x) else np.nan)
)

col_order = (
    ["Age", "age_grp", "Gender", "MaritalStatus", "Occupation", "displaced"]
    + LIKERT_COLS
    + ["overall_sat"]
    + [
        "quality_mean",
        "provider_mean",
        "env_mean",
        "conflict_mean",
        "overall_index",
        "sat_bin",
    ]
)
df = df[col_order]

df.to_excel(OUTPUT_PATH, index=False)
print(f"Saved: {OUTPUT_PATH}")
print(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")
print(f"Satisfied (%):         {(df['sat_bin'] == 1).mean() * 100:.1f}%")
print(f"Overall Index mean:    {df['overall_index'].mean():.2f}")
print(f"Quality of Care mean:  {df['quality_mean'].mean():.2f}")
