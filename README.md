
<img src="i/logo.svg" height="75">

[![Build Status](https://travis-ci.org/natasha/nerus.svg?branch=master)](https://travis-ci.org/natasha/nerus) [![Download Nerus](https://img.shields.io/badge/download-v1.0-green.svg)](https://github.com/natasha/nerus/releases)

<a href="https://github.com/yutkin/Lenta.Ru-News-Dataset">Lenta.ru dataset</a> annotated with <a href="https://github.com/deepmipt/DeepPavlov">DeepPavlov</a> BERT NER.

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

Dataset is gzip-compressed text file with <a href="http://jsonlines.org/">JSON lines</a>:

```bash
$ gzcat data/dumps/lenta.jsonl.gz | head -1 | jq .
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

`nerus` provides Python API. Python 2.7+, 3.4+ и PyPy 2, 3 are supported.

```bash
$ pip install nerus

```

```python
>>> from nerus.load import load_norm

>>> records = load_norm('data/dumps/lenta.jsonl.gz')
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

# pip install ipymarkup
>>> from ipymarkup import show_ascii_markup as show_markup

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
