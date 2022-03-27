"""
It is necessary for mode permissions to either be strings or octal literal
values in Ansible. Since we get an already-parsed file, detecting a leading
zero for octal literals is harder than ensuring that we have a string value.
This check helps ensure consistency in permissions.
"""

from typing import Any, Dict, Union, Optional

from ansiblelint.rules import AnsibleLintRule
from ansiblelint.file_utils import Lintable


class ModeIsString(AnsibleLintRule):
    id = "mode-is-string"
    description = "File and directory modes must be strings"
    severity = "MEDIUM"
    tags = ["idiom", "unpredictability"]

    def matchtask(
        self, task: Dict[str, Any], file: Optional[Lintable] = None
    ) -> Union[bool, str]:
        # Tasks without a mode should not be matched
        if "action" not in task:
            return False

        invalid_mode_keys = []
        # There are various mode-like keys, including "mode" and
        # "directory_mode"
        for key, value in task["action"].items():
            if key.endswith("mode") and not isinstance(value, str):
                invalid_mode_keys.append(key)

        if not invalid_mode_keys:
            return False

        return f"The value for {invalid_mode_keys} must be a string"
