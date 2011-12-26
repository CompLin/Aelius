# -*- coding: utf-8 -*-
# Aelius Brazilian Portuguese POS-Tagger and Corpus Annotation Tool
#
# Copyright (C) 2010-2011 Leonel F. de Alencar
# Author: Leonel F. de Alencar <leonel.de.alencar@ufc.br>
#          
# URL: <http://sourceforge.net/projects/aelius/>
# For license information, see LICENSE.TXT
#
# $Id: Extras.py $

"""Contém algumas funções utilizadas por diversos outros módulos,
como a função 'carrega', que facilita o uso de modelos,corpora e
outros recursos. 
Esses recursos devem estar armazenados ou no diretório 
$HOME/aelius_data ou no diretório especificado na variável de ambiente
AELIUS_DATA."""

import os

USUARIO=os.path.expanduser("~") # extração do valor de $HOME
CAMINHO=os.path.join(USUARIO,"aelius_data")

# AELIUS_DATA é o valor da variável de ambiente $AELIUS_DATA ou o valor
# da variável da variável global CAMINHO
AELIUS_DATA=os.environ.get("AELIUS_DATA",CAMINHO) 


def carrega(caminho):
    """Assume-se que 'caminho' é definido relativamente à variável AELIUS_DATA.
    """
    p=os.path.join(AELIUS_DATA,caminho)
    if os.path.exists(p):
        return p
    else:
        print "Arquivo ou diretório inexistente: %s" % p

def escreve_corpus(sentencas_anotadas,nome_do_arquivo):
	"""Escreve em arquivo sentenças no formato unicode, anotadas, dadas como listas de pares (w,t), onde w é uma palavra e t, uma etiqueta.
"""
	sep1="\t" # separador entre palavra e etiqueta
	sep2="\n" # separador de pares de palavra e etiqueta
	sep3= "\n" # separador de sentenças
	arquivo=open(nome_do_arquivo,"w")
	for s in tagged_sents:
		for w,t in s:
			arquivo.write("%s%s%s%s" % (w.encode("utf-8"),sep1,t.encode("utf-8"),sep2))
		arquivo.write(sep3)
	arquivo.close()
