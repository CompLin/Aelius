#! /usr/bin/env python2.6
# -*- coding: utf-8 -*-

# Aelius Brazilian Portuguese POS-Tagger and Corpus Annotation Tool
#
# Copyright (C) 2010-2011 Leonel F. de Alencar
# Author: Leonel F. de Alencar <leonel.de.alencar@ufc.br>
#          
# URL: <http://sourceforge.net/projects/aelius/>
# For license information, see LICENSE.TXT
#
# $Id: AeliusLite.py $

"""TODO.
"""

import os
from Extras import carrega
from AnotaCorpus import toqueniza_contracoes,anota_sentencas,anota_texto
from Toqueniza import TOK_PORT, TOK_PORT_LX

EXEMPLO=carrega("exemplo.txt")

def AnotaTextoBRUBT(caminho_do_arquivo=EXEMPLO):
	if os.path.isabs(caminho_do_arquivo):
		raiz,nome=os.path.split(caminho_do_arquivo)
		
	else:
		raiz,nome=os.path.split(os.path.join(os.getcwd(),caminho_do_arquivo))
	anota_texto(nome,raiz=raiz)

# acrescentar outras funções desse tipo, como 
# AnotaTextoHunPos(caminho_do_arquivo), 
# AnotaTextoLXTagger(caminho_do_arquivo) etc.

