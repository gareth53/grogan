__Grogan__

A proof-of-concept Asset Manager replacement.
In order to achieve the following goals:

- fewer crops and less overhead for editors
- Auto-cropping to facilitate easier RWD adn easier migration of services

__Setup Steps__

- virtualenv --no-site-packages venv
- venv/bin/pip install -r requirements.txt
- venv/bin/python grogan/manage.py runserver

__Creating A User Via The Shell___

from django.contrib.auth.models import User
u = User.objects.create_user(username='gareth')
u.is_superuser = True
u.is_staff = True
u.set_password('password')
u.save() 

__Creating a SuperUser Management Command___

python manage.py createsuperuser --username=gareth --email=gareth53@gmail.com

__Development Tasks for Basic POC__

- basic models
- basic admin
- custom admin to create crops
- fixtures for crop sizes
- dynamic crop logic
- API Endpoint
- Gusto Editorial Assets admin demo
- Front end RWD Demo

API call specifies a width and a height. Logic uses existing crops to figure out how best to do that crop to satisfy the dimensions supplied.

It selects the best crop based on size and ratios.
Then uses the centre point of the nearest crop for its centre point reference.
If that means a crop with bleed it may re position to fit within the image boundaries
If that still means bleed it may adjust the zoom.

__Feature Backlog__

- Better List View for Assets
- Custom admin widgets for metadata
- import sample metadata from Asset Manager
- Simple search 
- Advanced Search
- Admin Flow
	- Upload image (custom admin view)
	- Edit main model details
	- Do crops (custom admin view)

__Areas For Further Thought & Definition__

This works OK for editorial assets, and for RWD and for retina images. But how does this work for galleries?