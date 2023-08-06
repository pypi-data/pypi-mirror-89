# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['django_cloudtask',
 'django_cloudtask.management',
 'django_cloudtask.management.commands']

package_data = \
{'': ['*']}

install_requires = \
['django-structlog>=1.5.2,<2.0.0',
 'django>=2.2.12,<3.0.0',
 'google-api-core>=1.14.2,<2.0.0',
 'google-cloud-scheduler>=1.3.0,<2.0.0',
 'google-cloud-tasks>=1.5.0,<2.0.0',
 'structlog>=20.1.0,<21.0.0']

setup_kwargs = {
    'name': 'django-cloudtask',
    'version': '0.1.5',
    'description': 'A django package for managing long running tasks using GCP Cloud Task',
    'long_description': '# django-cloudtask\nA django package for managing long running tasks via Cloud Run and Cloud Scheduler\n\n[![CircleCI](https://circleci.com/gh/kogan/django-cloudtask.svg?style=svg)](https://circleci.com/gh/kogan/django-cloudtask)\n\n## Should I be using this package?\n\nNot yet - we\'re still trying to make this package usable by the general public.\n\nThere are a lot of assumptions being made that might not be suitable for your project.\n\n\n## Usage\n\n### Setup\n\ninclude `django_cloudtask` in your installed apps.\n\n### Configuration\n\nMake sure these are in your django settings:\n\n - `PROJECT_ID`\n   - the GCP project\n - `PROJECT_REGION`\n   - GCP region\n - `TASK_SERVICE_ACCOUNT`\n   - Service account which will be authenticated against\n - `TASK_DOMAIN`\n   - domain which receives tasks (cloud run)\n - `TASK_DEFAULT_QUEUE`\n   - default queue tasks will be added to\n\n### Defining a task\n\nTasks __must__ be defined in a file called `tasks.py` at the root level of an app directory.\n\ne.g.,\n\n```\nmy-project/\n  app/\n    tasks.py\n    urls.py\n    views.py\n  manage.py\n  settings.py\n\n```\n\nTasks are defined using the `@register_task` decorator.\n\n```\n@register_task(should_retry: bool, queue: str, schedule: str)\n```\n\n`:should_retry:` Will retry the task if there was an uncaught exception\n\n`:queue:` What Queue this task belongs to (Queues are set up in GCP)\n\n`:schedule:` Cron-like string defining when this task should be executed\n\nNote: a scheduled task cannot have any arguments (but can have kwargs with defaults).\n\ne.g.,\n\n```\nfrom django_cloudtask import register_task\n\n@register_task\ndef my_task(some, args, kwarg=False):\n   ...\n\n@register_task(schedule="0 5 * * *")\ndef scheduled_task():\n    ...\n\n```\n\n### Calling a task\n\nTasks may be scheduled by calling `enqueue(*args, **kwargs)`.\n\n`args` and `kwargs` must be JSON serialisable.\n\nTasks may also be called directly which will execute in the current call stack.\n\ne.g.,\n\n```\n# execute asynchronously\nmy_task.enqueue(1, "start the task", kwarg=True)\n\n\n# execute immediately\nscheduled_task()\n```\n\n\n## Contributing\n\nWe use `pre-commit <https://pre-commit.com/>` to enforce our code style rules\nlocally before you commit them into git. Once you install the pre-commit library\n(locally via pip is fine), just install the hooks::\n\n    pre-commit install -f --install-hooks\n\nThe same checks are executed on the build server, so skipping the local linting\n(with `git commit --no-verify`) will only result in a failed test build.\n\nCurrent style checking tools:\n\n- flake8: python linting\n- isort: python import sorting\n- black: python code formatting\n\nNote:\n\n    You must have python3.6 available on your path, as it is required for some\n    of the hooks.\n',
    'author': 'Alec McGavin',
    'author_email': 'alec.mcgavin@kogan.com.au',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://github.com/kogan/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
