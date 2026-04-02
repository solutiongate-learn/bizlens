"""
BizLens — Example 06: Text Analytics
======================================
Topics covered
--------------
• text.wordcloud()    — Word cloud visualization
• text.frequency()    — Word and n-gram frequency tables (unigrams, bigrams, trigrams)
• text.sentiment()    — Sentiment analysis (VADER / TextBlob / rule-based fallback)
• text.tfidf()        — TF-IDF keyword extraction and document scoring
• Corpus analysis     — Single strings, lists, and DataFrames all supported

Run anywhere
------------
  Google Colab : paste into a code cell and run
  VSCode / Jupyter / Terminal : python 06_text_analytics.py
"""

# ── Auto-install ──────────────────────────────────────────────────────────────
import subprocess, sys

def _install(pkg):
    subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q"])

for pkg in ["bizlens", "numpy", "pandas", "matplotlib"]:
    try:
        __import__(pkg)
    except ImportError:
        print(f"Installing {pkg}...")
        _install(pkg)

# Optional text analytics dependencies (install quietly, fallback handled inside bizlens)
for pkg in ["wordcloud", "vaderSentiment", "textblob", "scikit-learn"]:
    try:
        import_name = pkg.replace("-", "_").replace("scikit_learn", "sklearn")
        __import__(import_name)
    except ImportError:
        print(f"Installing {pkg} (optional)...")
        try:
            _install(pkg)
        except Exception:
            pass  # bizlens has built-in fallback for missing optional deps

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")   # Safe for Colab / headless; remove for pop-up windows
import matplotlib.pyplot as plt
import bizlens as bl

print(f"BizLens version: {bl.__version__}\n")

# ── Build sample corpus ───────────────────────────────────────────────────────
reviews = [
    "This product is absolutely amazing! Best purchase I've ever made. Highly recommended.",
    "Terrible quality. Broke after two days. Very disappointed with this purchase.",
    "Good value for money. Works as described. Delivery was fast and packaging excellent.",
    "Not great, not terrible. Average product. Some features are useful but it feels cheap.",
    "Outstanding customer service! They resolved my issue immediately. Very professional team.",
    "Worst product ever. Do not buy this. Complete waste of money and time.",
    "Excellent build quality and very easy to use. The interface is intuitive and clean.",
    "Product arrived damaged. Customer support was unhelpful and slow to respond.",
    "Great product for the price. A few minor issues but overall very satisfied with it.",
    "Perfect! Exceeded my expectations. Beautiful design and works flawlessly every time.",
    "Mediocre at best. Nothing special about this product. Other brands offer better value.",
    "Amazing quality and fast shipping. Will definitely order again from this company.",
    "Poor performance and bad battery life. Returned it immediately for a full refund.",
    "Solid product with good features. Setup was simple and the app works perfectly well.",
    "Disappointed with the quality. It looks nice but doesn't function as advertised.",
]
ratings = [5, 1, 4, 3, 5, 1, 5, 2, 4, 5, 3, 5, 1, 4, 2]
review_df = pd.DataFrame({"review": reviews, "rating": ratings})
print(f"Corpus: {len(reviews)} product reviews  |  Avg rating: {np.mean(ratings):.2f}/5\n")

# ── 1. Word Cloud ─────────────────────────────────────────────────────────────
print("="*60)
print("1. Word Cloud — all 15 product reviews:")
bl.text.wordcloud(
    texts=review_df,
    column="review",
    max_words=80,
    title="Product Review Word Cloud",
    stopwords=["product", "very", "good", "great"],
)

# ── 2. Unigram frequency ──────────────────────────────────────────────────────
print("\n" + "="*60)
print("2. Top 20 word frequencies (unigrams — single words):")
uni_freq = bl.text.frequency(
    texts=review_df,
    column="review",
    n=1,
    top_n=20,
    show_plot=True,
)
if uni_freq is not None and len(uni_freq) > 0:
    top_word = uni_freq.iloc[0]
    print(f"\n   Most common word: '{top_word['word'] if 'word' in top_word else top_word.name}'"
          f"  (appears {top_word['count'] if 'count' in top_word else top_word.iloc[0]} times)")

# ── 3. Bigram frequency ───────────────────────────────────────────────────────
print("\n" + "="*60)
print("3. Top 15 bigram frequencies (2-word phrases):")
bi_freq = bl.text.frequency(
    texts=review_df,
    column="review",
    n=2,
    top_n=15,
    show_plot=True,
)

# ── 4. Trigram frequency ──────────────────────────────────────────────────────
print("\n" + "="*60)
print("4. Top 10 trigram frequencies (3-word phrases):")
tri_freq = bl.text.frequency(
    texts=review_df,
    column="review",
    n=3,
    top_n=10,
    show_plot=True,
)

# ── 5. Sentiment Analysis — full corpus ──────────────────────────────────────
print("\n" + "="*60)
print("5. Sentiment Analysis — all 15 reviews:")
print("   (Uses VADER if available, else TextBlob, else rule-based fallback)")
sentiment_df = bl.text.sentiment(
    texts=review_df,
    column="review",
    show_plot=True,
)
print("\n   Sentiment distribution:")
if sentiment_df is not None and "Sentiment" in sentiment_df.columns:
    dist = sentiment_df["Sentiment"].value_counts()
    for label, count in dist.items():
        pct = count / len(sentiment_df) * 100
        bar = "█" * int(pct / 5)
        print(f"     {label:10s}: {count:2d} ({pct:.0f}%)  {bar}")

    # Correlation between compound score and star rating
    if "Compound" in sentiment_df.columns:
        compound_vals = sentiment_df["Compound"].values
        rating_vals   = np.array(ratings)
        corr = np.corrcoef(compound_vals, rating_vals)[0, 1]
        print(f"\n   Compound score vs star rating correlation: r = {corr:.4f}")
        print(f"   {'Strong positive ✅' if corr > 0.6 else 'Moderate ⚠️' if corr > 0.3 else 'Weak ❌'} alignment")

# ── 6. Sentiment by star-rating segment ──────────────────────────────────────
print("\n" + "="*60)
print("6. Sentiment — 5-star vs 1-star reviews (segment comparison):")
five_star_texts = [r for r, rt in zip(reviews, ratings) if rt == 5]
one_star_texts  = [r for r, rt in zip(reviews, ratings) if rt == 1]
print(f"   5-star reviews ({len(five_star_texts)} total):")
sent_5 = bl.text.sentiment(five_star_texts, show_plot=False)
print(f"   1-star reviews ({len(one_star_texts)} total):")
sent_1 = bl.text.sentiment(one_star_texts,  show_plot=False)

if (sent_5 is not None and "Compound" in sent_5.columns and
        sent_1 is not None and "Compound" in sent_1.columns):
    avg_5 = sent_5["Compound"].mean()
    avg_1 = sent_1["Compound"].mean()
    print(f"\n   Average compound score — 5-star: {avg_5:.3f}  |  1-star: {avg_1:.3f}")
    print(f"   Sentiment gap: {avg_5 - avg_1:.3f}")

# ── 7. TF-IDF Keyword Extraction ──────────────────────────────────────────────
print("\n" + "="*60)
print("7. TF-IDF keyword extraction — top 15 most distinctive terms:")
print("   (TF-IDF rewards words that are frequent in a doc but rare across corpus)")
tfidf_df = bl.text.tfidf(
    texts=review_df,
    column="review",
    top_n=15,
    show_plot=True,
)

# ── 8. Word cloud by sentiment group ─────────────────────────────────────────
print("\n" + "="*60)
print("8. Word cloud — positive reviews only (rating ≥ 4):")
positive_reviews = [r for r, rt in zip(reviews, ratings) if rt >= 4]
positive_df = pd.DataFrame({"review": positive_reviews})
bl.text.wordcloud(positive_df, column="review",
                  title="Positive Reviews Word Cloud (rating ≥ 4)")

print("\nWord cloud — negative reviews only (rating ≤ 2):")
negative_reviews = [r for r, rt in zip(reviews, ratings) if rt <= 2]
negative_df = pd.DataFrame({"review": negative_reviews})
bl.text.wordcloud(negative_df, column="review",
                  title="Negative Reviews Word Cloud (rating ≤ 2)")

# ── 9. Text analysis on a passage ────────────────────────────────────────────
print("\n" + "="*60)
print("9. Text analysis on a single business intelligence passage:")
passage = (
    "Data analytics is transforming business decision-making across industries. "
    "Organizations that leverage data-driven insights consistently outperform competitors "
    "and deliver superior customer experiences. Machine learning algorithms enable "
    "predictive models that forecast demand, detect fraud, and optimise supply chains. "
    "The future of business intelligence lies in prescriptive analytics, which recommends "
    "optimal actions based on data analysis and simulation models."
)
bl.text.wordcloud(passage, title="Business Intelligence Passage — Word Cloud")
bi_passage = bl.text.frequency(passage, n=1, top_n=15)
bl.text.sentiment([passage])

# ── 10. Sentiment interpretation guide ───────────────────────────────────────
print("\n" + "="*60)
print("10. VADER compound score interpretation guide:")
print("""
  ┌─────────────────┬───────────────┬─────────────────────────────────────┐
  │ Compound Score  │ Sentiment     │ Typical use                         │
  ├─────────────────┼───────────────┼─────────────────────────────────────┤
  │ ≥ 0.05          │ Positive      │ Product praise, good reviews        │
  │ −0.05 to 0.05   │ Neutral       │ Factual statements, mixed reviews   │
  │ ≤ −0.05         │ Negative      │ Complaints, returns, bad experience │
  └─────────────────┴───────────────┴─────────────────────────────────────┘

  TF-IDF (Term Frequency × Inverse Document Frequency)
  ─────────────────────────────────────────────────────
  High TF-IDF → word appears often in THIS doc but rarely in OTHERS
  Low TF-IDF  → word is too common across all documents (e.g. "the", "is")
  Use case: identify key themes per document, keyword extraction for search

  N-gram use cases
  ─────────────────
  Unigram  (n=1) : Overall vocabulary, top topics
  Bigram   (n=2) : Common phrases, collocations ("customer service")
  Trigram  (n=3) : Specific complaints / compliments ("very easy to use")
""")

print("✅ Example 06 complete — Text Analytics")
