
<p align="center">
    <br>
    <img src="https://raw.githubusercontent.com/nuwandavek/buskin/master/theater.png" width="100"/>
    <!-- <span style="font-size:100px">Buskin</span> -->
</p>

# Buskin

Buskin is a python package for analyzing various attributes of characters in fictional texts. This was developed as part of a project for the terrific [Computational Humanities](https://www.ischool.berkeley.edu/courses/info/190/ch) course at UC Berkeley. Buskin's pipeline utilizes state-of-the-art techniques in processing the text (to obtain Emotions, Characters, Character Arcs, Patient-agent-predicatives, Part-of-speech tags,etc.)

We created this package to understand character arcs from various novels, but we hope it will reduce the effort to get started in analyzing fictional text for any purpose. We hope that Buskin makes it easier to peel open any novel and the characters within, in all their idiosyncrasies. Over time, we intend to add more features to the package in pursuit of that goal. Also, this is very much a work in progress. We appreciate any feedback, or contribution to the project!

> “Plot is no more than footprints left in the snow after your characters have run by on their way to incredible destinations.” ― Ray Bradbury, Zen in the Art of Writing

Contributors : [nuwandavek](https://github.com/nuwandavek/), [Dmacracy](https://github.com/Dmacracy/)

---

## Usage

Buskin needs Pytorch (>=1.4) which can be installed from [here](https://pytorch.org/get-started/locally/). Once that's done, Buskin can be installed with Pip by : 

```
pip install buskin
```
Buskin requires `spacy`, `torch` and huggingface's `transformers` among other dependencies. So installation might take a while. 

Many examples can be found in the `example_notebooks` directory.

---

## Functions

### parse_book
> parse_book(book_path, batch_size=None, threads=None, max_chunk_size=None, pipeline=None,  model=None, tokenizer=None)

Description : Parse a fictional text

Parameters : 
- book_path : `str` : Path to the `.txt` file of the book
- batch_size : `int`, optional : Batch size of sentences for emotion classification (default = 8)
- threads : `int`, optional : Number of threads to be used in the processing of chunks (default = 5). The larger the number of threads, the faster the processing; but this might fill up the memory since neural coreference is memory heavy
- max_chunk_size : `int`, optional : Max size of a chunk that the text is divided into (default = 10k). The larger the chunks, the better the corefernce, but, memory is a constraint. 
- pipeline : `Spacy Pipeline`, optional : This is used to process the text tokens to obtain the POS tags, etc. If not provided, a default pipeline is initialized. 
- model : `HuggingFace BertForSequenceClassification model`, optional : Model used to obtain emotion for sentences. If not provided, a default model is initialized. 
- tokenizer : `HuggingFace BertTokenizer`, optional : Tokenizer used for the emotion model. If not provided, a default tokenizer is initialized. 

Returns: 
- Book : An instance of the `Book` class   

### load_default_models
> load_default_models()

Description : Explicitly initialize the pipeline, model and tokenizer in case a batch of books are parses and you want to avoid initializing for each book. 

Returns : 
- nlp : `Spacy Pipeline`, optional : This is used to process the text tokens to obtain the POS tags, etc.
- model : `HuggingFace BertForSequenceClassification model`, optional : Model used to obtain emotion for sentences.
- tokenizer : `HuggingFace BertTokenizer`, optional : Tokenizer used for the emotion model.

---

## Classes

### Book
> *Book(book_path=None, sentences=None, characters=None)*

| Attribute   |      Type      |  Description |
|----------|:-------------:|------:|
| book_path |  `str` | Path to the book text file |
| sentences |    List of `Sentence`   | List of all sentences in the fictional text |
| characters | List of `Character` | List of all characters in the fictional text |

<br>

### Sentence
> *Sentence(sentence_id=None, cluster_id=None,  global_token_start=None, text=None, token_tags=None, emotion_tags=None)*

| Attribute   |      Type      |  Description |
|----------|:-------------:|------:|
| sentence_id | `int` | ID of the sentence |
| cluster_id | `int` | ID of the sentence cluster used for coreference resolution |
| global_token_start | `int` | ID of the token |
| text | `str` | Text in the sentence |
| token_tags | List of `TokenTags` | List of all tags for each token in the sentence |
| emotion_tags | List of `Emotion` | List of all emotions for each token in the sentence |

<br>

### Character
> *Character(rank=None, name=None, mentions=None, agents=None, patients=None, predicatives=None)*

| Attribute   |      Type      |  Description |
|----------|:-------------:|------:|
| rank | `int` | Rank of the character (1 = most mentioned character) |
| name | `str` | Name of the character |
| mentions | List of `Occurrence` | List of all occurrences of the character mentions |
| agents | List of `Occurrence` | List of all occurrences of the character agent verbs |
| patients | List of `Occurrence` | List of all occurrences of the character patient verbs |
| predicatives | List of `Occurrence` | List of all occurrences of the character predicatives |

<br>

### TokenTags
> *TokenTags(token_id=None, token_global_id=None, token=None, lemma=None, pos=None, tag=None, dep=None, head_global_id=None)*

| Attribute   |      Type      |  Description |
|----------|:-------------:|------:|
| token_id | `int` | ID of the token |
| token_global_id | `int` | Global ID of the token |
| token | `str` | Text of the token |
| lemma | `str` | Lemma of the token |
| pos | `str` | Part of Speech of the token |
| tag | `str` | POS Tag of the token |
| dep | `str` | Dependency Parse tag of the token |
| head_global_id | `int` | ID of the parse-head of the token |

<br>

### Emotion
> *Emotion(emotion=None, mini_emotion=None, probability=None)*

| Attribute   |      Type      |  Description |
|----------|:-------------:|------:|
| emotion | `str` | Emotion of the sentence (28 values) |
| mini_emotion | `str` | Reduced Emotion of the sentence (3 values) |
| probability | `float` | Probability of the emotion [0,1] |

<br>

### Occurrence
> *Occurrence(text=None, sentence_id=None, cluster_id=None, start=None, end=None)*

| Attribute   |      Type      |  Description |
|----------|:-------------:|------:|
| text | `str` | Text of the occurrence |
| sentence_id | `int` | ID of the sentence with the occurrence |
| cluster_id | `int` | ID of the cluster with the occurrence |
| start | `int` | Start token ID of the occurrence |
| end | `int` | End token ID of the occurrence |

---

Icon made by <a href="https://www.flaticon.com/authors/freepik" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>
