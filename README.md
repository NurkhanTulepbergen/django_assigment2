﻿# django_assigment2

**Registration:

POST /api/auth/users/
Example payload:
{
  "email": "user@example.com",
  "username": "user",
  "password": "password123",
  "role": "teacher"
}


**Login:

POST /api/auth/jwt/create/
Example payload:
{
  "email": "user@example.com",
  "password": "password123"
}


**Logout:

POST /api/auth/jwt/destroy/


**View Profile:

GET /api/auth/users/me/
