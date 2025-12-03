import re
from core.plugin_base import BasePlugin  # adjust import if your path is different


class SentimentAnalysisPlugin(BasePlugin):
    """
    Analyzes the overall sentiment of the text (positive, negative, neutral)
    and prepends a short summary at the top of the text.
    """

    @property
    def name(self) -> str:
        return "Sentiment Analysis"

    def __init__(self) -> None:
        # Super simple word lists – you can expand these
        self.positive_words = {
            "good", "great", "excellent", "amazing", "awesome", "fantastic", "wonderful",
            "positive", "pleasant", "delightful", "superb", "brilliant", "outstanding",
            "exceptional", "favorable", "marvelous", "incredible", "impressive",
            "terrific", "spectacular", "perfect", "beautiful", "charming", "nice",
            "lovely", "enjoyable", "happy", "joyful", "cheerful", "smiling",
            "optimistic", "hopeful", "encouraging", "supportive", "helpful",
            "successful", "productive", "efficient", "effective", "creative",
            "innovative", "resourceful", "strong", "capable", "determined", "confident",
            "courageous", "brave", "resilient", "motivated", "ambitious",
            "inspired", "inspiring", "passionate", "enthusiastic", "energetic",
            "friendly", "kind", "thoughtful", "generous", "polite", "respectful",
            "honest", "trustworthy", "reliable", "loyal", "patient", "understanding",
            "forgiving", "grateful", "thankful", "appreciative", "calm", "peaceful",
            "relaxed", "comfortable", "safe", "supported", "valued", "satisfied",
            "content", "pleased", "glad", "excited", "thrilled", "joyous",
            "love", "like", "enjoy", "admire", "praise", "celebrate", "win",
            "victorious", "improving", "progress", "growth", "advance", "upgrade",
            "bright", "sunny", "warm", "heartwarming", "uplifting", "empowering",
            "refreshing", "hope", "promise", "fortune", "prosperity", "luck", "lucky"
        }

        self.negative_words = {
            "bad", "terrible", "awful", "horrible", "dreadful", "poor", "negative",
            "unpleasant", "disappointing", "upsetting", "sad", "depressing", "miserable",
            "unhappy", "angry", "furious", "frustrated", "annoyed", "irritated",
            "hate", "dislike", "detest", "resent", "hostile", "aggressive",
            "violent", "dangerous", "threatening", "fearful", "scared", "afraid",
            "anxious", "worried", "stressed", "tense", "nervous", "panicked",
            "critical", "harsh", "rude", "disrespectful", "dishonest", "untrustworthy",
            "selfish", "greedy", "jealous", "envious", "bitter",
            "broken", "damaged", "weak", "useless", "incompetent", "helpless",
            "hopeless", "desperate", "lost", "confused", "exhausted",
            "sick", "ill", "hurt", "injured", "painful", "aching",
            "boring", "dull", "lifeless", "meaningless", "pointless",
            "ugly", "messy", "dirty", "filthy", "disgusting",
            "fail", "failure", "failing", "worse", "worst", "decline", "downfall",
            "collapse", "crisis", "problem", "issue", "difficulty", "struggle",
            "accident", "error", "mistake", "blunder", "catastrophe", "disaster",
            "tragic", "tragedy", "chaos", "ruin", "nightmare", "suffering",
            "toxic", "harmful", "abusive", "cruel", "cold", "heartless",
            "reject", "ignored", "exclude", "punish", "loss", "lost", "losing",
            "bankrupt", "poverty", "weakness", "failures", "trouble", "troubles"
        }

        self.intensifiers = {
            "very", "really", "extremely", "super", "highly", "totally", "absolutely",
            "hugely", "deeply", "strongly", "incredibly", "remarkably", "solidly",
            "unusually", "greatly", "especially", "extraordinarily", "overly",
            "so", "too", "completely", "utterly", "insanely",
        }

        self.negations = {
            "not", "no", "never", "none", "nothing", "hardly", "barely", "scarcely"
        }



    def process(self, text: str) -> str:
        # tokenize
        words = re.findall(r"\w+", text.lower())
        pos_score = 0
        neg_score = 0

        i = 0
        while i < len(words):
            w = words[i]

            # Handle negation: check next word
            if w in self.negations and i + 1 < len(words):
                next_word = words[i + 1]
                if next_word in self.positive_words:
                    neg_score += 1   # "not good" flips to negative
                    i += 2
                    continue
                elif next_word in self.negative_words:
                    pos_score += 1   # "not bad" flips to positive
                    i += 2
                    continue

            # Handle intensifiers: check next word
            if w in self.intensifiers and i + 1 < len(words):
                next_word = words[i + 1]
                if next_word in self.positive_words:
                    pos_score += 2   # stronger positive
                    i += 2
                    continue
                elif next_word in self.negative_words:
                    neg_score += 2   # stronger negative
                    i += 2
                    continue

            # Regular sentiment scoring
            if w in self.positive_words:
                pos_score += 1
            elif w in self.negative_words:
                neg_score += 1

            i += 1

        # classify
        score = pos_score - neg_score
        if score > 1:
            label = "Positive"
        elif score < -1:
            label = "Negative"
        else:
            label = "Neutral"

        # Emit marker line for UI
        summary = (
            f"[SENTIMENT] Label = {label}  |  "
            f"Count: Positive = {pos_score} Negative = {neg_score}"
        )
        return summary + "\n" + text
