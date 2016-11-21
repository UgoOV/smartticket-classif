# -*- coding: utf-8 -*-
import re
import unicodedata
from collections import OrderedDict

from nltk.corpus import stopwords
from nltk.stem.snowball import FrenchStemmer


class Normalizer:
    """ Normalize Text """

    def __init__(self):
        self.list_stop_word_french = ['alors', 'au', 'aucuns', 'aussi', 'autre', 'avant', 'avec', 'avoir', 'bon', 'car',
                                      'ce',
                                      'cela', 'ces', 'ceux', 'chaque',
                                      'ci', 'comme', 'comment', 'dans', 'des', 'du', 'dedans', 'dehors', 'depuis',
                                      'devrait',
                                      'doit', 'donc', 'dos', 'début',
                                      'elle', 'elles', 'en', 'encore', 'essai', 'est', 'et', 'eu', 'fait', 'faites',
                                      'fois',
                                      'font', 'hors', 'ici', 'il', 'ils',
                                      'je', 'juste', 'la', 'le', 'les', 'leur', 'là', 'ma', 'maintenant', 'mais', 'mes',
                                      'mine',
                                      'moins', 'mon', 'mot', 'même',
                                      'ni', 'nommés', 'notre', 'nous', 'ou', 'où', 'par', 'parce', 'pas', 'peut', 'peu',
                                      'plupart', 'pour', 'pourquoi', 'quand',
                                      'que', 'quel', 'quelle', 'quelles', 'quels', 'qui', 'sa', 'sans', 'ses',
                                      'seulement', 'si',
                                      'sien', 'son', 'sont', 'sous',
                                      'soyez', 'sujet', 'sur', 'ta', 'tandis', 'tellement', 'tels', 'tes', 'ton',
                                      'tous', 'tout',
                                      'trop', 'très', 'tu', 'voient',
                                      'vont', 'votre', 'vous', 'vu', 'ça', 'étaient', 'état', 'étions', 'été', 'être',
                                      'a']

        # Suppress number
        self.reg_numb = re.compile('[^\D]')
        # Suppress punctuation
        self.reg_ponct = re.compile('[^a-z 0-9ÀÁÂÃÄÅàáâãäåÒÓÔÕÖØòóôõöøÈÉÊËèéêëÇçÌÍÎÏìíîïÙÚÛÜùúûüÿÑñ²°Ø×ßŠ”�œÐ…]')
        # Suppress apostrophe
        self.reg_apos = re.compile('( l\')|( d\')|( n\')|( m\')')

        # Suppress stop words
        self.french_stopwords_ini = stopwords.words('french')
        self.french_stopwords_ini.extend(self.list_stop_word_french)
        self.french_stopwords = set(self.french_stopwords_ini)

        # Stemming of words
        self.stemmer = FrenchStemmer()

    def to_lower(self, str1):
        """ to lower case """
        return str1.lower()
        # print 'low_case : ', str1

    def suppress_number(self, str1):
        """ Suppress number """
        return self.reg_numb.sub('', str1)
        # print 'only_letters : ', str1

    def suppress_apostrophe(self, str1):
        """ Suppress apostrophe """
        return self.reg_apos.sub(' ', str1)
        # print 'no apostrophe : ', str1

    def suppress_punctuation(self, str1):
        """ Suppress punctuation """
        return self.reg_ponct.sub('', str1)
        # print 'no_ponctuation : ', str1

    def suppress_stopword(self, str1):
        """ Suppress stop words """
        return [token for token in str1.split(' ') if token.lower() not in self.french_stopwords]
        # print 'no_stop_words : ', str1

    def suppress_accent(self, str1):
        """ Suppress accent """
        # return [word.encode('ascii', 'ignore') for word in str1]
        str2 = [word for word in str1 if word != '']
        return [unicodedata.normalize('NFKD', unicode(word, 'utf-8')).encode('ascii', 'ignore') for word in str2]
        # print 'no_accent : ', str1

    def stemm_words(self, str1):
        """ Stemming of words """
        return [self.stemmer.stem(word) for word in str1]
        # print 'stemming : ', str1

    def end_to_end_normalize(self, str1):
        """ Merging process """
        str2 = self.stemm_words(
            self.suppress_accent(
                self.suppress_stopword(
                    self.suppress_punctuation(
                        self.suppress_apostrophe(
                            self.suppress_number(
                                self.to_lower(str1)
                            ))))))
        # print 'merge_list : ', ' '.join(str1)
        return ' '.join(str2)

    def simple_normalize(self,str1):
        str2= self.suppress_stopword(
                    self.suppress_punctuation(
                        self.suppress_apostrophe(
                            self.suppress_number(
                                self.to_lower(str1)
                            ))))
        return ' '.join(str2)

    def clean_duplicate_string(self, str1):
        """ Suppress duplicate word into a sentence. Ordered"""
        return ' '.join(list(OrderedDict.fromkeys(str1.split())))

    def keep_first_letters(self, str1, nb_first):
        """
        From a sentence, create columns with only first letters of the words.
        if words smaller keep all characters
        """
        res = " ".join([word[:nb_first] for word in str1.split() if len(str1)>=nb_first])
        return self.clean_duplicate_string(res)