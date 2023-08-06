from datetime import datetime

from sceptre.stack import Stack

from hook.hook import CustomHook

stack = Stack(
    name="test/stack.yaml",
    project_code="test",
    template_path="template/path",
    region="coin-central-1"
)


def test_invoke_lambda():
    start_test = datetime.utcnow()

    def intercept_invoke_lambda(payload):
        assert payload["method"] == "deploy_start"
        assert payload["stack_name"] == "test/stack.yaml"
        time = datetime.fromisoformat(payload["time"])
        assert start_test < time < datetime.utcnow()
    hook = CustomHook("deploy_start", stack)
    hook._invoke_lambda = intercept_invoke_lambda
    hook.run()
