from django.shortcuts import render

DEMO_SIZES = [
	('324', '104'),				
	('500', '160'),
	('355', '190'),
	('618', '298'),
	('322', '114'),
	('138', '138'),
	('640', '360'),
	('500', '400'),	
	('640', '640'),
	('500', '500'),
	('640', '470'),	
	('1536', '1000'),
	('500', '266'),	
	('256', '336')
]

def demo(request, asset_id):

	specified_x = request.GET.get('width', DEMO_SIZES[0][0])
	specified_y = request.GET.get('height', DEMO_SIZES[0][1])
	ctxt = {
			'x': specified_x,
			'y': specified_y,
			'dims': DEMO_SIZES,
			'asset_id': asset_id
		}
	return render(request, 'demo/demo.html', ctxt)


 
