BUSINESS_TYPE_CHOICES = ( #from https://developer.paypal.com/docs/classic/adaptive-accounts/integration-guide/ACBusinessCategories/
		('0000','---'),
		('1000','Arts, crafts, and collectibles'),
		('1001','Baby'),
		('1002','Beauty and fragrances'),
		('1003','Books and magazines'),
		('1004','Business to business'),
		('1005','Clothing, accessories, and shoes'),
		('1006','Computers, accessories, and services'),
		('1007','Education'),
		('1008','Electronics and telecom'),
		('1009','Entertainment and media'),
		('1010','Financial services and products'),
		('1011','Food retail and service'),
		('1012','Gifts and flowers'),
		('1013','Government'),
		('1014','Health and personal care'),
		('1015','Home and garden'),
		('1016','Nonprofit'),
		('1017','Pets and animals'),
		('1018','Religion and spirituality (for profit)'),
		('1019','Retail (not elsewhere classified)'),
		('1020','Services - other'),
		('1021','Sports and outdoors'),
		('1022','Toys and hobbies'),
		('1023','Travel'),
		('1024','Vehicle sales'),
		('1025','Vehicle service and accessories.'),
	)

BUSINESS_TYPE_DICT = {entry[0]:entry[1] for entry in BUSINESS_TYPE_CHOICES}
REVERSE_BUSINESS_TYPE_DICT = {entry[1]:entry[0] for entry in BUSINESS_TYPE_CHOICES}

STATE_CHOICES = (
		('00','---'),
		('AL','Alabama'),
		('AK','Alaska'),
		('AZ','Arizona'),
		('AR','Arkansas'),
		('CA','California'),
		('CO','Colorado'),
		('CT','Connecticut'),
		('DE','Delware'),
		('FL','Florida'),
		('GA','Georgia'),
		('HI','Hawaii'),
		('ID','Idaho'),
		('IL','Illinois'),
		('IN','Indiana'),
		('IA','Iowa'),
		('KS','Kansas'),
		('KY','Kentucky'),
		('LA','Louisiana'),
		('ME','Maine'),
		('MD','Maryland'),
		('MA','Massachusetts'),
		('MI','Michigan'),
		('MN','Montana'),
		('MS','Mississippi'),
		('MO','Missouri'),
		('MT','Montana'),
		('NE','Nebraska'),
		('NV','Nevada'),
		('NH','New Hampshire'),
		('NJ','New Jersey'),
		('NM','New Mexico'),
		('NY','New York'),
		('NC','North Carolina'),
		('ND','North Dakota'),
		('OH','Ohio'),
		('OK','Oklahoma'),
		('OR','Oregon'),
		('PA','Pennsylvania'),
		('RI','Rhode Island'),
		('SC','South Carolina'),
		('SD','South Dakota'),
		('TN','Tennesee'),
		('TX','Texas'),
		('UT','Utah'),
		('VT','Vermont'),
		('VA','Virginia'),
		('WA','Washington'),
		('WV','West Viginia'),
		('WI','Wisconsin'),
		('WY','Wyoming'),
	)

STATE_DICT = {entry[0]:entry[1] for entry in STATE_CHOICES}
REVERSE_STATE_DICT = {entry[1]:entry[0] for entry in STATE_CHOICES}
