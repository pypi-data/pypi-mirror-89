class WordsapyDict():
    def __init__(self, entries):
            
        if isinstance(entries, dict):
            for key in entries:
                if isinstance(entries[key], list):
                    entries[key] = [WordsapyDict(item) if isinstance(item, dict) else item for item in entries[key]]
                if isinstance(entries[key], dict):
                    entries[key] = WordsapyDict(entries[key])

        self.__dict__.update(entries)
    
    def __str__(self):
        return self.word if hasattr(self, 'word') else '<WordsapyDict object>'