import logging, time
from multiprocessing import Pool
from transformers import BertTokenizer, BertForSequenceClassification
import spacy, neuralcoref
from torch import cuda
from functools import partial

from buskin.utils import convert_text_to_chunks, parse_into_sentences_characters, get_merged_characters, generate_sentence_batches, get_emotion_per_batch, merge_emotions_to_sentences
from buskin.entities import Book
from buskin.config import EMOTIONS, REDUCED_EMOTIONS, BATCH_SIZE, MAX_CHUNK_SIZE, THREADS

def load_default_models():
    tokenizer = BertTokenizer.from_pretrained("monologg/bert-base-cased-goemotions-original")
    device =  'cuda' if cuda.is_available() else 'cpu'
    model = BertForSequenceClassification.from_pretrained("monologg/bert-base-cased-goemotions-original", return_dict=True).to(device)
    model.eval()

    nlp = spacy.load('en_core_web_sm')
    neuralcoref.add_to_pipe(nlp, blacklist=True)
    
    return nlp, model, tokenizer


def parse_book(book_path, batch_size=BATCH_SIZE, threads=THREADS, max_chunk_size=MAX_CHUNK_SIZE, pipeline=None,  model=None, tokenizer=None):
    start = time.time()
    if pipeline==None or tokenizer==None or model==None:
        pipeline, model, tokenizer = load_default_models()

    with open(book_path, "r") as txtFile:
        text = txtFile.read()
        
    chunks = convert_text_to_chunks(text,max_chunk_size)
    logging.info(f'Number of chunks : {len(chunks)}')
    
    with Pool(threads) as p:
        pooled_opt = p.map(partial(parse_into_sentences_characters, nlp=pipeline),chunks)
        sentences = [sentence for par,_ in pooled_opt for sentence in par]
        characters = get_merged_characters([ coref_dict for _,coref_dict in pooled_opt])
    
    checkpoint_1 = time.time()
    logging.info(f'1. Sentences and Characters obtained ({round(checkpoint_1-start,2)} secs)')
    logging.info(f'Number of Sentences : {len(sentences)}')
    logging.info(f'Number of Characters : {len(characters)}')
        
    batch_generator = generate_sentence_batches(sentences, batch_size=batch_size)
    emotion_batches = []
    for batch in batch_generator:
        emotion_batches.append(get_emotion_per_batch(batch, tokenizer, model))
    
    sentences = merge_emotions_to_sentences(sentences, emotion_batches)
    checkpoint_2 = time.time()
    logging.info(f'2. Emotions obtained ({round(checkpoint_2-checkpoint_1,2)} secs)')
    end = time.time()
    logging.info(f'Processing Done ({end-start} secs)')
    return Book(book_path, sentences, characters)
