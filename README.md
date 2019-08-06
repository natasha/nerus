
<img src="i/logo.svg" height="75">

[![Build Status](https://travis-ci.org/natasha/nerus.svg?branch=master)](https://travis-ci.org/natasha/nerus)

Nerus is a large silver standard Russian NER corpus. Unlike small manually annotated gold standart <a href="https://github.com/dialogue-evaluation/factRuEval-2016/">factRuEval-2016</a>, <a href="http://www.labinform.ru/pub/named_entities/">Collection5</a> and <a href="https://www.researchgate.net/publication/262203599_Introducing_Baselines_for_Russian_Named_Entity_Recognition">Gareev</a> Nerus has errors in annotation. But overall quality is rather high, f1-scores for `PER`, `LOC`, `ORG` are ~0.95+, ~0.9+, ~0.8-0.9 respectively, see <a href="#evaluation">evaluation section</a> for more.

> Nerus = <a href="https://github.com/yutkin/Lenta.Ru-News-Dataset">Lenta.ru dataset</a> + <a href="https://github.com/deepmipt/DeepPavlov">DeepPavlov</a> BERT NER.

```
Европейский союз добавил в санкционный список девять политических 
LOC-------------                                                  
деятелей из самопровозглашенных республик Донбасса — Донецкой народной
                                          LOC-----   LOC--------------
 республики (ДНР) и Луганской народной республики (ЛНР) — в связи с 
-----------------   LOC--------------------------------             
прошедшими там выборами. Об этом говорится в документе, опубликованном
 в официальном журнале Евросоюза. В новом списке фигурирует Леонид 
                       LOC------                            PER----
Пасечник, который по итогам выборов стал главой ЛНР. Помимо него там 
--------                                        LOC                  
присутствуют Владимир Бидевка и Денис Мирошниченко, председатели 
             PER-------------   PER---------------               
законодательных органов ДНР и ЛНР, а также Ольга Позднякова и Елена 
                        LOC   LOC          PER-------------   PER---
Кравченко, председатели ЦИК обеих республик. Выборы прошли в 
---------               ORG                                  
непризнанных республиках Донбасса 11 ноября. На них удержали лидерство
                         LOC-----                                     
 действующие руководители и партии — Денис Пушилин и «Донецкая 
                                     PER----------    ORG------
республика» в ДНР и Леонид Пасечник с движением «Мир Луганщине» в ЛНР.
----------    LOC   PER------------              ORG----------    LOC 
 Президент Франции Эмманюэль Макрон и канцлер ФРГ Ангела Меркель после
           LOC---- PER-------------           LOC PER-----------      
 встречи с украинским лидером Петром Порошенко осудили проведение 
                              PER-------------                    
выборов, заявив, что они нелегитимны и «подрывают территориальную 
целостность и суверенитет Украины». Позже к осуждению присоединились 
                          LOC----                                    
США с обещаниями новых санкций для России.
LOC                                LOC--- 
...
```
See <a href="examples/lenta_500.txt">examples/lenta_500.txt</a> for ~1Mb of examples.


## Download

<dl>
  <dt>Link</dt>
  <dd>https://github.com/natasha/nerus/releases/download/v1.0/lenta.jsonl.gz</dd>

  <dt>Size</dt>
  <dd>612Mb</dd>

  <dt>Texts</dt>
  <dd>739 295</dd>
</dl>

## Usage

`lenta.jsonl.gz` is gzip-compressed text file with <a href="http://jsonlines.org/">JSON lines</a>. There are three types of entities: `PER`, `LOC` and `ORG`.

```bash
$ gzcat lenta.jsonl.gz | head -1 | jq .
{
  "article_id": 0,
  "content": "Вице-премьер по социальным вопросам Татьяна Голикова рассказала, в каких регионах России зафиксирована наиболее высокая смертность от рака, сообщает РИА Новости. По словам Голиковой, чаще всего онкологические заболевания становились причиной смерти в Псковской, Тверской, Тульской и Орловской областях, а также в Севастополе. Вице-премьер напомни
ла, что главные факторы смертности в России — рак и болезни системы кровообращения. В начале года стало известно, что смертность от онкологических заболеваний среди россиян снизилась впервые за три года. По данным Росстата, в 2017 году от рака умерли 289 тысяч человек. Это на 3,5 процента меньше, чем годом ранее.",
  "annotations": [
    {
      "span": {
        "start": 36,
        "end": 52
      },
      "type": "PER",
      "text": "Татьяна Голикова"
    },
    {
      "span": {
        "start": 82,
        "end": 88
      },
      "type": "LOC",
      "text": "России"
    },
	...
    {
      "span": {
        "start": 560,
        "end": 568
      },
      "type": "ORG",
      "text": "Росстата"
    }
  ]
}
```

`nerus` package provides Python API. Python 2.7+, 3.4+ и PyPy 2, 3 are supported.

```bash
$ pip install nerus

```

Load and vizualize:

```python
>>> from nerus.load import load_norm

>>> records = load_norm('lenta.jsonl.gz')
>>> record = next(records)
>>> record

Markup(
    text='Вице-премьер по социальным вопросам Татьяна Голикова рассказала, в каких регионах России зафиксирована наиболее высокая смертность от рака, сообщает РИА Новости. По словам Голиковой, чаще всего онкологические заболевания становились причиной смерти в Псковской, Тверской, Тульской и Орловской областях, а также в Севастополе. Вице-премьер напомнила, что главные факторы смертности в России — рак и болезни системы кровообращения. В начале года стало известно, что смертность от онкологических заболеваний среди россиян снизилась впервые за три года. По данным Росстата, в 2017 году от рака умерли 289 тысяч человек. Это на 3,5 процента меньше, чем годом ранее.',
    spans=[Span(
         start=36,
         stop=52,
         type='PER'
     ), Span(
         start=82,
         stop=88,
         type='LOC'
     ), Span(
         start=149,
         stop=160,
         type='ORG'
	 ...
	 ), Span(
         start=560,
         stop=568,
         type='ORG'
     )]
)

>>> from ipymarkup import show_ascii_markup as show_markup  # pip install ipymarkup

>>> show_markup(record.text, record.spans)
Вице-премьер по социальным вопросам Татьяна Голикова рассказала, в 
                                    PER-------------               
каких регионах России зафиксирована наиболее высокая смертность от 
               LOC---                                              
рака, сообщает РИА Новости. По словам Голиковой, чаще всего 
               ORG--------            PER------             
онкологические заболевания становились причиной смерти в Псковской, 
                                                         LOC------  
Тверской, Тульской и Орловской областях, а также в Севастополе. Вице-
LOC-----  LOC-----   LOC---------------            LOC--------       
премьер напомнила, что главные факторы смертности в России — рак и 
                                                    LOC---         
болезни системы кровообращения. В начале года стало известно, что 
смертность от онкологических заболеваний среди россиян снизилась 
впервые за три года. По данным Росстата, в 2017 году от рака умерли 
                               ORG-----                             
289 тысяч человек. Это на 3,5 процента меньше, чем годом ранее.
```

## Evaluation

Nerus was annotated with DeepPavlov BERT NER tagger, so let's evaluate its quality on gold standart datasets and assume its performance on Lenta.ru news articles is the same.

`deeppavlov` was trained on `ne5` so the score on this dataset is not informative. `gareev` dataset has no `LOC` annotation so one column is missing. `tomita` has open grammar just for `PER` so cells for `LOC` and `ORG` are empty.

On `factru` and `gareev` `deeppavlov` has way higher score then other freely available systems, f1-scores for `PER`, `LOC`, `ORG` are ~0.95+, ~0.9+, ~0.8-0.9 respectively.

<table border="0" class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th colspan="3" halign="left">factru</th>
      <th colspan="2" halign="left">gareev</th>
      <th colspan="3" halign="left">ne5</th>
    </tr>
    <tr>
      <th>f1</th>
      <th>PER</th>
      <th>LOC</th>
      <th>ORG</th>
      <th>PER</th>
      <th>ORG</th>
      <th>PER</th>
      <th>LOC</th>
      <th>ORG</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>deeppavlov</th>
      <td><b>0.971</b></td>
      <td><b>0.926</b></td>
      <td><b>0.824</b></td>
      <td><b>0.984</b></td>
      <td><b>0.917</b></td>
      <td><b>0.997</b></td>
      <td><b>0.989</b></td>
      <td><b>0.976</b></td>
    </tr>
    <tr>
      <th>pullenti</th>
      <td>0.905</td>
      <td>0.814</td>
      <td>0.687</td>
      <td>0.941</td>
      <td>0.639</td>
      <td>0.950</td>
      <td>0.862</td>
      <td>0.683</td>
    </tr>
    <tr>
      <th>texterra</th>
      <td>0.900</td>
      <td>0.800</td>
      <td>0.597</td>
      <td>0.888</td>
      <td>0.561</td>
      <td>0.901</td>
      <td>0.777</td>
      <td>0.594</td>
    </tr>
    <tr>
      <th>tomita</th>
      <td>0.929</td>
      <td></td>
      <td></td>
      <td>0.921</td>
      <td></td>
      <td>0.945</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>natasha</th>
      <td>0.867</td>
      <td>0.753</td>
      <td>0.297</td>
      <td>0.873</td>
      <td>0.347</td>
      <td>0.852</td>
      <td>0.709</td>
      <td>0.394</td>
    </tr>
    <tr>
      <th>mitie</th>
      <td>0.888</td>
      <td>0.861</td>
      <td>0.532</td>
      <td>0.849</td>
      <td>0.452</td>
      <td>0.753</td>
      <td>0.642</td>
      <td>0.432</td>
    </tr>
  </tbody>
</table>

It is also usefull to look at sentences with errors, on can see that usually differences are not significant:

```
[PER] factru / nerus
Список заключенных интернет-журналистов включает репортёров из Китая, 
независимых авторов из Кубы, которые пишут для зарубежных Интернет 
страниц и американского видео-блоггера Джошуа Вольфа (Joshua Wolf), 
                                       PER----------  PER--------   
который отказался передать материалы большому жюри.
>
Список заключенных интернет-журналистов включает репортёров из Китая, 
независимых авторов из Кубы, которые пишут для зарубежных Интернет 
страниц и американского видео-блоггера Джошуа Вольфа (Joshua Wolf), 
                                       PER------------------------  
который отказался передать материалы большому жюри.


[LOC] factru / nerus
В понедельник 28 июня у здания мэрии Москвы на Тверской площади 
                                     LOC---    LOC-----         
состоялась очередная несанкционированная акция протеста «День гнева», 
в этот раз направленная, главным образом, против политики московских и
 подмосковных властей.
>
В понедельник 28 июня у здания мэрии Москвы на Тверской площади 
                                     LOC---    LOC------------- 
состоялась очередная несанкционированная акция протеста «День гнева», 
в этот раз направленная, главным образом, против политики московских и
 подмосковных властей.

[ORG] factru / nerus
Об этом сообщает Комитет защиты журналистов (КЗЖ) (Committee to 
                 ORG-----------------------  ORG   ORG----------
Protect Journalists).
-------------------  
>
Об этом сообщает Комитет защиты журналистов (КЗЖ) (Committee to 
                 ORG--------------------------------------------
Protect Journalists).
-------------------- 
```

Sometimes `deeppavlov` annotations are even better than etalon:

```
[PER] gareev / nerus
Могу лишь сказать , что и в конгрессе , и в администрации неоднократно
 заявляли о важности отмены поправки Джексона – Вэника , особенно для 
американских компаний .
>
Могу лишь сказать , что и в конгрессе , и в администрации неоднократно
 заявляли о важности отмены поправки Джексона – Вэника , особенно для 
                                     PER--------------                
американских компаний .


[LOC] gareev / nerus
Предприятия НЛМК расположены в России , Европе и США .
>
Предприятия НЛМК расположены в России , Европе и США .
                               LOC---   LOC---   LOC  

[ORG] gareev / nerus
Место проведения : Россия , Москва , отель " Марриотт Роял Аврора " , 
ул . Петровка , д . 11 / 20 / м .
>
Место проведения : Россия , Москва , отель " Марриотт Роял Аврора " , 
                                             ORG-----------------     
ул . Петровка , д . 11 / 20 / м .

```
See <a href="examples/errors.txt">examples/errors.txt</a> for full list of errors.


## License

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.

# Development

Tests:

```bash
make test
make int  # runs containters with annotators
```

Package:

```bash
make version
git push
git push --tags

make clean wheel upload
```

Containers:

```bash
make image
make push

cd annotators
make images
make push
```

Deploy worker:

```bash
nerus-ctl worker create
nerus-ctl worker upload worker/setup.sh
nerus-ctl worker ssh 'sudo sh setup.sh'  # install docker + docker-compose

# ...
# + docker --version
# Docker version 18.09.3, build 774a1f4
# + docker-compose --version
# docker-compose version 1.23.2, build 1110ad01

nerus-ctl worker upload worker/remote.env .env
nerus-ctl worker upload worker/docker-compose.yml
nerus-ctl worker ssh 'docker-compose pull'
nerus-ctl worker ssh 'docker-compose up -d'
```

Update worker:

```bash
nerus-ctl worker ssh 'docker-compose pull'
nerus-ctl worker ssh 'docker-compose up -d'
```

Compute:

```bash
export WORKER_HOST=`nerus-ctl worker ip`

nerus-ctl db insert lenta --count=10000
nerus-ctl q insert --count=1000  # enqueue first 1000

# faster version
nerus-ctl worker ssh 'docker run --net=host -it --rm --name insert -e SOURCES_DIR=/tmp natasha/nerus-ctl db insert lenta'
nerus-ctl worker ssh 'docker run --net=host -it --rm --name insert natasha/nerus-ctl q insert'

```

Failed:

```bash
export WORKER_HOST=`nerus-ctl worker ip`

nerus-ctl q failed  # see failed stacktraces

# Id: ...
# Origin: tomita
# ...stack trace...

nerus-ctl q retry --chunk=10  # regroup chunks
nerus-ctl q retry --chunk=1
```


Monitor:

```bash
export WORKER_HOST=`nerus-ctl worker ip`

nerus-ctl worker ssh 'docker stats'
nerus-ctl q show
nerus-ctl db show
```

Dump:

```bash
export WORKER_HOST=`nerus-ctl worker ip`

nerus-ctl dump raw data/dumps/t.raw.jsonl.gz --count=10000
# norm 2x faster with pypy
nerus-ctl dump norm data/dumps/{,.raw}/t.jsonl.gz

# faster version
nerus-ctl worker ssh 'docker run --net=host -it --rm --name dump -v /tmp:/tmp natasha/nerus-ctl dump raw /tmp/t.raw.jsonl.gz'
nerus-ctl worker download /tmp/t.raw.jsonl.gz data/dumps/t.raw.jsonl.gz
```

Clear:

```bash
nerus-ctl db clear
nerus-ctl q clear
```

Remove instance

```bash
nerus-ctl worker rm
```
