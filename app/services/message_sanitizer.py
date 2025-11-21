import re


class MessageSanitizer:

    def strip_noise(self, text: str) -> str:
        t = text or ""
        # Normalize
        t = t.strip()

        # Remove emoji and non-word punctuation but KEEP letters/numbers/slashes/dashes
        # Replace emoji/non-word (except /:-) with space
        t = re.sub(r"[^\w\s/:-]", " ", t)

        # Reduce repeated letters: loooool -> loool (still keeps 'lol' content)
        t = re.sub(r"(.)\1{2,}", r"\1\1", t)

        # Remove only filler words but avoid deleting real words that may look like fillers
        filler_words = [
            r"\blol\b", r"\blmao\b", r"\brofl\b",
            r"\bhaha\b", r"\bhehe\b",
            r"\bbro\b", r"\bda\b", r"\bmachaa\b",
            r"\byo\b", r"\bbruh\b",
            r"\bpls\b", r"\bpleaseeee\b"
        ]
        for f in filler_words:
            t = re.sub(f, " ", t, flags=re.IGNORECASE)

        # collapse whitespace
        t = re.sub(r"\s+", " ", t).strip()
        return t

    def contains_humor_tokens(self, text: str) -> bool:
        if not text:
            return False
        text_l = text.lower()
        # emoji check (simple) plus laugh words
        if re.search(r"[😂🤣😁😆]", text):
            return True
        if any(w in text_l for w in ["lol", "lmao", "rofl", "haha", "hehe", "funny"]):
            return True
        return False

    def is_offtopic(self, text: str) -> bool:
        if not text:
            return False
        keywords = [
            "idly", "dosa", "sambar", "biryani", "rice", "coffee",
            "tea", "cinema", "movie", "weather", "cricket", "score"
        ]
        t = text.lower()
        return any(k in t for k in keywords)
