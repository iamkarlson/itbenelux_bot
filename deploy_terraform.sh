#!/usr/bin/env zsh

terraform init

terraform apply -auto-approve

HOOK_URL=$(terraform output -raw function_uri)

BOT_NAME=$(terraform output -raw bot_name)
BOT_REGION=$(terraform output -raw bot_region)
BOT_PROJECT=$(terraform output -raw bot_project)

# first I need to switch to a correct bot project
# Project ID is parsed from the prod.env.yaml
# Why yaml? because fuck google
# Load variables from YAML file
while IFS="=" read -r key value; do
  # Use eval to handle the value properly if it includes quotes
  eval $key='$value'
done < <(yq -r 'keys[] as $k | "\($k)=\(.[$k])"' prod.env.yaml)

# Now, all variables are set and can be used later in the script
echo "BOT_TOKEN is $BOT_TOKEN"
echo "AUTHORIZED_CHAT_IDS is $AUTHORIZED_CHAT_IDS"
echo "Var3 is $var3"

# Fix permissions because fuck terraform
# https://stackoverflow.com/questions/76592284/google-cloudfunctions-gen2-terraform-policy-doesnt-create-a-resource
gcloud functions add-invoker-policy-binding "$BOT_NAME" \
       --region="$BOT_REGION" \
       --member="allUsers"


#  # Registering bot in telegram API
echo "python -m setup_webhook '$BOT_TOKEN' '$HOOK_URL'"
python -m setup_webhook $BOT_TOKEN "$HOOK_URL"
