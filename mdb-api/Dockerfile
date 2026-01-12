FROM ubuntu:latest
#FROM openjdk:11-jdk

LABEL authors="jommel"
VOLUME /tmp

EXPOSE 8080
# Copy the application JAR file to the container
COPY target/mdb-0.0.0-SNAPSHOT-plain.jar mdb-0.0.0-SNAPSHOT-plain.jar
# Set the command to run the application when the container starts
CMD ["java", "-jar", "/mdb-0.0.0-SNAPSHOT-plain.jar"]

#ENTRYPOINT ["top", "-b"    ]