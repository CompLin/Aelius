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
# $Id: SimplificaEtiquetas.py $

"""Este módulo contém funções para simplificar as etiquetas de um corpus anotado ou transformar um conjunto de etiquetas em outro."""

from Aelius import carrega

ARQUIVO=carrega("tag_mapping.txt")

def constroiDicionarioDeArquivo(arquivo=ARQUIVO):
	"""Esta função transforma arquivo cujas linhas são pares do tipo

	etiqueta1 etiqueta

em um dicionário em que o valor de dic[etiqueta1] é etiqueta2.
	"""
	dic={}
	f=open(arquivo,"rU")
	for linha in f:
		chave,valor=linha.strip().split()
		dic[chave]=valor
	return dic

def LXTagger2CHPTB(etiqueta):
	"""Esta função converte uma etiqueta do LXTagger em uma etiqueta do CHPTB ou no estilo deste corpus, conforme um dicionário que mapeia um conjunto de etiquetas em outro. Caso uma etiqueta não esteja incluída como chave no dicionário, a função retorna simplesmente retorna a etiqueta dada como entrada.
	"""
	dicionario=constroiDicionarioDeArquivo()
	t=dicionario.get(etiqueta,0)
	if t:
		return t
	else:
		return etiqueta
