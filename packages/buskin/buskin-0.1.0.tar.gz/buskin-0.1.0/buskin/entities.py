from dataclasses import dataclass
from typing import List, Dict
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class TokenTags():
    token_id : int
    token_global_id : int
    token : str
    lemma : str
    pos : str
    tag : str
    dep : str
    head_global_id : int

@dataclass_json
@dataclass
class Emotion():
    emotion : str
    mini_emotion : str
    probability : float

@dataclass_json
@dataclass
class Sentence():
    sentence_id : int
    cluster_id : int
    global_token_start : int
    text : str
    token_tags : List[TokenTags]
    emotion_tags : Emotion

@dataclass_json
@dataclass
class Occurrence():
    text : str
    sentence_id : int
    cluster_id : int
    start : int
    end : int

@dataclass_json
@dataclass
class Character():
    rank : int
    name : str
    mentions : List[Occurrence]
    agents : List[Occurrence]
    patients : List[Occurrence]
    predicatives : List[Occurrence]

@dataclass_json
@dataclass
class Book():
    book_path : str
    sentences : List[Sentence]
    characters : List[Character]

