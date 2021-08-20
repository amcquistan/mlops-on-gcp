
if [ -d pubsub_schd ]
then
  cd pubsub_schd/python-pubsub/samples/snippets/
fi


export PUBSUB_PROJECT_ID=$(gcloud config get-value project)
export TOPIC_ID=quote-fetcher-topic
export PUSH_SUBSCRIPTION_ID=quote-fetcher-subscription
$(gcloud beta emulators pubsub env-init)

