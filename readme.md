__Grogan__

A proof-of-contept Asset Manager replacement.
In order to achieve the following goals:

# fewer crops and less overhead for editors
# Auto-cropping to facilitate easier RWD adn easier migration of services


__Setup Steps__

virtualenv --no-site-packages venv
venv/bin/pip install -r requirements.txt
venv/bin/python grogan/manage.py runserver


__Development Tasks for Basic POC___

- basic models
- basic admin


- 'Crop' Model
-- Asset FK
-- Width
-- Height
-- Zoom
-- Ratio

(Or whatever is needed for Pillow to rezies and crop on the fly)

- Editorial Assets admin demo
- Front end RWD Demo
- API Endpoint

API call specifies a width and a height
Logic uses existing crops to figure out how best to do that crop to satisfy the dimensions supplied

It slects the best crop based on size and ratios.
The uses the centre point of the nearest crop for its centre point reference.

If that means a crop with bleed it may re position to fit within the image boundaries

If that still means bleed it may adjust the zoom.


__Tasks For 'Showboating' Development__

- Better List View for Assets
- Custom admin widgets for metadata
- Simple search 
- Advanced Search


__Areas For Further Thought & Definition__

This works OK for editorial assets... And for RWD and for retina images.

How does this work for galleries?

