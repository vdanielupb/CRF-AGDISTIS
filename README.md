# CRF-AGDISTIS


## Requirements

* rasa_nlu version 0.10.6

* flask version 0.12.2

## Configurations

Configurations can be set in the file conf/conf.cnf

    [rasa]

        rasa_config_file = conf/conf.json

        rasa_model_directory = model/

        rasa_model = model/default/example_model/

        training_file = data/example.csv

    [flask]

        host=127.0.0.1

    [agdistis]

        agdistis_url = http://localhost:8080/AGDISTIS

    [files]

        file_to_annotate = data/example.csv

        file_to_write = out/nif_test.ttl

## Training of a new model
* annotate a Traingfile, annotate Entities like <entity>exampleEntity</entity>, where each line is one document

* use the scrpit buildpersistentmodel to train the model
* required settings:
  * rasa_config_file: the config for rasa nlu (example config can be found in the folder conf)
  * rasa_model_directory: folder to save the new model
  * training_file: File with the training data

## Run the Webservice
* start the script nifservice.py

* required settings:
  * rasa_config_file: the config for rasa nlu (example config can be found in the folder conf)
  * rasa_model: directory of the model to be used
  * host: The URL/IP where the webservice should be hosted
  * agdistis_url: location of the AGDISTIS Webservice
## Run the File Annotator
  
* start the script file annotator

* required settings:
  * rasa_config_file: the config for rasa nlu (example config can be found in the folder conf)
  * rasa_model: directory of the model to be used
  * agdistis_url: location of the AGDISTIS Webservice
