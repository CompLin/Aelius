# -*- coding: utf-8 -*-
# Aelius Brazilian Portuguese POS-Tagger and Corpus Annotation Tool
#
# Copyright (C) 2010-2011 Leonel F. de Alencar
# Author: Leonel F. de Alencar <leonel.de.alencar@ufc.br>
#          
# URL: <http://sourceforge.net/projects/aelius/>
# For license information, see LICENSE.TXT

"""TODO.
"""

# As variáveis abaixo iniciadas por __ são baseadas nas variáveis
# análogas do NLTK:

# Copyright (C) 2001-2011 NLTK Project
# Authors: Steven Bird <sb@csse.unimelb.edu.au>
#          Edward Loper <edloper@gradient.cis.upenn.edu>
# URL: <http://nltk.org/>

__versao__ = "0.9.4 dec-23-2011"
__version__ = __versao__
__copyright__ = """Copyright (C) 2010-2011 Leonel F. de Alencar

Distributed and Licensed under the Apache License, Version 2.0,
which is included by reference.
"""
__descricao__="""O Aelius integra um conjunto de módulos implementados em Python, com base no NLTK, bem como dados linguísticos para treino e avaliação de etiquetadores morfossintáticos e anotação de corpora nessa variedade.
"""
__description__="""Aelius is a suite of Python, NLTK-based modules and language data for training and evaluating POS-taggers for Brazilian Portuguese and annotating corpora in this language variety.
"""
__licenca__ = "Apache License, Version 2.0"
__license__ = __licenca__
__mantenedor__ = "Leonel F. de Alencar"
__maintainer__ = __mantenedor__
__email_do_mantenedor__ = "leonel.de.alencar@ufc.br"
__email__ = __email_do_mantenedor__
__autor__ = __mantenedor__
__author__ = __autor__
__email_do_autor__ = __email_do_mantenedor__

__all__=['ProcessaNomesProprios',
         'AnotaCorpus',
         'Avalia',
         'MXPOST',
         'CalculaEstatisticasLexicais',
         'ExpandeContracoes', 
         'Toqueniza',
         'SimplificaEtiquetas',
         'Chunking',
         'Extras']

