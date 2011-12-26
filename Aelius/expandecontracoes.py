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
# $Id: ExpandeContracoes.py $

def clitico(forma):
	"""Testa se uma etiqueta é um clítico (CL ou SE na anotação do CHPTB) ou uma combinação de clíticos.
	"""
	return forma=="CL" or forma=="SE" or forma.startswith("CL+") or forma.startswith("SE+")

def ProcessaFormasHifenizadas(t):
	"""Toma como entrada uma sentença anotada conforme o modelo do Aelius, que separa as formas ligadas por hífen, concatenando o hífen a cada forma pronominal enclítica ou mesoclítica bem como juntando os elementos de compostos como 'terça-feira' e 'pé-de-meia'.
	"""
	i=1
	c=len(t)
	while(i<c):
		if clitico(t[i][1]) and t[i-1]==("-","+"):
			print "-%s" % t[i][0]
			t[i]=("-%s" % t[i][0],t[i][1])
		if t[i]==("-","+") and not clitico(t[i+1][1]) and not clitico(t[i-1][1]):
			#print "%s-%s" % (t[i-1][0], t[i+1][0])
			t[i]=("%s-%s" % (t[i-1][0], t[i+1][0]),t[i+1][1])
			del t[i+1]
			del t[i-1]
			i-=2
			c-=2
		i+=1
		
def expande(s):
	"""Esta função toma contração em unicode como entrada e a expande, retornando uma dupla.
"""
	if s.lower().startswith("d"):
		return ("%se" % s[0],s[1:])
	elif s.lower().startswith("n"):
		return ("em",s[1:]) # talvez seja necessário converter em maiúscula em alguns casos
	elif s.lower() == ("à".decode("utf-8")):
		return ("a","a" )
	elif s.lower() == ("às".decode("utf-8")):
		return ("a","as" )
	elif s.lower() == ("ao"):
		return ("a","o" )
	elif s.lower() == ("aos"):
		return ("a","os" )
	elif s.lower().startswith("à".decode("utf-8")):
		return ("a","a%s" % s[1:])
	elif s.lower().startswith("p"):
		return ("por","%s" % s[3:])
	elif s.lower() == ("comigo"):
		return ("com","mim" )
	elif s.lower() == ("contigo"):
		return ("com","ti" )
	elif s.lower() == ("consigo"):
		return ("com","si" )
	elif s.lower() == ("conosco"):
		return ("com","nós".decode("utf-8"))
	elif s.lower() == ("convosco"):
		return ("com","vós".decode("utf-8") )
	elif s.lower().startswith("-m") or s.lower().startswith("-t"):
		return ("%se" % s[:2],"%s" % s[2:] )
	elif s.lower().startswith("-lh"): # não leva em conta "lhes" + "o" etc.; forma expandida é sempre "lhe"
		return ("%se" % s[:3],"%s" % s[3:] )
	else:
		return s,"CL"

	
def expande_contracoes(sentenca):
	"""Toma uma sentença anotada, sob a forma de uma lista de duplas (palavra,etiqueta), conforme o sistema do Aelius (baseado no do Corpus Histórico do Português Tycho Brahe) e retorna uma versão em que os tokens cujas etiquetas contenham o símbolo '+' são expandidos pela função expande(). Por exemplo, o par ('na', 'P+D-F') desdobra-se nos dois pares ('em','P') e (u'a', u'D-F').
	
>>> from Aelius import ExpandeContracoes, AnotaCorpus
>>> sent=AnotaCorpus.EXEMPLO
>>> print sent
Os candidatos classificáveis dos cursos de Sistemas de Informação poderão ocupar as vagas remanescentes do Curso de Engenharia de Software.
>>> tokens1=AnotaCorpus.TOK_PORT.tokenize(sent)
>>> anotados=AnotaCorpus.anota_sentencas([tokens1],AnotaCorpus.TAGGER)
>>> anotados
[[('Os', 'D-P'), ('candidatos', 'N-P'), ('classific\xc3\xa1veis', 'ADJ-G-P'), ('dos', 'P+D-P'), ('cursos', 'N-P'), ('de', 'P'), ('Sistemas', 'NPR-P'), ('de', 'P'), ('Informa\xc3\xa7\xc3\xa3o', 'NPR'), ('poder\xc3\xa3o', 'VB-R'), ('ocupar', 'VB'), ('as', 'D-F-P'), ('vagas', 'ADJ-F-P'), ('remanescentes', 'ADJ-G-P'), ('do', 'P+D'), ('Curso', 'NPR'), ('de', 'P'), ('Engenharia', 'NPR'), ('de', 'P'), ('Software', 'NPR'), ('.', '.')]]
>>> ExpandeContracoes.expande_contracoes(anotados[0])
[('Os', 'D-P'), ('candidatos', 'N-P'), ('classific\xc3\xa1veis', 'ADJ-G-P'), ('de', 'P'), ('os', 'D-P'), ('cursos', 'N-P'), ('de', 'P'), ('Sistemas', 'NPR-P'), ('de', 'P'), ('Informa\xc3\xa7\xc3\xa3o', 'NPR'), ('poder\xc3\xa3o', 'VB-R'), ('ocupar', 'VB'), ('as', 'D-F-P'), ('vagas', 'ADJ-F-P'), ('remanescentes', 'ADJ-G-P'), ('de', 'P'), ('o', 'D'), ('Curso', 'NPR'), ('de', 'P'), ('Engenharia', 'NPR'), ('de', 'P'), ('Software', 'NPR'), ('.', '.')]
	"""
	lista=[]
	for w,t in sentenca:
		# é preciso assegurar que a etiqueta não seja apenas "+", atribuída, no sistema do Aelius, ao hífen
		if len(t) > 2 and "+" in t:
			t1,t2=t.split("+")
			w1,w2=expande(w)
			lista.extend([(w1,t1),(w2,t2)])
		else:
			if not w=="-": # exclusão de hífen como token
				lista.append((w,t))
	return lista
