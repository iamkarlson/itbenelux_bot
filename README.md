# Richard Stallman Bot

Bot for chat "IT talks Benelux"

# Why

Because I can.

# Init

Create a GCP project. `create_infra.sh` will do it for you. You still need to enable billing for this account. Open this link https://console.cloud.google.com/billing/linkedaccount?project=itbenelux-bot and click "Link a billing account". You can use your existing billing account or create a new one.


# Deploy with terraform
3. Fix variables.tf (put them in damn secrets)
4. Run `deploy_terraform.sh`
5. Send your damn messages to your bot

# Deploy without terraform

1. Put your damn secrets in `prod.env.yaml`
2. Run `deploy_gcloud.sh`
3. Register webhook with `setup_webhook.py`. 
  * this sucks because you have to do it manually comparing to terraform
4. Send your damn messages to your bot


# Code structure

- `main.py` - entrypoint
- `config.py` - config for the bot, set ups all the configuration for different tasks. 