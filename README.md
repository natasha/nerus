# Silver standard russian named entity recognition corpus [![Download russian named entity recognition corpus](https://img.shields.io/badge/download-v1.0-green.svg)](https://github.com/bureaucratic-labs/russian-ner-corpus/releases)
## About

This corpus was bootstapped from [Lenta.ru news dataset](https://github.com/yutkin/Lenta.Ru-News-Dataset), using several freely available NER toolkits for russian language:

- [deepmipt/ner](https://github.com/deepmipt/ner)
- [Natasha](https://github.com/natasha/natasha)
- [ISPRAS Texterra](https://texterra.ispras.ru)
- [Lang.org.ua MITIE model for russian language](http://lang.org.ua/en/models/#anchor3)

This corpus shares almost same ideas, as for example, [GICR (General Internet Corpus of Russian Language)](http://www.webcorpora.ru/en/) which was annotated in automated manner, but in contrast - we use greater count of  annotators, hoping that there'll be less errors.

## Format

### Types of entities

Currently, due to differencies in used toolkits, we use only three types of entities:

- Person [PER]
- Organisation [ORG]
- Location [LOC]

Some toolkits (notably, `Texterra`) have additional types of entities.  
Since we don't see actual difference, for example, between LOC and GPE entities - we changed tag of all GPE entities to LOC.

### Annotations

Each annotated article from original dataset stored as JSON file with following structure:

```json
{
  "article_id": 100,
  "content": " ... ",
  "annotations": [
      {
        "span": {
          "start": 10,
          "end": 31
        },
        "type": "PER",
        "text": "Дмитрием Светозаровым"
      }
  ]
}
```

We decided to not use any tokenization - mostly because each of used toolkits have built-in tokenizer and, so `span` of each entity is actual position inside article's `content`. 

## Statistics (actual on 06.10.18)

Total entities with A = 3:

```
   tag | count
-------+--------
   PER | 316951
   ORG | 105442
   LOC | 471528
```

A = 2:
```
   tag |  count
-------+---------
   PER | 1280616
   ORG |  753189
   LOC | 1787637
```


## License

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.

# Development

Tests:

```bash
make test
make int  # runs containters with annotators
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

nerus-ctl worker upload worker/cpu.env .env
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

nerus-ctl q retry  # requeue all failed
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

nerus-ctl db dump dump.tar --count=500000

# faster version
nerus-ctl worker ssh 'docker run --net=host -it --rm --name dump natasha/nerus-ctl db dump dump.tar --count=400000'
```

# GPU vs CPU

On AWS p2.xlarge one can process ~100 000 Lenta docs in 1.5 hours
On YC 8 cores 16Gb instance same thing takes 3 hours, 2x slower
But AWS costs 0.9$ (60 rub) per hour, YC 10 rub per hour (3 rub for spot instance), so use YC
