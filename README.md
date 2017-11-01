# A Participant's Kit for RUSSE 2018 WSI&amp;D Competition

This repository contains instructions for participation in the [shared task on word sense induction and disambiguation for the Russian language](http://russe.nlpub.org/2018/wsi). 

Quick start
-------------

To be able to participate in the shared task you need to clone this repository and install dependencies of the evaluation script. Type this in console:

```
git clone https://github.com/nlpub/russe-wsi-kit.git
pip install -r requirements.txt
```

**Important note**: you need to have Python and pip package manager installed on your system (Linux/Windows/Mac OSX). The scripts work for both Python 2.7+ and 3.4+. We recommend using Python 3.4+.


Using the evaluation script
--------------------------

To evaluate a sample baseline based on the Adagram sense embeddings model, provided by the organizers, run:
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

Output of your script should have the same format as ```data/main/wiki-wiki/train.baseline-adagram.csv```. When the test data will be available, you'll need to run your script against it and submit to the organizers.


Description of the Datasets
--------

The participants of the shared task need to work with three datasets of varying sense inventories and types of texts. All the datasets are located in the directory ```data/main```. One dataset is located in one directory. The name of the directory is ```<inventory>-<corpus>```. For instance ```bts-rnc```, which represents a datasets based on the word sense inventory BTS (Большой Толковый Словарь) and the RNC corpus.

1. **wiki-wiki** located in ```data/main/wiki-wiki```: This dataset contains contexts from Wikipedia articles. The senses of this dataset correspond to a subset of Wikipedia articles.

2. **bts-rnc** located in ```data/main/bts-rcn```: 
This dataset contains contexts from the Russian National Corpus (RNC). The senses of this dataset correspond to the senses of the Gramota.ru online dictionary (and are equivalent to the senses of the Bolshoi Tolkovii Slovar, BTS).

3. **active-dict** located in ```data/main/active-dict```: The senses of this dataset correspond to the senses of the Active Dictionary of the Russian Language a.k.a. the 'Dictionary of Apresyan'. Contexts are extracted from examples and illustrations sections from the same dictionary.


For the three datasets described above we will release test parts which will be used for the computation of the final results and for ranking the participants. Note that in the test part, we will provide **new words**: the train datasets do not contain examples of the words in the test datasets.

In addition, in the directory ```data/additional``` we provide three extra datasets, which can be used as additional training data from (Lopukhin and Lopukhina, 2016). These datasets are based on various sense inventories (active dictionary, BTS) and various corpora (RNC, RuTenTen). Note that we will not release any test datasets that correspond to these datasets (yet they still may be useful e.g. for multi-task learning).  

The table below summarizes the datasets:

|Dataset|Type|Inventory|Corpus|Split|Num. of words|Num. of senses|Num. of contexts|
|-----|-----|---------|-----|------|:---------:|:----------:|:----------:|
|wiki-wiki|main|Wikipedia|Wikipedia|train|4|8|439
|bts-rnc|main|Gramota.ru|RNC|train|30|96|3491
|active-dict|main|Active Dict.|Apresyan Dict.|train|85|312|2073
|active-rnc|additional|Active Dict.|RNC|train|21|54|1662
|active-rutenten|additional|Active Dict.|ruTenTen|train|21|54|3052
|bts-rutenten|additional|Gramota.ru|ruTenTen|train|10|13|562

Format of the Dataset Files
----------

Train and test datasets are stored in .csv files (the name of the folder corresponds to the name of the dataset), each file has a header:

```
context_id	word	gold_sense_id	predict_sense_id	positions	context
```

**Type of the file and dialect**: CSV (TSV): tab separated,  with a header, no quote chars for fields, one row is one line in the file (no multi-line rows are supported). 

**Encoding**: utf-8

**Target**: ```predict_sense_id``` is the prediction of a system (this field is not filled by default)

**Sample**:

```
context_id	word	gold_sense_id	predict_sense_id	positions	context

1	граф	2		0-3,132-137	Граф -- это структура данных. Кроме этого, в дискретной математике теория графов ...

...	...	...	...	...	...
```

Structure of the Repository
---------------------------

- ```data``` -- directory with the train datasets and the corresponding baselines based on the Adagram
- ```evaluate.py``` -- evaluation script used to compute the official performance metric (ARI).
- ```baseline_trivial.py``` -- a script for generation of various trivial baselines, e.g. random labels.
- ```baseline_adagram.py``` -- the script used to generate the Adagram baselines
- ```requirements.txt``` -- list of all dependencies of the ```evaluate.py``` and ```baseline_trivial.py``` scripts (note that the ```baseline_adagram.py``` has more dependencies specified inside this file)

What should you do with the training data?
-------------------

Each training data contains a target word (the ```word``` column) and a context that represents the word (the ```context``` column). The ```gold_sense_id``` contains the corect sense identifier. For instance, take the first few examples from the **wiki-wiki** dataset:

The following context of the target word "замок" has id "1": 

```замок владимира мономаха в любече . многочисленные укрепленные монастыри также не          являлись замками как таковыми — это были крепости...```

and all the contexts of the word "замок" which refere to the same sense also have the sense id "1". On the other hand, the other sense of this word is represented with the sense id "2", e.g.: 

```
изобретатель поставил в тыльный конец ригеля круглую пластину , которая препятствовала передвижению засова ключом , пока пластина ( вращаемая часовым механизмом ) не становилась... 
```

Your goal really is to design a system which takes as an input a pair of (word, context) and outputs the sense identifier, e.g. "1" or "2". This is important to note that it does not matter which sense identifiers you use! They should not match sense identifiers of the gold standard! We use [clustering based evaluation](https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-clustering-1.html), namely we rely on the [Adjusted Rand Index](http://scikit-learn.org/stable/modules/generated/sklearn.metrics.adjusted_rand_score.html). Therefore, your "cluster sense labels" should not correspond nesesarily to the labels from the gold standard. 

Thus, the successfull submissions will group all contexts referring to the same word sense (by assigning the same ```predict_sense_id```). To achive this goal, you can you models which induce sense inventory from a large corpus for all words in the corpus, e.g. Adagram, or try to cluster directly the contexts of one word, e.g. using the k-Means algorithm. Besides, you can use an exising sense inventory from a dictionary to build your modes (which again do not match exactly the gold dataset, but this is not a problem).  
Below we provode more details on differences between two tracks. 

During the training phase of the shared task you are supposed to develop your models, testing them on the available datasets. You will be supposed to apply the developed models on the test data, once they will be made available.

Knowldege-free and Knowledge-Rich Tracks
----------------------------------------

During the test time, you are supposed to select between two tracks for each submission. The rule is simple: if you used any dictionaries to build your model, e.g. Wiktionary, offline dictionaries, RuThes, RuWordNet, YARN, and so on, you have to select the knowledge-rich track. Otherwise, you have to select the knowledge-free track. Thus, if you use not only text corpora, but instead you use some dictionaries your submissions must be in the knowledge-rich track. Otherwise, if the only resource your model is using is text corpora (or other resources which are not lexical dictionaries or databases containing explicit sense inventories) you can submit to the knowledge-free track. If you are not sure which track to use write to us. 

Restrictions
-----------

The only restriction which may disqualify a participant is that the use of the Gramota.ru or Bolshoi Tolkovii Slovar (Большой Толковый Словарь) is not alowed for the dataset **bts-rnc**. For the other two datasets (**wiki-wiki** and **active-dict**) there is no restrictions: participants are free to use any resources. 

Questions
---------

If you have any question, write an email to **rusemantics@googlegroups.com** or post it via [Google Groups](https://groups.google.com/forum/?fromgroups#!forum/rusemantics), which is the same thing (this is the primary way of obtaining updates about the shared task and contacting the organizers). Besides, you can follow the updates on our [Facebook group](https://www.facebook.com/rusemantics). Finally, discussions in Russian are also available at [NLPub Q&A forum](https://qa.nlpub.ru/c/russe).


