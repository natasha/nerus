FROM deeppavlov/base-gpu

WORKDIR /base/DeepPavlov
ENV DP_ROOT_PATH=/base

RUN git checkout master && \
    git pull && \
    python setup.py develop

RUN python -m deeppavlov install ner_rus_bert
RUN python -m deeppavlov download ner_rus_bert

EXPOSE 5000
CMD python -m deeppavlov.deep riseapi ner_rus_bert -p 5000