#!/bin/bash

TOKEN=$(kubectl describe secret $(kubectl get secrets -n jobs-test | grep default | cut -f1 -d ' ') -n jobs-test | grep -E '^token' | cut -f2 -d':' | tr -d '\t' | xargs )
echo $TOKEN

