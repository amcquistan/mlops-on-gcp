
export PUBSUB_PROJECT_ID=$(gcloud config get-value project)
export TOPIC_ID=quote-fetcher-topic
export PUSH_SUBSCRIPTION_ID=quote-fetcher-subscription
$(gcloud beta emulators pubsub env-init)

python publisher.py $PUBSUB_PROJECT_ID create $TOPIC_ID
python subscriber.py $PUBSUB_PROJECT_ID create-push $TOPIC_ID $PUSH_SUBSCRIPTION_ID http://localhost:808
