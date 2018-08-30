#!/usr/bin/python

import uuid
import argparse
import json
import requests
import os

class K8SJob(object):
    def __init__(self, name, command, namespace="jobs-test"):
        job_name = name + "-" + str(uuid.uuid1())
        self._job = {}
        self._job["apiVersion"] = "batch/v1"
        self._job["kind"] = "Job"
        self._job["metadata"] = {}
        self._job["metadata"]["name"] = job_name
        self._job["metadata"]["namespace"] = namespace
        self._job["metadata"]["labels"] = {}
        self._job["metadata"]["labels"]["job_group"] = name
        self._job["spec"] = {}
        self._job["spec"]["parallelism"] = 1
        self._job["spec"]["completions"] = 1
        self._job["spec"]["template"] = {}
        self._job["spec"]["template"]["metadata"] = {}
        self._job["spec"]["template"]["metadata"]["name"] = job_name
        self._job["spec"]["template"]["spec"] = {}
        self._job["spec"]["template"]["spec"]["containers"] = []
        self._job["spec"]["template"]["spec"]["restartPolicy"] = "Never"

        container = {}
        container["name"] = job_name
        container["image"] = "saifuddin53/sample-work"
        container["command"] = command
        self._job["spec"]["template"]["spec"]["containers"].append(container)

        self._job_api = "https://api.useast1.cis.kuberbots.com/apis/batch/v1/namespaces/" + namespace + "/jobs"

    def __str__(self):
        return json.dumps(self._job, indent=4, sort_keys=True)

    def run(self):
        r = requests.post(self._job_api,
                json=self._job,
                headers = {'Authorization': 'Bearer ' + os.environ['TOKEN']},
                verify=False)
        print r.text



def run_job(c_opts):
    K8SJob("sample-work", c_opts).run()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Sample k8s job')
    parser.add_argument("-t", "--wait_time", default=5, type=int)
    parser.add_argument("-a", "--arg1", default="apple", )
    parser.add_argument("-b", "--arg2", default="banana")
    parser.add_argument("-f", "--fail", action='store_true', default=False)

    options = parser.parse_args()
    # Convert container options to a list
    c_opts = [
        "/usr/bin/python",
        "/worker.py"
        ]
    c_opts.append("-a")
    c_opts.append(options.arg1)
    c_opts.append("-b")
    c_opts.append(options.arg2)
    c_opts.append("-t")
    c_opts.append(str(options.wait_time))
    if options.fail == True:
        c_opts.append("-f")
    run_job(c_opts)

