import re, string
from torch.nn.functional import softmax
import numpy as np
from fuzzywuzzy import fuzz

from buskin.config import MIN_PAR_SENTENCES, MIN_FUZZ_SCORE, STOP_WORDS, EMOTIONS, REDUCED_EMOTIONS
from buskin.entities import Character, Emotion, Sentence, TokenTags, Occurrence


def convert_text_to_chunks(text, max_chunk_size):
    # split on newlines followed by space
    pars = re.split(r"\n\s", text)
    # Replace newline chars
    pars = [par.replace("\n", " ") for par in pars]
    # Remove empty pars
    pars = [par for par in pars if len(par) > 0]

    # Preprocess "paragraphs" that are actually quotes or single lined text
    final_pars = []
    for p, paragraph in enumerate(pars):

        if paragraph.count(".") < MIN_PAR_SENTENCES:
            if p == 0:
                final_pars.append(paragraph)
            else:
                final_pars[-1] = final_pars[-1] + " " + paragraph
        else:
            final_pars.append(paragraph)

    final_chunks = [""]
    chunk_id = 0
    par_id = 0
    while par_id < len(final_pars):
        if len(final_chunks[chunk_id]) > max_chunk_size:
            chunk_id += 1
            final_chunks.append("")
        final_chunks[chunk_id] = final_chunks[chunk_id] + " " + final_pars[par_id]
        par_id += 1
    final_chunks = [(chunk, ch) for ch, chunk in enumerate(final_chunks)]
    return final_chunks


def get_merged_characters(coref_dicts, max_fuzz=MIN_FUZZ_SCORE):
    characters = []
    main_coref = {}
    for dict_ in coref_dicts:
        for k, v in dict_.items():
            if k in main_coref:
                main_coref[k]["mentions"] += v["mentions"]
                main_coref[k]["agents"] += v["agents"]
                main_coref[k]["patients"] += v["patients"]
                main_coref[k]["preds"] += v["preds"]
            else:
                main_coref[k] = v

    merged_coref = {}
    char_counts = {}
    for k, v in main_coref.items():
        added = 0
        for merged_char in merged_coref.keys():
            if fuzz.ratio(merged_char, k) > max_fuzz:
                merged_coref[merged_char]["mentions"] += v["mentions"]
                merged_coref[merged_char]["agents"] += v["agents"]
                merged_coref[merged_char]["patients"] += v["patients"]
                merged_coref[merged_char]["preds"] += v["preds"]
                added = 1
                char_counts[merged_char] += len(v["mentions"])
                break
        if added == 0:
            merged_coref[k] = v
            char_counts[k] = len(v["mentions"])

    char_counts = [[k, char_counts[k]] for k in char_counts]
    char_counts = sorted(char_counts, key=lambda x: x[1], reverse=True)
    ranked_chars = [x[0] for x in char_counts]
    for char in merged_coref:
        rank = ranked_chars.index(char) + 1
        character = Character(
            rank,
            char,
            merged_coref[char]["mentions"],
            merged_coref[char]["agents"],
            merged_coref[char]["patients"],
            merged_coref[char]["preds"],
        )
        characters.append(character)

    characters = sorted(characters, key=lambda x: x.rank)
    return characters


def generate_sentence_batches(sentences, batch_size):
    i = 0
    while i * batch_size < len(sentences):
        subset = sentences[i * batch_size : min((i + 1) * batch_size, len(sentences))]
        subset = [[t.token for t in s.token_tags] for s in subset]
        i += 1
        yield subset


def parse_into_sentences_characters(chunk, nlp=None):
    text, par_id = chunk
    doc = nlp(text)
    # parse into sentences
    sentences = []
    sentence_id_for_tokens = []
    for s, sent in enumerate(doc.sents):
        tokens = doc[sent.start : sent.end]
        sentence_id_for_tokens += [s] * len(tokens)
        token_tags = [
            TokenTags(
                i,
                token.i,
                token.text,
                token.lemma_,
                token.pos_,
                token.pos_,
                token.dep_,
                token.head.i,
            )
            for i, token in enumerate(tokens)
        ]
        emotion_tags = Emotion(None, None, None)
        sentences.append(
            Sentence(s, par_id, sent.start, sent.text, token_tags, emotion_tags)
        )
    corefs = {}
    if doc._.has_coref:

        for cluster in doc._.coref_clusters:
            # If an entry for this coref doesn't yet exist, create one
            main_name = denoise_string(cluster.main.text)

            if main_name in STOP_WORDS or main_name == "STOP_WORD":
                continue

            if not (main_name in corefs):
                corefs[main_name] = {
                    "mentions": [],
                    "agents": [],
                    "patients": [],
                    "preds": [],
                }
            # Update the entry with new mention and any parsed verbs or predicatives
            for mention in cluster.mentions:
                mention_name = denoise_string(mention.text)
                mention_sent = sentence_id_for_tokens[mention.start]
                corefs[main_name]["mentions"].append(
                    Occurrence(
                        mention_name, mention_sent, par_id, mention.start, mention.end
                    )
                )
                agents, patients, preds = parse_sent_and_mention(
                    sentences[mention_sent], mention, par_id
                )
                corefs[main_name]["agents"] += agents
                corefs[main_name]["patients"] += patients
                corefs[main_name]["preds"] += preds

    return sentences, corefs

def denoise_string(s):
    exclude = set(string.punctuation)
    s = s.lower()
    s = ''.join(ch for ch in s if ch not in exclude).strip()
    s = ' '.join([x for x in s.split(' ') if x not in STOP_WORDS])
    if s =='':
        s = 'STOP_WORD'
    return s

def parse_sent_and_mention(sent, mention, par_id):
    agents = []
    patients = []
    predicatives = []
    # Iterate over tokens in the mention
    for token in mention:
        token_tag = sent.token_tags[token.i - sent.global_token_start]
        # If the token's dependency tag is nsubj, find it's parent and set the lemma of this word to
        # be an agent of this entity.
        if token_tag.dep == 'nsubj':
            idx = token_tag.head_global_id - sent.global_token_start
            agent_verb = sent.token_tags[idx].lemma
            agents.append(Occurrence(agent_verb, sent.sentence_id, par_id, idx, idx+1))
            #print(" mention: ", mention, " token: ", token, " id ", token.i, "agent : ", agent_verb)
            
        # If the token's dependency tag is dobj or nsubjpass, find it's parent and set the lemma of this word to
        # be an patient of this entity.
        if (token_tag.dep ==  'dobj') or (token_tag.dep == 'nsubjpass'):
            idx = token_tag.head_global_id - sent.global_token_start
            patient_verb = sent.token_tags[idx].lemma
            patients.append(Occurrence(patient_verb, sent.sentence_id, par_id, idx, idx+1))
            #print(" mention: ", mention, " token: ", token, " id ", token.i, "patient : ", patient_verb)

    # Now we handle dependencies in the other direction to get predicatives.
    # 'man' is the predicative of 'Tim' in the sentence "Tim is a man."
    # Iterate over sentence tokens
    for token_tag in sent.token_tags:
        # Only consider tokens not in the mention:
        if not ((token_tag.token_global_id >= mention.start) and (token_tag.token_global_id <= mention.end)):
            # ignore punctuation
            if token_tag.pos != 'PUNCT':
                # Check if the parent of the word is a "be" verb (is, are, be, etc.)
                if sent.token_tags[token_tag.head_global_id - sent.global_token_start].lemma == "be":
                    to_be_verb = sent.token_tags[token_tag.head_global_id - sent.global_token_start]
                    # Check if the parent of the "be" verb is part of the mention
                    if (to_be_verb.head_global_id >= mention.start) and (to_be_verb.head_global_id <= mention.end):
                        idx = token_tag.token_global_id - sent.global_token_start
                        pred_word = sent.token_tags[idx].lemma
                        predicatives.append(Occurrence(pred_word, sent.sentence_id, par_id, idx, idx+1))
                        #print(" mention: ", mention, " token: ", token, " id ", token_tag.token_global_id,  "predicative : ", pred_word)
                    
    return agents, patients, predicatives

def get_emotion_per_batch(batch, tokenizer, model):
    inputs = tokenizer(batch, is_split_into_words=True, return_tensors='pt', padding=True).to('cuda')
    outputs = model(**inputs)
    logits = outputs.logits
    probs = softmax(logits, dim=1).cpu().data.numpy()
    emotion_res = [EMOTIONS[x] for x in np.argmax(probs, axis=1)]
    emo_prob = list(np.max(probs, axis=1))
    mini_emotion_res = [REDUCED_EMOTIONS[emotion] for emotion in emotion_res]
    return  (emotion_res, mini_emotion_res, emo_prob)

def merge_emotions_to_sentences(sentences, emotion_batches):
    emotions = []
    mini_emotions = []
    probs = []
    for e,m,p in emotion_batches:
        emotions+=e
        mini_emotions+=m
        probs+=p

    assert len(emotions) == len(mini_emotions) 
    assert len(emotions) == len(probs) 
    assert len(emotions) == len(sentences)

    for i in range(len(sentences)):
        sentences[i].emotion_tags = Emotion(emotions[i], mini_emotions[i], float(probs[i])) 
    return sentences
