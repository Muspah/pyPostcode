from pyPostcode import Api

postcodeapi = Api('{YOUR_API_KEY}')
result = postcodeapi.getaddress('1011AC', 154)  # use address search

print(result.street)
print(result.house_number)
print(result.postcode)
print(result.town)
print(result.municipality)
print(result.province)
