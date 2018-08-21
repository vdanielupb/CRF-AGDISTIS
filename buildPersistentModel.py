# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 11:24:01 2018

@author: Daniel
"""
#script for learning a model
import configparser
from rasa_nlu.converters import load_data
from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.model import Trainer
from rasa_nlu.model import Metadata, Interpreter
import DataExtraction as data_Extraction
config = configparser.RawConfigParser()
config.read('conf/conf.cnf')

def construct_persistent_model_from_training_data(training_file,configuration_file,output_directory):
    with open(file,'r',encoding='utf8') as f:
        content = f.readlines()
    train=data_Extraction.build_full_train_data_from_lines(content)
    #print(train)
    training_data = data_Extraction.load_rasa_data_from_string(train)
    
    trainer=Trainer(RasaNLUConfig(configuration_file))
    trainer.train(training_data)
    #print(model.parse(',,,D,Theater am Neumarkt,Die Kleinbürgerhochzeit,,,,,STS Leiter Dokumentation,04/09/2017,,,,0,Ambrosius Humm,Michel Seigner,,,"Henning Heers, Iris Erdmann, Hildegard Pintgen, Verena Reichhardt, Urs Bihler, Klaus Henner Russius, Nikola Weisse, Bernd Spitzer, Daniel Plancherel",,,,Christian Schneeberger,01/04/2003,0,S,Isolde Hahn,,,,,1,1,,6,,,,15/05/1976,1,CH: Zürich: Theater am Neumarkt,,Philippe Pilliod,,80003197605151,Zürich: Theater am Neumarkt Theater am Neumarkt,1975/76,,Bertolt Brecht,80003,,,,'.replace(',',' ')))
    trainer.persist(output_directory)
    


file=config.get('rasa','training_file')
conf=config.get('rasa','rasa_config_file')

construct_persistent_model_from_training_data(file,conf,config.get('rasa','rasa_model_directory'))
