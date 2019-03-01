
IMAGE = natasha/mitie-ner-ru

ru_model.dat:
	wget http://lang.org.ua/static/downloads/ner_models/ru_model.dat.bz2
	bzip2 -d ru_model.dat.bz2

image: ru_model.dat
	docker build -t $(IMAGE) .

push:
	docker push $(IMAGE)

run:
	docker run -it --rm -p 8083:8080 $(IMAGE)

