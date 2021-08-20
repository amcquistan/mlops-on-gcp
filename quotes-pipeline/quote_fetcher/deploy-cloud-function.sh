
#!/bin/bash

if [ -d quote_fetcher ]
then
  cd quote_fetcher
fi

set -ex

PROJECT_ID=$(gcloud config get-value project)
TOPIC_ID=quotes

gcloud functions deploy quote_fetcher \
  --set-env-vars PROJECT_ID=$PROJECT_ID,TOPIC_ID=$TOPIC_ID \
  --entry-point fetch_quote \
  --runtime python37 \
  --trigger-topic quote-fetcher-topic
