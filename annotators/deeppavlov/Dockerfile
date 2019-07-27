FROM deeppavlov/base

WORKDIR /app

RUN cd /base/DeepPavlov && \
    git pull && \
    python3.6 setup.py develop

RUN python3.6 -m deeppavlov install ner_rus_bert
RUN python3.6 -m deeppavlov download ner_rus_bert

EXPOSE 5000

CMD python3.6 -m deeppavlov.deep riseapi ner_rus_bert