Goal Analizer
====================================

##Requirements

- Python >= 2.6 or >= 3.3

###Natural Language Toolkit (NLTK)   nltk.org

NLTK -- the Natural Language Toolkit -- is a suite of open source
Python modules, data sets and tutorials supporting research and
development in Natural Language Processing.

Copyright (C) 2001-2013 NLTK Project. For documentation, please visit http://nltk.org/

To install NLTK, run setup.py from an administrator account, e.g.:

    sudo python setup.py install

For full installation instructions, please see http://nltk.github.com/install.html


###TextBlob: Simplified Text Processing

Homepage: https://textblob.readthedocs.org/

**TextBlob** is a Python (2 and 3) library for processing textual data. It provides a simple API for diving into common natural language processing (NLP) tasks such as part-of-speech tagging, noun phrase extraction, sentiment analysis, classification, translation, and more. TextBlob stands on the giant shoulders of `NLTK`_ and `pattern`_, and plays nicely with both.

####Get it now

    $ pip install -U textblob
    $ curl https://raw.github.com/sloria/TextBlob/master/download_corpora.py | python

Full documentation is available at https://textblob.readthedocs.org/.


###gensim -- Python Framework for Topic Modelling

Gensim is a Python library for *topic modelling*, *document indexing* and *similarity retrieval* with large corpora.
Target audience is the *natural language processing* (NLP) and *information retrieval* (IR) community.

For a Python3 port of gensim by Parikshit Samant, visit `this fork <https://github.com/samantp/gensimPy3>`_.

####Installation

This software depends on `NumPy and Scipy <http://www.scipy.org/Download>`_, two Python packages for scientific computing.
You must have them installed prior to installing `gensim`.

It is also recommended you install a fast BLAS library prior to installing NumPy. This is optional, but using an optimized BLAS such as `ATLAS <http://math-atlas.sourceforge.net/>`_ or `OpenBLAS <http://xianyi.github.io/OpenBLAS/>`_ is known to improve performance by as much as an order of magnitude.

The simple way to install `gensim` is::

    sudo easy_install gensim

Or, if you have instead downloaded and unzipped the `source tar.gz <http://pypi.python.org/pypi/gensim>`_ package,
you'll need to run::

    python setup.py test
    sudo python setup.py install


For alternative modes of installation (without root privileges, development
installation, optional install features), see the `documentation <http://radimrehurek.com/gensim/install.html>`_.

This version has been tested under Python 2.5, 2.6 and 2.7, and should run on any 2.5 <= Python < 3.0.

