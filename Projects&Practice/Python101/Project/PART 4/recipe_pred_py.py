# %% [markdown]
# ## Comprehensive Case Study – Recipe Review Ratings Prediction
#  
# 
# Deliver a structured analysis and a final report containing your findings, supported by data, visualizations, and code.
# 
# 1 - Data Clenaing
# 2 - Exploratory Data Aalysis
# 3 - Visualization
# 4 - Feature Engineering
# 5 - Model Building
# 6 - Model Evaluation
# 7 - Insights, Interpretation, and Reporting

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

# check unique values in each non numeric column
for i in df.select_dtypes(include=['object']).columns:
    print(f"\n Unique values in '{i}':")
    print(df[i].value_counts())



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
df

# %% [markdown]
# Upon a closer look, many columns act as IDs or indexes that cannot be generalized. Since the goal is to create a prediction model, those will be dropped to avoid unecessary or useless work.

# %%
# Drop: IDs (recipe_code, user_index, user_id, created_at, comment_id, recipe_name, user_name).
df = df.drop(columns=["recipe_code", "user_index", "user_id", "created_at", "comment_id", "user_name"])
# creating date showed a small window of time, so it won't be useful for prediction
df

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
# Bag-of-words / TF-IDF on recipe_name
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer(
    max_features=500,  # keep top words only
    stop_words="english",
    ngram_range=(1,2)  # unigrams + bigrams
)
X_text = vectorizer.fit_transform(df["recipe_name"].fillna(""))


# %%
# Keyword analysis
import pandas as pd
from collections import Counter

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
import numpy as np
import pandas as pd
import re
from collections import Counter
import matplotlib.pyplot as plt

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
# Check Class balance
counts = df["stars"].value_counts().sort_index()
props  = (counts / counts.sum()).round(3)
display(pd.DataFrame({"count": counts, "proportion": props}))


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
import seaborn as sns
import matplotlib.pyplot as plt

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
pip install wordcloud

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
# naming (or ingredients) linked to certain words may influence perception and ratings — with savory meat-related terms skewing lower, and pasta, vegetarian, and dessert-related terms skewing higher.

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re

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
plt.figure(figsize=(10, 12))
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
# # 4 Feature Engineering:
# Create or refine features to enhance model quality.
# - 	Transform or derive features
# - 	Encode categorical variables
# - 	Normalize or scale features as appropriate
# 

# %%
df.info()

# %% [markdown]
# # 5 Model Building:
# Build classification models to predict the exact star rating (1–5) of a review.
# - 	Use at least two models (such as Logistic Regression, Random Forest)
# - 	Perform a proper train-test split
# - 	Apply appropriate preprocessing (e.g., scaling, encoding)
# - 	Tune hyperparameters if needed
# 

# %%
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

# Use recipe names, fill NaNs
names = df["recipe_name"].fillna("")
y = df["stars"]

# Build pipeline
pipe = Pipeline([
    ("tfidf", TfidfVectorizer(
        max_features=1000,   # top N words
        stop_words="english",
        ngram_range=(1,2)    # include unigrams+bigrams
    )),
    ("clf", LogisticRegression(
        max_iter=1000,
        multi_class="multinomial"
    ))
])

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(names, y, test_size=0.2, stratify=y, random_state=42)

pipe.fit(X_train, y_train)
print("Validation accuracy:", pipe.score(X_test, y_test))


# %%
import numpy as np

tfidf = pipe.named_steps["tfidf"]
clf = pipe.named_steps["clf"]

feature_names = np.array(tfidf.get_feature_names_out())
coefs = clf.coef_  # shape = (n_classes, n_features)

# Example: top words for 5★
top_idx = np.argsort(coefs[4])[-20:]
print("Top 20 words for 5★:", feature_names[top_idx])


# %% [markdown]
# Step 4 — Integration with your full model
# 
# Use ColumnTransformer to combine:
# 
# TF-IDF features from recipe_name
# 
# Numeric engineered features (likes, dislikes, vote_ratio, etc.)
# 
# Categorical features (region, device_type)
# 
# So your pipeline can handle everything end-to-end.

# %%
# --- 0) Imports
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler, FunctionTransformer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.feature_extraction.text import TfidfVectorizer

# --- 1) Define target and drop unrated
df_model = df.loc[df["stars"].between(1, 5)].copy()

# --- 2) Columns to DROP entirely (IDs / leakage / artifacts)
drop_cols = [
    "Unnamed: 0", "recipe_number", "recipe_code", "user_index",
    "comment_id", "user_id", "user_name"
]
drop_cols = [c for c in drop_cols if c in df_model.columns]
df_model = df_model.drop(columns=drop_cols)

# --- 3) Feature groups
# Categorical (low-cardinality you want to keep)
cat_cols = [c for c in ["region", "device_type"] if c in df_model.columns]

# Text feature (recipe_name). If you don't want text yet, set text_col = None
text_col = "recipe_name" if "recipe_name" in df_model.columns else None

# Base numeric candidates (exclude target and non-numerics)
num_cols = df_model.select_dtypes(include=np.number).columns.drop("stars").tolist()

# Heavily skewed count-like features -> log1p transform
skewed = [c for c in ["likes", "dislikes", "responses", "user_score", "ranking_score"]
          if c in df_model.columns]

# Keep only those skewed cols that are actually present
skewed = [c for c in skewed if c in num_cols]

# Other numeric features = remaining numerics minus skewed
other_num = [c for c in num_cols if c not in skewed]

# --- 4) Simple feature engineering (exposure & ratios)
# total interactions
if all(c in df_model.columns for c in ["likes", "dislikes", "responses"]):
    df_model["total_interactions"] = (
        df_model["likes"].fillna(0) + df_model["dislikes"].fillna(0) + df_model["responses"].fillna(0)
    )
    if "total_interactions" not in other_num:
        other_num.append("total_interactions")

# safe like ratio (if not already provided as vote_ratio)
if "vote_ratio" not in df_model.columns and all(c in df_model.columns for c in ["likes", "dislikes"]):
    df_model["vote_ratio"] = df_model["likes"] / (df_model["likes"] + df_model["dislikes"] + 1.0)
    if "vote_ratio" not in other_num:
        other_num.append("vote_ratio")
elif "vote_ratio" in df_model.columns and "vote_ratio" not in other_num:
    other_num.append("vote_ratio")

# Time features (optional): from created_at if present & already converted to datetime
if "created_at" in df_model.columns and np.issubdtype(df_model["created_at"].dtype, np.datetime64):
    df_model["dow"] = df_model["created_at"].dt.dayofweek
    df_model["hour"] = df_model["created_at"].dt.hour
    df_model["month"] = df_model["created_at"].dt.month
    # treat as categorical (low cardinality)
    for c in ["dow", "hour", "month"]:
        if c not in cat_cols:
            cat_cols.append(c)

# --- 5) X / y
y = df_model["stars"].astype(int)
X = df_model.drop(columns=["stars"])

# --- 6) Transformers
# 6a) Numeric: log1p for skewed, scale others
log1p_tf = FunctionTransformer(lambda x: np.log1p(np.clip(x, a_min=0, a_max=None)), validate=False)

num_pipeline = ColumnTransformer(
    transformers=[
        ("log_skewed", Pipeline([("log1p", log1p_tf), ("scaler", StandardScaler())]), skewed) if skewed else ("passthrough", "passthrough", []),
        ("other_num", Pipeline([("scaler", StandardScaler())]), other_num) if other_num else ("passthrough2", "passthrough", [])
    ],
    remainder="drop"
)

# 6b) Categorical: one-hot
cat_encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=True)

# 6c) Text: TF-IDF on recipe_name (optional)
tfidf = TfidfVectorizer(
    max_features=2000,       # adjust (e.g., 1k–10k)
    stop_words="english",
    ngram_range=(1, 2),      # unigrams + bigrams
    min_df=5                 # drop very rare tokens
)

# --- 7) ColumnTransformer (combine all)
transformers = []
if skewed or other_num:
    transformers.append(("num", num_pipeline, skewed + other_num))
if cat_cols:
    transformers.append(("cat", cat_encoder, cat_cols))
if text_col is not None:
    transformers.append(("txt", tfidf, text_col))

preprocess = ColumnTransformer(
    transformers=transformers,
    remainder="drop",        # drop anything not listed above
    sparse_threshold=0.3     # keep memory reasonable
)

# --- 8) Classifier (simple & strong baseline)
# Multinomial logistic with class_weight to handle 5★ dominance
clf = LogisticRegression(
    max_iter=2000,
    multi_class="multinomial",
    class_weight="balanced",
    n_jobs=None
)

# Full pipeline
pipe = Pipeline([
    ("preprocess", preprocess),
    ("model", clf)
])

# --- 9) Train/test split (stratified)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# --- 10) Fit & evaluate
pipe.fit(X_train, y_train)

print("Train accuracy:", pipe.score(X_train, y_train))
print("Test  accuracy:", pipe.score(X_test, y_test))
print("\nClassification report (test):\n", classification_report(y_test, pipe.predict(X_test)))
print("\nConfusion matrix (test):\n", confusion_matrix(y_test, pipe.predict(X_test)))


# %% [markdown]
# 6 Model Evaluation: 
# Evaluate how well your models perform.
# - 	Use metrics such as accuracy, precision, recall, F1-score, AUC-ROC
# - 	You can include confusion matrices and interpret results
# - 	Discuss the effect of class imbalance and possible mitigation
# - 	Compare model performance meaningfully
# 

# %%


# %% [markdown]
# 7 Insights, Interpretation, and Reporting: Communicate your findings clearly, professionally, and meaningfully.
# - Include a summary outlining key findings and recommendations
# - Clearly explain what factors most influence star ratings
# - Highlight any patterns in user reputation, engagement, or other features
# - Suggest improvements or potential applications (e.g., helping platforms understand review behavior)
# - Reflect on limitations of your analysis and model
# - Structure your report into logical, readable sections with explanations
# 


