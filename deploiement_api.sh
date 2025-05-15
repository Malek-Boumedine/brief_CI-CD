#!/bin/bash
set -e

PORT=8080

# Suppression du conteneur existant (ignore les erreurs si le conteneur n'existe pas)
az container delete --name $CONTAINER_NAME --resource-group $RESOURCE_GROUP -y || true

# Déploiement
az container create \
  --name $CONTAINER_NAME \
  --resource-group $RESOURCE_GROUP \
  --location $REGION \
  --image $ACR_LOGIN_SERVER/$ACR_IMAGE \
  --cpu 1 \
  --memory 2 \
  --registry-login-server $ACR_LOGIN_SERVER \
  --registry-username $ACR_USERNAME \
  --registry-password $ACR_PASSWORD \
  --ports $PORT \
  --ip-address Public \
  --os-type Linux \
  --dns-name-label $DNS_LABEL \
  --environment-variables \
    SECRET_KEY="$SECRET_KEY" \
    ALGORITHM="$ALGORITHM" \
    ACCESS_TOKEN_EXPIRE_MINUTES="$ACCESS_TOKEN_EXPIRE_MINUTES" \
    DATABASE_URL="$DATABASE_URL" \
    API_USER="$API_USER" \
    EMAIL_API="$EMAIL_API" \
    PASSWORD_API="$PASSWORD_API"

echo "Le déploiement a réussi."
