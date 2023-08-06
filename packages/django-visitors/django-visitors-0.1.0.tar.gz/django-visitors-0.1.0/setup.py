# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['visitors', 'visitors.migrations']

package_data = \
{'': ['*']}

install_requires = \
['django>=3.0,<4.0']

setup_kwargs = {
    'name': 'django-visitors',
    'version': '0.1.0',
    'description': "Django support for 'visitors' - who are neither anonymous nor authenticated.",
    'long_description': '# Django Visitors\n\nDjango app for managing temporary session-based users.\n\n### Background\n\nThis package has been extracted out of `django-request-token` as a specific use\ncase - that of temporary site "visitors". It enables a type of ephemeral user\nwho is neither anonymous nor authenticated, but somewhere in between - known for\nthe duration of their session.\n\n### Motivation\n\nWe\'ve been using `django-request-token` for a while, and have issued over\n100,000 tokens. A recent analysis showed two main use cases - single-use "magic\nlinks" for logging people in, and a more involved case where we invite\nunregistered users on to the platform to perform some action - providing a\nreference perhaps, or collaborating on something with (registered) users. The\nformer we have extracted out into `django-magic-links` - and this package\naddresses the latter.\n\n### What is a "visitor"?\n\nIn the standard Django model you have the concept of an `AnonymousUser`, and an\nauthenticated `User` - someone who has logged in. We have a third, intermediate,\ntype of user - which we have historically referred to as a "Temp User", which is\nsomeone we know _of_, but who has not yet registered.\n\nThe canonical example of this is leaving a reference: user A on the site invites\nuser B to leave a reference for them. They (A) give us B\'s name and email, we\ninvite them to click on a link and fill out a form. That\'s it. We store their\nname and email so that we can contact them, but it\'s ephemeral - we don\'t need\nit, and we don\'t use it. Storing this data in the User table made sense (as it\nhas name and email fields), but it led to a lot of `user_type=TEMP` munging to\ndetermine who is a \'real\' user on the site.\n\nWhat we really want is to \'stash\' this information somewhere outside of the auth\nsystem, and to enable these temp users to have restricted access to specific\nareas of the application, for a limited period, after which we can forget about\nthem and clear out the data.\n\nWe call these users "visitors".\n\n### Use Case - request a reference\n\nFred is a registered user on the site, and would like a reference from Ginger,\nhis dance partner.\n\n1. Fred fills out the reference request form:\n\n```\n   Name: Ginger\n   Email: ginger@[...].com\n   Message: ...\n   Scope: REFERENCE_REQUEST [hidden field]\n```\n\n2. We save this information, and generate a unique link which we send to Ginger,\n   along with the message.\n\n3. Ginger clicks on the link, at which point we recognise that this is someone\n   we know about - a "visitor" - but who is in all other respects an\n   `AnonymousUser`.\n\n4. We stash the visitor info in the standard session object - so that even\n   though Ginger is not authenticated, we know who she is, and more importantly\n   we know why she\'s here (REFERENCE_REQUEST).\n\n5. Ginger submits the reference - which may be a multi-step process, involving\n   GETs and POSTs, all of which are guarded by a decorator that restricts access\n   to visitors with the appropriate Scope (just like `django-request-token`).\n\n6. At the final step we can (optionally) choose to clear the session info\n   immediately, effectively removing all further access.\n\n### Implementation\n\nThis code has been extracted out of `django-request-token` and simplified. It\nstores the visitor data in the `Visitor` model, and on each successful first\nrequest (where the token is \'processed\' and the session filled) we record a\n`VisitorLog` record. This includes HTTP request info (session_key, referer,\nclient IP, user-agent). This information is for analytics only - for instance\ndetermining whether links are being shared.\n\n#### Configuration\n\n1. Add `visitors` to `INSTALLED_APPS`\n1. Add `visitors.middleware.VisitorRequestMiddleware` to `MIDDLEWARE`\n1. Add `visitors.middleware.VisitorSessionMiddleware` to `MIDDLEWARE`\n\n#### Settings\n\n* `VISITOR_SESSION_KEY`: session key used to stash visitor info\n  ("visitor:session")\n\n* `VISITOR_QUERYSTRING_KEY`: querystring param used on tokenised links ("vid")\n',
    'author': 'YunoJuno',
    'author_email': 'code@yunojuno.com',
    'maintainer': 'YunoJuno',
    'maintainer_email': 'code@yunojuno.com',
    'url': 'https://github.com/yunojuno/django-visitors',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
