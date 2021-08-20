
sudo apt-get install openjdk-11-jdk google-cloud-sdk-pubsub-emulator -y

if [ -d pubsub_schd ]
then
  cd pubsub_schd
fi

export PUBSUB_PROJECT_ID=$(gcloud config get-value project)
export TOPIC_ID=quote-fetcher-topic
export PUSH_SUBSCRIPTION_ID=quote-fetcher-subscription
$(gcloud beta emulators pubsub env-init)

git clone https://github.com/googleapis/python-pubsub.git
cd python-pubsub/samples/snippets/
pip install -r requirements.txt

python publisher.py $PUBSUB_PROJECT_ID create $TOPIC_ID
python subscriber.py $PUBSUB_PROJECT_ID create-push $TOPIC_ID $PUSH_SUBSCRIPTION_ID http://localhost:8085
