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
