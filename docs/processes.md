# Processes

## Multitenant SaaS architecture

### 1. **Request Initiation** (Req) [RI]

- A client makes an HTTP request to the application (e.g., via a REST API or web interface).

### 2. **Middleware Processing** (Req) [MP]

- **Tenant Identification:** [TI] Middleware extracts the tenant identifier from the request. This could be from a subdomain, URL path, request header, or other metadata.
- **Authentication:** [AN] Middleware checks the presence of authentication tokens (e.g., JWTs). If present, the token is validated.
- **Session Initialization:** [SI] The middleware sets up the database session for the request. It configures the session to use the schema associated with the identified tenant.

### 3. **Routing** (Req) [RR]

- The request is routed to the appropriate FastAPI endpoint based on the request path and method (e.g., GET, POST).

### 4. **Dependency Injection** (Req) [DI]

- **Request Scope:** [RS] Dependencies (like database sessions or service objects) are provided to the endpoint handler through FastAPI's dependency injection system.

### 5. **Endpoint Execution** (PreRes) [EE]

- **Data Validation:** [DV] Request data is validated against predefined Pydantic schemas. This ensures that the data conforms to expected formats and types.
- **Business Logic:** [BL] The endpoint handler executes business logic. This could include creating, reading, updating, or deleting resources specific to the tenant.
- **Database Operations:** [DO] The handler interacts with the database using SQLAlchemy ORM or Core to perform CRUD operations. These operations are isolated within the tenant's schema.
- **Data Security:** [DS] Throughout the process, data is handled securely, ensuring sensitive information is encrypted and access controls are enforced.
- **Authorization Checks:** Authorization checks are performed to ensure the authenticated user has the appropriate permissions to perform the requested actions.

### 6. **Service Layer Interactions** (PreRes) [SL]

- The endpoint may call additional service layer functions to handle complex logic, such as sending notifications, processing payments, or interacting with third-party APIs.

### 7. **Result Generation** (Res) [RG]

- **Data Processing:** [DP] Any data retrieved or manipulated is processed and formatted. This could involve transforming database results into API-friendly formats or applying business rules.
- **Response Creation:** [RC] The endpoint constructs a response object, including the appropriate HTTP status code, headers, and body content.

### 8. **Database Session Management** (Res) [DM]

- **Session Commit/Rollback:** [SC] If the request is successful, the database session commits the transaction. If an error occurs, the session rolls back the transaction to maintain data integrity.
- **Session Closure:** [SD] The database session is closed, releasing any resources.

### 9. **Response Delivery** (Res) [RD]

- The constructed response is sent back to the client. This includes the HTTP status code, headers, and any response body data.

### 10. **Logging and Monitoring** (PosRes) [ML]

- **Request Logging:** [RL] Details of the request, such as the endpoint accessed, request duration, and outcome (success or error), are logged for auditing and monitoring purposes.
- **Error Handling:** [EH] If an error occurred, appropriate error handling mechanisms capture and log the error. Depending on the severity, an error response is sent to the client with a suitable message and status code (e.g., 400 for bad requests, 500 for server errors).
- **Metrics Collection:** [MC] Metrics related to request processing time, database query performance, and other relevant metrics are collected for monitoring.

### 11. **Security Measures** (PosReq) [SM]

### 12. **Post-Request Actions** (PosReq) [PR]

- **Asynchronous Tasks:** [AT] Any asynchronous tasks (such as sending confirmation emails, processing data in the background, etc.) are triggered and handled by separate worker processes if needed.
- **Session Cleanup:** [SR] Final cleanup actions are performed, such as clearing cached data or temporary files related to the request.

### 13. **Audit Logging** (PosReq) [AL]

- **Audit Trail:** [TA] Key actions performed during the request, especially those involving data modifications, are logged for auditing purposes, ensuring compliance with regulations and traceability.

This process flow ensures that each tenant's data and operations are properly isolated, authenticated, and authorized, providing a secure and efficient multitenant environment.
