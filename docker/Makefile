
ANNS = deeppavlov mitie natasha texterra tomita

images:
	for i in $(ANNS); do make -C $$i image; done

push:
	for i in $(ANNS); do make -C $$i push; done
