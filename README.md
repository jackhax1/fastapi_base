## FastAPI Base

### Description
Main goal of this repo is to provide a base/template project for someone wanting to quickly deploy an API. 
I would like to keep it simple for beginner as well as modular for pros to add in features quickly to suit your need

### Features
1. Multiple different routes with GET/POST request types
2. Basic authentication
3. ApiKey checking
4. Pydantic data models defined for parsing request body
5. SQLalchemy based ORM that enables easy interfacing with a database (tested with PostgreSQL and MySQL)
6. API rate limiting with Redis

### TO DO
- [x] separate secrets into a different file
- [ ] Add comments
- [x] Create middleware for basic auth and apikey checking
- [ ] User table in db
- [ ] CI/CD pipeline with Actions
- [ ] Robust json schema
- [x] Ratelimiting with Redis
- [ ] AI model deployment
- [ ] ...(Please raise and issue if you suggestions)
