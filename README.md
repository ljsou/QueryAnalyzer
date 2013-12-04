Query Analizer
====================================

Usually, the terms used by users during tagging are different from the terms/queries used when searching for web resources, this problem is known as the "*gulf of execution*”, which describes the cognitive gap between a user’s goals and a system’s functionality or content. In this sense, this project tries to deal the above problem. 

This is a project developed within the research group on telematics engineering at the University of Cauca.

##Requirements

- Python >= 2.6 or >= 3.3
- NLTK
- TextBlob
- Gensim

###1. Natural Language Toolkit (NLTK)   nltk.org

NLTK -- the Natural Language Toolkit -- is a suite of open source
Python modules, data sets and tutorials supporting research and
development in Natural Language Processing. For documentation, please visit http://nltk.org/

To install NLTK, run setup.py from an administrator account, e.g.:

    sudo python setup.py install

For full installation instructions, please see http://nltk.github.com/install.html


###2. TextBlob: Simplified Text Processing

**TextBlob** is a Python (2 and 3) library for processing textual data. It provides a simple API for diving into common natural language processing (NLP) tasks such as part-of-speech tagging, noun phrase extraction, sentiment analysis, classification, translation, and more. TextBlob stands on the giant shoulders of `NLTK` and `pattern`, and plays nicely with both. Homepage: https://textblob.readthedocs.org/

####Get it now

    $ pip install -U textblob
    $ curl https://raw.github.com/sloria/TextBlob/master/download_corpora.py | python

Full documentation is available at https://textblob.readthedocs.org/.


###3. gensim -- Python Framework for Topic Modelling

Gensim is a Python library for *topic modelling*, *document indexing* and *similarity retrieval* with large corpora.
Target audience is the *natural language processing* (NLP) and *information retrieval* (IR) community.

For a Python3 port of gensim by Parikshit Samant, visit ["this fork"](https://github.com/samantp/gensimPy3).

####Installation

This software depends on ["NumPy"](http://www.numpy.org/) and ["Scipy"](http://www.scipy.org/Download), two Python packages for scientific computing.
You must have them installed prior to installing `gensim`.

The simple way to install `gensim` is::

    sudo easy_install gensim

Or, if you have instead downloaded and unzipped the [source tar.gz](http://pypi.python.org/pypi/gensim) package,
you'll need to run:

    python setup.py test
    sudo python setup.py install


For alternative modes of installation (without root privileges, development
installation, optional install features), see the [documentation](http://radimrehurek.com/gensim/install.html).

This version has been tested under Python 2.7, and should run on any 2.5 <= Python < 3.0.

