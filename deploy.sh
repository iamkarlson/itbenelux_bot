gcloud functions deploy itbenelux-bot \
--env-vars-file prod.env.yaml \
--gen2 \
--runtime=python311 \
--region=itbenelux-bot \
--source=src/ \
--entry-point=handle \
--trigger-http \
--allow-unauthenticated
