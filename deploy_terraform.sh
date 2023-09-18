#!/usr/bin/env zsh

terraform init

terraform apply -auto-approve

HOOK_URL=$(terraform output -raw function_uri)

BOT_NAME=$(terraform output -raw bot_name)
BOT_REGION=$(terraform output -raw bot_region)
BOT_PROJECT=$(terraform output -raw bot_project)

# Fix permissions because fuck terraform
# https://stackoverflow.com/questions/76592284/google-cloudfunctions-gen2-terraform-policy-doesnt-create-a-resource
 gcloud functions add-invoker-policy-binding "$BOT_NAME" \
      --region="$BOT_REGION" \
      --member="allUsers"


 # Registering bot in telegram API
 python -m setup_webhook "$HOOK_URL"
