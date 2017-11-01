from __future__ import print_function
from pandas import read_csv
from random import randrange
from os.path import join
from evaluate import evaluate


def save(df, name):
    output_fpath = join(dataset_fpath, "train.{}.csv".format(name))
    df.to_csv(output_fpath, sep="\t", encoding="utf-8")
    print("Generated {} baseline dataset: {}".format(name, output_fpath))
    return output_fpath


datasets = ["data/main/wiki-wiki", "data/main/bts-rnc", "data/main/active-dict"]

for dataset_fpath in datasets:
    df = read_csv(join(dataset_fpath,"train.csv"), sep="\t", encoding="utf-8")
    
    df.predict_sense_id = df.gold_sense_id
    evaluate(save(df, "oracle"))  
    
    df.predict_sense_id = 1
    evaluate(save(df, "constant"))

    df.predict_sense_id = range(len(df))
    evaluate(save(df, "unique-dataset-wise"))

    df.predict_sense_id = [randrange(1,4) for x in range(len(df))]
    evaluate(save(df, "random-1-3"))

    df.predict_sense_id = [randrange(1,7) for x in range(len(df))]
    evaluate(save(df, "random-1-6"))

