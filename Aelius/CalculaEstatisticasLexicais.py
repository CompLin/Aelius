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
# $Id: CalculaEstatisticasLexicais.py $

"""Este módulo contém funções para análise automática de textos.
Certifique-se de que os arquivo a serem processados estão em utf-8."""

import nltk, pickle, os
from nltk.probability import FreqDist

MODELO=os.path.join(os.path.expanduser("~"),"aelius_data/freq_tycho_a.pkl")

def FreqCorpusRef(arquivo=MODELO):
    """Extrai de arquivo a distribuição de freqüências de um corpus de
    referência
    """
    f=open(arquivo,"rb")
    return pickle.load(f)

def CriaLeitorDeCorpus(diretorio=".",arquivo="conquista_div_01.txt", codificacao="utf-8"):
    return nltk.corpus.PlaintextCorpusReader(diretorio,arquivo,encoding=codificacao)

def ExtraiAlfabeticas(palavras):
    'A partir de uma lista de token, extrai as palavras alfabéticas e as minusculiza'
    # minusculize p para p na lista de palavras se p é alfabético
    return [p.lower() for p in palavras if p.isalpha()]

def CalculaDiversidadeLexical(freq):
    '''Esta função calcula a diversidade lexical de um texto a partir de
uma distribuição de frequências do NLTK.'''
    print "Calculando diversidade lexical..."
    return 100*float(freq.B())/freq.N()

def ExibeListaDeFrequencias(freq, maximo=30):
    """A partir de instância da classe FreqDist do NLTK, esta função constrói
    uma lista dos itens mais freqüentes, com as respectivas quantidades de ocorrências
    e freqüencias.
    """
    i=0
    for k in freq:
	if i < maximo:
		print "%d\t%s\t%d\t%.4f" % (i+1,k, freq[k],100*freq.freq(k))
	else:
		break
	i+=1

def ComparaListasDeFrequencias(freq,freq_ref=FreqCorpusRef(),maximo=30,dif_min=0.0015):
    """Compara as distribuições de freqüências de um corpus de estudo
    e de um corpus de referência.
    """
    r=[] # resultados
    i=0
    print "nr.\tpalavra\t%\tdiferença %"
    for f in freq:
	if i > maximo-1:
		break
	if (freq.freq(f) - freq_ref.freq(f)) > dif_min:
            r.append((freq.freq(f) - freq_ref.freq(f),f,freq.freq(f)) )
            #print i
            print "%d\t%s\t\t%.3f\t%.6f" % (i+1,f,freq.freq(f) ,freq.freq(f) - freq_ref.freq(f))
            i+=1
	
    r.sort(reverse=True)
    print "\nResultados ordenados decrescentemente pelas diferenças de freqüência\n"
    for e in r:
        print "%.6f\t\t%s\t\t%.3f" % e

def DefinePontuacao(incluir=[],excluir=[]):
    """Esta função permite incluir ou excluir elementos da lista 
pré-definida de sinais de pontuação de Python.
"""
    from string import punctuation as punct
    punct=[p for p in punct]
    if incluir:
        punct.extend(incluir)
    if excluir:
        punct=[p for p in punct if p not in excluir]
    return punct

def SeparaPontuacao(texto, pontuacao=DefinePontuacao(excluir=["-"])):
    """Esta função separa as palavras dos sinais de pontuação, contidos
por defeito na lista retornada pela função DefinePontuacao().
"""
    s=""
    for c in linha:
        if c in pontuacao:
            s="%s %s" % (s,c)
        else:
            s="%s%s" % (s,c)
    return s

def ProcessaArquivo(f):
    """Calcula estatísticas do arquivo dado."""
    print "Processando arquivo %s..." % f
    corpus=CriaLeitorDeCorpus(arquivo=f)
    tokens=corpus.words()
    print "Quantidade de tokens: %d." % len(tokens)
    alfabeticas=ExtraiAlfabeticas(tokens)
    print "Quantidade de tokens alfabéticos: %d." % len(alfabeticas)
    freq=FreqDist(alfabeticas)
    print "Diversidade lexical: %.2f%%" % CalculaDiversidadeLexical(freq)
    print "Quantidade de hapaxes: %d.\n\n\n" % len(freq.hapaxes())


def ProcessaArquivos(*lista_de_arquivos):
    for f in lista_de_arquivos:
	if os.path.isfile(f):
            ProcessaArquivo(f)
	else:
	    print 'Arquivo "%s" inexistente em %s\n\n' % (f,os.getcwd())

		
