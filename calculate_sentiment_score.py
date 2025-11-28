def calculate_sentiment_score(review_text, user_score=None):
    import re

    # Define word categories
    positive_strong = {"amazing", "excellent", "love", "masterpiece", "incredible", "fantastic", "awesome", "brilliant"}
    positive_mild = {"good", "fun", "enjoyable", "nice", "cool", "decent", "smooth"}
    negative_mild = {"boring", "laggy", "buggy", "slow", "average", "ok", "annoying"}
    negative_strong = {"hate", "terrible", "awful", "trash", "worst", "broken", "crash", "disgusting"}

    # Emoji lists
    positive_emojis = {"😍", "🔥", "😊", "👍", "🎉", "❤️"}
    negative_emojis = {"😡", "😭", "👎", "💀", "🤬"}

    # Validate review text
    if not isinstance(review_text, str) or review_text.strip() == "":
        return 5.0  # Neutral default

    review_lower = review_text.lower()
    words = re.findall(r'\w+', review_lower)
    score = 5  # Neutral base score

    # Keyword-based scoring
    for word in words:
        if word in positive_strong:
            score += 2
        elif word in positive_mild:
            score += 1
        elif word in negative_mild:
            score -= 1
        elif word in negative_strong:
            score -= 2

    # Punctuation impact
    score += min(review_text.count("!") * 0.1, 1)  # Max +1 from exclamations
    score -= min(review_text.count("?") * 0.1, 1)  # Max -1 from confusion/frustration

    # Emoji impact
    for char in review_text:
        if char in positive_emojis:
            score += 1
        elif char in negative_emojis:
            score -= 1

    # Include user rating if available
    if user_score is not None:
        try:
            user_score = float(user_score)
            score += (user_score - 5) / 2  # Normalize to sentiment scale
        except:
            pass

    # Final clamp between 1 and 10
    return round(max(1, min(10, score)), 2)
