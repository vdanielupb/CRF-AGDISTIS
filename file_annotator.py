# -*- coding: utf-8 -*-
"""
Created on Tue May 22 10:35:31 2018

@author: Daniel
"""
import requests
import nif.NIFDocument as NIFDocument
import nif.NIFContent as NIFContent
import nif.NIFContent
from rasa_nlu.model import Metadata, Interpreter
import configparser
def add_nif_entities(reference_context,base_uri,entities,doc):
    print(doc.get_nif_string())
    for ent in entities:
        nif_content=NIFContent.NIFContent(base_uri+'#'+str(ent['start'])+','+str(ent['end']))
        nif_content.set_begin_index(ent['start'])
        nif_content.set_end_index(ent['end'])
        nif_content.set_reference_context(reference_context)
        nif_content.set_anchor_of(ent['value'])
        doc.addContent(nif_content)
    print(doc.get_nif_string())
    return doc
config = configparser.RawConfigParser()
config.read('conf/conf.cnf')


rasa_config=config.get('rasa','rasa_config_file')
agdistis_url=config.get('agdistis','agdistis_url')
interpreter = Interpreter.load(config.get('rasa','rasa_model'), rasa_config)


#file = request.files['file']
with open(config.get('files','file_to_annotate'),'r',encoding='utf8') as f:
        content = f.readlines()
doc=NIFDocument.NIFDocument()
i=0
for line in content:
    base_uri="http://dataset/"+str(i)
    uri=base_uri+'#char=0'+','+str(len(line))
    nif_content=NIFContent.NIFContent(uri)
    nif_content.is_string=line.replace('\n','').replace('\"','\\"')
    nif_content.begin_index=0
    nif_content.end_index=len(line)
    doc_with_annotations=NIFDocument.NIFDocument()
    doc_with_annotations.addContent(nif_content)
    #line=str(line.encode('utf-8'))
    res=interpreter.parse(line.replace(',',' ').replace('"',' ').replace('\\','').replace('\n',''))
    doc_with_annotations=add_nif_entities(nif_content.uri,base_uri,res['entities'],doc_with_annotations)
    ag_string=doc_with_annotations.get_nif_string()    
    resp=requests.post(agdistis_url,ag_string.encode('utf-8'))
    print('cont'+resp.content.decode())
    doc_with_annotations=NIFDocument.nifStringToNifDocument(resp.content.decode())
    for cont in doc_with_annotations.nifContent:
        doc.addContent(cont)
    i=i+1
out_file=open(config.get('files','file_to_write'),'w')
out_file.write(doc.get_nif_string())
