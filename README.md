## Sample program to demonstrate a k8s job.

Each namespace has a default service account created.

$ kubectl create namespace jobs-test

$ kubectl get sa -n jobs-test

This service account will have a token created and regsitered as a secret that can be made available to the containers.

$ kubectl describe sa -n jobs-test
Name:                default
Namespace:           jobs-test
Labels:              <none>
Annotations:         <none>
Image pull secrets:  <none>
Mountable secrets:   default-token-bg5cm
Tokens:              default-token-bg5cm
Events:              <none>

The mountable secret default-token-xxxx above can be made available to container as an environment variable.

For our test, we will extract and make it available via shell script.

$ export TOKEN=`./get-token.sh`

./run_job.py is a python program that will make api call to kubernetes api server to create a job. The job definition is created dynamically.

$ ./run_job.py
/usr/local/lib/python2.7/dist-packages/urllib3/connectionpool.py:857: InsecureRequestWarning: Unverified HTTPS request is being made. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
  InsecureRequestWarning)
  {"kind":"Job","apiVersion":"batch/v1","metadata":{"name":"sample-work-9978a662-ac3a-11e8-b2a2-0ad04fef5a10","namespace":"jobs-test","selfLink":"/apis/batch/v1/namespaces/jobs-test/jobs/sample-work-9978a662-ac3a-11e8-b2a2-0ad04fef5a10","uid":"997c1c5f-ac3a-11e8-a0d9-0a010a6eb61a","resourceVersion":"7105719","creationTimestamp":"2018-08-30T09:53:51Z","labels":{"job_group":"sample-work"}},"spec":{"parallelism":1,"completions":1,"backoffLimit":6,"selector":{"matchLabels":{"controller-uid":"997c1c5f-ac3a-11e8-a0d9-0a010a6eb61a"}},"template":{"metadata":{"name":"sample-work-9978a662-ac3a-11e8-b2a2-0ad04fef5a10","creationTimestamp":null,"labels":{"controller-uid":"997c1c5f-ac3a-11e8-a0d9-0a010a6eb61a","job-name":"sample-work-9978a662-ac3a-11e8-b2a2-0ad04fef5a10"}},"spec":{"containers":[{"name":"sample-work-9978a662-ac3a-11e8-b2a2-0ad04fef5a10","image":"saifuddin53/sample-work","command":["/usr/bin/python","/worker.py","-a","apple","-b","banana","-t","5"],"resources":{},"terminationMessagePath":"/dev/termination-log","terminationMessagePolicy":"File","imagePullPolicy":"Always"}],"restartPolicy":"Never","terminationGracePeriodSeconds":30,"dnsPolicy":"ClusterFirst","securityContext":{},"schedulerName":"default-scheduler"}}},"status":{}}

Job got created, pod executed succesfully and we can see the status. The below status can also be fetched via k8s api call.

$ kubectl get jobs,pods -n jobs-test
NAME                                                    DESIRED   SUCCESSFUL   AGE
jobs/sample-work-9978a662-ac3a-11e8-b2a2-0ad04fef5a10   1         1            2m

As you can see from the output of ./run_job.py, it also created a label job_group=sample-work. These labels can be used to cleanup all the completed jobs. Jobs are logical entities and not deleted after the job run is complete.
Below command can be used to clean up all jobs, of course it needs to include filters to select only the ones that are completed.
$ kubectl delete jobs -l job_group=sample-work -n jobs-test
job "sample-work-06a22270-ac33-11e8-b2a2-0ad04fef5a10" deleted
job "sample-work-145cd1a8-ac33-11e8-b2a2-0ad04fef5a10" deleted
job "sample-work-1cf81494-ac47-11e8-b2a2-0ad04fef5a10" deleted
job "sample-work-2c692af8-ac47-11e8-b2a2-0ad04fef5a10" deleted
job "sample-work-34a45d50-ac47-11e8-b2a2-0ad04fef5a10" deleted
job "sample-work-45be940c-ac33-11e8-b2a2-0ad04fef5a10" deleted
job "sample-work-9978a662-ac3a-11e8-b2a2-0ad04fef5a10" deleted
job "sample-work-fcf740de-ac46-11e8-b2a2-0ad04fef5a10" deleted


The service account token we used to create jobs by default doesnt have the required permissions. We need to provide the permissions for the same
$ ./setup-roles.sh
role "default-role" unchanged
rolebinding "default-role-binding" unchanged

Check roles-job.yml for details of permissions

# Failure handling

Jobs can be configured to retry or restart pods on failure for a given number of times before it fails or succeeds. For example, setting backoffLimit=1(like in this example) will ensure that the job will create the pod only once if case of pod failure. See https://kubernetes.io/docs/concepts/workloads/controllers/jobs-run-to-completion/#job-termination-and-cleanup for more details.

This can be tested by creating and running the sample job to failure by passsing -f flag.

$ ./run_job.py -f


$ ./run_job.py -h to see the options it supports.



