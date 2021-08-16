#!/bin/bash


CLUSTER_NAME=$1
ZONE=$2

gcloud config set compute/zone $ZONE
gcloud container clusters create $CLUSTER_NAME --scopes 'https://www.googleapis.com/auth/cloud-language,default,bigquery,compute-rw,datastore,storage-full,taskqueue,userinfo-email,sql-admin'

gcloud container clusters list

gcloud container clusters get-credentials $CLUSTER_NAME

kubectl create deployment quote-sentiment --image=gcr.io/qwiklabs-gcp-04-2ad6a04dc593/quote-sentiment:0.2.0

kubectl expose deployment quote-sentiment --type=LoadBalancer --port 5000

kubectl get service

gcloud container clusters --quiet delete $CLUSTER_NAME 