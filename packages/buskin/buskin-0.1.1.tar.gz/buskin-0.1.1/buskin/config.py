from spacy.lang.en.stop_words import STOP_WORDS as words

EMOTIONS = ['admiration','amusement','anger','annoyance','approval','caring','confusion','curiosity',\
            'desire','disappointment','disapproval','disgust','embarrassment','excitement','fear',\
            'gratitude','grief','joy','love','nervousness','optimism','pride','realization','relief',\
            'remorse','sadness','surprise','neutral']
REDUCED_EMOTIONS = { 'admiration' : 'pos', 'amusement' : 'pos', 'anger' : 'neg', 'annoyance' : 'neg', 'approval' : 'pos',
            'caring' : 'pos', 'confusion' : 'amb', 'curiosity' : 'amb', 'desire' : 'pos', 'disappointment' : 'neg', 'disapproval' : 'neg',
            'disgust' : 'neg', 'embarrassment' : 'neg', 'excitement' : 'pos', 'fear' : 'neg', 'gratitude' : 'pos', 'grief' : 'neg',
            'joy' : 'pos', 'love' : 'pos', 'nervousness' : 'neg', 'optimism' : 'pos','pride' : 'pos', 'realization' : 'amb',
            'relief' : 'pos', 'remorse' : 'neg', 'sadness' : 'neg', 'surprise' : 'amb', 'neutral' : 'amb'}

STOP_WORDS = words
MIN_PAR_SENTENCES = 5
THREADS = 5
BATCH_SIZE = 8
MAX_CHUNK_SIZE = 20000

MIN_FUZZ_SCORE = 70