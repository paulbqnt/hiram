version: '3.8'

services:
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "5173:5173"
    volumes:
      - ./frontend:/app
      - /app/node_modules
    environment:
      - CHOKIDAR_USEPOLLING=true

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8080:8080"
    volumes:
      - ./backend/src:/app/src  # Only mount source code, not the entire app directory
    environment:
      - JAVA_OPTS="-Xmx512m"  # You can add JVM options here if needed

  pricer:
    build:
      context: ./pricer
      dockerfile: Dockerfile
    ports:
      - "8081:8080"  # Map host port 8081 to container port 8080
    volumes:
      - ./pricer/src:/app/src  # Only mount source code, not the entire app directory