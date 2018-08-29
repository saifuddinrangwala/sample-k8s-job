#!/bin/bash

set -x

#kubectl apply -f roles-job.yml

TOKEN=$(kubectl describe secret $(kubectl get secrets -n jobs-test | grep default | cut -f1 -d ' ') -n jobs-test | grep -E '^token' | cut -f2 -d':' | tr -d '\t' | xargs )

curl -v -k \
	--header "Authorization: Bearer $TOKEN" \
	-X DELETE https://api.useast1.cis.kuberbots.com/apis/batch/v1/namespaces/jobs-test/jobs/job-wq-2

curl -v -k \
	--header "Content-Type: application/json" \
	--header "Authorization: Bearer $TOKEN" \
	 https://api.useast1.cis.kuberbots.com/apis/batch/v1/namespaces/jobs-test/jobs \
	-d @job.json

