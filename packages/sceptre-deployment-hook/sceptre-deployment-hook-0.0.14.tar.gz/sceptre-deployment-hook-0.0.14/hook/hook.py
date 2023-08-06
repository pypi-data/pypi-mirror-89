import inspect
import os
from datetime import datetime

from sceptre.hooks import Hook
import subprocess
import json
from typing import List

from sceptre.plan.actions import StackActions


class CustomHook(Hook):
    def __init__(self, *args, **kwargs):
        super(CustomHook, self).__init__(*args, **kwargs)

    def run(self):
        """
        run is the method called by Sceptre. It should carry out the work
        intended by this hook.
        """
        # self.argument == "deploy_start" || "deploy_end"
        try:
            stack = self._get_stack()
            self.lambda_handler(self.argument, stack)
        except AssertionError:
            raise
        except Exception as e:
            print(e)
            # just ignore all other errors for now
            pass

    def lambda_handler(self, method: str, stack) -> None:
        payload = {
            "method": method,
            "git_commit_message": self._get_last_git_commit_message(),
            "git_branch_name": self._get_git_branch_name(),
            "stack_name": stack.name,
            "ci_job_id": self._get_job_id(),
            "time": datetime.utcnow().isoformat()
        }
        self._invoke_lambda(payload)

    def _get_last_git_commit_message(self) -> str:
        return self._get_output_subprocess(["git", "log", "-1"])

    def _invoke_lambda(self, payload: dict) -> None:
        self.stack.connection_manager.call(
            "lambda",
            "invoke",
            kwargs={
                "FunctionName": "arn:aws:lambda:eu-central-1:521248050649:function:sceptre-lifecycle-provider-vpc-cad5d5a2",
                "InvocationType": "RequestResponse",
                "Payload": json.dumps(payload)
            },
            region="eu-central-1"
        )

    def _get_git_branch_name(self) -> str:
        return self._getenv("CI_COMMIT_BRANCH")

    def _get_job_id(self) -> str:
        return self._getenv("CI_JOB_ID")

    @staticmethod
    def _get_stack():
        #  Get reference to 'decorated' function in call stack. This is where sceptre hooks are applied.
        #  Moreover, the 'decorated' function has a reference to StackActions containing the correct Stack-instance.
        #  The 'self.stack' in this object is not necessarily the right Stack.
        fr = next(stack for stack in inspect.stack() if stack.function == 'decorated')[0]
        args, _, _, value_dict = inspect.getargvalues(fr)
        instance = value_dict.get('self', None) if len(args) and args[0] == 'self' else None
        return instance.stack if isinstance(instance, StackActions) else None

    @staticmethod
    def _getenv(key) -> str:
        return os.getenv(key, "")

    @staticmethod
    def _get_output_subprocess(command: List[str]) -> str:
        return subprocess.run(command, capture_output=True).stdout.decode("utf-8")
