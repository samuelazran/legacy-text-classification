import re
import htmlentitydefs

#TODO:

#1. add regexp for dates (e.g. "10:01:02","2014-01-01","01/01/2014","1st of Jun" => "DATE")
    
#2. add regexp to convert html characters code to text characters (e.g "&amp;" => "&"): PARTIALLY DONE

#3. mark hashtags as HASHTAGS (convert "#" to "HASHTAGS")
#4. upgrade numbers normalizer for numbers names (e.g  "one","twenti one" => "NUM")
class Normalizer:
    def __init__(self): 
        self.params = {"unescape": True, "lower":True, "url": True, "email": True, "num": True, "stem": True, "lemma":True, "punctuation": True}
        self.numFinder = re.compile("(\d+(\.\d+)?)+")
        #self.urlFinder = re.compile("(ht|f)tp(s?)\:\/\/[0-9a-zA-Z]([-.\w]*[0-9a-zA-Z])*(:(0-9)*)*(\/?)([a-zA-Z0-9\-??\.\?\,\'\/\\\+&amp;%\$#_]*)?")
        self.urlFinder = re.compile("(ht|f)tp(s?)\:\/\/[0-9a-zA-Z]([-.\w]*[0-9a-zA-Z])")
        self.emailFinder = re.compile("[A-z0-9._%+-]+@[A-z0-9.-]+\.[A-z]{2,4}")
        self.multipleDotsFinder = re.compile("[.]{2,}")
        self.multipleCommasFinder = re.compile("[,]{2,}")
        self.multipleQuestionMarksFinder = re.compile("[?]{2,}")
        self.multipleExclamationMarksFinder = re.compile("[!]{2,}")
        self.linesDelimiterFinder = re.compile("(-|_|=|\*){3,}")
    def normalize(self, text):
        normalizedText = text
        if self.params['unescape']: 
            normalizedText = self.unescape(normalizedText)
            normalizedText = normalizedText.replace("&","AND")
        if self.params['lower']: 
            normalizedText = normalizedText.lower()
        if self.params['num']:
            normalizedText=self.numFinder.sub(" NUM ", normalizedText)
        if self.params['url']:
            normalizedText=self.urlFinder.sub(" URL ", normalizedText)
        if self.params['email']:
            normalizedText=self.emailFinder.sub(" EMAIL ", normalizedText)
        if self.params['punctuation']:
            normalizedText=self.multipleDotsFinder.sub(" MultipleDots. ", normalizedText)
            normalizedText=self.multipleCommasFinder.sub(" MultipleCommas, ", normalizedText)
            normalizedText=self.multipleQuestionMarksFinder.sub(" MultipleQuestionnMarks? ", normalizedText)
            normalizedText=self.multipleExclamationMarksFinder.sub(" MultipleExclamationMarks! ", normalizedText)
            normalizedText=self.linesDelimiterFinder.sub(" \nLinesDelimiter\n ", normalizedText)
        return normalizedText
    ##
    # Removes HTML or XML character references and entities from a text string.
    #
    # @param text The HTML (or XML) source text.
    # @return The plain text, as a Unicode string, if necessary.
    def unescape(self, text):
        def fixup(m):
            text = m.group(0)
            if text[:2] == "&#":
                # character reference
                try:
                    if text[:3] == "&#x":
                        return unichr(int(text[3:-1], 16))
                    else:
                        return unichr(int(text[2:-1]))
                except ValueError:
                    pass
            else:
                # named entity
                try:
                    text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
                except KeyError:
                    pass
            return text # leave as is
        return re.sub("&#?\w+;", fixup, text)
    

