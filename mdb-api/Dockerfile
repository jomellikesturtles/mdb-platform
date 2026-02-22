FROM eclipse-temurin:21-jdk
#FROM openjdk:21-jre-slim
VOLUME /tmp

LABEL authors="jommel"
# VOLUME /tmp

EXPOSE 8084

# Copy the application JAR file to the container
COPY mdb-0.0.0-SNAPSHOT.jar mdb-0.0.0-SNAPSHOT.jar
# Set the command to run the application when the container starts
CMD ["java", "-jar", "/mdb-0.0.0-SNAPSHOT.jar"]