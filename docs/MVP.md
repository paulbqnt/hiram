# MVP Document: Hiram Web App

## Project Overview
The Hiram Web App allows users to calculate the price of financial products through a web interface.

## MVP Goals
1. Backend API:
    - Price calculation logic.
    - `POST /pricer/calculate`: Endpoint for submitting pricing data.

2. Frontend:
    - Form to input pricing parameters.
    - Display pricing results returned by the backend.

3. Docker:
    - Backend and frontend deployed as Docker services.

## Out of Scope
- User authentication.
- Persistent storage for pricing results.
- Advanced UI styling and animations.

## Technical Details
- Backend: Kotlin with Spring Boot.
- Frontend: React with TypeScript and Vite.
- Communication: REST APIs.
- Deployment: Docker.

## Next Steps
- Post-MVP enhancements:
    - Add database integration for storing pricing data.
    - Introduce user authentication and authorization.
    - Deploy to production with CI/CD.
