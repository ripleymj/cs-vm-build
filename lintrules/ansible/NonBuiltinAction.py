"""
This checks whether an action being used is not a builtin action. This has
become far easier to check in newer versions of Ansible.
"""

from typing import Any, Dict, Union, Optional

from ansiblelint.rules import AnsibleLintRule
from ansiblelint.file_utils import Lintable

# Theoretically, we should allow this to expand to other namespaces that we
# trust to be present in the target environment. Who knows what Ubuntu 22.04
# or newer Mint versions may include!
ALLOWED_NAMESPACES = ["ansible.builtin."]
ALLOWED_MATCHES = ["command", "shell"]


# This rule is somewhat based on the fqcn-builtins from upstream ansible-lint
class NonBuiltinAction(AnsibleLintRule):
    id = "non-builtin-action"
    description = "Check whether the action is in a builtin module"
    severity = "MEDIUM"
    tags = ["unpredictability"]

    def matchtask(
        self, task: Dict[str, Any], file: Optional[Lintable] = None
    ) -> Union[bool, str]:
        # __ansible_module__ may have been normalized to the shortname
        # instead of the original/fully-qualified name.
        action_name: str = task["action"]["__ansible_module_original__"]
        if action_name in ALLOWED_NAMESPACES:
            return False
        for allowed_namespace in ALLOWED_NAMESPACES:
            if action_name.startswith(allowed_namespace):
                return False
        return f"{action_name} is not builtin and may not always be available"
