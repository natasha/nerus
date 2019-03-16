FROM python:3.5

WORKDIR /

COPY algfio algfio
COPY tomita-linux64 .
COPY app.py .

ENV CONFIG_DIR algfio
ENV TOMITA_BIN tomita-linux64
CMD ["python", "app.py"]