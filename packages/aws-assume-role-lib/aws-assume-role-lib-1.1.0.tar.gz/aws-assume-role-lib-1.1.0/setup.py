# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['aws_assume_role_lib']
install_requires = \
['boto3>=1.13.0,<2.0.0']

setup_kwargs = {
    'name': 'aws-assume-role-lib',
    'version': '1.1.0',
    'description': 'Assumed role session chaining (with credential refreshing) for boto3',
    'long_description': '# aws-assume-role-lib\n**Assumed role session chaining (with credential refreshing) for boto3**\n\nThe typical way to use boto3 when programmatically assuming a role is to explicitly call [`sts.AssumeRole`](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sts.html#STS.Client.assume_role) and use the returned credentials to create a new [`boto3.Session`](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/session.html).\nHowever, these credentials expire, and the code must explicitly handle this situation (e.g., in a Lambda function, calling `AssumeRole` in every invocation).\n\nWith `aws-assume-role-lib`, you can easily create assumed role sessions from parent sessions that automatically refresh expired credentials.\n\nIn a Lambda function that needs to assume a role, you can create the assumed role session during initialization and use it for the lifetime of the execution environment.\n\nNote that in `~/.aws/config`, [you have the option to have profiles that assume a role based on another profile](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-role.html), and this automatically handles refreshing expired credentials as well.\n\n# Installation\n\n```bash\npip install --user aws-assume-role-lib\n```\n\nOr just add [`aws_assume_role_lib.py`](https://raw.githubusercontent.com/benkehoe/aws-assume-role-lib/main/aws_assume_role_lib.py) to your project.\n\n# Usage\n\n```python\nimport boto3\nfrom aws_assume_role_lib import assume_role\n\n# Get a session\nsession = boto3.Session()\n# or with a profile:\n# session = boto3.Session(profile_name="my-profile")\n\n# Assume the session\nassumed_role_session = assume_role(session, "arn:aws:iam::123456789012:role/MyRole")\n\nprint(assumed_role_session.client("sts").get_caller_identity()["Arn"])\n```\n\n`assume_role()` takes a session and a role ARN, and optionally [other keyword arguments for `sts.AssumeRole`](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sts.html#STS.Client.assume_role).\nUnlike the `AssumeRole` API call itself, `RoleArn` is required, but `RoleSessionName` is not; it\'s automatically generated if one is not provided.\nIf any new arguments are added to `AssumeRole` in the future, they can be passed in via the `additional_kwargs` argument.\n\nBy default, `assume_role()` checks if the parameters are invalid.\nWithout this validation, errors for these issues are more confusingly raised when the child session is first used to make an API call (boto3 does make the call to retrieve credentials until they are needed).\nHowever, this incurs a small time penalty, so parameter validation can be disabled by passing `validate=False`.\n\nThe parent session is available on the child session in the `assume_role_parent_session` property.\nNote this property is added by this library; ordinary boto3 sessions do not have it.\n\nIf you would like to cache the credentials on the file system, you can use the `JSONFileCache` class, which will create files under the directory you provide in the constructor (which it will create if it doesn\'t exist).\nUse it like:\n```python\nassumed_role_session = assume_role(session, "arn:aws:iam::123456789012:role/MyRole", cache=JSONFileCache("path/to/dir"))\n```\nYou can also use any `dict`-like object for the cache (supporting `__getitem__`/`__setitem__`/`__contains__`).\n',
    'author': 'Ben Kehoe',
    'author_email': 'ben@kehoe.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/benkehoe/aws-assume-role-lib',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
