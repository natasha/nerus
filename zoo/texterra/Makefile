
IMAGE = natasha/texterra-russian

texterra-russian:
	wget https://at.ispras.ru/owncloud/index.php/s/Jkgrw6iIInwfKFv/download -O texterra-russian.zip
	unzip texterra-russian.zip
	rm texterra-russian.zip

image: texterra-russian
	docker build -t $(IMAGE) .

push:
	docker push $(IMAGE)

run:
	docker run -it --rm -p 8082:8080 --name texterra $(IMAGE)
