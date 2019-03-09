CPU_IMAGE = natasha/deeppavlov-ner-ru
GPU_IMAGE = natasha/deeppavlov-ner-ru-gpu

gpu-image:
	docker build -f Dockerfile.gpu -t $(GPU_IMAGE) .

cpu-image:
	docker build -t $(CPU_IMAGE) .

images: cpu-image gpu-image

image: images

push-cpu:
	docker push $(CPU_IMAGE)

push-gpu:
	docker push $(GPU_IMAGE)

push: push-cpu push-gpu

run-cpu:
	docker run -it --rm -p 8081:6004 $(CPU_IMAGE)

run: run-cpu
