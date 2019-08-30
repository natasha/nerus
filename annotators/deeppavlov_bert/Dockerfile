FROM deeppavlov/base-gpu

WORKDIR /base/DeepPavlov
ENV DP_ROOT_PATH=/base

RUN git checkout master && \
    git pull && \
    python setup.py develop

RUN python -m deeppavlov install ner_rus_bert
RUN python -m deeppavlov download ner_rus_bert

WORKDIR /root
COPY onstart.sh .

CMD ["/bin/bash", "onstart.sh"]
