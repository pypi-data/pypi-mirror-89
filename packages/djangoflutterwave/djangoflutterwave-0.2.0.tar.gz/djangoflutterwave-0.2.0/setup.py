# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['djangoflutterwave',
 'djangoflutterwave.migrations',
 'djangoflutterwave.templatetags',
 'djangoflutterwave.tests']

package_data = \
{'': ['*'],
 'djangoflutterwave': ['static/djangoflutterwave/js/*',
                       'templates/djangoflutterwave/*']}

install_requires = \
['django>=2.2,<4', 'djangorestframework>=3.10,<4.0', 'requests>=2.22,<3.0']

setup_kwargs = {
    'name': 'djangoflutterwave',
    'version': '0.2.0',
    'description': 'Django integration for Flutterwave payments and subscriptions',
    'long_description': '# Django Flutterwave\n\n## Project Description\n\nThis project provides Django integration for [Flutterwave](https://flutterwave.com/) payments and subscriptions.\n\nCurrent functionality:\n- Allow users to make payments (once off and subscription)\n- Create payment buttons which launch inline payment modals\n- Maintain a payment transaction history linked to users\n\n# Requirements\n\n- Python >= 3.6\n- Django >= 2.0\n\n# Installation\n\n```bash\npip install djangoflutterwave\n```\n\n# Setup\n\nAdd `"djangoflutterwave"` to your `INSTALLED_APPS`\n\nRun Django migrations:\n\n```python\nmanage.py migrate\n```\n\nAdd the following to your `settings.py`:\n\n```python\nFLW_PRODUCTION_PUBLIC_KEY = "your key"\nFLW_PRODUCTION_SECRET_KEY = "your key"\nFLW_SANDBOX_PUBLIC_KEY = "your key"\nFLW_SANDBOX_SECRET_KEY = "your key"\nFLW_SANDBOX = True\n```\n\nThe above config will ensure `djangoflutterwave` uses your sandbox. Once you\'re ready to\ngo live, set `FLW_SANDBOX = False`\n\nAdd `djangoflutterwave` to your `urls.py`:\n\n```python\npath("djangoflutterwave/", include("djangoflutterwave.urls", namespace="djangoflutterwave"))\n```\n\nAdd the following url as a webhook in your Flutterwave dashboard. This will be used by\nFlutterwave to `POST` payment transactions to your site:\n\n```bash\nhttp://yoursite.com/djangoflutterwave/transaction/\n```\n\n`Note:` while in development, a tool like ngrok (or similar) may prove useful to ensure\nyour localhost is accessible to Flutterwave for the above webhook calls.\n\n# Usage\n\n`djangoflutterwave` provides two models, namely:\n\n- The `DRPlanModel` allows you to create `once off` or `subscription` plans. When creating a `subscription` plan, you will need to create the plan in Flutterwave first and then enter the corresonding information as a `DRPlanModel` instance (ie: `flw_plan_id` field corresponds to the Flutterwave `Plan ID`).\n- The `DRTransactionModel` creates transactions when Flutterwave POSTS to the above mentioned webhook url. This provides a history of all transactions (once off or recurring), linked to the relevant `DRPlanModel` and `user`.\n\nA payment button can be created as follows:\n\n1. Create a new plan (ie: `DRPlanModel`) using the django admin.\n2. In the view where you wish the button to appear, add the above created `DRPlanModel` instance to your context, eg:\n\n```python\nfrom djangoflutterwave.models import DRPlanModel\n\nclass SignUpView(TemplateView):\n    """Sign Up view"""\n\n    template_name = "my_payment_template.html"\n\n    def get_context_data(self, **kwargs):\n        """Add payment type to context data"""\n        kwargs = super().get_context_data(**kwargs)\n        kwargs["pro_plan"] = DRPlanModel.objects.filter(\n            name="Pro Plan"\n        ).first()\n        return kwargs\n```\n\n3. In your template, add the button wherever you wish for it to appear as follows:\n\n```python\n{% include \'djangoflutterwave/pay_button.html\' with plan=pro_plan %}\n```\n\n`Note:` You can add multiple buttons to a single template by simply adding multiple\nplans to your context data and then including each of them with their own `include`\ntag as above.\n\n4. Add the following to your django base template (or anywhere in your template heirarchy that ensures it is loaded before your payment buttons):\n\n```html\n<script type="text/javascript" src="https://checkout.flutterwave.com/v3.js"></script>\n<script src="{% static \'djangoflutterwave/js/payment.js\' %}"></script>\n```\n\n# Button Styling\n\nUse the `pay_button_css_classes` field on the `DRPlanModel` model to add css classes to\nbuttons which will be rendered in your template.\n\n# Transaction Detail Page\n\nFollowing a user payment, they will be redirected to the transaction detail page\nlocated at `/djangoflutterwave/<str:tx_ref>/`.\n\nA default transaction detail template is already available, however if you want\nto override it, you may do so by creating a new template in your root\ntemplates directory, ie: `/templates/djangoflutterwave/transaction.html`\n\nYou will have access to `{{ transaction }}` within that template.\n\n# Development and contribution\n\nIf you wish to contribute to the project, there is an example app that demonstrates\ngeneral usage.\n\n### Running the example:\n\n```bash\ngit clone https://github.com/bdelate/django-flutterwave.git\ncd django-flutterwave\n```\n\nCreate file `example/env/dev.env` and populate it with the following:\n\n```bash\nFLW_SANDBOX_PUBLIC_KEY=your_sandbox_public_key\nFLW_SANDBOX_SECRET_KEY=your_sandbox_secret_key\nFLW_PRODUCTION_PUBLIC_KEY=test\nFLW_PRODUCTION_SECRET_KEY=test\n```\n\nRun the following commands:\n\n```bash\nmake build\nmake migrate\nmake import\nmake dup\n```\n\nFlutterwave requires payments to be associated with users who have an email address.\nTherefore, create and login with a new django user or use the existing user which will\nhave been created by the above import command:\n\n```\nusername: admin\npassword: adminadmin\n```\n\nNavigate to http://localhost:8000/',
    'author': 'Brendon Delate',
    'author_email': 'brendon.delate@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bdelate/django-flutterwave.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4',
}


setup(**setup_kwargs)
