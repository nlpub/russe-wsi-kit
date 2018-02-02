# A Participant's Kit for RUSSE 2018 Word Sense Induction and Disambiguation Shared Task

This repository contains instructions for participation in the [shared task on word sense induction and disambiguation for the Russian language](http://russe.nlpub.org/2018/wsi). **TLDR**: You are given a word, e.g. ```"замок"``` and a bunch of text fragments (aka "contexts") where this word occurs, e.g. ```"замок владимира мономаха в любече"``` and  ```"передвижению засова ключом в замке"```. You need to cluster these contexts in the (unknown in advance) number of clusters which correspond to various senses of the word. In this example, you want to have two groups with the contexts of the "lock" and the "castle" senses of the word ```"замок"```. For each of the three test datasets, you need to download the **text.csv** file, fill the ``predicted_sense_id`` in this file and submit it using at [CodaLab](https://competitions.codalab.org/) platform. You will immediately see your results in the leaderboard computed on a part of the test dataset. The final results will be announced on the 15th of February.

# Making a submission (test dataset)

Starting from the **15th of December** until the **4th of February** you can make a submission to the shared task. All submissions after the 4th of February will not be considered for the final ranking. The submissions are performed via the [CodaLab](https://competitions.codalab.org/) platform. To participate, follow the steps below.

## Set by step instruction: how to submit

### 1. Get the CSV files with the test datasets 

Checkout the repository:

```
git clone https://github.com/nlpub/russe-wsi-kit.git
```

You will find three files with the test datasets each named ``test.csv`` in the respective sub-directories in the ``data`` folder:

|Dataset|Inventory|Corpus|Num. of words|Num. of contexts|
|-----|---------|-----|:---------:|:----------:|
|[wiki-wiki](https://github.com/nlpub/russe-wsi-kit/blob/master/data/main/wiki-wiki/test.csv)|Wikipedia|Wikipedia|7|638
|[bts-rnc](https://github.com/nlpub/russe-wsi-kit/blob/master/data/main/bts-rnc/test.csv)|Gramota.ru|RNC|51|6556
|[active-dict](https://github.com/nlpub/russe-wsi-kit/blob/master/data/main/active-dict/test.csv)|Active Dict.|Active Dict.|168|3729


### 2. Perform word sense induction based on the test data 

Apply the model you developed on the training dataset to the test data from the mentioned above CSV files. Namely, your goal is to fill the column ``predict_sense_id`` in each file with an integer identifier of a word sense which corresponds to the given context. This procedure is exactly the same as for the training dataset (see the instructions for the training dataset for more details). In brief: you can assign sense identifiers from ANY sense inventory to the contexts. They should not match certain gold standard inventory (we do not provide any test sense inventory). The contexts (sentences) which share the same meaning should have the same ``predict_sense_id``. The context with use different meanings of the target word, e.g. ``bank (area)`` vs ``bank (company)`` should have different sense identifiers. 

In the end, you need to apply your models to the three mentioned above datasets and generate three ``test.csv`` files corresponding to your solutions of these datasets. You can use different models to solve different datasets.

### 3. Compress the test.csv into a zip archive 

This is a requirement of the CodaLab platform: all submissions should be inside a zip archive. Compress each of your ``test.csv`` file, e.g. like this: 

```
zip wiki-wiki.zip data/main/wiki-wiki/test.csv
```

In the end, you need to obtain three zip archives with the solutions. 


### 4. Register at the CodaLab platform 

Go to  [Codalab.org](https://competitions.codalab.org) and press "Sign Up". If you are already registered, press "Sign In".

**Note**: If you for some reasons cannot or do not want to use the CodaLab platform, you can send us the submissions by email to  *panchenko.alexander@gmail.com*. Please try to avoid using this option as much as possible as it creates some extra work for us. 

### 4. Submit at CodaLab the three datasets

For each of the three datasets, there exists a separate task on the CodaLab. Depending on the dataset you want to submit at the moment, you need to use the corresponding shared task: 

- **[wiki-wiki dataset](https://competitions.codalab.org/competitions/17810)**  

- **[bts-rnc dataset](https://competitions.codalab.org/competitions/17809)**

- **[active-dict](https://competitions.codalab.org/competitions/17806)** 


Follow these steps to submit a model:

  1. Click the "Participate" link. 
  
  2. If you are making the first submission register for the task by pressing the "Register" button.
  
  3. Click the "Submit / View Results" link. 
  
  4. Click "Submit" button to select zip archive from your computer. The file will be uploaded. 
   
  5. Click "Update description" and enter the name of your track ("knowledge-free" or "knowledge-rich"). It is required to indicate in the description of your job "knowledge-free" or "knowledge-rich" to let us know in which track you participate. Optionally, you can also provide a short description of your approach in the description field. Press "Save description" once you entered the text.
 
  6. Click the "Results" tab to see evaluation results of your submission.

Please let us know if you have any questions. 

## Number of submissions

We do not limit the number of submissions. You can select which submissions will be shown in the leaderboard in the settings of the CodaLab platform. 


## Knowledge-free and knowledge-rich tracks

During the test time, you are supposed to select between two tracks for each submission. The rule is simple: if you used any dictionaries to build your model, e.g. Wiktionary, offline dictionaries, RuThes, RuWordNet, YARN, and so on, you have to select the knowledge-rich track. Otherwise, you have to select the knowledge-free track. Thus, if you use not only text corpora, but instead you use some dictionaries your submissions must be in the knowledge-rich track. Otherwise, if the only resource your model is using is text corpora (or other resources which are not lexical dictionaries or databases containing explicit sense inventories) you can submit to the knowledge-free track. If you are not sure which track to use write to us.

## Restrictions

The only restriction which may disqualify a participant is that the use of the Gramota.ru or Bolshoi Tolkovii Slovar (Большой Толковый Словарь) is not allowed for developing the models for the dataset **bts-rnc**. For the other two datasets (**wiki-wiki** and **active-dict**) there are no restrictions: participants are free to use any resources.


# Developing a model (train dataset)

Quick start
-------------

To be able to participate in the shared task you need to clone this repository and install dependencies of the evaluation script. Type this in the console:

```
git clone https://github.com/nlpub/russe-wsi-kit.git
pip install -r requirements.txt
```

**System requirements**: you need to have Python and pip package manager installed on your system (Linux/Windows/Mac OSX). The scripts work for both Python 2.7+ and 3.4+. We recommend using Python 3.4+.


Using the evaluation script
--------------------------

To evaluate a sample baseline based on the Adagram sense embeddings model, provided by the organizers, run:
```
python3 evaluate.py data/main/wiki-wiki/train.baseline-adagram.csv
```

You should get the ARI scores per word and also the final value per dataset (the last value, here 0.392449):

```
word   ari       count
бор    0.591175  56
замок  0.495386  138
лук    0.637076  110
суда   0.005465  135
       0.392449  439
```

The output of your system should have the same format as the sample baseline file provided in this repository ```data/main/wiki-wiki/train.baseline-adagram.csv```. When the test data will be available, you'll need to run your system against a test file in the similar format and submit to a CSV file with the result to the organizers.


Description of the datasets
--------

The participants of the shared task need to work with three datasets of varying sense inventories and types of texts. All the datasets are located in the directory ```data/main```. One dataset is located in one directory. The name of the directory is ```<inventory>-<corpus>```. For instance ```bts-rnc```, which represents datasets based on the word sense inventory BTS (Bolshoi Tolkovii Slovar') and the RNC corpus. Here is the list of the datasets:

1. **wiki-wiki** located in ```data/main/wiki-wiki```: This dataset contains contexts from Wikipedia articles. The senses of this dataset correspond to a subset of Wikipedia articles.

2. **bts-rnc** located in ```data/main/bts-rcn```:
This dataset contains contexts from the Russian National Corpus (RNC). The senses of this dataset correspond to the senses of the Gramota.ru online dictionary (and are equivalent to the senses of the Bolshoi Tolkovii Slovar, BTS).

3. **active-dict** located in ```data/main/active-dict```: The senses of this dataset correspond to the senses of the Active Dictionary of the Russian Language a.k.a. the 'Dictionary of Apresyan'. Contexts are extracted from examples and illustrations sections from the same dictionary.


For the three datasets described above, we will release test parts which will be used for the computation of the final results and for ranking the participants. Note that **in the test part, we will provide new words: the train datasets do not contain examples of the words in the test datasets**.

In addition, in the directory ```data/additional```, we provide three extra datasets, which can be used as additional training data from (Lopukhin and Lopukhina, 2016). These datasets are based on various sense inventories (active dictionary, BTS) and various corpora (RNC, RuTenTen). Note that we will not release any test datasets that correspond to these datasets (yet they still may be useful e.g. for multi-task learning).  

The table below summarizes the datasets:

|Dataset|Type|Inventory|Corpus|Split|Num. of words|Num. of senses|Avg. num. of senses|Num. of contexts|
|-----|-----|---------|-----|------|:---------:|:----------:|:----------:|:----------:|
|wiki-wiki|main|Wikipedia|Wikipedia|train|4|8|2.0|439
|wiki-wiki|main|Wikipedia|Wikipedia|test|7|?|?|638
|bts-rnc|main|Gramota.ru|RNC|train|30|96|3.2|3491
|bts-rnc|main|Gramota.ru|RNC|test|51|?|?|6556
|active-dict|main|Active Dict.|Active Dict.|train|85|312|3.7|2073
|active-dict|main|Active Dict.|Active Dict.|test|168|?|?|3729
|active-rnc|additional|Active Dict.|RNC|train|20|71|3.6|1829
|active-rutenten|additional|Active Dict.|ruTenTen|train|21|71|3.4|3671
|bts-rutenten|additional|Gramota.ru|ruTenTen|train|11|25|2.3|956

Format of the dataset files
----------

Train and test datasets are stored in .csv files (the name of the folder corresponds to the name of the dataset), each file has a header:

```
context_id    word    gold_sense_id    predict_sense_id    positions    context
```

**Type of the file and dialect**: CSV (TSV): tab separated,  with a header, no quote chars for fields, one row is one line in the file (no multi-line rows are supported).

**Encoding**: utf-8

**Target**: ```predict_sense_id``` is the prediction of a system (this field is not filled by default)

**Sample**:

```
context_id    word    gold_sense_id    predict_sense_id    positions    context

1    граф    2        0-3,132-137    Граф -- это структура данных. Кроме этого, в дискретной математике теория графов ...

...    ...    ...    ...    ...    ...
```

Structure of this repository
---------------------------

- ```data``` -- directory with the train datasets and the corresponding baselines based on the Adagram
- ```evaluate.py``` -- evaluation script used to compute the official performance metric (ARI).
- ```baseline_trivial.py``` -- a script for generation of various trivial baselines, e.g. random labels.
- ```baseline_adagram.py``` -- the script used to generate the Adagram baselines
- ```requirements.txt``` -- the list of all dependencies of the ```evaluate.py``` and ```baseline_trivial.py``` scripts (note that the ```baseline_adagram.py``` has more dependencies specified inside this file)

What should you do with the training data (how to start)?
-------------------

Each training data contains a target word (the ```word``` column) and a context that represents the word (the ```context``` column). The ```gold_sense_id``` contains the corect sense identifier. For instance, take the first few examples from the **wiki-wiki** dataset:

The following context of the target word "замок" has id "1":

```
замок владимира мономаха в любече . многочисленные укрепленные монастыри также не  являлись замками как таковыми — это были крепости...
```

and all the contexts of the word "замок" which refer to the same "building" sense also have the sense id "1". On the other hand, the other "lock" sense of this word is represented with the sense id "2", e.g.:

```
изобретатель поставил в тыльный конец ригеля круглую пластину , которая препятствовала передвижению засова ключом , пока пластина ( вращаемая часовым механизмом ) не становилась...
```

Your goal is to **design a system which takes as an input a pair of (word, context) and outputs the sense identifier**, e.g. "1" or "2". This is important to note that it does not matter which sense identifiers you use (numbers in the "gold_sense_id" and "predict_sense_id" columns)! It is not needed that they match sense identifiers of the gold standard! For instance, if in the "gold_sense_id" column you use identifiers {a,b,c} and in the "predict_sense_id" you use identifiers {1,2,3}, but the labelling of the data match so that each context labeled with "1" is always labeled with "a", each context labeled with "2" is always labeled with "b", etc. you will get the top score. Matching of the gold and predict sense inventories is not a requirement as we use [clustering based evaluation](https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-clustering-1.html), namely we rely on the [Adjusted Rand Index](http://scikit-learn.org/stable/modules/generated/sklearn.metrics.adjusted_rand_score.html). Therefore, your cluster sense labels should not necessarily correspond to the labels from the gold standard.

Thus, the successful submissions will group all contexts referring to the same word sense (by assigning the same ```predict_sense_id```). To achieve this goal, you can you models which induce sense inventory from a large corpus of all words in the corpus, e.g. Adagram or try to cluster directly the contexts of one word, e.g. using the k-Means algorithm. Besides, you can use an existing sense inventory from a dictionary, e.g. RuWordNet, to build your modes (which again do not match exactly the gold dataset, but this is not a problem).  
Below we provide more details on differences between two tracks.

During the training phase of the shared task, you are supposed to develop your models, testing them on the available datasets. You will be supposed to apply the developed models to the test data, once they will be made available.

# Questions

If you have any question, write an email to **rusemantics@googlegroups.com** or post it via [Google Groups](https://groups.google.com/forum/?fromgroups#!forum/rusemantics), which is the same thing (this is the primary way of obtaining updates about the shared task and contacting the organizers). Besides, you can follow the updates on our [Facebook group](https://www.facebook.com/rusemantics). Finally, discussions in Russian are also available at [NLPub Q&A forum](https://qa.nlpub.ru/c/russe).
