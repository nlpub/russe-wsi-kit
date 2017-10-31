Labeled context for WSI/WSD
===========================

Installation
-------------

To be able to run the evaluation script ```evaluate.py``` you need to install dependencies:

```
pip install -r requirements.txt
```

Using the evaluation script
--------------------------

To evaluate a sample baseline based on the Adagram sense embeddings model, provided by the organizers run:
```
python3 evaluate.py data/main/wiki-wiki/train.baseline-adagram.csv
```

You should get the ARI scores per word and also the final value per dataset (the last value, here 0.392449):

```
word    ari count
бор 0.591175    56
замок   0.495386    138
лук 0.637076    110
суда    0.005465    135
    0.392449    439
```

Your goal is to create a file similar to ```data/main/wiki-wiki/train.baseline-adagram.csv``` and submit it to the organizers.


Datasets
--------

The participants of the shared task need to work with three datasets of varying sense inventories and types of texts. All the datasets are located in the directory ```data/main```. One dataset is located in one directory. The name of the directory is <inventory>-<corpus>. For instance ```bts-rnc```, which represents a datasets based on the word sense inventory BTS (Большой Толковый Словарь) and the RNC corpus.

1. **wiki-wiki** located in ```data/main/wiki-wiki```: This dataset contains contexts from Wikipedia articles. The senses of this dataset correspond to a subset of Wikipedia articles.

2. **bts-rnc** located in ```data/main/bts-rcn```: 
This dataset contains contexts from the Russian National Corpus (RNC). The senses of this dataset correspond to the senses of the Gramota.ru online dictionary (and are equivalent to the senses of the Bolshoi Tolkovii Slovar, BTS).

3. **active-dict** located in ```data/main/active-dict```: This dataset contains contexts from Wikipedia articles. The senses of this dataset correspond to the senses of the Active Dictionary of the Russian Language a.k.a. the 'Dictionary of Apresyan'.


The three datasets described above are train parts of the datasets which will be used for testing (ie. for the computation of the final resuls and for ranking the participants). Note that in the test part, we will provide **new words**: the train datasets do not contain examples of the words in the test datasets. 

In addition, in the directory ```data/additional``` we provide three extra datasets, which can be used as additional training data from (Lopukhin and Lopukhina, 2016). These datasets are based on various sense inventories (active dictionary, BTS) and various corpora (RNC, RuTenTen). Note that we will not release any test datasets that correspond to these datasets (yet they still may be useful e.g. for multi-task learning).  

The table below summarizes the datasets provided in this repository:


Data format
----------

Train and test datasets is stored in .csv files named by words, each file has a header:

```
context_id	word	gold_sense_id	predict_sense_id	positions	context
```

**Type of the file and dialect**: CSV (TSV): tab separated,  with a header, no quote chars for fields, one row is one line in the file (no multi-line rows are supported). 

**Encoding**: utf-8
```predict_sense_id``` is the prediction of a system (this field is not filled by default)

**Sample**:

```
context_id	word	gold_sense_id	predict_sense_id	positions	context

1	граф	2		0-3,132-137	Граф -- это структура данных. Кроме этого, в дискретной математике теория графов ...

...	...	...	...	...	...
```

Structure of the repository
---------------------------

- ```data``` -- directory with the train datasets and the corresponding baselines based on the Adagram
- ```evaluate.py``` -- evaluation script used to compute the official performance metric (ARI).
- ```baseline_trivial.py``` -- a script for generation of various trivial baselines, e.g. random labels.
- ```baseline_adagram.py``` -- the script used to generate the Adagram baselines (you can use it e.g. for re-training the model on other corpora)
- ```requirements.txt``` -- list of all dependencies of the ```evaluate.py``` and ```baseline_trivial.py``` scripts (note that the ```baseline_adagram.py``` has more dependencies specified inside this file)

Restrictions
-----------

The only restriction which may disqualify a participant is that the use of the Gramota.ru or Bolshoi Tolkovii Slovar (Большой Толковый Словарь) is not alowed for the dataset ```
