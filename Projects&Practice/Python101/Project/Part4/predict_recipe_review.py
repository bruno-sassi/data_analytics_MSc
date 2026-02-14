# %% [markdown]
# # Comprehensive Case Study – Recipe Review Ratings Prediction
#  
# #### Bruno de Arantes Leite Sassi

# %% [markdown]
# # 1 Data Cleaning:
# Prepare the dataset for analysis by resolving common data quality issues.
# -	Identify and handle missing values. In this dataset, the value '2' is sometimes used as a placeholder for missing data.
# -	Remove or review duplicates and inconsistencies
# -	Ensure correct data types
# -	Normalize inconsistent categorical values
# 

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.compose import make_column_selector as selector
from sklearn.impute import SimpleImputer


df = pd.read_csv('recipe_reviews.csv')
df.head()

# %%
# Display basic information about the DataFrame
print(df.info())

# Check for missing values in each column
print(df.isnull().sum())

# %%
# convert created_at to date (UTC) - considering Unix seconds :
df["created_at"] = pd.to_datetime(df["created_at"], unit="s", utc=True)

# check the range of resulting dates
print(df["created_at"].min(), df["created_at"].max())


# %%
# check '2' values in each column based on data type
print(df.select_dtypes(include="int64").eq(2).sum())
print(df.select_dtypes(include="float64").eq(2.0).sum())
print(df.select_dtypes(include="object").eq("2").sum())

# basic dedupe + dtype + categorical normalization (safe patch)

print("Rows before drop_duplicates:", len(df))
df = df.drop_duplicates()
print("Rows after  drop_duplicates:", len(df))

# Coerce obvious numeric-typed strings to numeric (won't touch true strings)
num_like_cols = [
    "likes", "dislikes", "responses", "user_score", "ranking_score",
    "ranking_value", "vote_ratio", "score_log", "text_word_count", "text_char_count",
    # add any other count/rate columns if they arrived as object
]
for col in num_like_cols:
    if col in df.columns and df[col].dtype == "O":
        df[col] = pd.to_numeric(df[col].str.replace(",", "", regex=False), errors="coerce")

# Handle missing numerics (simple, transparent policy; models use scaling)
for col in [c for c in num_like_cols if c in df.columns]:
    df[col] = df[col].astype("float64")
    if df[col].isna().any():
        df[col] = df[col].fillna(df[col].median())

# Normalize categoricals: lowercase/strip; bucket ultra-rare levels to 'Other'
def _norm_cat(s):
    return s.astype(str).str.strip().str.lower()

cat_cols_norm = [c for c in ["region", "device_type"] if c in df.columns]
for c in cat_cols_norm:
    df[c] = _norm_cat(df[c])
    vc = df[c].value_counts(normalize=True, dropna=False)
    rare = vc[vc < 0.01].index  # <1% frequency → 'other'
    df[c] = df[c].where(~df[c].isin(rare), "other")

# print quick sanity
for c in cat_cols_norm:
    print(f"\nValue counts (normalized) for {c} after normalization:")
    print(df[c].value_counts(normalize=True).round(4).head(15))


# check unique values in each non numeric column
for i in df.select_dtypes(include=['object']).columns:
    print(f"\n Unique values in '{i}':")
    print(df[i].value_counts())


# %% [markdown]
# ### Data Cleaning Addendum – Duplicates, Dtypes, and Categoricals
# - **Duplicates:** Printed counts show how many rows were removed.
# - **Dtypes:** Numeric-like strings were coerced; remaining NaN filled with median.
# - **Categoricals:** Lowercased/trimmed and rare levels (<1%) bucketed to **other**.
# 

# %% [markdown]
# Looking into the data, the potential placeholders for missing data could be:
# 
# Unnamed: 0 (100)
# recipe_number (509)
# 
# And likely real data (true value = 2):
# 
# responses (24)
# likes (624)
# dislikes (388)
# stars (232)

# %%
# with that, we look int the potential placeholders for missing data
print(df.loc[df['Unnamed: 0'] == 2].head())
df.loc[df['recipe_number'] == 2].head()

# %%
# check if all rows in recipe_code are the same when recipe_number == 2
df.loc[df['recipe_number'] == 2, ['recipe_code', 'recipe_number']].nunique()

# %% [markdown]
# Whenever recipe_number == 2, the recipe_code is consistently 3309.
# 
# That consistency suggests those records are real recipes that genuinely have recipe_number = 2.
# 
# So in this case, 2 is valid data, not a missing placeholder. From this is worth checking if the two columns are redundant.
# 
# For the Unnamed: 0 column, on the other hand, it does look like number 2 entries are potential placeholders for missing data, but the column itself doesnt seem to add any value , so it better to drop the whole column.

# %%
# drop Unnamed: 0 since it is just an index
df = df.drop(columns=["Unnamed: 0"])

# Check column redundancy between recipe_number and recipe_code
# Check if each recipe_number maps to a single recipe_code
num_to_code = df.groupby("recipe_number")["recipe_code"].nunique()

# Check if each recipe_code maps to a single recipe_number
code_to_num = df.groupby("recipe_code")["recipe_number"].nunique()

print("recipe_number → unique recipe_code counts:")
print(num_to_code.value_counts())  # distribution of how many codes per number

print("\nrecipe_code → unique recipe_number counts:")
print(code_to_num.value_counts())

# %%
# drop recipe_number since it is redundant
df = df.drop(columns=["recipe_number"])
df.head(3)

# %% [markdown]
# Upon a closer look, many columns act as IDs or indexes that cannot be generalized, including 'recipe_code'. Since the goal is to create a prediction model, those will be dropped to avoid unecessary or useless work.

# %%
# Drop: IDs (recipe_code, user_index, user_id, created_at, comment_id, recipe_name, user_name).
df = df.drop(columns=["recipe_code", "user_index", "user_id", "created_at", "comment_id", "user_name"])
# converting created_at to date showed a small window of time, so it probably won't be useful for prediction too
df.head(3)

# %% [markdown]
# # 2 Exploratory Data Analysis (EDA):
# Explore and understand the structure, trends, and relationships in the data.
# - 	Analyze data and generate summary statistics
# - 	Visualize distributions and correlations
# - 	Explore how different features relate to star ratings
# 

# %%
#check basic statistics for numerical columns
df.describe()

# %%
# Check Class balance
counts = df["stars"].value_counts().sort_index()
props  = (counts / counts.sum()).round(3)
display(pd.DataFrame({"count": counts, "proportion": props}))


# %%
# Bag-of-words / TF-IDF on recipe_name
vectorizer = TfidfVectorizer(
    max_features=500,  # keep top words only
    stop_words="english",
    ngram_range=(1,2)  # unigrams + bigrams
)
X_text = vectorizer.fit_transform(df["recipe_name"].fillna(""))


# %%
# Keyword analysis
# simple token split
words = df["recipe_name"].str.lower().str.split()
word_counts = Counter([w for row in words.dropna() for w in row])
top_words = [w for w, c in word_counts.most_common(50)]

# see mean stars per top word
out = {}
for w in top_words:
    mask = df["recipe_name"].str.lower().str.contains(rf"\b{w}\b", na=False)
    out[w] = df.loc[mask, "stars"].mean()
pd.Series(out).sort_values()


# %%
# --- basic tokenization (keep words & simple bigrams if you want) ---
def tokenize(s):
    if pd.isna(s): return []
    # lowercase, keep letters, numbers, apostrophes; split on non-word boundaries
    tokens = re.findall(r"[a-zA-Z0-9']+", s.lower())
    return tokens

# tokens per row
tokens_series = df["recipe_name"].apply(tokenize)

# frequency table (unigrams)
freq = Counter([t for row in tokens_series for t in row])

# pick a vocabulary to analyze (e.g., top 200 frequent, drop 1-char tokens)
vocab = [w for w, c in freq.most_common(200) if len(w) > 1]


# %%
# Create a column with lenght of text
df['text_word_count'] = df['text'].fillna('').apply(lambda x: len(x.split()))
df['text_char_count'] = df['text'].fillna('').apply(lambda x: len(x.replace(' ', '')))
df[['text_word_count', 'text_char_count']].describe()

# %%
# Select numerical columns for visualization
numerical_columns = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
print(len(numerical_columns), numerical_columns)

# remove id-like and categorical-like features
numerical_columns.remove('response_level') 

# Create a grid of subplots for the selected numerical features
fig, axes = plt.subplots(nrows=5, ncols=3, figsize=(12, 12))  # Adjust grid size
axes = axes.flatten()

# Plot histograms for the selected numerical features
for i, col in enumerate(numerical_columns):
    sns.histplot(df[col], kde=True, bins=30, ax=axes[i])
    axes[i].set_title(f'Distribution of {col}')

# Adjust layout
plt.tight_layout()
plt.show()

# %% [markdown]
# * likes_score — Mass near 0 with a long right tail → most items have low scores; a few get very large.
# 
# * dislike_index — Same pattern as likes_score: heavy near 0, long tail.
# 
# * ranking_value — Unimodal cluster with a noticeable right tail; plausible continuous score; check for outliers.
# 
# * vote_ratio — Values packed near 0 with distinct clumps (likely from small integer counts, e.g., 0, 1/2, 2/3, etc.). Ratio is in [0,1]; heavy zero-inflation.
# 
# * score_log — Peak at low values and a long tail up to ~6 → a typical log-transformed popularity metric with a few very large items.
# 
# * user_score — Zero-inflated with a long tail to very large values; strong popularity/engagement skew.
# 
# * responses — Small integer support (0–3) with a dominant 0 → most items have no responses; classic zero-inflation.
# 
# * likes — Many zeros and a long tail (further than dislikes) → few items accumulate lots of likes.
# 
# * dislikes — Same shape as likes but lower overall and shorter tail → dislikes are rarer than likes.
# 
# * ranking_score — Concentrated at low values with a right tail; consistent with an aggregate/derived score.
# 
# * stars — Discrete at 0–5 with tall bars at 0 and 5 → bimodal. The 0s may mean “no rating / unrated” rather than a true star value; worth confirming business logic.
# 
# * text_word_count - More concentrated in low values, right skewed and with long tail
# 
# * text_chart_count - More concentrated in low values, right skewed and with long tail
# 
# What stands out / action items
# 
# * Zero-inflation + long tails: likes, dislikes, responses, user_score, likes_score, dislike_index → consider log1p transforms, robust scalers, or zero-inflated models; be careful with outliers.
# 
# * Stars: The spike at 0 suggests a special meaning (unrated). Decide whether stars==0 should be treated as missing.

# %%
# checking star == 0 entries to decide is 0 is a valid rate or absense of it (missing)
df.loc[df['stars'] == 0]

# %% [markdown]
# Sample Results indicate that 0 stars is more likely to be the absense of rating, rather than a zero score, since a good proportion of texts speak highly of the recipe.

# %%
# percentage of 0 stars entries
print(len(df.loc[df['stars'] == 0])/len(df)*100 )
print( "Total entries x 0 stars entries: ", len(df), " x ", len(df.loc[df['stars'] == 0]) )

# %% [markdown]
# The percentage of missing ratings in stars is relevant (9,33%), however stars are the core of the current research and even without this entries the dataset has a good size, so I'll drop those rows.

# %%
# Drop rows with 0 stars since they are likely missing ratings
df = df[df['stars'] != 0]
# check the new size of the dataset
df.shape

# %% [markdown]
# Check relationship between numerical features and 'stars'
# 

# %%
# Check relationship between numerical features and 'stars'
n = len(numerical_columns)
ncols = 3
nrows = (n + ncols - 1) // ncols
fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(10, 3*nrows))
axes = axes.flatten()

for i, col in enumerate(numerical_columns):
    ax = axes[i]
    sns.violinplot(x="stars", y=col, data=df, inner=None, cut=0, ax=ax)
    sns.stripplot(x="stars", y=col, data=df, ax=ax, size=2, alpha=0.4, jitter=True)
    ax.set_title(f"{col} by stars")
    # optional for heavy-tailed metrics:
    # ax.set_yscale("symlog")

for j in range(len(numerical_columns), len(axes)):
    fig.delaxes(axes[j])

plt.tight_layout()
plt.show()


# %% [markdown]
# Focusing on shape, trend or any highlight.
# 
# * **likes\_score by stars** — Clear upward trend; dispersion explodes at 5. Heavy zero-inflation at low stars.
# * **dislike\_index by stars** — Mostly near zero across all stars; slight rise and longer tail at 5 (likely exposure effect—popular items get more of everything, including dislikes).
# * **ranking\_value by stars** — Increases with stars; much fatter tail at 5 → aligns with rating.
# * **vote\_ratio by stars** — Nicely monotonic upward separation across star levels; looks like a strong predictor.
# * **score\_log by stars** — Steady rise with stars; compact at low stars, wider at 4–5 → strong association.
# * **user\_score by stars** — Same story as likes\_score: higher stars → higher center and variance; heavy right tail at 5.
# * **responses by stars** — Small integer support; mostly 0’s at every star, slight uptick with higher stars but weak separation.
# * **likes by stars** — Strongly increasing with stars; zero-inflated overall, very long tail at 5.
# * **dislikes by stars** — Low counts everywhere; modest increase and longer tail at 5 (again likely exposure, not sentiment).
# * **ranking\_score by stars** — Strong positive relationship; extreme spread for 5-star items.
# * stars by stars — created automatically → ignore
# * **text_word_coutn** - The distribution widens as stars increase, with 4–5 star reviews tending to have higher word counts.
# * **text_char_count** - The distribution widens as stars increase, with 4–5 star reviews tending to have higher charactercounts.
# 
# What stands out
# 
# * **Monotonic relationships:** vote\_ratio, score\_log, ranking\_value/score, likes/user\_score all rise with stars → likely the most informative features.
# * **Exposure effect:** dislikes and dislike\_index also rise at high stars; not contradictory—popular items attract more interactions of all kinds.
# * **Zero-inflation & heavy tails:** likes, user\_score, responses show many zeros and a few very large values → consider `log1p`/robust scaling and outlier-aware summaries.
# * **Class imbalance risk:** low-star categories look sparser than 5-star.
# * **text count** - users who leave bigger reviews tend to give higher stars 
# 

# %%
# make stars an ordered categorical (handy for plots / stats)
df["stars_cat"] = pd.Categorical(df["stars"], categories=[1,2,3,4,5], ordered=True)

# pick numeric columns (drop the target)
num_cols = df.select_dtypes(include="number").columns.drop("stars")

# drop obvious ID-like columns automatically
uniq_ratio = df[num_cols].nunique() / len(df)
id_like = uniq_ratio[uniq_ratio > 0.9].index  
num_cols = [c for c in num_cols if c not in id_like]
num_cols
print (num_cols)
print (id_like)

# %%
# Monotonic association (Spearman’s ρ)
from scipy.stats import spearmanr

rows = []
for col in num_cols:
    s = df[col]
    ok = s.notna() & df["stars"].notna()
    rho, p = spearmanr(s[ok], df.loc[ok, "stars"])
    rows.append((col, rho, p))

spearman_df = (pd.DataFrame(rows, columns=["feature","spearman_rho","p"])
                 .assign(abs_rho=lambda x: x["spearman_rho"].abs())
                 .sort_values("abs_rho", ascending=False))
spearman_df.head(10)


# %%
# Nonparametric group differences (Kruskal–Wallis) + effect size
# “do distributions differ across 1–5★ ?

from scipy.stats import kruskal

kw_rows = []
groups = [g for _, g in df.groupby("stars")]
k = len(groups)
N = len(df)

for col in num_cols:
    arrays = [g[col].dropna().values for g in groups]
    if sum(len(a) > 0 for a in arrays) < k:  # need data in all groups
        continue
    H, p = kruskal(*arrays)
    # Epsilon-squared (nonparametric effect size)
    eps2 = (H - (k - 1)) / (N - 1)
    kw_rows.append((col, H, p, eps2))

kw_df = (pd.DataFrame(kw_rows, columns=["feature","H","p","epsilon_sq"])
           .sort_values("epsilon_sq", ascending=False))
kw_df.head(10)


# %%
# Multiple testing control (BH–FDR)
# Benjamini-Hochberg procedure

def bh_fdr(pvals, alpha=0.05):
    p = np.asarray(pvals)
    m = len(p)
    order = np.argsort(p)
    ranked = p[order]
    thresh = alpha * (np.arange(1, m+1) / m)
    passed = ranked <= thresh
    cutoff = np.max(np.where(passed)[0]) if passed.any() else -1
    crit = ranked[cutoff] if cutoff >= 0 else 0
    return (p <= crit), crit

kw_df = kw_df.copy()
kw_df["reject_fdr"], fdr_cut = bh_fdr(kw_df["p"].values, alpha=0.05)
kw_df.head(10)


# %%
# re-run Spearman on log1p for heavy-tailed metrics
heavy = [c for c in num_cols if (df[c] >= 0).all() and (df[c] == 0).mean() > 0.3]

rows = []
for col in heavy:
    s = np.log1p(df[col])
    ok = s.notna()
    rho, p = spearmanr(s[ok], df.loc[ok, "stars"])
    rows.append((col, rho, p))

spearman_log_df = (pd.DataFrame(rows, columns=["feature","spearman_rho_log1p","p_log1p"])
                     .assign(abs_rho_log1p=lambda x: x["spearman_rho_log1p"].abs())
                     .sort_values("abs_rho_log1p", ascending=False))
spearman_log_df.head(10)


# %% [markdown]
# Why p-values look tiny but correlations are tiny
# 
# * huge sample size + many ties/zeros → very small p-values even when the effect size is trivial.
# 
# * Focus on effect sizes: only dislikes is “moderate-ish” (ε² ≈ 0.057). Everything else is small to negligible.
# 
# About the log1p re-run
# 
# * Spearman uses ranks, so any monotonic transform (like log1p) doesn’t change ranks → the correlations stay the same. That’s why “log1p” table didn’t move.
# 
# What stands out / implications
# 
# * Dislikes decreases with higher stars (as expected) and is the clearest separator.
# 
# * Responses, likes, ranking_score, vote_ratio show visually sensible trends, but on the whole dataset their effects are weak because of zero-inflation and overlap.
# 
# * For relationships to pop out more, control for exposure will be needed (items with more visibility get more of everything).

# %%
# Visualize top features
# pick top features by Spearman’s ρ
top = spearman_df.head(6)["feature"].tolist()

n = len(top); ncols = 3; nrows = (n + ncols - 1)//ncols
fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(10, 3*nrows))
axes = axes.flatten()

for ax, col in zip(axes, top):
    sns.boxplot(data=df, x="stars_cat", y=col, ax=ax, showfliers=False)
    sns.stripplot(data=df, x="stars_cat", y=col, ax=ax, size=2, alpha=0.35, jitter=True)
    ax.set_title(f"{col} by stars")
for j in range(len(top), len(axes)): fig.delaxes(axes[j])
plt.tight_layout(); plt.show()


# %% [markdown]
# Panel-by-panel (x = stars 1–5)
# 
# * **dislikes by stars** – Medians drop as stars rise; a few huge outliers at low stars.
# ⇒ Matches Spearman ρ = −0.18 (strongest signal here) and the largest KW effect (ε² ≈ 0.057).
# 
# * **responses by stars** – Almost all zeros at every star, tiny lift at low stars.
# ⇒ ρ = −0.10, KW significant but small effect (ε² ≈ 0.015).
# 
# * **likes by stars** – Most rows have 0 likes; big tails appear at 4–5★ but medians stay ~0.
# ⇒ Visual “more big values at 5★” but overall ρ ≈ −0.03 (essentially none), KW significant yet tiny effect (ε² ≈ 0.002) due to large N.
# 
# * **ranking_score by stars** – Tends upward, especially at 5★, but still heavy overlap.
# ⇒ ρ ≈ −0.019 (negligible), KW significant with very small effect (ε² ≈ 0.0007).
# 
# * **vote_ratio by stars** – Clear upward shift across stars (lower stars near 0, 5★ near 0.8–0.9).
# ⇒ Spearman shows ρ ≈ −0.017 (basically zero; the sign is dominated by ties/zeros), KW significant but again tiny effect (ε² ≈ 0.0006).
# 
# * **score_log by stars** – Step up at higher stars but lots of ties at 0/low values; broad overlap.
# ⇒ ρ ≈ −0.009 and KW not significant after FDR (tiny effect).
# 

# %% [markdown]
# # 3 Visualization:
# Use effective visuals to support your analysis.
# - 	Include charts such as bar plots, feature importance, and heatmaps
# - 	Make all visualizations interpretable and relevant
# - 	Label axes, legends, and titles clearly
# 

# %%
cat_cols = df.select_dtypes(include="object").columns
df[cat_cols].nunique().sort_values()


# %%
# Class balance by category
cat_cols = cat_cols.tolist()
cat_cols.remove('recipe_name')  # too many levels
cat_cols.remove('text')         # too many levels

for col in cat_cols:
    plt.figure(figsize=(8,4))
    sns.countplot(data=df, x=col, hue="stars")
    plt.title(f"{col} vs stars")
    plt.xticks(rotation=45)
    plt.show()


# %%
! pip install wordcloud

# %%
from wordcloud import WordCloud

# %%
# choose a threshold; you can change to your scale (e.g., 4.5)
hi_mask = df["stars"] >= df["stars"].median()
lo_mask = ~hi_mask

hi_tokens = df.loc[hi_mask, "recipe_name"].apply(tokenize)
lo_tokens = df.loc[lo_mask, "recipe_name"].apply(tokenize)

hi_freq = Counter([t for row in hi_tokens for t in row])
lo_freq = Counter([t for row in lo_tokens for t in row])

hi_wc = WordCloud(width=900, height=500, background_color="white").generate_from_frequencies(
    {w: hi_freq[w] for w in vocab if hi_freq[w] > 0}
)
lo_wc = WordCloud(width=900, height=500, background_color="white").generate_from_frequencies(
    {w: lo_freq[w] for w in vocab if lo_freq[w] > 0}
)

plt.figure(figsize=(14,9))
plt.subplot(2,1,1)
plt.imshow(hi_wc); plt.axis("off"); plt.title("Higher-rated recipes")
plt.subplot(2,1,2)
plt.imshow(lo_wc); plt.axis("off"); plt.title("Lower-rated recipes")
plt.tight_layout()
plt.show()


# %%
# Word lift vs. overall rating
# Highlight how specific words in recipe names relate to average star ratings compared to the overall mean
overall_mean = df["stars"].mean()

means, counts_ = {}, {}
name_lower = df["recipe_name"].str.lower()

for w in vocab:
    m = name_lower.str.contains(rf"\b{re.escape(w)}\b", na=False)
    if m.sum() >= 20:  # min support to avoid noise
        means[w] = df.loc[m, "stars"].mean()
        counts_[w] = int(m.sum())

lift = (
    pd.DataFrame({"mean": pd.Series(means), "n": pd.Series(counts_)})
      .assign(lift=lambda d: d["mean"] - overall_mean)
      .sort_values("lift", ascending=False)
)

# top/bottom 15
k = 15
sub = pd.concat([lift.head(k), lift.tail(k)])

plt.figure(figsize=(8, 7))
y = np.arange(len(sub))
plt.barh(y, sub["lift"].values)  # default style/colors
plt.yticks(y, sub.index)
plt.axvline(0, linestyle="--")
plt.xlabel("Mean stars minus overall mean")
plt.title("Word lift vs. overall rating (min support = 20)")
plt.tight_layout()
plt.show()


# %% [markdown]
# Naming (or ingredients) linked to certain words may influence perception and ratings — with savory meat-related terms skewing lower, and pasta, vegetarian, and dessert-related terms skewing higher.

# %%
# --- build presence matrix for top words ---
def has_word(series, word):
    return series.str.lower().str.contains(rf"\b{re.escape(word)}\b", na=False)

vocab = [w for w, c in freq.most_common(50) if len(w) > 1]  # pick top N

presence = {}
for w in vocab:
    presence[w] = has_word(df["recipe_name"], w).astype(int)

pres_df = pd.DataFrame(presence)

# concat with stars
tmp = pd.concat([pres_df, df["stars"]], axis=1)

# counts of (word × stars)
counts = (
    tmp.melt(id_vars="stars", var_name="word", value_name="present")
      .query("present == 1")
      .groupby(["word", "stars"])
      .size()
      .unstack(fill_value=0)
      .reindex(sorted(df["stars"].dropna().unique()), axis=1, fill_value=0)
)

# row-normalize to show distribution per word
row_sums = counts.sum(axis=1).replace(0, np.nan)
dist = counts.div(row_sums, axis=0).fillna(0)

# optional: order words by mean star
mean_star = (dist * dist.columns.values).sum(axis=1)
dist_sorted = dist.loc[mean_star.sort_values(ascending=False).index]

# plot
plt.figure(figsize=(8, 10))
plt.imshow(dist_sorted.values, aspect="auto", cmap="viridis")
plt.yticks(range(dist_sorted.shape[0]), dist_sorted.index)
plt.xticks(range(dist_sorted.shape[1]), dist_sorted.columns)
plt.xlabel("Stars")
plt.ylabel("Word")
plt.title("Distribution of ratings for recipes containing each word")
plt.colorbar(label="Proportion")
plt.tight_layout()
plt.show()


# %% [markdown]
# The heatmap confirms a strong positive bias in ratings, with most words heavily skewed toward 4 and especially 5-star ratings. That suggests recipes generally receive high ratings regardless of wording. However, certain comfort-food or superlative terms (best, homemade, favorite) linked even more strongly to 5-star clusters, while some savory/neutral terms distribute slightly more evenly across 3–5 stars.

# %% [markdown]
# # 4 Feature Engineering
# 
# The goal here is to create a set of features that are simple but robust, aligned with the main patterns discovered during EDA:
# 
# - **Zero-inflated, skewed counts** (likes, dislikes, responses, user_score, ranking_score)  
#   → apply log1p transforms and add binary presence flags.
# 
# - **Ratios and interactions** help normalize popularity/exposure bias.  
#   → e.g., like ratio, total interactions.
# 
# - **Text-derived features** (basic word/char counts) to capture review length.  
#   → complements TF-IDF embeddings.
# 
# - **Categorical encoding** for region/device/time-related variables.
# 
# This balances interpretability with predictive power.
# 

# %%
# --- Feature Engineering ---
df_fe = df.copy()

# 1) Handle skewed / zero-inflated counts
skewed_cols = ["likes", "dislikes", "responses", "user_score", "ranking_score"]
for col in skewed_cols:
    if col in df_fe.columns:
        df_fe[f"log1p_{col}"] = np.log1p(df_fe[col].clip(lower=0))
        df_fe[f"has_{col}"] = (df_fe[col] > 0).astype(int)

# 2) Ratios and interactions
if all(c in df_fe.columns for c in ["likes", "dislikes"]):
    df_fe["like_ratio"] = df_fe["likes"] / (df_fe["likes"] + df_fe["dislikes"] + 1.0)

if all(c in df_fe.columns for c in ["likes", "dislikes", "responses"]):
    df_fe["total_interactions"] = (
        df_fe["likes"].fillna(0) +
        df_fe["dislikes"].fillna(0) +
        df_fe["responses"].fillna(0)
    )

# 3) Text-derived stats
if "text" in df_fe.columns:
    df_fe["text_word_count"] = df_fe["text"].fillna("").apply(lambda x: len(x.split()))
    df_fe["text_char_count"] = df_fe["text"].fillna("").apply(lambda x: len(x.replace(" ", "")))


# Check result
df_fe.head()


# %% [markdown]
# ### Summary of Engineered Features
# - **Log-transformed counts:** log1p_likes, log1p_dislikes, log1p_responses, log1p_user_score, log1p_ranking_score
# - **Presence flags:** has_likes, has_dislikes, has_responses, has_user_score, has_ranking_score
# - **Ratios:** like_ratio, total_interactions
# - **Text stats:** text_word_count, text_char_count
# 
# These will be combined later with TF-IDF features (from recipe names) and categorical encodings in the modeling pipeline.
# 

# %%
# quick Spearman heatmap over engineered numeric features 
import matplotlib.pyplot as plt

num_cols_for_heat = [c for c in df_fe.columns
                     if pd.api.types.is_numeric_dtype(df_fe[c]) and c != "stars"]

corr = df_fe[num_cols_for_heat].corr(method="spearman")
plt.figure(figsize=(8,6))
plt.imshow(corr, aspect="auto")
plt.title("Spearman Correlations (Engineered Numeric Features)")
plt.xticks(range(len(num_cols_for_heat)), num_cols_for_heat, rotation=90)
plt.yticks(range(len(num_cols_for_heat)), num_cols_for_heat)
plt.colorbar()
plt.tight_layout()
plt.show()


# %% [markdown]
# ### Correlation Heatmap (Spearman) — Key Takeaways
# - **Engagement cluster:** likes, dislikes, responses and their log/flag versions strongly co-move, as expected for exposure-driven interactions. total_interactions sits at the center of this cluster.
# - **Ratios track together:** like_ratio and vote_ratio are tightly aligned, signaling they encode a similar “approval balance.”
# - **Text length proxies:** text_word_count and text_char_count are near-collinear; keep one of them in regularized models to avoid redundancy.
# - **Rank signals:** ranking_score/log1p_ranking_score show meaningful association with raw interactions and ratios, suggesting platform ranking correlates with community feedback.
# - **Weak/near-zero ties:** user_score and log1p_user_score exhibit low correlations with most interaction features—useful as a potentially independent predictor.
# 
# The heatmap validates feature engineering: 
# * (i) log transforms reduce extreme skew while preserving rank-order signal; 
# * (ii) ratio features capture a different axis (sentiment/approval) than raw counts (exposure).
# 

# %% [markdown]
# # 5 Model Building:
# Build classification models to predict the exact star rating (1–5) of a review.
# - 	Use at least two models (such as Logistic Regression, Random Forest)
# - 	Perform a proper train-test split
# - 	Apply appropriate preprocessing (e.g., scaling, encoding)
# - 	Tune hyperparameters if needed
# #### Multiclass Logistic Regression

# %%
# 1. Define target and features
# --------------------------
y = df_fe["stars"].astype(int)
X = df_fe.drop(columns=["stars", "stars_cat"])  # drop target + duplicate

# --------------------------
# 2. Feature groups
# --------------------------
# categorical
cat_cols = ["region", "device_type"]

# numeric (all engineered numeric features except IDs/text)
num_cols = [
    "likes_score", "dislike_index", "response_level", "ranking_value", "vote_ratio", "score_log",
    "user_score", "responses", "likes", "dislikes", "ranking_score",
    "text_word_count", "text_char_count",
    "log1p_likes", "has_likes",
    "log1p_dislikes", "has_dislikes",
    "log1p_responses", "has_responses",
    "log1p_user_score", "has_user_score",
    "log1p_ranking_score", "has_ranking_score",
    "like_ratio", "total_interactions"
]

# text
text_col = "recipe_name"

# --------------------------
# 3. Transformers
# --------------------------
# numeric pipeline: scale everything
num_transformer = Pipeline(steps=[
    ("scaler", StandardScaler())
])

# categorical pipeline: one-hot encode
cat_transformer = OneHotEncoder(handle_unknown="ignore")

# text pipeline: TF-IDF
text_transformer = TfidfVectorizer(
    max_features=2000,
    stop_words="english",
    ngram_range=(1, 2),
    min_df=5
)

# --------------------------
# 4. ColumnTransformer
# --------------------------
preprocess = ColumnTransformer(
    transformers=[
        ("num", num_transformer, num_cols),
        ("cat", cat_transformer, cat_cols),
        ("txt", text_transformer, text_col)
    ],
    remainder="drop",
    sparse_threshold=0.3
)

# --------------------------
# 5. Classifier
# --------------------------
clf = LogisticRegression(
    max_iter=2000,
    multi_class="multinomial",
    class_weight="balanced"
)

pipe = Pipeline(steps=[
    ("preprocess", preprocess),
    ("model", clf)
])

# --------------------------
# 6. Train/test split + fit
# --------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

pipe.fit(X_train, y_train)

print("Train accuracy:", pipe.score(X_train, y_train))
print("Test  accuracy:", pipe.score(X_test, y_test))
print("\nClassification report:\n", classification_report(y_test, pipe.predict(X_test)))
print("\nConfusion matrix:\n", confusion_matrix(y_test, pipe.predict(X_test)))


# %% [markdown]
# ### Results Commentary
# 
# **Overall performance.** Test accuracy is **38.6%**, with a **macro-F1 of 0.19**. This reflects the strong **class imbalance** and the model’s difficulty distinguishing minority classes (1–3★).
# 
# **Majority-class context.** The test set is heavily skewed toward **5★ (2,767 / 3,298 ≈ 84%)**. Because we used `class_weight="balanced"`, the classifier became **conservative** about predicting 5★ (high precision = **0.90**) but **low recall = 0.40**, which drags down accuracy.
# 
# **Minority classes.** 1–3★ have very **low precision/recall** (F1 ≤ 0.11). Given EDA showed small effect sizes and zero-inflated signals, there’s limited separability among these classes using current features.
# 
# **Confusion patterns.** Many true 5★ are predicted as 4★/3★/2★, and most 1–3★ scatter across 4★/5★. This suggests (a) **overlap** in feature distributions and (b) **exposure/popularity effects** dominating raw counts.
# 
# **Implication.** To improve: (1) simplify and de-duplicate features, (2) **leverage review text** (not just recipe name), and (3) revisit imbalance handling/thresholds. If the goal tolerates it, **ordinal or collapsed labels** (e.g., 1–2 = Low, 3–4 = Mid, 5 = High) can also stabilize performance.
# 

# %%
# Interpretable LR with num+cat only for feature importance

from sklearn.linear_model import LogisticRegression

preprocess_numcat = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(with_mean=True, with_std=True), num_cols),   # you already defined num_cols
        ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),          # you already defined cat_cols
    ],
    remainder="drop",
    sparse_threshold=0.0
)

lr_numcat = Pipeline([
    ("preprocess", preprocess_numcat),
    ("model", LogisticRegression(max_iter=2000, multi_class="multinomial", class_weight="balanced"))
])

X_tr, X_te, y_tr, y_te = train_test_split(X[num_cols + cat_cols], y, test_size=0.2, stratify=y, random_state=42)
lr_numcat.fit(X_tr, y_tr)
print("Num+Cat only (LR) Test accuracy:", lr_numcat.score(X_te, y_te))

# Recover feature names
feat_names_num = lr_numcat.named_steps["preprocess"].named_transformers_["num"].get_feature_names_out(num_cols)
feat_names_cat = lr_numcat.named_steps["preprocess"].named_transformers_["cat"].get_feature_names_out(cat_cols)
feat_names = np.concatenate([feat_names_num, feat_names_cat])

# Coefficients: shape (n_classes, n_features); we can summarize by overall magnitude
coef = lr_numcat.named_steps["model"].coef_  # multinomial
coef_abs = np.mean(np.abs(coef), axis=0)
top_idx = np.argsort(coef_abs)[-15:][::-1]
top_feats = [(feat_names[i], coef_abs[i]) for i in top_idx]

print("\nTop 15 (by |coef| averaged across classes) — Num+Cat only:")
for name, val in top_feats:
    print(f"{name:40s} {val: .4f}")


# %% [markdown]
# #### What Most Influences Star Ratings (Interpretable LR — Num+Cat Only)
# **Test accuracy (num+cat only): 0.547** — as expected, this lags behind the text-rich model, but it gives a clear drivers view.
# 
# **Strongest positive/negative drivers (by |coef|):**
# - **Engagement intensity dominates:** log1p_likes (#1) and log1p_dislikes (top-5) carry the most weight; higher likes push predictions toward higher stars, while dislikes pull them down.
# - **Platform ranking signal:** log1p_ranking_score and ranking_value rank highly, indicating platform quality/reputation aligns with star outcomes.
# - **Review verbosity:** text_char_count/text_word_count matter—longer reviews tend to be more polarized (helps the classifier separate classes).
# - **Approval balance:** like_ratio / vote_ratio add sentiment-like information beyond raw counts.
# - **Responsiveness:** has_responses and log1p_responses suggest threads with creator/community replies skew toward clearer (often higher) star outcomes.
# - **Context effects (smaller, but non-zero):** region_north, region_west, device_type_mobile, and has_ranking_score have modest influence compared to engagement and ranking.
# 
# **Takeaway:** Even without text, **engagement + platform rank + verbosity** explain much of the variance. This aligns with broader finding that **text features** further boost separability, especially between adjacent ratings (e.g., 4 vs. 5).
# 

# %% [markdown]
# #### Feature Selection / Sanity Check
# * Keep a curated numeric set (ratios, log counts, flags, simple text length).
# 
# * Keep categoricals (region, device_type) with OHE.
# 
# * Keep TF-IDF on recipe_name only for this step (we’ll add full review text next).
# 
# * Still use Logistic Regression; keep class_weight="balanced" for apples-to-apples.

# %%
# ===== Curate features =====
y = df_fe["stars"].astype(int)
X = df_fe.drop(columns=["stars", "stars_cat"])  # drop target & duplicate

cat_cols = ["region", "device_type"]

# Keep small, meaningful numeric core (drop raw counts when log versions exist)
num_cols = [
    "vote_ratio", "like_ratio",
    "total_interactions",
    "text_word_count", "text_char_count",
    "log1p_likes", "log1p_dislikes", "log1p_responses",
    "log1p_user_score", "log1p_ranking_score",
    "has_likes", "has_dislikes", "has_responses", "has_user_score", "has_ranking_score",
    # optional: keep exactly ONE of these global popularity scores (not all)
    "ranking_value"
]
num_cols = [c for c in num_cols if c in X.columns]

text_name_col = "recipe_name"

# ===== Transformers =====
num_tf = Pipeline([("scaler", StandardScaler())])
cat_tf = OneHotEncoder(handle_unknown="ignore")
name_tfidf = TfidfVectorizer(max_features=2000, stop_words="english",
                             ngram_range=(1,2), min_df=5)

preprocess = ColumnTransformer(
    transformers=[
        ("num", num_tf, num_cols),
        ("cat", cat_tf, cat_cols),
        ("name", name_tfidf, text_name_col),
    ],
    remainder="drop",
    sparse_threshold=0.3
)

clf = LogisticRegression(max_iter=2000, multi_class="multinomial", class_weight="balanced")

pipe = Pipeline([("preprocess", preprocess), ("model", clf)])

# ===== Train / Evaluate =====
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, stratify=y, random_state=42
)

pipe.fit(X_train, y_train)
print("Train accuracy:", pipe.score(X_train, y_train))
print("Test  accuracy:", pipe.score(X_test, y_test))
print("\nClassification report:\n", classification_report(y_test, pipe.predict(X_test)))
print("\nConfusion matrix:\n", confusion_matrix(y_test, pipe.predict(X_test)))


# %% [markdown]
# #### Full Review Text
# 

# %%
# ===== Add review text =====
text_body_col = "text"  # 2 missing, TF-IDF will handle empty strings via fillna

# Rebuild the ColumnTransformer with TWO text branches
preprocess_2 = ColumnTransformer(
    transformers=[
        ("num", num_tf, num_cols),
        ("cat", cat_tf, cat_cols),
        ("name", TfidfVectorizer(max_features=2000, stop_words="english",
                                 ngram_range=(1,2), min_df=5), text_name_col),
        ("body", TfidfVectorizer(max_features=5000, stop_words="english",
                                 ngram_range=(1,2), min_df=5), text_body_col),
    ],
    remainder="drop",
    sparse_threshold=0.3
)

pipe_2 = Pipeline([("preprocess", preprocess_2),
                   ("model", LogisticRegression(max_iter=2000,
                                                multi_class="multinomial",
                                                class_weight="balanced"))])

X2 = X.copy()
X2[text_body_col] = X2[text_body_col].fillna("")

X_tr, X_te, y_tr, y_te = train_test_split(
    X2, y, test_size=0.20, stratify=y, random_state=42
)

pipe_2.fit(X_tr, y_tr)
print("Test accuracy (with review text):", pipe_2.score(X_te, y_te))
print("\nClassification report:\n", classification_report(y_te, pipe_2.predict(X_te)))
print("\nConfusion matrix:\n", confusion_matrix(y_te, pipe_2.predict(X_te)))


# %%
# Multiclass ROC-AUC (OvR macro) for 5-class LR+TFIDF model 

from sklearn.preprocessing import label_binarize
from sklearn.metrics import roc_auc_score, RocCurveDisplay

# Ensure we have X2, y and a fitted pipe_2 
classes_sorted = np.sort(y.unique())
y_test_bin = label_binarize(y_test, classes=classes_sorted)

# predict_proba from the balanced LR+TFIDF pipeline
y_proba = pipe_2.predict_proba(X_test)

macro_roc_auc = roc_auc_score(y_test_bin, y_proba, average="macro", multi_class="ovr")
print(f"Macro ROC-AUC (5-class, LR+TFIDF balanced): {macro_roc_auc:.3f}")


# %%
# Plot per-class ROC curves (optional, quick view)
from sklearn.metrics import roc_curve
plt.figure(figsize=(6,5))
for i, cls in enumerate(classes_sorted):
    fpr, tpr, _ = roc_curve(y_test_bin[:, i], y_proba[:, i])
    plt.plot(fpr, tpr, label=f"Class {cls}")
plt.plot([0,1],[0,1],"--")
plt.title("One-vs-Rest ROC Curves (5-class LR+TFIDF)")
plt.xlabel("FPR"); plt.ylabel("TPR")
plt.legend()
plt.tight_layout()
plt.show()


# %% [markdown]
# #### Multiclass ROC–AUC (OvR) — Interpretation
# - **Overall ranking quality:** **Macro ROC–AUC = 0.826** for the 5-class LR+TF-IDF (balanced). That’s a strong result for a fine-grained (1–5) classification under class imbalance.
# - **Per-class curves (visual read):**
#   - The **Class 1** curve rises fastest (highest TPR at low FPR), indicating the model ranks 1-star reviews most distinctly from others.
#   - **Classes 2–3–5** show solid separation with smooth curves above the diagonal—good discriminability.
#   - **Class 4** lags (curve closer to the diagonal), meaning it’s the hardest to separate; common in ordinal setups where 4 sits near 5.
# 

# %% [markdown]
# ### Imbalance Handling Toggle
# Compare with vs. without balanced weights after adding review text

# %%
# A) Balanced (current)
pipe_bal = pipe_2
print("Balanced test accuracy:", pipe_bal.score(X_te, y_te))

# B) Unbalanced (let majority dominate a bit more)
pipe_unbal = Pipeline([("preprocess", preprocess_2),
                       ("model", LogisticRegression(max_iter=2000,
                                                    multi_class="multinomial",
                                                    class_weight=None))])
pipe_unbal.fit(X_tr, y_tr)
print("Unbalanced test accuracy:", pipe_unbal.score(X_te, y_te))

# Compare macro-F1 for fairness to minority classes
from sklearn.metrics import f1_score
pred_bal = pipe_bal.predict(X_te)
pred_unbal = pipe_unbal.predict(X_te)
print("Macro-F1 (balanced):  ", f1_score(y_te, pred_bal, average="macro"))
print("Macro-F1 (unbalanced):", f1_score(y_te, pred_unbal, average="macro"))


# %% [markdown]
# ### Collapsed Labels
# Ordinal-ish buckets: Low (1–2), Mid (3–4), High (5)

# %%
# ===== 3-class classification =====
# buckets: 1-2★, 3-4★, 5★
def bucketize(s):
    return np.select([s<=2, (s>=3)&(s<=4), s==5], [0,1,2]).astype(int)

y_3 = bucketize(y)

X3_tr, X3_te, y3_tr, y3_te = train_test_split(X2, y_3, test_size=0.2, stratify=y_3, random_state=42)

pipe_3 = Pipeline([("preprocess", preprocess_2),
                   ("model", LogisticRegression(max_iter=2000, multi_class="multinomial", class_weight="balanced"))])
pipe_3.fit(X3_tr, y3_tr)

print("3-class accuracy:", pipe_3.score(X3_te, y3_te))
print("\nClassification report:\n", classification_report(y3_te, pipe_3.predict(X3_te)))
print("\nConfusion matrix:\n", confusion_matrix(y3_te, pipe_3.predict(X3_te)))


# %% [markdown]
# ### Tree Benchmark (no text)
# Gradient Boosting on numeric + OHE categorical

# %%
# numeric+cat only
num_cols_tree = num_cols
cat_cols_tree = cat_cols

pre_tree = ColumnTransformer(
    transformers=[
        ("num", Pipeline([("imp", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]), num_cols_tree),
        ("cat", Pipeline([("imp", SimpleImputer(strategy="most_frequent")),
                          ("ohe", OneHotEncoder(handle_unknown="ignore"))]), cat_cols_tree),
    ],
    remainder="drop"
)

tree = Pipeline([("pre", pre_tree),
                 ("clf", HistGradientBoostingClassifier(random_state=42))])

Xt_tr, Xt_te, yt_tr, yt_te = train_test_split(
    df_fe[num_cols_tree + cat_cols_tree], y, test_size=0.2, stratify=y, random_state=42
)

tree.fit(Xt_tr, yt_tr)
print("Tree (no-text) accuracy:", tree.score(Xt_te, yt_te))
print("\nClassification report:\n", classification_report(yt_te, tree.predict(Xt_te)))
print("\nConfusion matrix:\n", confusion_matrix(yt_te, tree.predict(Xt_te)))


# %% [markdown]
# # 6 Model Evaluation
# 
# This section evaluates the predictive performance of different models and feature sets.  
# We proceed step by step, starting with a simple logistic regression and progressively adding features or reframing the target variable.
# 
# ---
# 
# ### Step 1 – Logistic Regression (Numeric + Recipe Name)
# 
# - **Test Accuracy:** 0.39  
# - **Macro-F1:** 0.19  
# - **Observation:** Performance on minority classes (1–3★) is very weak, with recall below 0.20.  
# - Confusion matrix shows most cases collapsed into 5★ predictions.  
# - Numeric features and recipe name alone do not provide enough discriminative power.
# 
# ---
# 
# ### Step 2 – Logistic Regression + Review Text (TF-IDF)
# 
# - **Test Accuracy:** 0.72  
# - **Macro-F1:** 0.40  
# - **Observation:** Adding the full review body as TF-IDF features substantially improves performance.  
# - Minority classes (1–4★) gain recall, while precision on 5★ remains very high (0.95).  
# - This highlights the strong predictive signal in textual content.
# 
# ---
# 
# ### Step 3 – Balanced vs. Unbalanced Logistic Regression
# 
# - **Balanced Logistic Regression**  
#   - Accuracy = 0.72  
#   - Macro-F1 = 0.40  
#   - Better fairness across all classes.  
# 
# - **Unbalanced Logistic Regression**  
#   - Accuracy = 0.85  
#   - Macro-F1 = 0.34  
#   - Inflated accuracy due to majority-class bias (predicts 5★ most of the time).  
# 
# - **Conclusion:** Balanced class weights are essential to avoid “fake” accuracy that ignores minority classes.
# 
# ---
# 
# ### Step 4 – Ordinal Buckets (Low = 1–2, Mid = 3–4, High = 5)
# 
# - **Test Accuracy:** 0.77  
# - **Macro-F1:** 0.58  
# - **Observation:** Collapsing into three categories yields a more robust model.  
# - Recall improves for Low (0.57) and Mid (0.54) classes, while High (5★) remains strong.  
# - This framing reduces noise and imbalance, and is recommended when fine-grained prediction is not critical.
# 
# ---
# 
# ### Step 5 – Gradient Boosting (Numeric + Categorical only, no text)
# 
# - **Test Accuracy:** 0.84  
# - **Macro-F1:** 0.27  
# - **Observation:** Despite high accuracy, the model predicts 5★ almost exclusively.  
# - Minority classes are ignored (recall ≈ 0 for 4★ and below).  
# - Confirms that **review text is indispensable** for balanced star prediction.
# 
# 

# %% [markdown]
# ### 6.1 Evaluation Plots
# 
# The figures below summarize performance for:
# - **Balanced Logistic Regression (5-class)** using TF-IDF on `recipe_name` + `text` + engineered numeric + OHE categorical.
# - **Balanced Logistic Regression (3-class ordinal buckets)** where 0=Low (1–2★), 1=Mid (3–4★), 2=High (5★).
# 
# We include:
# 1) Confusion matrices  
# 2) Bar charts for precision / recall / F1 by class
# 

# %%
# --- Helpers (Matplotlib-only, one chart per figure) ---

def plot_confusion_matrix(y_true, y_pred, title="Confusion Matrix", class_names=None):
    cm = confusion_matrix(y_true, y_pred)
    if class_names is None:
        labels = np.unique(np.concatenate([y_true, y_pred]))
        class_names = [str(c) for c in labels]
    plt.figure(figsize=(6,5))
    plt.imshow(cm, aspect="auto")
    plt.title(title)
    plt.xlabel("Predicted")
    plt.ylabel("True")
    plt.xticks(ticks=np.arange(len(class_names)), labels=class_names, rotation=0)
    plt.yticks(ticks=np.arange(len(class_names)), labels=class_names)
    # overlay counts
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            plt.text(j, i, str(cm[i, j]), ha="center", va="center")
    plt.colorbar()
    plt.tight_layout()
    plt.show()

def plot_class_report_bars(y_true, y_pred, title_prefix=""):
    report = classification_report(y_true, y_pred, output_dict=True, zero_division=0)
    # collect per-class rows only (ignore 'accuracy', 'macro avg', 'weighted avg')
    class_keys = [k for k in report.keys() if k.isdigit()]
    class_keys_sorted = sorted(class_keys, key=lambda x: int(x))
    metrics = ["precision", "recall", "f1-score"]
    for m in metrics:
        vals = [report[k][m] for k in class_keys_sorted]
        plt.figure(figsize=(6,4))
        x = np.arange(len(class_keys_sorted))
        plt.bar(x, vals)
        plt.title(f"{title_prefix}{m.capitalize()} by Class")
        plt.xticks(ticks=x, labels=class_keys_sorted)
        plt.ylim(0, 1)
        plt.ylabel(m.capitalize())
        plt.tight_layout()
        plt.show()


# %%
# --- 5-class (Balanced Logistic Regression + text) ---

# Assumes you already built pipe_2 (balanced) and X2, y from prior steps:
#   - preprocess_2 includes numeric + OHE + TF-IDF(name) + TF-IDF(text)
#   - pipe_2 = Pipeline([("preprocess", preprocess_2), ("model", LogisticRegression(..., class_weight="balanced"))])
#   - X2["text"] already filled with "" for NaNs, y = df_fe["stars"].astype(int)

from sklearn.model_selection import train_test_split

X_tr, X_te, y_tr, y_te = train_test_split(
    X2, y, test_size=0.20, stratify=y, random_state=42
)

# Fit (or reuse your fitted pipe_2)
pipe_2.fit(X_tr, y_tr)
pred5 = pipe_2.predict(X_te)

# Plots
plot_confusion_matrix(y_te, pred5, title="5-Class Confusion Matrix (Balanced Logistic + Text)", 
                      class_names=[str(c) for c in sorted(np.unique(y_te))])
plot_class_report_bars(y_te, pred5, title_prefix="5-Class ")


# %%
# --- 3-class ordinal (Balanced Logistic Regression + text) ---

import numpy as np

def bucketize(s):
    return np.select([s<=2, (s>=3)&(s<=4), s==5], [0,1,2]).astype(int)

y_3 = bucketize(y)

X3_tr, X3_te, y3_tr, y3_te = train_test_split(
    X2, y_3, test_size=0.20, stratify=y_3, random_state=42
)

pipe_3 = Pipeline([
    ("preprocess", preprocess_2),  # same features: numeric + OHE + name TF-IDF + text TF-IDF
    ("model", LogisticRegression(max_iter=2000, multi_class="multinomial", class_weight="balanced"))
])

pipe_3.fit(X3_tr, y3_tr)
pred3 = pipe_3.predict(X3_te)

# Plots
plot_confusion_matrix(y3_te, pred3, title="3-Class Confusion Matrix (Balanced Logistic + Text)", 
                      class_names=["Low (1–2)", "Mid (3–4)", "High (5)"])

# For the bars, sklearn's report will output classes as "0,1,2"
plot_class_report_bars(y3_te, pred3, title_prefix="3-Class ")


# %% [markdown]
# - The **5-class confusion matrix** shows where minority classes (1–4★) still confuse with adjacent classes, while 5★ dominates but is no longer over-predicted (balanced weights).
# - The **3-class matrix** should show cleaner separation, with “High (5★)” well recognized and improved recall for “Low” and “Mid.”
# - The bar charts help spot which specific class needs attention (typically Low/Mid for precision, sometimes recall).
# 

# %%


# %% [markdown]
# # 7. Insights, Interpretation, and Reporting
# 
# ### Executive Summary
# - **Text matters most.** Adding TF-IDF over the review body lifted test accuracy from ~0.39 to ~0.72 and macro-F1 from ~0.19 to ~0.40.
# - **Fair > “fake” accuracy.** Unbalanced models inflate accuracy by predicting 5★; balanced logistic regression provides fairer performance across all classes.
# - **Pragmatic framing helps.** Collapsing labels to **Low (1–2), Mid (3–4), High (5)** improves stability (accuracy ~0.77; macro-F1 ~0.58).
# - **Numeric-only signals are weak.** Engagement counts are zero-inflated and exposure-driven; they help after log/ratio transforms but don’t replace text.
# 
# ---
# 
# ### Key Findings
# 1. **Best simple model:** Balanced multinomial Logistic Regression with:
#    - TF-IDF over **text** (review body) and **recipe_name**
#    - One-hot **region**, **device_type**
#    - Scaled numeric engineered features (log1p counts, presence flags, ratios)
# 2. **Drivers of higher stars (qualitative):**
#    - Higher **vote/like ratios** trend with higher ratings; **dislikes** inversely correlate.
#    - Certain words/tones in names/text associate with higher/lower ratings (e.g., superlatives and comfort terms skew higher).
# 3. **Engagement patterns & exposure:**
#    - **likes, dislikes, responses, user_score** are **zero-inflated** with long tails.
#    - **log1p** transforms and **presence flags** reduce skew; ratios (e.g., like_ratio) help normalize exposure.
# 
# ---
# 
# ### Recommendations
# - **Deploy** the balanced LR + TF-IDF pipeline as the **baseline** for 5-class prediction and **also** report the 3-class (Low/Mid/High) variant for robust, operational summaries.
# - **Monitor** both overall accuracy and **macro-F1** to avoid majority-class bias.
# - **Add lightweight sentiment** (lexicon score or simple polarity) if you need a quick boost without heavy modeling.
# - **Consider ordinal approaches** (ordinal logistic / thresholded probabilities) if exact 1–5 ordering is more important than class labels.
# 
# ---
# 
# ### Potential Applications
# - **Quality Ops / CX:** Flag likely-low reviews for proactive follow-up; auto-route to support.
# - **Creator guidance:** While users draft reviews/recipes, nudge phrasing and clarity associated with higher satisfaction.
# - **Content refresh:** Prioritize recipes predicted as Mid/Low for improvements (instructions, photos, ingredient clarity).
# 
# ---
# 
# ### Limitations
# - **Label imbalance:** Dataset is heavily skewed to 5★; minority classes (1–3★) have limited support.
# - **Assumption on 0★:** Rows with "stars == 0" were treated as unrated and removed.
# - **Exposure bias:** Engagement counts reflect popularity/visibility, not just quality.
# - **Single split:** Results reported on one stratified split; k-fold CV would better quantify variance.
# - **Style sensitivity:** Text models may learn stylistic correlates (tone/phrasing), not only true quality.
# 
# ---
# 
# ### Reproducibility Notes
# - Stratified train/test split (80/20), fixed random_state=42.
# - Logistic Regression: multi_class="multinomial", class_weight="balanced", max_iter=2000.
# - TF-IDF: unigrams+bigrams, min_df=5; max_features ~2k (name) and ~5k (text).
# - Numeric scaling via StandardScaler; categorical via OneHotEncoder(handle_unknown="ignore").
# 
# ---
# 
# ### Appendix A — Engineered Features (one-liners)
# - **log1p_***: Log-scaled counts (likes, dislikes, responses, user_score, ranking_score) to tame long tails.
# - **has_***: Binary flags for presence (>0) of each count feature.
# - **like_ratio**: likes / (likes + dislikes + 1); normalizes by total votes.
# - **total_interactions**: likes + dislikes + responses; proxy for exposure.
# - **text_word_count, text_char_count**: Review length proxies.
# - **Categoricals**: region, device_type (OHE).
# - **Text**: TF-IDF on recipe_name and full review text.
# 
# ---
# 
# ### Appendix B — Best Baseline Pipeline (summary)
# - **Preprocessing (ColumnTransformer):**
#   - Numeric: scale engineered features (StandardScaler)
#   - Categorical: OHE on region, device_type
#   - Text: TF-IDF on recipe_name (2k feats) + text (5k feats), n-grams (1,2), min_df=5
# - **Model:** Logistic Regression (multinomial, balanced)
# - **Primary metrics:** Accuracy and **macro-F1** (report both 5-class and 3-class)
# 

# %%
# === FINAL CELL — Baseline Refit & Compact Summary (5-class and 3-class) ===

# 1) Define features & target
# -----------------------------
cat_cols = ["region", "device_type"]

# Curated numeric core (simple but robust)
num_cols = [
    "vote_ratio", "like_ratio",
    "total_interactions",
    "text_word_count", "text_char_count",
    "log1p_likes", "log1p_dislikes", "log1p_responses",
    "log1p_user_score", "log1p_ranking_score",
    "has_likes", "has_dislikes", "has_responses", "has_user_score", "has_ranking_score",
    "ranking_value",  # keep one global popularity signal
]
num_cols = [c for c in num_cols if c in df_fe.columns]

text_name = "recipe_name"
text_body = "text"

# Target
y5 = df_fe["stars"].astype(int)

# Feature frame
use_cols = cat_cols + num_cols + [text_name, text_body]
X = df_fe[use_cols].copy()
X[text_body] = X[text_body].fillna("")
X[text_name] = X[text_name].fillna("")

# -----------------------------
# 2) Preprocessing & model
# -----------------------------
num_tf = Pipeline([("scaler", StandardScaler())])
cat_tf = OneHotEncoder(handle_unknown="ignore")

preprocess = ColumnTransformer(
    transformers=[
        ("num", num_tf, num_cols),
        ("cat", cat_tf, cat_cols),
        ("name", TfidfVectorizer(max_features=2000, stop_words="english",
                                 ngram_range=(1,2), min_df=5), text_name),
        ("body", TfidfVectorizer(max_features=5000, stop_words="english",
                                 ngram_range=(1,2), min_df=5), text_body),
    ],
    remainder="drop",
    sparse_threshold=0.3,
)

clf_bal = LogisticRegression(
    max_iter=2000,
    multi_class="multinomial",
    class_weight="balanced",
)

pipe5 = Pipeline([
    ("preprocess", preprocess),
    ("model", clf_bal),
])

# -----------------------------
# 3) Train/test split & fit (5-class)
# -----------------------------
X5_tr, X5_te, y5_tr, y5_te = train_test_split(
    X, y5, test_size=0.20, stratify=y5, random_state=42
)
pipe5.fit(X5_tr, y5_tr)
y5_pred = pipe5.predict(X5_te)

# -----------------------------
# 4) 3-class (Low/Mid/High) setup
# -----------------------------
def bucketize(s):
    # 0=Low (1–2), 1=Mid (3–4), 2=High (5)
    return np.select([s<=2, (s>=3)&(s<=4), s==5], [0,1,2]).astype(int)

y3 = bucketize(y5)
X3_tr, X3_te, y3_tr, y3_te = train_test_split(
    X, y3, test_size=0.20, stratify=y3, random_state=42
)
pipe3 = Pipeline([
    ("preprocess", preprocess),
    ("model", LogisticRegression(max_iter=2000, multi_class="multinomial", class_weight="balanced")),
])
pipe3.fit(X3_tr, y3_tr)
y3_pred = pipe3.predict(X3_te)

# -----------------------------
# 5) Compact summary table
# -----------------------------
def summarize(y_true, y_pred):
    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "macro_f1": f1_score(y_true, y_pred, average="macro"),
        "weighted_f1": f1_score(y_true, y_pred, average="weighted"),
    }

summary = pd.DataFrame([
    {"setup": "5-class (balanced LR + TF-IDF)", **summarize(y5_te, y5_pred)},
    {"setup": "3-class (Low/Mid/High; balanced LR + TF-IDF)", **summarize(y3_te, y3_pred)},
]).round(3)

print(summary.to_string(index=False))

# quick reports
print("\n5-class classification report:\n", classification_report(y5_te, y5_pred))
print("\n3-class classification report:\n", classification_report(y3_te, y3_pred))



