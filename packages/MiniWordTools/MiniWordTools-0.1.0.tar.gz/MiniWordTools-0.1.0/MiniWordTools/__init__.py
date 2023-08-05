class word(object):
    def __init__(self, text):
        self.word = text

    def clearfront(self, count):
        self.word = self.word[count:]

    def clearback(self, count):
        self.word = self.word[:-count]

    def startswith(self, text):
        if len(text) > len(self.word):
            return False

        return self.word[:len(text)] == text

    def endswith(self, text):
        if len(text) > len(self.word):
            return False

        return self.word[-len(text):] == text

    def contains(self, text):
        return text in self.word

    def __getIndexes__(self, text, returnFormat=1):
        indexes = []
        for n in range(len(self.word) - len(text) + 1):
            if self.word[n:n + len(text)] == text:
                if returnFormat == 1:
                    [indexes.append(x) for x in range(n, n + len(text))]
                elif returnFormat == 2:
                    indexes.append([n, n + len(text)])
        return indexes

    def remove(self, text, index=-1):
        indexes = self.__getIndexes__(text, 1 if index < 0 else 2)
        if index < 0:
            new = ''
            for n in range(len(self.word)):
                if n not in indexes:
                    new += self.word[n]
            self.word = new
        else:
            self.word = self.word[:indexes[index][0]] + self.word[indexes[index][1]:]

    def removeWhitespace(self):
        self.remove(' ')
        self.remove('\t')
        self.remove('\n')

    def countInstances(self, text, deny=None) -> int:
        if deny is None:
            deny = []
        if type(deny) is str:
            deny = [deny]
        if '' in deny:
            return 0

        count = 0

        for n in range(len(self.word) - len(text) + 1):
            if self.word[n:n + len(text)] == text:
                denyInstance = False

                for denyText in deny:
                    try:
                        if self.word[n:n+len(denyText)] == denyText:
                            denyInstance = True
                    except IndexError:
                        continue

                count += 0 if denyInstance else 1

        return count

    def replace(self, text, modified):
        self.word = str.replace(self.word, text, modified)
