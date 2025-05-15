#!/bin/bash

python3 api/create_admin.py

uvicorn main:app --host 0.0.0.0 --port 8080
