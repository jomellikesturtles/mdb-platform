#FROM openjdk:11-jdk
FROM eclipse-temurin:21-jdk
#FROM openjdk:21-jre-slim
VOLUME /tmp

EXPOSE 9090
COPY media-data-gateway-service-0.0.1-SNAPSHOT.jar media-data-gateway-service-0.0.1-SNAPSHOT.jar

CMD ["java", "-jar", "/media-data-gateway-service-0.0.1-SNAPSHOT.jar"]

