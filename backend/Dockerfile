# Use the official Maven image to build the application
FROM maven:3.8.4-openjdk-17-slim AS build
WORKDIR /app

# Copy only pom.xml first to leverage Docker cache
COPY pom.xml .

# Download dependencies
RUN mvn dependency:go-offline

# Copy source code
COPY src ./src

# Build the application
RUN mvn clean package -DskipTests

# Debugging step to list contents of target directory
RUN ls -l /app/target

# Final image
FROM openjdk:17-jdk-slim
WORKDIR /app

# Explicitly copy the JAR by name
COPY --from=build /app/target/*.jar app.jar
# Expose the port the application runs on
EXPOSE 8080

# Command to run the application
ENTRYPOINT ["java", "-jar", "app.jar"]