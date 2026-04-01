"""
BizLens — Example 06: Text Analytics
======================================
Covers:
  • text.wordcloud()    — Word cloud visualization
  • text.frequency()    — Word and n-gram frequency tables
  • text.sentiment()    — Sentiment analysis (VADER / TextBlob / fallback)
  • text.tfidf()        — TF-IDF keyword extraction

Run:   python 06_text_analytics.py
       pip install bizlens wordcloud vaderSentiment
"""

import bizlens as bl

# ──────────────────────────────────────────────────────────────────────────────
# Sample text corpus — product reviews
# ──────────────────────────────────────────────────────────────────────────────
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

import pandas as pd
review_df = pd.DataFrame({"review": reviews, "rating": [5,1,4,3,5,1,5,2,4,5,3,5,1,4,2]})

# ──────────────────────────────────────────────────────────────────────────────
# 1. Word Cloud
# ──────────────────────────────────────────────────────────────────────────────
print("="*60)
print("1. Word Cloud — all reviews:")
bl.text.wordcloud(
    texts=review_df,
    column="review",
    max_words=80,
    title="Product Review Word Cloud",
    stopwords=["product", "very", "good", "great"],
)

# ──────────────────────────────────────────────────────────────────────────────
# 2. Word Frequency (unigrams)
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("2. Top 20 word frequencies (unigrams):")
uni_freq = bl.text.frequency(
    texts=review_df,
    column="review",
    n=1,
    top_n=20,
    show_plot=True,
)

# ──────────────────────────────────────────────────────────────────────────────
# 3. Bigram frequency
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("3. Top 15 bigram frequencies:")
bi_freq = bl.text.frequency(
    texts=review_df,
    column="review",
    n=2,
    top_n=15,
    show_plot=True,
)

# ──────────────────────────────────────────────────────────────────────────────
# 4. Trigram frequency
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("4. Top 10 trigram frequencies:")
tri_freq = bl.text.frequency(
    texts=review_df,
    column="review",
    n=3,
    top_n=10,
    show_plot=True,
)

# ──────────────────────────────────────────────────────────────────────────────
# 5. Sentiment Analysis
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("5. Sentiment Analysis — product reviews:")
sentiment_df = bl.text.sentiment(
    texts=review_df,
    column="review",
    show_plot=True,
)
print("\nSentiment distribution:")
print(sentiment_df["Sentiment"].value_counts())

# Correlate sentiment with star rating
if "Compound" in sentiment_df.columns:
    import numpy as np
    corr = np.corrcoef(sentiment_df["Compound"].values, review_df["rating"].values)[0,1]
    print(f"\nCorrelation between compound sentiment score and star rating: {corr:.4f}")

# ──────────────────────────────────────────────────────────────────────────────
# 6. Sentiment on positive vs negative subsets
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("6. Sentiment — 5-star vs 1-star reviews:")
five_star = review_df[review_df["rating"] == 5]["review"].tolist()
one_star  = review_df[review_df["rating"] == 1]["review"].tolist()

print("  Five-star reviews:")
bl.text.sentiment(five_star, show_plot=False)
print("  One-star reviews:")
bl.text.sentiment(one_star, show_plot=False)

# ──────────────────────────────────────────────────────────────────────────────
# 7. TF-IDF Keyword Extraction
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("7. TF-IDF keyword extraction — top 15 keywords:")
tfidf_df = bl.text.tfidf(
    texts=review_df,
    column="review",
    top_n=15,
    show_plot=True,
)

# ──────────────────────────────────────────────────────────────────────────────
# 8. Analysis on a plain text string
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("8. Text analysis on a single passage:")
passage = """
Data analytics is transforming business decision-making across industries.
Organizations that leverage data-driven insights consistently outperform competitors
and deliver superior customer experiences. Machine learning algorithms enable
predictive models that forecast demand, detect fraud, and optimise supply chains.
The future of business intelligence lies in prescriptive analytics, which recommends
optimal actions based on data analysis and simulation models.
"""
bl.text.wordcloud(passage, title="Data Analytics Passage — Word Cloud")
bl.text.frequency(passage, n=1, top_n=15)
bl.text.sentiment([passage])

print("\n✅ Example 06 complete.")
