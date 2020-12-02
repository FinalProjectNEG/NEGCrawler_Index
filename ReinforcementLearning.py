import pickle

import lda
from gensim import similarities, models, corpora
import nltk
from gensim.models import LdaModel
from gensim.test.test_hdpmodel import corpus
from nltk.stem.porter import PorterStemmer
from gensim.test.utils import common_corpus
from nltk.tokenize.regexp import WordPunctTokenizer
from sklearn.metrics.pairwise import cosine_similarity



stemmer = PorterStemmer()
stopwords = nltk.corpus.stopwords.words('english')
# for tokenize the text from the page
tokenizer = WordPunctTokenizer()


class ReinforrcementLearning:
    def __init__(self, docTexts):
        self.keywords = []
        self.dictionary = None;
        self.model = None;
        self.similarityModel = None;
        self.constructModel(docTexts)


    def constructModel(self, docTexts):

        """ Given document texts, constructs the tf-idf and similarity models"""
        # construct list of document token lists
        try:
            docs = []
            docs.append(self.tokenizeDocText(docTexts))
            print(docs)
            # construct the corpus
            self.dictionary = corpora.Dictionary(docs)
            self.keywords = self.dictionary.values()

            #corpus = self.dictionary.doc2bow(docs[0])
            corpus = [self.dictionary.doc2bow(text) for text in docs]
            #print(corpus.decode("utf-8"))

            # construct the tf-idf model
            tfidf_model = models.TfidfModel(corpus)

            corpus_tfidf = tfidf_model[corpus]
            print(corpus)
            print("corpus tf = ", corpus_tfidf)

            print("beforeeeeeeeeeeeeeeeees")
            # construct the lsi model
            self.model = models.LsiModel(corpus_tfidf, id2word=self.dictionary, num_topics=2)

            print("beginnnnnnnnnnnnnnnnnnnnnnn")
            corpus_lsi = self.model[corpus_tfidf]


            # construct the similarity model
            self.similarityModel = similarities.MatrixSimilarity(self.model[corpus_lsi])
            print("enddddddddddddddddddddddddddddd")
        except Exception as err:
            print(err)

    def check(self, string):

        for i in string:
            if ord(i) >= 128:
                return False
        return True

    def calculate_score(self ,docText):
        """ Given document text, returns relevancy score.
        Document text is tokenized, transformed into vector space,
        and then the maximum dot-product is returned"""
        # send string and return list with tokenize
        docTokens = self.tokenizeDocText(docText)

        # remove all the nonsense words by function "check"
        docTokens= list(i for i in docTokens if self.check(i))

        # create lists in list
        #list_doc_tokens = [docTokens]

        # create dictionary
        #dictionary = corpora.Dictionary(list_doc_tokens)

        doc_bow = self.dictionary.doc2bow(docTokens)
        # transform document into model's vector space
        #corpus = [dictionary.doc2bow(text) for text in list_doc_tokens]

        #dictionary.save('dictionary.gensim')

        #id_words = [(dictionary[id], count) for id, count in corpus]
        #print(id_words)

        # display the word with the count
        # self.model = LdaModel(corpus, id2word = dictionary ,num_topics=10)
        # self.model.save('model5.gensim')
        # for idx, topic in self.model.print_topics(-1):
        #     print('Topic: {} \nWords: {}'.format(idx, topic))
        vec = self.model[doc_bow]

        print("===================")




        # return maximum similarity (dot products)
        simList = self.similarityModel[vec]
        return max(simList)


    def tokenizeDocText(self, docText):
        """Given document text, returns list of tokens.
        These tokens are:
            - separated by whitespace/punctuation
            - not in stopword list and longer than 2
            - reduced to stem (e.g. 'computer' -> 'comput'
        """
        tokens = tokenizer.tokenize(docText)
        clean = [token.lower() for token in tokens if token.lower() not in stopwords and len(token) > 2]
        final = [stemmer.stem(word) for word in clean]
        return final