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
# $Id: AnotaCorpus.py $

"""Anota sentenças enquanto listas de tokens unicode ou arquivos de texto em utf-8, utilizando os toquenizadores e etiquetadores morfossintáticos especificados. Para anotar um texto de um arquivo, consultar documentação da função AnotaCorpus.anota_texto. Exemplo de toquenização e etiquetagem de uma sentença:

>>> from Aelius.Extras import carrega
>>> from Aelius import Toqueniza, AnotaCorpus
>>> h=carrega('AeliusHunPos')
>>> b=carrega('AeliusBRUBT.pkl')
>>> lx=carrega('lxtagger')
>>> tokens1=Toqueniza.TOK_PORT.tokenize(AnotaCorpus.EXEMPLO)
>>> tokens2=Toqueniza.TOK_PORT_LX.tokenize(AnotaCorpus.EXEMPLO)
>>> AnotaCorpus.anota_sentencas([tokens1],b)
[[('Os', 'D-P'), ('candidatos', 'N-P'), ('classific\xc3\xa1veis', 'ADJ-G-P'), ('dos', 'P+D-P'), ('cursos', 'N-P'), ('de', 'P'), ('Sistemas', 'NPR-P'), ('de', 'P'), ('Informa\xc3\xa7\xc3\xa3o', 'NPR'), ('poder\xc3\xa3o', 'VB-R'), ('ocupar', 'VB'), ('as', 'D-F-P'), ('vagas', 'ADJ-F-P'), ('remanescentes', 'ADJ-G-P'), ('do', 'P+D'), ('Curso', 'NPR'), ('de', 'P'), ('Engenharia', 'NPR'), ('de', 'P'), ('Software', 'NPR'), ('.', '.')]]
>>> AnotaCorpus.anota_sentencas([tokens1],h,'hunpos')
[[('Os', 'D-P'), ('candidatos', 'N-P'), ('classific\xc3\xa1veis', 'ADJ-G-P'), ('dos', 'P+D-P'), ('cursos', 'N-P'), ('de', 'P'), ('Sistemas', 'NPR'), ('de', 'P'), ('Informa\xc3\xa7\xc3\xa3o', 'NPR'), ('poder\xc3\xa3o', 'VB-R'), ('ocupar', 'VB'), ('as', 'D-F-P'), ('vagas', 'ADJ-F-P'), ('remanescentes', 'N-P'), ('do', 'P+D'), ('Curso', 'NPR'), ('de', 'P'), ('Engenharia', 'NPR'), ('de', 'P'), ('Software', 'NPR'), ('.', '.')]]
>>> AnotaCorpus.anota_sentencas([tokens2],lx,'mxpost')
[[('Os', 'DA'), ('candidatos', 'CN'), ('classific\xc3\xa1veis', 'ADJ'), ('de', 'PREP'), ('os', 'DA'), ('cursos', 'CN'), ('de', 'PREP'), ('Sistemas', 'PNM'), ('de', 'PREP'), ('Informa\xc3\xa7\xc3\xa3o', 'PNM'), ('poder\xc3\xa3o', 'V'), ('ocupar', 'INF'), ('as', 'DA'), ('vagas', 'CN'), ('remanescentes', 'ADJ'), ('de', 'PREP'), ('o', 'DA'), ('Curso', 'PNM'), ('de', 'PREP'), ('Engenharia', 'PNM'), ('de', 'PREP'), ('Software', 'PNM'), ('.', 'PNT')]]

"""
import os,sys,nltk
from cPickle import load
from Aelius.Extras import carrega
from ProcessaNomesProprios import *
from ExpandeContracoes import expande_contracoes
from Toqueniza import PUNKT,TOK_PORT
from MXPOST import MXPOSTTagger

EXEMPLO="Os candidatos classificáveis dos cursos de Sistemas de Informação poderão ocupar as vagas remanescentes do Curso de Engenharia de Software.".decode("utf-8")
# Extraído da seguinte fonte:

# UFC convoca os classificáveis do Vestibular 2010. Disponível em: 
# <http://noticias.universia.com.br/destaque/noticia/2010/02/17/411825/
# fc-convoca-os-classificaveis-do-vestibular-2010.html> 
# Acesso em: 17/05/2011.

# A seguinte variável permite expandir contrações para obter maior
# acurácia com o LXTagger:
EXPANDE_CONTRACOES=True

TAGGER=carrega("AeliusBRUBT.pkl")
    
# A seguinte variável global permite definir um
# infixo para arquivos anotados; caso essa variável
# permaneça com cadeia vazia como valor, o infixo é dado
# pela arquitetura do etiquetador:
INFIXO=""

USUARIO= os.path.expanduser("~")

HUNPOS=carrega("AeliusHunPos")

DESTINO="."


# O AeliusRUBT, usado como parte do procedimento
# de expansão de contrações, é mais rápido que o AeliusBRUBT,
# embora menos preciso:
TAGGER2=carrega("AeliusRUBT.pkl")

def toqueniza_contracoes(sentencas):
    """Esta função primeiro anota as sentenças com o TAGGER2, para depois utilizar seu output para separar as contrações.
    
>>> tokens1=AnotaCorpus.TOK_PORT.tokenize(AnotaCorpus.EXEMPLO)
>>> tokens1
[u'Os', u'candidatos', u'classific\xe1veis', u'dos', u'cursos', u'de', u'Sistemas', u'de', u'Informa\xe7\xe3o', u'poder\xe3o', u'ocupar', u'as', u'vagas', u'remanescentes', u'do', u'Curso', u'de', u'Engenharia', u'de', u'Software', u'.']
>>> AnotaCorpus.toqueniza_contracoes([tokens1])
[[u'Os', u'candidatos', u'classific\xe1veis', u'de', u'os', u'cursos', u'de', u'Sistemas', u'de', u'Informa\xe7\xe3o', u'poder\xe3o', u'ocupar', u'as', u'vagas', u'remanescentes', u'de', u'o', u'Curso', u'de', u'Engenharia', u'de', u'Software', u'.']]
>>> 
    """
    sents=anota_sentencas(sentencas,TAGGER2)
    sents=decodifica_sentencas_anotadas(sents)
    sents=[expande_contracoes(sent) for sent in sents]
    return [nltk.tag.untag(sent) for sent in sents]
    
# as duas funções seguintes representam uma modularização do programa
# e devem substituir partes de funções deste módulo e do módulo Avalia
def codifica_sentencas(sentencas):
    """Toma unicode como input e retorna string.
    """
    lista_sentencas=[]
    for sent in sentencas:
	cols=[]
	for w in sent:
		cols.append(w.encode("utf-8"))
	lista_sentencas.append(cols)
    return lista_sentencas

def decodifica_sentencas(sentencas):
    """Toma string como input e retorna unicode.
    """
    lista_sentencas=[]
    for sent in sentencas:
	cols=[]
	for w in sent:
		cols.append(w.decode("utf-8"))
	lista_sentencas.append(cols)
    return lista_sentencas

def codifica_sentencas_anotadas(sentencas_anotadas):
    lista_codificada=[]
    for sent in sentencas_anotadas:
        cols=[]
	for w,t in sent:
            #print w,t # teste
            cols.append((w.encode("utf-8"),t.encode("utf-8")))
        lista_codificada.append(cols)
    return lista_codificada

def decodifica_sentencas_anotadas(sentencas_anotadas):
    lista_codificada=[]
    for sent in sentencas_anotadas:
        cols=[]
	for w,t in sent:
		cols.append((w.decode("utf-8"),t.decode("utf-8")))
        lista_codificada.append(cols)
    return lista_codificada

def extrai_corpus(arquivos,raiz=".",
                   toquenizador_sentencial= PUNKT,
                   #toquenizador_sentencial= REGEXP,
                   toquenizador_vocabular=TOK_PORT,
                   codificacao="utf-8"):

    """Retorna um corpus no formato do NLTK a partir de um arquivo de texto puro sem anotações. O texto é segmentado em palavras com base na expressão regular dada como argumento de nltk.RegexpTokenizer(), que retorna toquenizador armazenado na variável global em TOK_PORT. A segmentação em sentenças ocorre a cada quebra de linha. Em textos extraídos da WWW geralmente não há coincidência entre quebra de linha e final de sentença, o que torna necessária a definição de um outro toquenizador, o que é feito na função main, onde se utiliza o nltk.data.load('tokenizers/punkt/portuguese.pickle'). Assume-se que a codificação do texto-fonte é utf-8."""

    return nltk.corpus.PlaintextCorpusReader(raiz,
                                             arquivos,
                                             sent_tokenizer=toquenizador_sentencial,
                                             word_tokenizer=toquenizador_vocabular,
                                             encoding=codificacao)

def abre_etiquetador(modelo,arquitetura="nltk"):
    """Retorna etiquetador a partir do modelo e arquitetura especificados. O parâmetro 'arquitetura' tem como default 'nltk' e pode assumir também um dos seguintes valores: 'hunpos', 'stanford' ou 'mxpost'. Nesse último caso, é construída e retornada instância de etiquetador de um desses tipos, invocando o construtor das classes HunposTagger, StanfordTagger e MXPOSTTagger, respectivamente. A codificação dos modelos deve ser utf-8. Caso a arquitetura seja nltk, assume-se que se trata de instância de etiquetador do NLTK armazenada em formato binário (extensão do arquivo '.pkl' ou '.pickle', por exemplo), sendo retornada instância de etiquetador do NLTK armazenada em formato binário."""
    if arquitetura == "nltk":
        f=open(modelo,"rb")
        etiquetador=load(f)
        f.close()
        return etiquetador
    if arquitetura =="hunpos":
        return nltk.tag.HunposTagger(modelo,encoding="utf-8")
    if arquitetura =="stanford":
        return nltk.tag.StanfordTagger(modelo,encoding="utf-8")
    if arquitetura =="mxpost":
        return MXPOSTTagger(modelo,encoding="utf-8")
    

def anota_sentencas(sents,modelo,arquitetura="nltk"):
    '''A partir de uma lista de sentenças (cada sentença consituindo, por sua vez, uma lista de palavras), retorna uma lista de sentenças anotadas pelo etiquetador especificado nos parâmetros modelo e arquitetura (ver documentação da função abre_etiquetador). Cada sentença anotada é uma lista de duplas (w,t), onde w é uma palavra e t, uma etiqueta.'''

# As cadeias da lista de entrada são primeiro
# codificadas em utf-8, antes de serem etiquetadas. Isso se mostrou necessário
# para que o anotador baseado em expressões regulares pudesse reconhecer
# afixos com caracteres com código fora do intervalo definido por range(128), 
# não suportados pelo codec 'ascii'. 

# Simplicar, no futuro, esta função, pois, no caso da etiquetagem
# pelas arquiteruras HunPos, StanfordTagger e MXPOST, as sentenças 
# precisam ser decodificadas e, depois, recodificadas. No caso
# dessas arquiteturas, não haveria nem codificação nem decodificação;
# a função tomaria unicode como entrada e retornaria unicode. Para
# tanto, o módulo ProcessaNomesProprios também operaria em unicode.
# A versão  ProcessaNomesProprios02.py já opera com unicode.

    sents=codifica_sentencas(sents)
    
 #minusculiza palavras exceto as que ocorrem com maiúscula em posição não inicial    
    sents=minusculiza_nao_nomes_proprios(sents)
    etiquetador=abre_etiquetador(modelo,arquitetura)
    if arquitetura in ["hunpos","stanford","mxpost"]:
        sents=decodifica_sentencas(sents)
    if EXPANDE_CONTRACOES and arquitetura == "mxpost": # para funcionar com o LX-Tagger
        sents=toqueniza_contracoes(sents)
    etiquetadas=etiquetador.batch_tag(sents)
    #print etiquetadas[0][0]
    #print type(etiquetadas[0][0][0])
    if isinstance(etiquetadas[0][0][0],unicode):
        etiquetadas=codifica_sentencas_anotadas(etiquetadas)
    maiusculiza_inicio(etiquetadas)
    return etiquetadas
    
def anota_paragrafos(paras,modelo,arquitetura):
    paragrafos=[]
    for paragrafo in paras:
        paragrafos.append(anota_sentencas(
            paragrafo,modelo,arquitetura))
    return paragrafos

# esta função foi substituída por várias funções de
# escrita de corpus em arquivo (ver infra)
def escreve_corpus(lista_de_sentencas,nome):
    """A partir de lista de sentenças anotadas, onde cada sentença é uma lista de pares ordenados do tipo de ('palavra','N'), escreve corpus em arquivo de texto 'nome' em que os tokens são etiquetados da forma canônica palavra/N."""
    #f=open(os.path.join(USUARIO,nome),"w")
    f=open(nome,"w") # salva por defeito no diretório de trabalho
    c=1 # inicialização de um contador de palavras
    for sentenca in lista_de_sentencas:
        for palavra in sentenca:
            f.write("%s/%s<%d> " % (palavra[0],
                        palavra[1], c ) )
            c+=1
        f.write("\n")
        f.write("\n====================\n") # recurso para fase de teste
    f.close()

def maiusculiza_inicio(lista_de_sentencas):
    '''Maiusculiza as palavras minúsculas no início de sentença.
'''
    for indice in range(len(lista_de_sentencas)):
        palavras,etiquetas= separa_palavras_de_etiquetas(lista_de_sentencas[indice])
        palavras=maiusculiza_inicio_de_sentenca(palavras)
        lista_de_sentencas[indice]=zip(palavras,etiquetas)

def formata_paragrafos(paras):
    '''Maiusculiza o início de cada sentença do parágrafo.
'''
    paragrafos=[]
    for p in paras:
        maiusculiza_inicio(p)
    

def escreve_formato_nltk(paras,nome,desenvolvimento=False):
    separa_linhas="\n"
    separa_paragrafos="\n\n"
    c=1 # inicialização de um contador de palavras
    contador=""

    # recurso para fase de teste
    if desenvolvimento:
        separa_linhas="\n---------------\n"
        separa_paragrafos="\n====================\n"
        
    f=open(os.path.join(DESTINO,nome),"w")
    
    for p in paras:
        for sentenca in p:
            for palavra in sentenca:
                f.write("%s/%s%s " % (palavra[0],palavra[1], contador ) )
                if desenvolvimento:
                    contador="<%s>" % str(c)
                    c+=1
            f.write(separa_linhas)
        f.write(separa_paragrafos)
    f.close()

def escreve_formato_xml(paras,nome,capitulo="1"):
    # inicialização de contadores para palavras, sentenças e parágrafos
    c,s,p=1,1,1
    f=open(os.path.join(DESTINO,nome),"w")
    f.write('<div type="chap" n="%s">' % capitulo)
    for para in paras:
        f.write('<p n="%d">' % p)
        for sentenca in para:
            f.write('<s n="%d">' %s)
            for palavra in sentenca:
                f.write('<w xml:id="w%d" type="%s">%s</w> ' % (c, palavra[1],palavra[0] ) )
                c+=1
            f.write('</s>')
            s+=1
        f.write('</p>')
        p+=1
    f.write('</div>')
    f.close()

def main(modelo="AeliusBRUBT.pkl",
         arquitetura="nltk",
         toquenizador=TOK_PORT,
         textos_fonte=r"corpus\.txt",
         diretorio=".",
         caminho_de_destino=".",
         arquivo_de_destino="corpus.pos.txt"):
    
    '''Compila e anota um corpus.'''
    
    caminho=os.path.join(USUARIO,diretorio)
    corpus_nao_anotado=extrai_corpus(textos_fonte,
                                      caminho,
                                      toquenizador_sentencial=PUNKT,
                                     toquenizador_vocabular=toquenizador
                                      )

    sentencas_nao_anotadas=list(corpus_nao_anotado.sents())

    sentencas_anotadas=anota_sentencas(sentencas_nao_anotadas,modelo,arquitetura)
    
    escreve_corpus(sentencas_anotadas,os.path.join(caminho_de_destino,arquivo_de_destino))

def anota_texto(arquivo,
                modelo=TAGGER,
                arquitetura="nltk",
                toquenizador=TOK_PORT,
                raiz=".",
                codificacao="utf-8",
                formato=None):
    """Anota arquivo e salva o resultado, no atual diretório de trabalho,
em arquivo com extensão .INFIXO.txt (onde INFIXO é o valor dessa variável
global, se definida como cadeia não vazia, ou, caso contrário, o valor do
parâmetro arquitetura). É possível especificar um dos três formatos da
anotação: nltk (default), aelius e xml.
Exemplo de anotação de um texto com o etiquetador default AeliusBRUBT.pkl:

>>> import os
>>> os.getcwd()
'/Users/leonel'
>>> os.chdir("analises")
>>> os.getcwd()
'/Users/leonel/analises'
>>> from Aelius import AnotaCorpus
>>> from Aelius.Extras import carrega
>>> raiz,nome=os.path.split(carrega("exemplo.txt"))
>>> AnotaCorpus.anota_texto(nome,raiz=raiz)
Arquivo anotado:
/Users/leonel/analises/exemplo.nltk.txt
>>> AnotaCorpus.anota_texto(nome,raiz=raiz,formato="xml")
Arquivo anotado:
/Users/leonel/analises/exemplo.nltk.xml
>>> 

    """

    nome_output=""
    corpus=extrai_corpus(arquivo,
                         raiz=raiz,
                         toquenizador_vocabular=toquenizador,
                   codificacao=codificacao)
    paragrafos=corpus.paras()
    anotados=anota_paragrafos(paragrafos,modelo,arquitetura)
    if INFIXO:
        infixo=INFIXO
    else:
        infixo=arquitetura
    #formata_paragrafos(anotados) # linha a ser eliminada? 30.03.2011
    lista=arquivo.split(".txt")
    base_nome_input=lista[0]
    if formato:
        if formato == "aelius":
            nome_output="%s.pos.%s.txt" % (base_nome_input,formato)
            nome_output=escreve_formato_nltk(anotados,nome_output,desenvolvimento=True)
        elif formato == "xml":
            nome_output="%s.%s.%s" % (base_nome_input,infixo,formato)
            escreve_formato_xml(anotados,nome_output)
        else:
            nome_output="%s.%s.txt" % (base_nome_input,infixo)
            escreve_formato_nltk(anotados,nome_output)
    else:
        nome_output="%s.%s.txt" % (base_nome_input,infixo)
        escreve_formato_nltk(anotados,nome_output)
    print "Arquivo anotado:\n%s" % os.path.join(os.getcwd(),nome_output)


# a função main pode ser executada a partir da shell do sistema 
# operacional
if __name__ == '__main__':
    if len(sys.argv) == 1: # sem argumentos executa-se main com os valores default
        main()
    else: # os parâmetros da função podem ser especificados na linha de comando
        main(arquivo_do_etiquetador=sys.argv[1],
         textos_fonte=r"%s" % sys.argv[2],
         diretorio=sys.argv[3],
         caminho_de_destino=sys.argv[4],
         arquivo_de_destino=sys.argv[5])

def teste(s):
    lista = TOK_PORT.tokenize(s)
    for e in lista:
	print e
    return lista
