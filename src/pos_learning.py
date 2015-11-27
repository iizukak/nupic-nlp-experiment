#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from nupic.data.inference_shifter import InferenceShifter
from nupic.frameworks.opf.modelfactory import ModelFactory
import os

import nltk
from nltk.corpus import brown

import model_params.model_params as model_params

MODEL_DIR = os.getcwd() + "/model"

def addCategoryEncoder(params, categories):
    params["modelParams"]["sensorParams"]["encoders"].update({ 
        "token": {
            "fieldname": u"token",
            "name": u"token",
            "type": "SDRCategoryEncoder",
            "categoryList": categories,
            "w": 23,
            "n": len(categories) * 23
        }
    })
    return params


def createModel(verbosity, categories):
    model = ModelFactory.create(addCategoryEncoder(model_params.MODEL_PARAMS, categories))
    model.enableInference({"predictedField": "token"})

    if verbosity:
        print(model)

    return model


def fetchCorpus():
    corpus = nltk.pos_tag(brown.words(categories="news") +
                          brown.words(categories="editorial") + 
                          brown.words(categories="reviews"))
    categories = list(set(map(lambda x:x[1], corpus)))

    return corpus, categories


def main():
    corpus, categories = fetchCorpus()
    model = createModel(True, categories)
    shifter = InferenceShifter()
    counter = 1

    for word in corpus:
        model_input = {"token": word[1]}
        result = shifter.shift(model.run(model_input))

        if counter % 100 == 0:
            print("input line:", counter)
        if counter % 1000 == 0:
            print("result:", result)
        if counter % 5000 == 0:
            print("save model")
            model.save(MODEL_DIR)

        counter += 1
    print("saving model to", MODEL_DIR)
    model.save(MODEL_DIR)

if __name__ == "__main__":
    main()

