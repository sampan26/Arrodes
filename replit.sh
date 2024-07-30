#!/bin/bash

# Install dependencies using Poetry
poetry install

# Install prisma
poetry run prisma generate

# Run Prisma migration
poetry run prisma migrate dev

# Start the application with auto-reload
