Corenlpy documentation
======================

This documentation is best viewed on 
`ReadTheDocs <http://corenlpy.readthedocs.io/en/latest/>`_.

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
_____________
The first thing we do is import the module and get an ``AnnotatedText`` 
object.

.. code-block:: python

   >>> from corenlpy import AnnotatedText as A
   >>> xml = open('obama.txt.xml').read()
   >>> annotated_text = A(xml)

Sentences
_________

Usually you'll access parts of the document using the ``sentences`` list.

.. code-block:: python

   >>> len(annotated_text.sentences)
   1
   >>> sentence = annotated_text.sentences[0]
   >>> sentence.keys()
   ['tokens', 'entities', 'references', 'mentions', 'root', 'id']


A ``Sentence`` is a special class that, for the most part, feels like a 
simple ``dict``.  

The ``tokens`` property is a list of the sentence's tokens:

.. code-block:: python

   >>> obama = sentence['tokens'][1]
   >>> obama
   ' 0: Obama (10,14) NNP PERSON'
   >>> term = sentence['tokens'][7]
   >>> term
   ' 7: term (39,42) NN -'

Tokens
_______
Tokens have properties corresponding to CoreNLP's annotations, plus some 
other stuff:

.. code-block:: python

   >>> obama.keys()
   ['word', 'character_offset_begin', 'character_offset_end', 'pos', 
   'lemma', 'sentence_id', 'entity_idx', 'speaker', 'mentions', 'parents', 
   'ner', 'id']


Named Entities
______________
"Obama" is the name of a person, so, if CoreNLP is working well, it should
pick that up.  Named entity information is found in the ``ner`` property:

.. code-block:: python

   >>> obama['ner']
   'PERSON'
   >>> term['ner'] is None
   True

POS Tags
________
Similarly we can check the part-of-speech:

.. code-block:: python

   >>> obama['pos']
   'NNP'
   >>> term['pos']
   'NN'

Dependency Tree
_______________
We can traverse the dependency tree using the ``parents`` and ``children``
properties.  In our example, "run" is the parent of "Obama" 
(because "Obama" is the subject (``nsubj``) of "run"):

.. code-block:: python

    >>> relation, parent = obama['parents'][0]
    >>> relation
    u'nsubj'
    >>> parent
    ' 3: run (23,25) -'

If you're processing dependency trees, you'll often want to start with
the head word (which is like the root of the sentence).  Sentences have a
special ``root`` property that stores the head word.  Usually it's a verb:

.. code-block:: python

   >>> sentence['root']
   ' 3: run (23,25) -'

Coreference Chains
__________________
A coreference chain is a series of references to the same entity.  In our 
example, "President Obama" and "he" are each *mentions* from the same
coreference chain.  We can access all the mentions of a coreference chain.

First, we can get the mention that "Obama" is part of:

.. code-block:: python

    >>> first_mention = obama['mentions'][0]
    >>> first_mention['tokens']
    [' 0: President (0,8) -', ' 1: Obama (10,14) PERSON']

Note that a token can be part of multiple mentions.  For example, consider
the phrase "Obama's pyjamas".  If his pyjamas are mentioned multiple times,
then there will be a coreference chain made for it, as well as for Obama
himself.  And in the phrase "Obama's pyjamas", the token "Obama" is both 
part of a mention corresponding to the 44th President of the United States,
and part of a mention corresponding to some garments for sleeping.

Once we have gotten ahold of a mention, we can access the coreference
chain that it belongs to, which is found in the mention's ``'reference'`` 
property.  Conversely, if we have accessed a coreference chain, we can
find all of its mentions by looking at its ``'mentions'`` property.

So,  starting from the mention containing the token "Obama", we can get
to the other mention ("he") like this:

.. code-block:: python

   >>> reference = first_mention['reference']
   >>> len(reference['mentions'])
   2
   >>> second_mention = reference['mentions'][1]
   >>> second_mention['tokens']
   ['12: he (57,58) -']

Mentions have various properties:

.. code-block:: python

   >>> first_mention.keys()
   ['head', 'end', 'reference', 'tokens', 'start', 'sentence_id']

In addition to the coreference chain (``'reference'``), we get the id of 
the sentence in which the mention is found, the list
of token objects in the mention, the slice indices 
(``'start'`` and ``'end'``) for those tokens as they occur in the 
sentence's token list, and the head token of the 
mention.

References have various properties too:

.. code-block:: python

   >>> reference.keys()
   ['mentions', 'id', 'representative']

In addition to the mentions that are part of the coreference chain, we
get an id for the coreference chain (unique on a per-article-basis), 
and a reference to the
"representative" mention.  The representative mention is the one that is
deemed to have the fullest realization of the object's name.  So in our
example, the representative reference would be "President Obama", not "he".
This is useful for getting the human-readable name to represent the
coreference chain.

We can access all of the mentions or all of the coreference chains, for 
a given sentence, using its ``mentions`` and ``references`` properties. 

.. code-block:: python

    >>> len(sentence['mentions'])
    2
    >>> len(sentence['references'])
    1

One thing to note is that mentions and references aren't necessarily 
anchored to any named entity (though they often are). 
For example, consider this sentence:

   *The police are yet to find any suspects.  They say they will continue 
   their search.*

Here, "The police", "they" (which occurs twice), and "their" are all 
part of one coreference chain, yet none is a named entity.

To access *only* mentions that are named entities, use the ``entities`` 
property of the sentence.

The document as a whole also provides global ``mentions``, ``references``,
and ``entities`` properties which can be iterated over directly..

Reference
---------
.. py:class:: AnnotatedText(corenlp_xml, **kwargs)

   Create a new AnnotatedText object.  Only the first parameter is normally
   needed.  The remaining parameters enable adding entity linking data from
   the AIDA software, controlling the kind of dependency parse
   used, and filtering the kinds of named entities, coreference chains,
   and mentions that are included (by default all those provided by CoreNLP
   are are included).

   :param str corenlp_xml: An xml string output by CoreNLP.
   :param str aida_json=None: A JSON string output by AIDA.  AIDA is a program that disambiguates named entities, linking them to the YAGO knowledge base.  If the JSON output of AIDA is provided, then ``entities``, ``mentions`` and ``references`` entries will be augmented with entity linking information.
   :param str dependencies='collapsed-ccprocessed': Determines which kind of dependencies will be used in constructing dependency trees.  Three options are available: ``'collapsed-ccprocessed'`` (the default), ``'collapsed'``, and ``'basic'``.
   :param bool exclude_ordinal_NERs=False: Whether to recognize ordinal named entities.  If ``True``, named entities of the following types will be ignored: ``'TIME'``, ``'DATE'``, ``'NUMBER'``, ``'DURATION'``, ``'PERCENT'``, ``'SET'``, ``'ORDINAL'``, and ``'MONEY'``.
   :param bool exclude_long_mentions=False: CoreNLP occaisionally includes mentions, as part of coreference chains, that are very long noun phrases.  These mentions can be surprising and are often not useful.  Setting this option to ``True`` causes any mentions longer that the value specified by ``long_mention_threshold`` to be discarded (default length is 5 tokens).
   :param int long_mention_threshold=5: Maximum number of tokens allowed in a coreference chain mention, above which the mention will be ignored if ``exclude_long_mentions`` is ``True``.
   :param bool exclude_non_ner_coreferences=False: In some cases, it is only desirable to consider those coreference chains that have at least one named entity as a mention.  Setting this option to ``True`` will exclude references and their mentions if the reference includes no named entities.

