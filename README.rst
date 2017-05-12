Corenlpy documentation
======================

Purpose
-------

CoreNLP is an excellent multi-purpose NLP tool written in Java by folks at
Stanford.  Have a look at at the 
`CoreNLP website <https://stanfordnlp.github.io/CoreNLP/>`_.  
This package is meant to make it a bit easier for python users to enjoy 
CoreNLP, by providing two basic functionalities:

    1. Invoke the CoreNLP pipeline to process text from within a Python 
       script

    2. Load an annotated text file into memory as an AnnotatedText object,
       so you can traverse dependency parses, inspect POS tags, or
       find coreferent mentions without munging xml.

Installation
____________

To use ``corenlpy`` you will need to install CoreNLP itself first.  Follow
these steps:

    1. `Download CoreNLP <https://stanfordnlp.github.io/CoreNLP/#download>`_.
    2. Unzip it, and move (rename) the resulting unzipped directory to 
       ``~/corenlp``.
    3. ``pip install corenlpy``

You're ready to get parsing!

By default, ``corenlpy`` looks for a CoreNLP installation at ``~/corenlp``. 
Optionally, you can put CoreNLP somewhere else, and tell ``corenlpy`` where 
to find it by writing an rc file at ``~/.corenlpyrc`` with the following 
line:

.. code-block:: JSON

    {"corenlp_path": "/path/to/the/corenlp/unzipped/dir"}


Run CoreNLP in python
---------------------
OK, let's annotate some files!  To run corenlp on all the files in, say, 
``my_dir``, you would do something like this:

.. code-block:: python

    >>> import corenlpy
    >>> corenlpy.corenlp('path/to/my_dir')

By default, all the files present in ``my_dir`` will be annotated and stored
as xml files in the same directory (named by appending '.xml').

You can control how CoreNLP is run using various keyword arugments.  
Specify multiple input directories, or provide an iterable of 
individual files to annotate, and specify the output directory.  You 
can take advantage of more cores by running CoreNLP with 
multiple threads.  You can also choose from the available output formats 
(default is ``'xml'``; others that are available are 
``'json'``, ``'conll'``, ``'conllu'``, 
``'text'``, and ``'serialized'``, as explained `here <http://stanfordnlp.github.io/CoreNLP/cmdline.html>`_.).

The CoreNLP tool allows you to specify various annotators that perform
different core NLP tasks, like tokenizing, sentence splitting, 
POS-tagging, lemmatization,  named entity recognition, etc.  You can specify
which annotators you want by providing a list of them.  Read about 
the available annotators
`here <http://stanfordnlp.github.io/CoreNLP/annotators.html>`_.  

Here is an example of all these options in action:

.. code-block:: python

    >>> corenlpy.corenlp(
            in_dirs=['path/to/dir1', 'path/to/dir2'],
            in_files=['path/to/some/file1', 'path/to/some/file2'],
            out_dir='path/to/output_direcoty',
            annotators=['tokenize', 'ssplit', 'pos', 'lemma', 'ner', 'parse', 'dcoref'],
            threads=4,
            output_format='xml'
        )

Note that ``in_dirs`` can be a single directory or a list thereof, and
``in_files`` can be a single file or a list thereof.  When directories
are provided, CoreNLP will be invoked on *all* files within them.

CoreNLP has many other options that can be specified by a 
`"properties file" <http://stanfordnlp.github.io/CoreNLP/cmdline.html>`_ 
(see subheading "Configuration").  In ``corenlpy``, those options can be 
set by passing in a dictionary, where the keys are property names, and the
values are the property values.  E.g.:

.. code-block:: python

    >>> c.corenlp(
            'path/to/my_file',
            properties={'ner.model':'edu/stanford/nlp/models/ner/english.conll.4class.distsim.crf.ser.gz'}
        )

Note that some of the keyword options we saw above can also be set in a 
properties file; the value in the properties file takes precedence.

Working with ``AnnotatedText``
------------------------------
The ``AnnotatedText`` class is what originally motivated the creation of
this package.  If you need to work with annotation outputs from CoreNLP
in Python, this will save you a lot of time.  It's best to illustrate how
it works using an example.

Example
-------

Suppose we have the one-sentence document:

   *President Obama cannot run for a third term (but I think he wants to).*

Let's assume that it has been processed by CoreNLP, creating the output 
file ``obama.txt.xml``.  

Instantiation
-------------
The first thing we do is import the module and get an ``AnnotatedText`` 
object.

