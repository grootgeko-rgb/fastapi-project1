
def senti(review , analyzer):
    sentiment_scores = analyzer.polarity_scores(review)
    compound_score = float(sentiment_scores["compound"])

    if compound_score >= 0.05:
        sentiment_label = "Positive"
    elif compound_score <= -0.05:
        sentiment_label = "Negative"
    else:
        sentiment_label = "Neutral"

    return sentiment_label, compound_score