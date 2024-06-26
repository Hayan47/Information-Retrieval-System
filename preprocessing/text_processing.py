import pandas as pd
import string
import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk import pos_tag
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
import re
from spellchecker import SpellChecker
from nltk.tokenize import word_tokenize
import unicodedata
import contractions
import inflect


class TextProcessing:

    def __init__(self):
        self.punctuations = string.punctuation
        self.stop_words = set(stopwords.words('english'))
        self.stemmer = nltk.PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()
        self.wordnet_map = {'N': wordnet.NOUN, 'V': wordnet.VERB, 'J': wordnet.ADJ, 'R': wordnet.ADV}
        self.url_pattern = r'(http[s]?://\S+|www\.\S+)'
        self.spell_checker = SpellChecker()
        self.p = inflect.engine()


        


    def remove_punctuations(self, text):
        return text.translate(str.maketrans('', '', self.punctuations))


    def remove_stopwords(self, tokens):
        return [token for token in tokens if token not in self.stop_words]


    def stem_text(self, tokens):
        return [self.stemmer.stem(token) for token in tokens]
    
    
    def lemmatize_text(self, tokens):
        pos_text = pos_tag(tokens)
        return [self.lemmatizer.lemmatize(token, self.wordnet_map.get(pos[0], wordnet.NOUN)) for token, pos in pos_text]


    def remove_urls(self, tokens):
        cleaned_tokens = [re.sub(self.url_pattern, '', token) for token in tokens]
        return cleaned_tokens


    def remove_html_tags(self, tokens):
        cleaned_tokens = [re.sub(r'<.*?>', '', token) for token in tokens]
        return cleaned_tokens


    def correct_spelling(self, tokens):
        corrected_tokens = []
        misspelled_tokens = self.spell_checker.unknown(tokens)
        
        for token in tokens:
            if token in misspelled_tokens:
                corrected_word = self.spell_checker.correction(token)
                if corrected_word is None:
                    corrected_tokens.append(token)  # Keep the original misspelled token
                else:
                    corrected_tokens.append(corrected_word)
            else:
                corrected_tokens.append(token)
        
        return corrected_tokens
    

    def remove_alphanumeric_tokens(self, tokens):
        return [token for token in tokens if not re.search(r'[A-Za-z]', token) or not re.search(r'\d', token)]


    def remove_single_letters(self, tokens):
        cleaned_tokens = [token for token in tokens if len(token) > 1]
        return cleaned_tokens


    def remove_numbers(self, tokens):
        return [token for token in tokens if not token.isdigit()]


    def remove_triple_letters(self, tokens):
        filtered_tokens = []
        for token in tokens:
            has_triple = False
            for i in range(2, len(token)):
                if token[i] == token[i-1] == token[i-2]:
                    has_triple = True
                    break
            if not has_triple:
                filtered_tokens.append(token)
        return filtered_tokens
    
    
    def remove_non_english(self, tokens):
        english_letters = re.compile(r'^[a-zA-Z]+$')
        filtered_tokens = []
        for token in tokens:
            if english_letters.match(token):
                filtered_tokens.append(token)
        return filtered_tokens


    def remove_specific_words(self, tokens):
        words = ['etc','one','hundred','two','think','get','thousand','people','know','go','three','like','u','believe','good','four','five','word','day','onto','will','cause','say','would','tell','something','believe','little','every','also','really','thing','might','someone','maybe','could','many','may','id','without'
        'with','nobecause','no','because','question','answer','plugsredyellowwhite','yor','coz','cuz','ever','let','nothing','anything','come','thing','lot','lol','everyone','bla','ha']
        filtered_tokens = [token for token in tokens if token not in words]
        return filtered_tokens



    def normalize_text(self, text):
        normalized_text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        return normalized_text
    

    def expand_contractions(self, text):
        expanded_text = contractions.fix(text)
        return expanded_text


    def replace_numbers_with_words(self, text):
        words = text.split()
        processed_words = []
        for word in words:
            if word.isdigit():
                if len(word) < 10:
                    processed_words.append(self.p.number_to_words(word))
                else:
                    # Skip adding the word to the list, effectively removing it
                    continue
            else:
                processed_words.append(word)
        return ' '.join(processed_words)


    def replace_words(self, tokens):
        substitution_dict = {
        'mom': 'mother',
        'dad': 'father',
        'kid': 'child',
        'bday': 'birthday',
        'ur': 'your',
        'pls': 'please',
        'thx': 'thanks',
        'bro': 'brother',
        'sis': 'sister',
        'women': 'woman',
        'men': 'man',
        }
        return [substitution_dict.get(token, token) for token in tokens]
    
    def preprocess_text(self, text):
        text = text.lower()
        
        text = self.remove_punctuations(text)
        text = self.normalize_text(text)
        text = self.expand_contractions(text)
        # text = self.replace_numbers_with_words(text)
        
        #tokenizing
        tokens = word_tokenize(text)
        tokens = self.remove_stopwords(tokens)
        tokens = self.remove_alphanumeric_tokens(tokens)
        tokens = self.remove_single_letters(tokens)
        tokens = self.remove_triple_letters(tokens)
        tokens = self.remove_non_english(tokens)
        tokens = self.remove_specific_words(tokens)
        tokens = self.remove_urls(tokens)
        tokens = self.remove_html_tags(tokens)
        tokens = self.replace_words(tokens)
        # stemming
        # tokens = self.stem_text(tokens)
        
        # lemmatization
        tokens = self.lemmatize_text(tokens)
        
        # Spell checking and correction
        # tokens = self.correct_spelling(tokens)
        return tokens


    
    



