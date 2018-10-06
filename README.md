Silver standard russian named entity recognition corpus

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
