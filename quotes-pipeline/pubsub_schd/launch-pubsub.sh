
set -xe 

export PROJECT_ID=$(gcloud config get-value project)
gcloud beta emulators pubsub start --project $PROJECT_ID --host-port 8085
