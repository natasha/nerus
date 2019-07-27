IMAGE = natasha/deeppavlov-ner-ru

image:
	docker build -t $(IMAGE) .

push:
	docker push $(IMAGE)

run:
	docker run -it --rm -p 8081:5000 $(IMAGE)
