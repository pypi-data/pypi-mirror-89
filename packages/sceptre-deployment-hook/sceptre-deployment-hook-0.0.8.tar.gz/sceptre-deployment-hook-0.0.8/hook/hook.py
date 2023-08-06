from datetime import datetime
from sceptre.hooks import Hook
import boto3
import subprocess
import json

from typing import List


class CustomHook(Hook):
    def __init__(self, *args, **kwargs):
        super(CustomHook, self).__init__(*args, **kwargs)

    def run(self):
        """
        run is the method called by Sceptre. It should carry out the work
        intended by this hook.
        """
        # self.argument == "deploy_start" || "deploy_end"
        print(self.argument)
        try:
            self.lambda_handler(self.argument)
        except:
            # just ignore any error for now
            pass

    def lambda_handler(self, method: str) -> None:
        invoke_lambda = boto3.client("lambda", region_name="eu-central-1")
        payload = {
            "method": method,
            "git_commit_message": self._get_last_git_commit_message(),
            "git_branch_name": self._get_git_branch_name(),
            "stack_name": self.stack.name,
            "time": datetime.utcnow().isoformat()
        }
        resp = invoke_lambda.invoke(
            FunctionName="arn:aws:lambda:eu-central-1:521248050649:function:sceptre-lifecycle-provider-vpc-cad5d5a2",
            InvocationType="RequestResponse", Payload=json.dumps(payload))
        print(resp.read())

    def _get_last_git_commit_message(self) -> str:
        return self._get_output_subprocess(["git", "log", "-1"])

    def _get_git_branch_name(self) -> str:
        return self._get_output_subprocess(["git", "branch", "--show-current"])

    @staticmethod
    def _get_output_subprocess(command: List[str]) -> str:
        return subprocess.run(command, capture_output=True).stdout.decode("utf-8")
