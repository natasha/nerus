FROM pypy:3

WORKDIR /

RUN pip install --no-cache-dir natasha==0.10.0
COPY app.py .

CMD ["pypy3", "app.py"]