# In 191 MaxRAMFraction is renamed to MaxRAMPercentage
FROM openjdk:8u181-jre

COPY texterra-russian app
COPY texterra.properties.xml app
WORKDIR app

# If memory available to docker is 2Gb, for example, then max heap
# size is 500Mb, it is not enough to texterra, so set heap size equal
# to docker RAM
ENV JAVA_OPTS -XX:MaxRAMFraction=1

CMD ["bin/texterra", "-c", "texterra.properties.xml", "server", "start"]