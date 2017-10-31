#!/usr/bin/env python
"""
AdaGram (Bartunov et al., 2015) baseline.

Installation

This should work on Python 2.7 and Python 3.5+, better use Python 3.5+.
First install dependencies:

    pip install Cython numpy pandas pymystem3 sklearn tqdm

Then install python-adagram:

    pip install git+https://github.com/lopuhin/python-adagram.git

And download the model from
https://s3.amazonaws.com/kostia.lopuhin/all.a010.p10.d300.w5.m100.nonorm.slim.joblib
and place it into current directory.

    wget 'https://s3.amazonaws.com/kostia.lopuhin/all.a010.p10.d300.w5.m100.nonorm.slim.joblib'

"""
from __future__ import print_function
import argparse
import os.path
import re
import sys
import warnings

try:
    import adagram
    from pymystem3 import Mystem
    import pandas as pd
    import numpy as np
    from sklearn.metrics import adjusted_rand_score
    import tqdm
except ImportError as e:
    print('Error, please install dependencies:', e, file=sys.stderr)
    print(__doc__, file=sys.stderr)
    sys.exit(1)


mystem = Mystem()


def disambiguate(model, word, context):
    word, = lemmatized_context(word)
    probs = model.disambiguate(word, lemmatized_context(context))
    return 1 + probs.argmax()


def lemmatized_context(s):
    # This adagram model was trained with mystem lemmatizer, so better
    # use it here as well.
    return [w.lower() for w in mystem.lemmatize(s) if re.match('[\w\-]+$', w)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    arg = parser.add_argument
    arg('input', help='Path to input file with contexts')
    arg('--output', help='Path to output file with predictions')
    arg('--model', help='Path to AdaGram model (%(default)s by default)',
        default=os.path.abspath('all.a010.p10.d300.w5.m100.nonorm.slim.joblib'))
    arg('--ari-per-word', help='show ARI per-word')
    args = parser.parse_args()

    df = pd.read_csv(args.input, sep='\t')

    if not os.path.exists(args.model):
        print('Error: can not find model at {}'.format(args.model),
              file=sys.stderr)
        print(__doc__, file=sys.stderr)
        sys.exit(1)

    print('Loading AdaGram model')
    model = adagram.VectorModel.load(args.model)
    print('done')

    with warnings.catch_warnings():
        warnings.simplefilter('ignore', RuntimeWarning)
        df['predict_sense_id'] = [
            disambiguate(model, word, context)
            for word, context in tqdm.tqdm(zip(df['word'], df['context']),
                                           total=len(df))]

    if df['gold_sense_id'].any():
        per_word = df.groupby('word').aggregate(
            lambda f: adjusted_rand_score(
                f['gold_sense_id'], f['predict_sense_id']))
        per_word_ari = per_word['predict_sense_id']
        if args.ari_per_word:
            for word, ari in zip(per_word.index, per_word_ari):
                print('{:<20} {:+.4f}'.format(word, ari))
        print('Mean word ARI: {:.4f}'.format(np.mean(per_word_ari)))

    if args.output:
        print('Saving predictions to {}'.format(args.output))
        df.to_csv(args.output, sep='\t', index=None)


if __name__ == '__main__':
    main()
