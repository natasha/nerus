FROM deeppavlov/base-gpu

WORKDIR /base/DeepPavlov

# for some reason download does not work with default
# /root/.deeppavlov
ENV DP_ROOT_PATH=/base

RUN git checkout master && \
    git pull && \
    python setup.py develop

RUN python -m deeppavlov install ner_rus
RUN python -m deeppavlov download ner_rus

WORKDIR /root
COPY onstart.sh .

CMD ["/bin/bash", "onstart.sh"]
