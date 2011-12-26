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
# $Id: Chunking.py $

"""Chunker simples para o português baseado no tagset do LX-Tagger
http://lxcenter.di.fc.ul.pt/tools/pt/conteudo/LXTagger.html"""

import nltk
from os.path import join,splitext

RAIZ="analises"
TEXTO="ufc_07042011.pdt.mxpost.txt"

CHUNKER= nltk.chunk.RegexpParser(r'''
NP:
{<DA>?<PNM>(<PREP>?<DA>?<CJ>?<PNM>)*}
{<QNT>?<DA>?<UM>?<IA>?<ORD>?<POSS>?<CARD>?<DEM>?<DGTR?>?<STT>*<AD[VJ]>*<PPA>*(<CN>|<WD>|<MHT>)<AD[VJ]>*<PPA>*}
''')

def CriaChunkedCorpus(raiz,texto,chunker=CHUNKER,destino=None,formato="trees"):
    nome_do_destino=""
    if destino:
        nome_do_destino=destino
    else:
        nome_do_destino=join(raiz,"%s.%s.txt" % (splitext(texto)[0],formato))
    f=open(nome_do_destino,"w")
    c=nltk.corpus.TaggedCorpusReader(raiz,texto,encoding="utf-8")
    sents=c.tagged_sents()
    chunked_sents=chunker.batch_parse(sents)
    if formato=="IOB":
        for s in chunked_sents:
            s=nltk.chunk.tree2conllstr(chunker.parse(s))
            f.write("%s\n\n" % (s.encode("utf-8")))
    else:
        for s in chunked_sents:
            f.write("%s\n\n" % (s.pprint().encode("utf-8")))
    f.close()

def IOB2trees(arquivo):
    """A partir de um arquivo de sentenças cujos chunks do tipo NP estão anotados no formato IOB, retorna uma lista de árvores do tipo nltk.Tree.
    """
    linhas=open(arquivo).read().strip().split("\n\n")
    return [nltk.chunk.conllstr2tree(c) for c in linhas]

def avalia(arquivo,chunker=CHUNKER):
    """Avalia um chunker com base num arquivo no formato IOB corrigido por humano.
    """
    trees=IOB2trees(arquivo)
    print chunker.evaluate(trees)
    
def main():
    CriaChunkedCorpus(RAIZ,TEXTO,CHUNKER,destino=None,formato="trees")
    CriaChunkedCorpus(RAIZ,TEXTO,CHUNKER,destino=None,formato="IOB")
