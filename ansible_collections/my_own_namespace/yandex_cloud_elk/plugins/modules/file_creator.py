#!/usr/bin/python
# Copyright: (c) 2024, Chehlov1M <chehlov1m@example.com>
# GNU General Public License v3.0+
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: file_creator
short_description: Creates a text file with given content on the target host
description:
  - Creates a file at a specified path with provided content.
  - Supports idempotency: if the file exists and content matches, changed=false.
options:
  path:
    description: Path to the file to create.
    required: true
    type: str
  content:
    description: Content to write into the file.
    required: true
    type: str
author:
  - Chehlov1M (@Chehlov1M)
'''

EXAMPLES = r'''
- name: Create a file with content
  file_creator:
    path: /tmp/hello.txt
    content: "Hello from my custom module!"
'''

RETURN = r'''
original_path:
  description: The path passed to the module.
  type: str
  returned: always
  sample: "/tmp/hello.txt"
original_content:
  description: The content passed to the module.
  type: str
  returned: always
  sample: "Hello from my custom module!"
changed:
  description: Whether the file was created or updated.
  type: bool
  returned: always
  sample: true
'''

from ansible.module_utils.basic import AnsibleModule
import os

def run_module():
    module_args = dict(
        path=dict(type='str', required=True),
        content=dict(type='str', required=True),
    )

    result = dict(
        changed=False,
        original_path='',
        original_content='',
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    path = module.params['path']
    content = module.params['content']

    result['original_path'] = path
    result['original_content'] = content

    if module.check_mode:
        if os.path.exists(path):
            with open(path, 'r') as f:
                existing = f.read()
            result['changed'] = (existing != content)
        else:
            result['changed'] = True
        module.exit_json(**result)

    file_exists = os.path.exists(path)
    if file_exists:
        with open(path, 'r') as f:
            existing_content = f.read()
        if existing_content == content:
            module.exit_json(**result)

    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write(content)
        result['changed'] = True
    except Exception as e:
        module.fail_json(msg=f"Failed to write file: {e}", **result)

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
