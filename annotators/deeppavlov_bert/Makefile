IMAGE = natasha/deeppavlov-ner-ru-bert

image:
	docker build -t $(IMAGE) .

push:
	docker push $(IMAGE)

run:
	docker run -it --rm -p 8086:5000 $(IMAGE)
