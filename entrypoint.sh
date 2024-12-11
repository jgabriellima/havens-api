#!/bin/bash
set -e

# Ensure the MODE environment variable is set
if [ -z "$MODE" ]; then
  echo "Error: MODE environment variable is not set."
  echo "Please set the MODE environment variable to 'api', 'worker', 'beat', 'flower', 'debug', 'alembic', or 'test'."
  exit 1
fi

# Ensure the ENV environment variable is set (dev or prod)
if [ -z "$ENV" ]; then
  echo "Warning: ENV environment variable is not set. Defaulting to 'prod'."
  ENV="prod"
fi

# Function to start the Celery healthcheck service
start_healthcheck() {
  echo "Starting Celery healthcheck service..."
  python -m uvicorn api_template.celery.core.health_check:router --host 0.0.0.0 --port 8001 &
}

# Function to check if a service is ready
wait_for_service() {
  echo "Waiting for $1 to be ready..."
  until nc -z $2 $3; do
    echo "$1 is unavailable - sleeping"
    sleep 1
  done
  echo "$1 is up - executing command"
}

# Function to wait for all required services
wait_for_services() {
  wait_for_service "RabbitMQ" ${RABBITMQ_HOST:-rabbitmq} ${RABBITMQ_PORT:-5672}
  wait_for_service "Redis" ${REDIS_HOST:-redis} ${REDIS_PORT:-6379}
}

# Function to run database migrations
run_migrations() {
  echo "Running database migrations..."
  /app/scripts/run_migration.sh || {
    echo "Database migration failed. Exiting...";
    exit 1;
  }
}

# Trap SIGTERM
trap 'echo "Received SIGTERM. Shutting down..."; kill -TERM $PID; wait $PID' TERM

# Start the correct service based on the MODE environment variable
if [ "$MODE" = "alembic" ]; then
    echo "Running Alembic command..."
    shift  # Remove 'alembic' from the arguments
    exec alembic "$@"
elif [ "$MODE" = "test" ]; then
    echo "Running tests..."
    shift  # Remove 'test' from the arguments
    exec pytest "$@"
elif [ "$MODE" = "api" ]; then
    echo "Starting API service..."
    wait_for_services  # Espera pelos serviços apenas quando necessário
    run_migrations
    if [ "$ENV" = "dev" ]; then
      exec uvicorn api_template.server:app --host 0.0.0.0 --port ${API_PORT:-8000} --reload --log-level debug
    else
      exec uvicorn api_template.server:app --host 0.0.0.0 --port ${API_PORT:-8000} --workers ${API_WORKERS:-4} --log-config /app/log_config.json
    fi
elif [ "$MODE" = "worker" ]; then
    echo "Starting Celery worker..."
    wait_for_services  # Espera pelos serviços apenas quando necessário
    start_healthcheck
    if [ "$ENV" = "dev" ]; then
      exec celery -A api_template.celery.celery_app worker --loglevel=${LOG_LEVEL:-info} --pool=solo &
    else
      exec celery -A api_template.celery.celery_app worker --loglevel=${LOG_LEVEL:-info} &
    fi
    PID=$!
    wait $PID
elif [ "$MODE" = "beat" ]; then
    echo "Starting Celery beat..."
    wait_for_services  # Espera pelos serviços apenas quando necessário
    exec celery -A api_template.celery.celery_app beat --loglevel=${LOG_LEVEL:-info} &
    PID=$!
    wait $PID
elif [ "$MODE" = "flower" ]; then
    echo "Starting Flower Monitoring..."
    wait_for_services  # Espera pelos serviços apenas quando necessário
    exec celery -A api_template.celery.celery_app flower &
    PID=$!
    wait $PID
elif [ "$MODE" = "debug" ]; then
    echo "Starting in debug mode..."
    wait_for_services  # Espera pelos serviços apenas quando necessário
    exec uvicorn api_template.server:app --host 0.0.0.0 --port ${API_PORT:-8000} --reload --log-level debug
else
    echo "Invalid MODE. Use 'api', 'worker', 'beat', 'flower', 'debug', 'alembic', or 'test'."
    exit 1
fi
