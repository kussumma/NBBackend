from thefuzz import fuzz

class AdvancedProfanityFilter:
    def __init__(self, blacklist_file, whitelist_file=None):
        self.blacklist = self.load_blacklist(blacklist_file)
        self.whitelist = self.load_whitelist(whitelist_file) if whitelist_file else []
        self.CHARS_MAPPING = {
            "a": ("a", "@", "*", "4"),
            "i": ("i", "*", "l", "1"),
            "o": ("o", "*", "0", "@"),
            "u": ("u", "*", "v"),
            "v": ("v", "*", "u"),
            "l": ("l", "1"),
            "e": ("e", "*", "3"),
            "s": ("s", "$", "5"),
            "t": ("t", "7"),
        }

    def load_blacklist(self, blacklist_file):
        with open(blacklist_file, 'r') as file:
            return [line.strip() for line in file]
        
    def load_whitelist(self, whitelist_file):
        with open(whitelist_file, 'r') as file:
            return [line.strip() for line in file]
        
    def replace_profanity(self, text):
        for char in self.CHARS_MAPPING:
            for sub in self.CHARS_MAPPING[char]:
                text = text.lower().replace(sub, char)
        return text

    def is_similar(self, word, profane_word):
        if word == profane_word:
            return True
        else:
            similarity = fuzz.partial_ratio(word, profane_word)
            return similarity > 90
        
    def is_whitelisted(self, word):
        for whitelisted_word in self.whitelist:
            if word == whitelisted_word:
                return True
        return False

    def is_profanity(self, word):
        for profane_word in self.blacklist:
            new_word = self.replace_profanity(word)
            if self.is_similar(new_word, profane_word):
                return True
        return False

    def censor(self, text):
        words = text.split()
        censored_words = []
        for word in words:
            if self.is_whitelisted(word):
                censored_words.append(word)
            elif self.is_profanity(word):
                censored_word = '*' * 5
                censored_words.append(censored_word)
            else:
                censored_words.append(word)
        return ' '.join(censored_words)