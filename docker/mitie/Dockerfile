FROM python:3.5

WORKDIR /

RUN pip install --no-cache-dir git+https://github.com/mit-nlp/MITIE.git@v0.6
COPY ru_model.dat .
COPY app.py .

CMD ["python", "app.py"]