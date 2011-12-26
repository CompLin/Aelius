# -*- coding: utf-8 -*-
# Aelius Brazilian Portuguese POS-Tagger and Corpus Annotation Tool
#
# Interface to Adwait Ratnaparkhi's MXPOST POS-tagger
#
# Copyright (C) 2010-2011 Leonel F. de Alencar
# Author: Leonel F. de Alencar <leonel.de.alencar@ufc.br>
# URL: <http://sourceforge.net/projects/aelius/>
# For license information, see LICENSE.TXT
#
# $Id: mxpost.py $

# Code and documentation mostly adapted from the following open source,
# licensed under the Apache License, Version 2.0:
# Natural Language Toolkit: Interface to the Stanford POS-tagger
#
# Copyright (C) 2001-2011 NLTK Project
# Author: Nitin Madnani <nmadnani@ets.org>
# URL: <http://www.nltk.org/>
#
# $Id: stanford.py $

"""
A module for interfacing with Adwait Ratnaparkhi's MXPOST POS-tagger.
"""

import os
from subprocess import PIPE
import tempfile
import nltk
#from api import *

_mxpost_url = 'http://sites.google.com/site/adwaitratnaparkhi/publications'

class MXPOSTTagger(nltk.TaggerI):
    """
    A class for pos tagging with MXPOST Tagger. The input is the paths to:
     - a model trained on training data
     - (optionally) the path to the mxpost tagger jar file. If not specified here,
       then this jar file must be specified in the CLASSPATH envinroment variable.
     - (optionally) the encoding of the training data (default: ASCII)

    Example using the LX-Tagger Portuguese model from http://lxcenter.di.fc.ul.pt/tools/en/LXTaggerEN.html, described in the following paper:

Branco, António and João Silva, 2004, Evaluating Solutions for the Rapid Development of State-of-the-Art POS Taggers for Portuguese. In Maria Teresa Lino, Maria Francisca Xavier, Fátima Ferreira, Rute Costa and Raquel Silva (eds.), Proceedings of the 4th International Conference on Language Resources and Evaluation (LREC2004), Paris, ELRA, ISBN 2-9517408-1-6, pp.507-510.

        >>> mx = MXPOSTTagger('UTF-8_Model_Cintil_Written')
       >>> mx.tag('Será que está funcionando ?'.decode('utf-8').split())
[(u'Ser\xe1', u'V'), (u'que', u'CJ'), (u'est\xe1', u'V'), (u'funcionando', u'GER'), (u'?', u'PNT')]
    """
    def __init__(self, path_to_model, path_to_jar=None, encoding=None, verbose=False):

        self._mxpost_jar = nltk.internals.find_jar(
                'mxpost.jar', path_to_jar,
                searchpath=(), url=_mxpost_url,
                verbose=verbose)

        if not os.path.isdir(path_to_model):
            raise IOError("MXPOST tagger model file not found: %s" % path_to_model)
        self._mxpost_model = path_to_model
        self._encoding = encoding

    def tag(self, tokens):
        return self.batch_tag([tokens])[0]

    def batch_tag(self, sentences):
        encoding = self._encoding
        nltk.internals.config_java(options='-mx30m', verbose=False)

        # Create a temporary input file
        _input_fh, _input_file_path = tempfile.mkstemp(text=True)

        # Build the java command to run the tagger
        _mxpos_cmd = ['tagger.TestTagger', \
                         self._mxpost_model]

        # Write the actual sentences to the temporary input file
        _input_fh = os.fdopen(_input_fh, 'w')
        _input = '\n'.join((' '.join(x) for x in sentences))
        if isinstance(_input, unicode) and encoding:
            #_input = _input.encode("utf-8")
            _input = _input.encode(encoding)
        _input_fh.write(_input)
        _input_fh.close()

        # Run the tagger and get the output
        _input_fh=open(_input_file_path,"r")
        mxpos_output, _stderr = nltk.internals.java(_mxpos_cmd,
        classpath=self._mxpost_jar,
        stdin= _input_fh,stdout=PIPE, stderr=PIPE)
        _input_fh.close()
        if encoding:
            mxpos_output = mxpos_output.decode(encoding)

        # Delete the temporary file
        os.unlink(_input_file_path)

        # Output the tagged sentences
        tagged_sentences = []
        for tagged_sentence in mxpos_output.strip().split("\n"):
            sentence = [tuple(tagged_word.strip().split("_"))
                        for tagged_word in tagged_sentence.strip().split()]
            tagged_sentences.append(sentence)
        return tagged_sentences

