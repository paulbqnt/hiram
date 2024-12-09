FROM amazoncorretto:21-alpine-jdk

WORKDIR /app

# Copy Gradle wrapper and Kotlin build scripts first to leverage Docker cache
COPY gradlew gradlew.bat settings.gradle.kts build.gradle.kts ./
COPY gradle ./gradle

# Ensure Gradle has execution permissions
RUN chmod +x gradlew

# Download dependencies to cache them
RUN ./gradlew dependencies --no-daemon || true

# Copy the rest of the application files
COPY . .

# Build the project
RUN ./gradlew clean build -x test --no-daemon

# Expose the application port
EXPOSE 8080

# Run the correct JAR file
CMD ["java", "-jar", "./build/libs/hiram-0.0.1-SNAPSHOT.jar"]
