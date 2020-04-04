
from nerus import parse_nerus


DATA = '''
# newdoc id = 0
# sent_id = 0_0
# text = Вице-премьер по социальным вопросам Татьяна Голикова рассказала, в каких регионах России зафиксирована наиболее высокая смертность от рака, сообщает РИА Новости.
1	Вице-премьер	_	NOUN	_	Animacy=Anim|Case=Nom|Gender=Masc|Number=Sing	7	nsubj	_	Tag=O
2	по	_	ADP	_	_	4	case	_	Tag=O
3	социальным	_	ADJ	_	Case=Dat|Degree=Pos|Number=Plur	4	amod	_	Tag=O
4	вопросам	_	NOUN	_	Animacy=Inan|Case=Dat|Gender=Masc|Number=Plur	1	nmod	_	Tag=O
5	Татьяна	_	PROPN	_	Animacy=Anim|Case=Nom|Gender=Fem|Number=Sing	1	appos	_	Tag=B-PER
6	Голикова	_	PROPN	_	Animacy=Anim|Case=Nom|Gender=Fem|Number=Sing	5	flat:name	_	Tag=I-PER
7	рассказала	_	VERB	_	Aspect=Perf|Gender=Fem|Mood=Ind|Number=Sing|Tense=Past|VerbForm=Fin|Voice=Act	0	root	_	Tag=O
8	,	_	PUNCT	_	_	13	punct	_	Tag=O
9	в	_	ADP	_	_	11	case	_	Tag=O
10	каких	_	DET	_	Case=Loc|Number=Plur	11	det	_	Tag=O
11	регионах	_	NOUN	_	Animacy=Inan|Case=Loc|Gender=Masc|Number=Plur	13	obl	_	Tag=O
12	России	_	PROPN	_	Animacy=Inan|Case=Gen|Gender=Fem|Number=Sing	11	nmod	_	Tag=B-LOC
13	зафиксирована	_	VERB	_	Aspect=Perf|Gender=Fem|Number=Sing|Tense=Past|Variant=Short|VerbForm=Part|Voice=Pass	7	ccomp	_	Tag=O
14	наиболее	_	ADV	_	Degree=Pos	15	advmod	_	Tag=O
15	высокая	_	ADJ	_	Case=Nom|Degree=Pos|Gender=Fem|Number=Sing	16	amod	_	Tag=O
16	смертность	_	NOUN	_	Animacy=Inan|Case=Nom|Gender=Fem|Number=Sing	13	nsubj:pass	_	Tag=O
17	от	_	ADP	_	_	18	case	_	Tag=O
18	рака	_	NOUN	_	Animacy=Inan|Case=Gen|Gender=Masc|Number=Sing	16	nmod	_	Tag=O
19	,	_	PUNCT	_	_	20	punct	_	Tag=O
20	сообщает	_	VERB	_	Aspect=Imp|Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act	0	root	_	Tag=O
21	РИА	_	PROPN	_	Animacy=Inan|Case=Nom|Gender=Neut|Number=Sing	20	nsubj	_	Tag=B-ORG
22	Новости	_	PROPN	_	Animacy=Inan|Case=Nom|Gender=Fem|Number=Plur	21	appos	_	Tag=I-ORG
23	.	_	PUNCT	_	_	20	punct	_	Tag=O

# sent_id = 0_1
# text = По словам Голиковой, чаще всего онкологические заболевания становились причиной смерти в Псковской, Тверской, Тульской и Орловской областях, а также в Севастополе.
1	По	_	ADP	_	_	2	case	_	Tag=O
2	словам	_	NOUN	_	Animacy=Inan|Case=Dat|Gender=Neut|Number=Plur	9	parataxis	_	Tag=O
3	Голиковой	_	PROPN	_	Animacy=Anim|Case=Gen|Gender=Fem|Number=Sing	2	nmod	_	Tag=B-PER
4	,	_	PUNCT	_	_	2	punct	_	Tag=O
5	чаще	_	ADV	_	Degree=Cmp	9	advmod	_	Tag=O
6	всего	_	PRON	_	Animacy=Inan|Case=Gen|Gender=Neut|Number=Sing	5	obl	_	Tag=O
7	онкологические	_	ADJ	_	Case=Nom|Degree=Pos|Number=Plur	8	amod	_	Tag=O
8	заболевания	_	NOUN	_	Animacy=Inan|Case=Nom|Gender=Neut|Number=Plur	9	nsubj	_	Tag=O
9	становились	_	VERB	_	Aspect=Imp|Mood=Ind|Number=Plur|Tense=Past|VerbForm=Fin|Voice=Mid	0	root	_	Tag=O
10	причиной	_	NOUN	_	Animacy=Inan|Case=Ins|Gender=Fem|Number=Sing	9	xcomp	_	Tag=O
11	смерти	_	NOUN	_	Animacy=Inan|Case=Gen|Gender=Fem|Number=Sing	10	nmod	_	Tag=O
12	в	_	ADP	_	_	20	case	_	Tag=O
13	Псковской	_	ADJ	_	Case=Loc|Degree=Pos|Gender=Fem|Number=Sing	20	amod	_	Tag=B-LOC
14	,	_	PUNCT	_	_	15	punct	_	Tag=O
15	Тверской	_	ADJ	_	Case=Loc|Degree=Pos|Gender=Fem|Number=Sing	13	conj	_	Tag=B-LOC
16	,	_	PUNCT	_	_	17	punct	_	Tag=O
17	Тульской	_	ADJ	_	Case=Loc|Degree=Pos|Gender=Fem|Number=Sing	13	conj	_	Tag=B-LOC
18	и	_	CCONJ	_	_	19	cc	_	Tag=O
19	Орловской	_	ADJ	_	Case=Loc|Degree=Pos|Gender=Fem|Number=Sing	13	conj	_	Tag=B-LOC
20	областях	_	NOUN	_	Animacy=Inan|Case=Loc|Gender=Fem|Number=Plur	9	obl	_	Tag=I-LOC
21	,	_	PUNCT	_	_	25	punct	_	Tag=O
22	а	_	CCONJ	_	_	25	cc	_	Tag=O
23	также	_	ADV	_	Degree=Pos	22	fixed	_	Tag=O
24	в	_	ADP	_	_	25	case	_	Tag=O
25	Севастополе	_	PROPN	_	Animacy=Inan|Case=Loc|Gender=Masc|Number=Sing	20	conj	_	Tag=B-LOC
26	.	_	PUNCT	_	_	9	punct	_	Tag=O
'''.strip().splitlines()

REPR = '''NerusDoc(id='0', sents=[NerusSent(id='0_0', text='Вице-премьер по социальным вопросам Татьяна Голикова рассказала, в каких регионах России зафиксирована наиболее высокая смертность от рака, сообщает РИА Новости.', tokens=[NerusToken(id='1', text='Вице-премьер', pos='NOUN', feats='''


NER = '''
Вице-премьер по социальным вопросам Татьяна Голикова рассказала, в 
                                    PER─────────────               
каких регионах России зафиксирована наиболее высокая смертность от 
               LOC───                                              
рака, сообщает РИА Новости. По словам Голиковой, чаще всего 
               ORG────────            PER──────             
онкологические заболевания становились причиной смерти в Псковской, 
                                                         LOC──────  
Тверской, Тульской и Орловской областях, а также в Севастополе.
LOC─────  LOC─────   LOC───────────────            LOC──────── 
'''[1:]

MORPH = '''
        Вице-премьер  NOUN|Animacy=Anim|Case=Nom|Gender=Masc|Number=Sing
                  по  ADP
          социальным  ADJ|Case=Dat|Degree=Pos|Number=Plur
            вопросам  NOUN|Animacy=Inan|Case=Dat|Gender=Masc|Number=Plur
             Татьяна  PROPN|Animacy=Anim|Case=Nom|Gender=Fem|Number=Sing
            Голикова  PROPN|Animacy=Anim|Case=Nom|Gender=Fem|Number=Sing
          рассказала  VERB|Aspect=Perf|Gender=Fem|Mood=Ind|Number=Sing|Tense=Past|VerbForm=Fin|Voice=Act
                   ,  PUNCT
                   в  ADP
               каких  DET|Case=Loc|Number=Plur
            регионах  NOUN|Animacy=Inan|Case=Loc|Gender=Masc|Number=Plur
              России  PROPN|Animacy=Inan|Case=Gen|Gender=Fem|Number=Sing
       зафиксирована  VERB|Aspect=Perf|Gender=Fem|Number=Sing|Tense=Past|Variant=Short|VerbForm=Part|Voice=Pass
            наиболее  ADV|Degree=Pos
             высокая  ADJ|Case=Nom|Degree=Pos|Gender=Fem|Number=Sing
          смертность  NOUN|Animacy=Inan|Case=Nom|Gender=Fem|Number=Sing
                  от  ADP
                рака  NOUN|Animacy=Inan|Case=Gen|Gender=Masc|Number=Sing
                   ,  PUNCT
            сообщает  VERB|Aspect=Imp|Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act
                 РИА  PROPN|Animacy=Inan|Case=Nom|Gender=Neut|Number=Sing
             Новости  PROPN|Animacy=Inan|Case=Nom|Gender=Fem|Number=Plur
                   .  PUNCT
'''[1:]

SYNTAX = '''
  ┌►┌─┌───── Вице-премьер  nsubj
  │ │ │ ┌──► по            case
  │ │ │ │ ┌► социальным    amod
  │ │ └►└─└─ вопросам      nmod
  │ └────►┌─ Татьяна       appos
  │       └► Голикова      flat:name
┌─└───────── рассказала    
│   ┌──────► ,             punct
│   │   ┌──► в             case
│   │   │ ┌► каких         det
│   │ ┌►└─└─ регионах      obl
│   │ │ └──► России        nmod
└──►└─└───── зафиксирована ccomp
    │     ┌► наиболее      advmod
    │   ┌►└─ высокая       amod
    └►┌─└─── смертность    nsubj:pass
      │   ┌► от            case
      └──►└─ рака          nmod
          ┌► ,             punct
      ┌─┌─└─ сообщает      
      │ └►┌─ РИА           nsubj
      │   └► Новости       appos
      └────► .             punct
'''[1:]


def test(capsys):
    doc = next(parse_nerus(DATA))

    assert repr(doc).startswith(REPR)

    doc.ner.show()
    assert capsys.readouterr().out == NER

    sent = doc.sents[0]
    sent.morph.show()
    assert capsys.readouterr().out == MORPH

    sent.syntax.show()
    assert capsys.readouterr().out == SYNTAX
