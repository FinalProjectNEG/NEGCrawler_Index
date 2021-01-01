#לבדוק את המידע שהובא אלינו מהאתרים ש'זחלנו' אליהם ולבדוק אם המידע:
# (1) עדכני, (2) חשוב ולא סתם עמוד מפגר (3) בעל סמכות ולא משהו מוזר שיכול להוות כגורם מזיק
# לאחר שנמצא אתרים שמקיימים את שלושת התנאים הללו אנו נשמור אותם בבסיס נתונים כ-אינדקס
import pickle

from DB import insertDB
from Url_Address import UrlAdd
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.tokenize.regexp import WordPunctTokenizer

import Setting
stemmer = PorterStemmer()
stopwords = nltk.corpus.stopwords.words('english')
# for tokenize the text from the page
tokenizer = WordPunctTokenizer()


class Index:
    def __init__(self, docTexts, url, title, description, time):
        self.keywords = []
        self.title = title
        self.description = description
        self.dictionary = None;
        self.docTexts = docTexts
        self.url = url
        self.time = time



    def index_one_file(self,termlist):
        fileIndex = {}
        sum = 0
        for index, word in enumerate(termlist):
            sum+=1
            if word in fileIndex.keys():
                fileIndex[word].append(index)
            else:
                fileIndex[word] = [index]

        for key in fileIndex:
            count = len(fileIndex.get(key))
            tf = count/sum
            fileIndex[key] = [count,tf]



        #print(fileIndex)
        return fileIndex

    def Add2Dictionary(self, obj_dict):
        for key in obj_dict.keys():
            for url_add in obj_dict[key].keys():
                if key in Setting.dictionary_global.keys():
                    Setting.dictionary_global[key][url_add] = obj_dict[key][url_add]
                else:
                    Setting.dictionary_global[key]=obj_dict[key]


    def Make_New_Dictionary(self,p1):

        for file_name in self.dictionary.keys():
            for word in self.dictionary[file_name]:
                self.dictionary[file_name][word] = p1




    def calculate_score(self):
        """ Given document text, returns relevancy score.
        Document text is tokenized, transformed into vector space,
        and then the maximum dot-product is returned"""
        # send string and return list with tokenize
        docTokens = {self.url : self.tokenizeDocText()}
        self.dictionary = self.make_indices(docTokens)
        ## create object....
        #print(self.dictionary.get(self.url))
        p1 = UrlAdd(self.url, self.title,self.description, self.dictionary.get(self.url),self.time)
        self.Make_New_Dictionary(p1)

        self.dictionary = self.fullIndex(self.dictionary)


        self.Add2Dictionary(self.dictionary)
        print()
        print(len(Setting.dictionary_global.keys()))


    def make_indices(self,termlists): #URL+WORD WITY INDEX
        total = {}
        for filename in termlists.keys():
            total[filename] = self.index_one_file(termlists[filename])
        #print(total)
        return total


    def fullIndex(self, regdex):
        total_index = {}
        for filename in regdex.keys():
            for word in regdex[filename].keys():
                if word in total_index.keys():
                    if filename in total_index[word].keys():
                        total_index[word][filename].extend(regdex[filename][word][:])
                    else:
                        total_index[word][filename] = regdex[filename][word]
                else:
                    total_index[word] = {filename: regdex[filename][word]}
        #print(total_index)
        return total_index

    def tokenizeDocText(self):
        """Given document text, returns list of tokens.
        These tokens are:
            - separated by whitespace/punctuation
            - not in stopword list and longer than 2
            - reduced to stem (e.g. 'computer' -> 'comput'
        """
        tokens = tokenizer.tokenize(self.docTexts)
        clean = [token.lower() for token in tokens if token.lower() not in stopwords and len(token) > 2]
        clean1 = []
        for token in clean:
            token = token.replace('.', '')
            token = token.replace('$', '')
            token = token.replace('/', '')
            token = token.replace('?', '')
            token = token.replace('"', '')
            token = token.replace('*', '')
            token = token.replace('<', '')
            token = token.replace('>', '')
            token = token.replace(':', '')
            token = token.replace('|', '')

            if token == "":
                continue
            clean1.append(token)
        final = [stemmer.stem(word) for word in clean1]
        return final