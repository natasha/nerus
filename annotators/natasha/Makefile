IMAGE = natasha/natasha

image:
	docker build -t $(IMAGE) .

push:
	docker push $(IMAGE)

run:
	docker run -it --rm -p 8085:8080 $(IMAGE)
