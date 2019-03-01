
IMAGE = natasha/tomita-algfio
CONFIG = algfio

tomita-mac:
	wget http://download.cdn.yandex.net/tomita/tomita-mac.bz2
	bzip2 -d tomita-mac.bz2
	chmod u+x tomita-mac

tomita-linux64:
	wget http://download.cdn.yandex.net/tomita/tomita-linux64.bz2
	bzip2 -d tomita-linux64.bz2
	chmod u+x tomita-linux64

image: tomita-linux64 clean
	docker build -t $(IMAGE) .

push:
	docker push $(IMAGE)

run:
	docker run -it --rm -p 8084:8080 $(IMAGE)

clean:
	rm -f $(CONFIG)/*.bin
