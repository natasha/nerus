
ZOO = deeppavlov mitie natasha texterra tomita

images:
	for i in $(ZOO); do make -C $$i image; done

push:
	for i in $(ZOO); do make -C $$i push; done

run:
	docker-compose up --rm
