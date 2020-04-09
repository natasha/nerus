
<img src="https://github.com/natasha/natasha-logos/blob/master/nerus.svg">

![CI](https://github.com/natasha/nerus/workflows/CI/badge.svg) [![codecov](https://codecov.io/gh/natasha/nerus/branch/master/graph/badge.svg)](https://codecov.io/gh/natasha/nerus)

Nerus is a large silver standard Russian corpus annotated with morphology tags, syntax trees and PER, LOC, ORG NER-tags. Nerus has errors in markup, but quality is high, see <a href="#evaluation">evaluation section</a>. Corpus contains ~700K news articles from Lenta.ru. Tools from <a href="https://github.com/natasha">project Natasha</a> were used: <a href="https://github.com/natasha/razdel">Razdel</a> for sentence and token segmentation, <a href="https://github.com/natasha/slovnet">Slovnet</a> BERT models for morphology, syntax and NER annotation. Markup is stored in standart <a href="https://universaldependencies.org/format.html">CoNLL-U</a> format.

> Nerus = <a href="https://github.com/yutkin/Lenta.Ru-News-Dataset">Lenta.ru dataset</a> + <a href="https://github.com/natasha/razdel">Razdel</a> + <a href="https://github.com/natasha/slovnet">Slovnet</a> BERT morphology, syntax, NER + <a href="https://universaldependencies.org/format.html">CoNLL-U</a>.

```
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
...

```

## Download

<a href="https://storage.yandexcloud.net/natasha-nerus/data/nerus_lenta.conllu.gz">nerus_lenta.conllu.gz</a> ~2GB, ~700K texts

## Usage

Dataset is gzip-compressed <a href="https://universaldependencies.org/format.html">CoNLL-U</a> file:

```bash
$ gunzip -c nerus_lenta.conllu.gz | head

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
...

```

Nerus package provides convenient Python 3.5+ API:

```bash
$ pip install nerus

```

Load and show annotations (uses <a href="https://github.com/natasha/ipymarkup">ipymarkup</a>):

```python
>>> from nerus import load_nerus

>>> docs = load_nerus(NERUS)
>>> doc = next(docs)
>>> doc

NerusDoc(
    id='0',
    sents=[NerusSent(
         id='0_0',
         text='Вице-премьер по социальным вопросам Татьяна Голикова рассказала, в каких регионах России зафиксирована наиболее высокая смертность от рака, сообщает РИА Новости.',
         tokens=[NerusToken(
              id='1',
              text='Вице-премьер',
              pos='NOUN',
              feats={'Animacy': 'Anim',
               'Case': 'Nom',
               'Gender': 'Masc',
               'Number': 'Sing'},
              head_id='7',
              rel='nsubj',
              tag='O'
          ),
          NerusToken(
              id='2',
              text='по',
              pos='ADP',
...

>>> doc.ner.show()
Вице-премьер по социальным вопросам Татьяна Голикова рассказала, в 
                                    PER─────────────               
каких регионах России зафиксирована наиболее высокая смертность от 
               LOC───                                              
рака, сообщает РИА Новости. По словам Голиковой, чаще всего 
               ORG────────            PER──────             
онкологические заболевания становились причиной смерти в Псковской, 
                                                         LOC──────  
Тверской, Тульской и Орловской областях, а также в Севастополе. Вице-
LOC─────  LOC─────   LOC───────────────            LOC────────       
премьер напомнила, что главные факторы смертности в России — рак и 
                                                    LOC───         
болезни системы кровообращения. В начале года стало известно, что 
смертность от онкологических заболеваний среди россиян снизилась 
впервые за три года. По данным Росстата, в 2017 году от рака умерли 
                               ORG─────                             
289 тысяч человек. Это на 3,5 процента меньше, чем годом ранее.
​
>>> sent = doc.sents[0]
>>> sent.morph.show()
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
				   
>>> sent.syntax.show()
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

```

## Evaluation

Nerus is automatically annotated silver standart dataset, it has errors in markup. It is important to estimate the quality of annotation and types of errors. We apply the same pipeline to Lenta.ru articles and several golden datasets: <a href="https://github.com/natasha/corus#load_ud_syntag">SynTagRus</a>, <a href="https://github.com/natasha/corus#load_gramru">GramEval2020 Taiga News</a>, <a href="https://github.com/natasha/corus#load_ne5">Collection5</a>. Then we compare golden markup with our automatic one and estimate error rates. 

### Token segmentation

There are ~5 tokenization errors per 1000 tokens, see <a href="https://github.com/natasha/naeval#tokenization">Naeval tokenization section</a>. Error examples, first is golden partition from <a href="https://github.com/natasha/corus#load_ud_syntag">SynTagRus</a>:

```
Иногда| |на| |первое| |место| |в| |списке| |гаджетов|-|неудачников| |попадают| |устройства|,| |подобной| |участи| |совершенно| |не| |заслуживающие|.
Иногда| |на| |первое| |место| |в| |списке| |гаджетов-неудачников| |попадают| |устройства|,| |подобной| |участи| |совершенно| |не| |заслуживающие|.

Средний| |размер| |вуза| |на| |Западе| |-| |25000|-|30000| |студентов|.
Средний| |размер| |вуза| |на| |Западе| |-| |25000-30000| |студентов|.

-| |Какое| |же| |тут| |зверье| |может| |быть|?|!| |-|  |донельзя| |испугался| |толстяк| |Леонтий|.
-| |Какое| |же| |тут| |зверье| |может| |быть|?!| |-|  |донельзя| |испугался| |толстяк| |Леонтий|.

Наука| |и| |жизнь|,| |№| |10|,| |2005|.
Наука| |и| |жизнь|,| |№| |10,| |2005|.

В| |это| |же| |время| |в| |стране| |строились| |планеры| |оригинальных| |конструкций|,| |например| |БП-2| |(|ЦАГИ|-|2|)|.
В| |это| |же| |время| |в| |стране| |строились| |планеры| |оригинальных| |конструкций|,| |например| |БП-2| |(|ЦАГИ-2|)|.

Причиненный| |пожарами| |ущерб| |оценивается| |в| |50| |млн.| |австралийских| |долларов| |(|$|27| |млн.|)|.
Причиненный| |пожарами| |ущерб| |оценивается| |в| |50| |млн|.| |австралийских| |долларов| |(|$|27| |млн|.|)|.

Самый| |же| |главный| |юмор| |ситуации| |в| |том|,| |что| |поклонники| |Андропова| |явно| |прочат| |Юрия| |Владимировича| |на| |роль| |"|славного| |предшественника|"| |В.| |В.| |Путина|.
Самый| |же| |главный| |юмор| |ситуации| |в| |том|,| |что| |поклонники| |Андропова| |явно| |прочат| |Юрия| |Владимировича| |на| |роль| |"|славного| |предшественника|"| |В|.| |В|.| |Путина|.

```

### Morphology

We use <a href="https://github.com/dialogue-evaluation/morphoRuEval-2017/blob/master/morphostandard">morphoRuEval-2017 methodology</a> and <a href="https://github.com/natasha/corus#load_gramru">GramEval2020 Taiga News dataset</a> to score morphology tags. Accuracy is 94%, more relaxed morphoRuEval version is 98% (see <a href="https://github.com/natasha/naeval#morphology-taggers">Naeval morphology section</a>). Examples of errors, top is correct, "!" marks errors, "?" marks different tags that are same according to morphoRuEval:

```
         Официальные   ADJ|Animacy=Inan|Case=Nom|Degree=Pos|Number=Plur
                     ? ADJ|Case=Nom|Degree=Pos|Number=Plur
        американские   ADJ|Case=Nom|Degree=Pos|Number=Plur
              власти   NOUN|Animacy=Inan|Case=Nom|Gender=Fem|Number=Plur
        отказываются   VERB|Aspect=Imp|Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin|Voice=Mid
      комментировать   VERB|Aspect=Imp|VerbForm=Inf|Voice=Act
         подробности   NOUN|Animacy=Inan|Case=Acc|Gender=Fem|Number=Plur
           программы   NOUN|Animacy=Inan|Case=Gen|Gender=Fem|Number=Sing
                   ,   PUNCT
            ссылаясь   VERB|Aspect=Imp|Tense=Pres|VerbForm=Conv|Voice=Mid
                  на   ADP
                  ее   DET
         секретность   NOUN|Animacy=Inan|Case=Acc|Gender=Fem|Number=Sing
                   .   PUNCT

              Бейкер   PROPN|Animacy=Anim|Case=Nom|Gender=Masc|Number=Sing
           считается   VERB|Aspect=Imp|Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Mid
                     ? VERB|Aspect=Imp|Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Pass
              давним   ADJ|Case=Ins|Degree=Pos|Gender=Masc|Number=Sing
              другом   NOUN|Animacy=Anim|Case=Ins|Gender=Masc|Number=Sing
               семьи   NOUN|Animacy=Inan|Case=Gen|Gender=Fem|Number=Sing
               Бушей   PROPN|Animacy=Anim|Case=Gen|Gender=Masc|Number=Plur
                   .   PUNCT

               Обоим   NUM|Case=Dat|Gender=Masc
                  по   ADP
                  24   NUM|NumForm=Digit
                     ? NUM
                года   NOUN|Animacy=Inan|Case=Gen|Gender=Masc|Number=Sing
                   ,   PUNCT
                   в   ADP
              Греции   PROPN|Animacy=Inan|Case=Loc|Gender=Fem|Number=Sing
                 они   PRON|Case=Nom|Number=Plur|Person=3
             провели   VERB|Aspect=Perf|Mood=Ind|Number=Plur|Tense=Past|VerbForm=Fin|Voice=Act
                  по   ADP
               шесть   NUM|Case=Acc
                 лет   NOUN|Animacy=Inan|Case=Gen|Gender=Masc|Number=Plur
                   и   CCONJ
               ранее   ADV|Degree=Cmp
                     ! ADV|Degree=Pos
                   в   ADP
     правонарушениях   NOUN|Animacy=Inan|Case=Loc|Gender=Neut|Number=Plur
                  на   ADP
           греческой   ADJ|Case=Loc|Degree=Pos|Gender=Fem|Number=Sing
          территории   NOUN|Animacy=Inan|Case=Loc|Gender=Fem|Number=Sing
            замечены   VERB|Aspect=Perf|Number=Plur|Tense=Past|Variant=Short|VerbForm=Part|Voice=Pass
                  не   PART|Polarity=Neg
                были   AUX|Mood=Ind|Number=Plur|Tense=Past|VerbForm=Fin|Voice=Act
                     ? AUX|Aspect=Imp|Mood=Ind|Number=Plur|Tense=Past|VerbForm=Fin|Voice=Act
                   .   PUNCT

             Тихонов   PROPN|Animacy=Anim|Case=Nom|Gender=Masc|Number=Sing
             сообщил   VERB|Aspect=Perf|Gender=Masc|Mood=Ind|Number=Sing|Tense=Past|VerbForm=Fin|Voice=Act
                   ,   PUNCT
                 что   SCONJ
                 уже   ADV|Degree=Pos
              шестой   ADJ|Case=Nom|Degree=Pos|Gender=Masc|Number=Sing
                     ! ADJ|Animacy=Inan|Case=Acc|Degree=Pos|Gender=Masc|Number=Sing
                день   NOUN|Animacy=Inan|Case=Nom|Gender=Masc|Number=Sing
                     ! NOUN|Animacy=Inan|Case=Acc|Gender=Masc|Number=Sing
           находится   VERB|Aspect=Imp|Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Mid
                   в   ADP
             Австрии   PROPN|Animacy=Inan|Case=Loc|Gender=Fem|Number=Sing
                   ,   PUNCT
                   в   ADP
               одной   NUM|Case=Loc|Gender=Fem|Number=Sing
                  из   ADP
              лучших   ADJ|Case=Gen|Degree=Pos|Number=Plur
              клиник   NOUN|Animacy=Inan|Case=Gen|Gender=Fem|Number=Plur
                мира   NOUN|Animacy=Inan|Case=Gen|Gender=Masc|Number=Sing
                  по   ADP
       нейрохирургии   NOUN|Animacy=Inan|Case=Dat|Gender=Fem|Number=Sing
                   и   CCONJ
 сердечно-сосудистым   ADJ|Case=Dat|Degree=Pos|Number=Plur
        заболеваниям   NOUN|Animacy=Inan|Case=Dat|Gender=Neut|Number=Plur
                   .   PUNCT

```

### Syntax

We use <a href="https://github.com/natasha/corus#load_gramru">GramEval2020 Taiga News</a> as test dataset, UAS is 96%, LAS 93% (see <a href="https://github.com/natasha/naeval#syntax-parser">Naeval syntax section</a>). Error examples, left is correct:

```
    ┌──► Официальные    amod        ┌──► Официальные    amod
    │ ┌► американские   amod        │ ┌► американские   amod
    └─└─ власти         nsubj       └─└─ власти         nsubj
┌─┌─└─┌─ отказываются         | ┌───└─┌─ отказываются   
│ │ ┌─└► комментировать xcomp | │ ┌─┌─└► комментировать xcomp
│ │ └►┌─ подробности    obj     │ │ └►┌─ подробности    obj
│ │   └► программы      nmod    │ │   └► программы      nmod
│ │   ┌► ,              punct   │ │   ┌► ,              punct
│ └──►└─ ссылаясь       advcl   │ └──►└─ ссылаясь       advcl
│ │ ┌──► на             case    │ │ ┌──► на             case
│ │ │ ┌► ее             det     │ │ │ ┌► ее             det
│ └►└─└─ секретность    obl     │ └►└─└─ секретность    obl
└──────► .              punct   └──────► .              punct

            ┌► Единственный       amod                 ┌► Единственный       amod
    ┌────►┌─└─ сын                nsubj        ┌────►┌─└─ сын                nsubj
    │ ┌───└──► одного             nmod         │ ┌───└──► одного             nmod
    │ │ ┌────► из                 case         │ │ ┌────► из                 case
    │ │ │ ┌──► высокопоставленных amod         │ │ │ ┌──► высокопоставленных amod
    │ │ │ │ ┌► северокорейских    amod         │ │ │ │ ┌► северокорейских    amod
    │ └►└─└─└─ генералов          nmod         │ └►└─└─└─ генералов          nmod
┌─┌─└───┌─┌─── бежал                       ┌─┌─└───┌─┌─── бежал              
│ │     │ │ ┌► из                 case     │ │     │ │ ┌► из                 case
│ │     │ └►└─ страны             obl      │ │     │ └►└─ страны             obl
│ │     │ ┌──► вместе             advmod | │ │     └►┌─── вместе             advmod
│ │     │ │ ┌► с                  case   | │ │       │ ┌► с                  case
│ │     └►└─└─ семьей             obl    | │ │       └►└─ семьей             obl
│ │       ┌──► и                  cc       │ │       ┌──► и                  cc
│ │       │ ┌► сейчас             advmod   │ │       │ ┌► сейчас             advmod
│ └────►┌─└─└─ находится          conj     │ └────►┌─└─└─ находится          conj
│       │   ┌► в                  case     │       │   ┌► в                  case
│     ┌─└──►└─ руках              obl      │     ┌─└──►└─ руках              obl
│     │     ┌► американской       amod     │     │     ┌► американской       amod
│     └────►└─ разведки           nmod     │     └────►└─ разведки           nmod
└────────────► .                  punct    └────────────► .                  punct

    ┌► Бейкер    nsubj |     ┌► Бейкер    nsubj:pass
┌─┌─└─ считается         ┌─┌─└─ считается 
│ │ ┌► давним    amod    │ │ ┌► давним    amod
│ └►└─ другом    xcomp   │ └►└─ другом    xcomp
│ └►┌─ семьи     nmod    │ └►┌─ семьи     nmod
│   └► Бушей     nmod    │   └► Бушей     nmod
└────► .         punct   └────► .         punct

          ┌► По             case                   ┌► По             case
  ┌►┌───┌─└─ сведениям      parataxis      ┌►┌───┌─└─ сведениям      parataxis
  │ │   │ ┌► из             case           │ │   │ ┌► из             case
  │ │ ┌─└►└─ источника      nmod           │ │ ┌─└►└─ источника      nmod
  │ │ │   ┌► "              punct          │ │ │   ┌► "              punct
  │ │ └►┌─└─ Интерфакса     nmod           │ │ └►┌─└─ Интерфакса     nmod
  │ │   └──► "              punct          │ │   └──► "              punct
  │ └──────► ,              punct          │ └──────► ,              punct
  │       ┌► на             case           │       ┌► на             case
  │     ┌►└─ процессе       obl            │     ┌►└─ процессе       obl
  │     │ ┌► также          advmod         │     │ ┌► также          advmod
┌─└─────└─└─ представлены                ┌─└─────└─└─ представлены   
│     ┌─└──► адвокаты       nsubj:pass   │     ┌─└──► адвокаты       nsubj:pass
│     │   ┌► "              punct        │     │   ┌► "              punct
│   ┌─└►┌─└─ Газпрома       nmod         │   ┌─└►┌─└─ Газпрома       nmod
│   │   └──► "              punct        │   │   └──► "              punct
│   │ ┌────► —              punct        │   │ ┌────► —              punct
│   │ │   ┌► самого         amod         │   │ │   ┌► самого         amod
│   │ │ ┌►└─ вероятного     amod         │   │ │ ┌►└─ вероятного     amod
│   └►└─└─┌─ покупателя     appos        │   └►└─└─┌─ покупателя     appos
│     ┌─┌─└► компании       nmod         │     ┌─┌─└► компании       nmod
│     │ │ ┌► "              punct        │     │ │ ┌► "              punct
│     │ └►└─ Юганскнефтегаз appos        │     │ └►└─ Юганскнефтегаз appos
│     │ └──► "              punct        │     │ └──► "              punct
│     │ ┌──► ,              punct        │     │ ┌──► ,              punct
│     │ │ ┌► основного      amod         │     │ │ ┌► основного      amod
│     └►└─└─ актива         conj       | │     └►└─└─ актива         appos
│     │   ┌► "              punct        │     │   ┌► "              punct
│     └►┌─└─ ЮКОСа          nmod         │     └►┌─└─ ЮКОСа          nmod
│       └──► "              punct        │       └──► "              punct
└──────────► .              punct        └──────────► .              punct

          ┌► Между           obl       |         ┌► Между           case
    ┌────►└─ тем             parataxis |   ┌────►└─ тем             obl
    │ ┌►┌─── руководство     nsubj     |   │ ┌►┌─── руководство     nsubj
    │ │ │ ┌► "               punct     |   │ │ │ ┌► "               punct
    │ │ └►└─ ЮКОСа           nmod      |   │ │ └►└─ ЮКОСа           nmod
    │ │ └──► "               punct     |   │ │ └──► "               punct
┌─┌─└─└───┌─ опротестовало             | ┌─└─└───┌─ опротестовало   
│ │     ┌─└► решение         obj       | │     ┌─└► решение         obj
│ │     │ ┌► об              case      | │     │ ┌► об              case
│ │     └►└─ аресте          nmod      | │ ┌───└►└─ аресте          nmod
│ │   ┌─└──► акций           nmod      | │ │ ┌─└──► акций           nmod
│ │   │   ┌► "               punct     | │ │ │   ┌► "               punct
│ │   └►┌─└─ Юганскнефтегаза nmod      | │ │ └►┌─└─ Юганскнефтегаза nmod
│ │     └──► "               punct     | │ │   └──► "               punct
│ │   ┌────► в               case      | │ │ ┌────► в               case
│ │   │ ┌──► Высшем          amod      | │ │ │ ┌──► Высшем          amod
│ │   │ │ ┌► арбитражном     amod      | │ │ │ │ ┌► арбитражном     amod
│ └──►└─└─└─ суде            obl       | │ └►└─└─└─ суде            nmod
│       └──► России          nmod      | │     └──► России          nmod
└──────────► .               punct     | └────────► .               punct

            ┌► Это             det                     ┌► Это             det
        ┌──►└─ решение         nsubj     |         ┌──►└─ решение         nsubj:pass
        │   ┌► уже             advmod              │   ┌► уже             advmod
        │ ┌►└─ трижды          advmod              │ ┌►└─ трижды          advmod
┌─────┌─└─└─── рассматривалось             ┌─────┌─└─└─── рассматривалось 
│     │ │   ┌► в               case        │     │ │   ┌► в               case
│     │ └──►└─ судах           obl         │     │ └──►└─ судах           obl
│     │ ┌────► —               punct       │     │ ┌────► —               punct
│     │ │   ┌► первая          amod        │     │ │   ┌► первая          amod
│     │ │ ┌►└─ инстанция       nsubj       │     │ │ ┌►└─ инстанция       nsubj
│ ┌───└►└─└─┌─ удовлетворила   parataxis   │ ┌───└►└─└─┌─ удовлетворила   parataxis
│ │       ┌─└► жалобу          obj         │ │       ┌─└► жалобу          obj
│ │       │ ┌► "               punct       │ │       │ ┌► "               punct
│ │       └►└─ ЮКОСа           nmod        │ │       └►└─ ЮКОСа           nmod
│ │       └──► "               punct       │ │       └──► "               punct
│ │ ┌────────► ,               punct       │ │ ┌────────► ,               punct
│ │ │ ┌──────► однако          advmod      │ │ │ ┌──────► однако          advmod
│ │ │ │ ┌►┌─── вторая          nsubj       │ │ │ │ ┌►┌─── вторая          nsubj
│ │ │ │ │ │ ┌► и               cc          │ │ │ │ │ │ ┌► и               cc
│ │ │ │ │ └►└─ третья          conj        │ │ │ │ │ └►└─ третья          conj
│ └►└─└─└───┌─ признали        conj        │ └►└─└─└───┌─ признали        conj
│     │   ┌─└► арест           obj         │     │   ┌─└► арест           obj
│     │   └──► акций           nmod        │     │   └──► акций           nmod
│     └──────► законным        xcomp       │     └──────► законным        xcomp
└────────────► .               punct       └────────────► .               punct

```

### NER

We use first 100 news articles from <a href="https://github.com/natasha/corus#load_ne5">Collection5</a> for evaluation, PER F1 is 99.7%, LOC — 98.6%, ORG — 97.2%. Error examples, top is correct:

```
Выборы Верховного совета Аджарской автономной республики назначены в 
       ORG────────────── LOC────────────────────────────             
соответствии с 241-ой статьей и 4-м пунктом 10-й статьи 
Конституционного закона Грузии <О статусе Аджарской автономной 
                        LOC───            LOC──────────────────
республики>.
──────────  
>
Выборы Верховного совета Аджарской автономной республики назначены в 
       ORG────────────── LOC────────────────────────────             
соответствии с 241-ой статьей и 4-м пунктом 10-й статьи 
Конституционного закона Грузии <О статусе Аджарской автономной 
                        LOC───            LOC───────────────── 
республики>.



Следственное управление при прокуратуре требует наказать премьера 
ORG────────────────────────────────────                           
Якутии
LOC───
>
Следственное управление при прокуратуре требует наказать премьера 
ORG────────────────────                                           
Якутии
LOC───



Следственное управление Следственного комитета при прокуратуре 
ORG──────────────────── ORG─────────────────────────────────── 
Российской Федерации по Якутии обжаловало решение прокуратуры 
LOC─────────────────    LOC───                                
республики.
>
Следственное управление Следственного комитета при прокуратуре 
ORG──────────────────── ORG───────────────────                 
Российской Федерации по Якутии обжаловало решение прокуратуры 
LOC─────────────────    LOC───                                
республики.



Как сообщили в четверг корреспонденту Агентства национальных новостей 
                                      ORG──────────────────────────── 
в следственном управлении, еще 16 мая 2007 г. прокуратурой Якутии было
                                                           LOC───     
 возбуждено уголовное дело № 66144 по признакам преступления, 
предусмотренного ч. 4 ст. 159 УК РФ по факту причинения имущественного
                                 LO                                   
 ущерба в размере 30 млн руб. государственному унитарному предприятию 
<Дирекция по строительству железной дороги <Беркакит-Томмот-Якутск>.
 ORG──────────────────────────────────────────────────────────────  
>
Как сообщили в четверг корреспонденту Агентства национальных новостей 
                                      ORG──────────────────────────── 
в следственном управлении, еще 16 мая 2007 г. прокуратурой Якутии было
                                                           LOC───     
 возбуждено уголовное дело № 66144 по признакам преступления, 
предусмотренного ч. 4 ст. 159 УК РФ по факту причинения имущественного
                                 LO                                   
 ущерба в размере 30 млн руб. государственному унитарному предприятию 
<Дирекция по строительству железной дороги <Беркакит-Томмот-Якутск>.
 ORG──────────────────────                  LOC───────────────────  



Для установления процессуальным путем всех обстоятельств, касающихся 
причинения ущерба, 4 августа 2008 года Следственное управление 
                                       ORG──────────────────── 
Следственного комитета при прокуратуре Российской Федерации по Якутии 
ORG─────────────────────────────────── LOC─────────────────    LOC─── 
возбудило уголовное дело № 49234 в отношении Егора Борисова по 
                                             PER───────────    
признакам составов преступлений, предусмотренных ч. 2 ст. 286, ч. 5 
ст. 33, ч. 4 ст. 160 и ч. 2 ст. 286 УК РФ.
                                       LO 
>
Для установления процессуальным путем всех обстоятельств, касающихся 
причинения ущерба, 4 августа 2008 года Следственное управление 
                                       ORG──────────────────── 
Следственного комитета при прокуратуре Российской Федерации по Якутии 
ORG───────────────────                 LOC─────────────────    LOC─── 
возбудило уголовное дело № 49234 в отношении Егора Борисова по 
                                             PER───────────    
признакам составов преступлений, предусмотренных ч. 2 ст. 286, ч. 5 
ст. 33, ч. 4 ст. 160 и ч. 2 ст. 286 УК РФ.
                                       LO 



Начальник полигона твердых бытовых отходов <Игумново> в Нижегородской 
                                            ORG─────    LOC───────────
области осужден за загрязнение атмосферы и грунтовых вод.
───────                                                  
>
Начальник полигона твердых бытовых отходов <Игумново> в Нижегородской 
                                                        LOC───────────
области осужден за загрязнение атмосферы и грунтовых вод.
───────                                                  



Федеральная антимонопольная служба (ФАС) России признала, что группа 
ORG───────────────────────────────  ORG  LOC───                      
компаний <Мечел> нарушила статью 10 закона <О защите конкуренции> в 
          ORG──                                                     
части создания дискриминационных условий для отдельных потребителей 
продукции, а также экономически и технологически необоснованного 
отказа от заключения договора на поставку продукции и поддержания 
монопольно высокой цены на товар.
>
Федеральная антимонопольная служба (ФАС) России признала, что группа 
ORG───────────────────────────────────── LOC───                      
компаний <Мечел> нарушила статью 10 закона <О защите конкуренции> в 
          ORG──                                                     
части создания дискриминационных условий для отдельных потребителей 
продукции, а также экономически и технологически необоснованного 
отказа от заключения договора на поставку продукции и поддержания 
монопольно высокой цены на товар.



Страны Азии и Африки поддержали позицию России в конфликте с Грузией
       LOC─   LOC───                    LOC───               LOC────
>
Страны Азии и Африки поддержали позицию России в конфликте с Грузией
                                        LOC───               LOC────

```

## License

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.

## Support

- Chat — https://telegram.me/natural_language_processing
- Issues — https://github.com/natasha/nerus/issues

## Development

Tests:

```bash
make test
```

Package:

```bash
make version
git push
git push --tags

make clean wheel upload
```

Rent YC GPU:

```bash
yc compute instance create \
  --name gpu \
  --zone ru-central1-a \
  --network-interface subnet-name=default,nat-ip-version=ipv4 \
  --create-boot-disk image-folder-id=standard-images,image-family=ubuntu-1804-lts-ngc,type=network-ssd,size=20 \
  --cores=8 \
  --memory=96 \
  --gpus=1 \
  --ssh-key ~/.ssh/id_rsa.pub \
  --folder-name default \
  --platform-id gpu-standard-v1 \
  --preemptible

yc compute instance list
yc compute instance delete fhmj2ftcm32qgqt4igjf

```

Setup instance:

```
sudo locale-gen ru_RU.UTF-8

sudo apt-get update
sudo apt-get install -y python3-pip
sudo pip3 install jupyter

nohup jupyter notebook \
  --no-browser \
  --allow-root \
  --ip=localhost \
  --port=8888 \
  --NotebookApp.token='' \
  --NotebookApp.password='' &

ssh -Nf gpu -L 8888:localhost:8888
http://localhost:8888/

```

Sync remote:

```
scp ~/.nerus.json gpu:~
rsync --exclude data -rv . gpu:~/nerus
rsync -u --exclude data -rv 'gpu:~/nerus/*' .

```

Intall dev:

```bash
sudo pip3 install -r nerus/requirements/dev.txt
sudo pip3 install -e nerus

```
