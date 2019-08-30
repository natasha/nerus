
ANNOTATORS = deeppavlov deeppavlov_bert mitie natasha texterra tomita

images:
	for i in $(ANNOTATORS); do make -C $$i image; done

push:
	for i in $(ANNOTATORS); do make -C $$i push; done
