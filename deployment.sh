#!/usr/bin/env bash

gcloud container clusters get-credentials  ip-code-builder-us-east1b

echo "Current context\n"
kubectl config current-context

DATE=`date '+%Y-%m-%d-%H-%M'`
RELEASE_TAG="RELEASE-"$DATE
echo "Releaseing:: "$RELEASE_TAG
docker build -t spacy-server:$RELEASE_TAG .
docker tag spacy-server:$RELEASE_TAG gcr.io/interviewparrot/spacy-server:$RELEASE_TAG
### Push the image to gcr
docker push gcr.io/interviewparrot/spacy-server:$RELEASE_TAG
DEPLOYMENT_FILE=spacy-server.yaml
echo $DEPLOYMENT_FILE
sed -i "s,RELEASE_TAG,$RELEASE_TAG,g" $DEPLOYMENT_FILE

### Apply to prod cluster
kubectl apply -f $DEPLOYMENT_FILE

## Restore the deployment file
sed -i "s,$RELEASE_TAG,RELEASE_TAG,g" $DEPLOYMENT_FILE

### get pods
kubectl get pods

