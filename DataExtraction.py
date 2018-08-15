# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 11:46:08 2018

@author: Daniel
"""

import re
from rasa_nlu.model import Trainer
from rasa_nlu.model import Metadata, Interpreter
import json
import rasa_nlu.converters as converters
import logging
from rasa_nlu.training_data import TrainingData, Message
logger = logging.getLogger(__name__)

def build_full_train_data_from_lines(lines):
    data='{ \"rasa_nlu_data\": {\"common_examples\": ['
    for x in range(1,len(lines)-1):
        row=lines[x]
        entities=constructentReplaceComma(row)
        data+='{'+entities+'},'
    row=lines[len(lines)-1]
    entities=constructentReplaceComma(row)
    data+='{'+entities+'}'
    data+=']}}'
    return data



def constructentReplaceComma(te):
    regexStart = re.compile('<entity>')
    regexEnd = re.compile('</entity>')
    entities=''
    while te.find('<entity>') >-1:
        entitystring='{'
        startindex=te.find('<entity>')
        te=regexStart.sub('',te,1)
        entity=te[startindex:te.find('</entity>')]
        
        endindex=te.find('</entity>')
        te=regexEnd.sub('',te,1)
        entitystring+='\"start\":'+str(startindex)+','
        entitystring+='\"end\":'+str(endindex)+','
        entitystring+='\"value\":\"'+entity.replace(',',' ').replace('"',' ').replace('\\','')+'\",'
        entitystring+='\"entity\":\"entity\"}'
        #print(entitystring)
        entities+=entitystring
        if te.find('<entity>') >-1:
            entities+=','
    resultstring='\"text\":\"'+te.replace(',',' ').replace('"',' ').replace('\\','').replace('\n',"")+'\",\"entities\":['+entities+']'
    return resultstring

def _read_json_from_string(text):
    return json.loads(text)

def load_rasa_data_from_string(text):
    # type: (Text) -> TrainingData
    """Loads training data stored in the rasa NLU data format."""

    data = _read_json_from_string(text)
    converters.validate_rasa_nlu_data(data)

    common = data['rasa_nlu_data'].get("common_examples", list())
    intent = data['rasa_nlu_data'].get("intent_examples", list())
    entity = data['rasa_nlu_data'].get("entity_examples", list())
    regex_features = data['rasa_nlu_data'].get("regex_features", list())
    synonyms = data['rasa_nlu_data'].get("entity_synonyms", list())

    entity_synonyms = converters.get_entity_synonyms_dict(synonyms)

    if intent or entity:
        logger.warn("DEPRECATION warning: Data file contains 'intent_examples' "
                    "or 'entity_examples' which will be "
                    "removed in the future. Consider putting all your examples "
                    "into the 'common_examples' section.")

    all_examples = common + intent + entity
    training_examples = []
    for e in all_examples:
        data = e.copy()
        if "text" in data:
            del data["text"]
        training_examples.append(Message(e["text"], data))

    return TrainingData(training_examples, entity_synonyms, regex_features)