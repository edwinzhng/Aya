#!/usr/bin/python
import http.client, urllib.request, urllib.parse, urllib.error, base64, json
from azure.storage.blob import BlockBlobService, ContentSettings

with open('key', 'rb') as f:
    subscription_key, account_key = f.readline().split()
block_blob_service = BlockBlobService(account_name='ayastore', account_key=account_key)
uri_base = 'westus.api.cognitive.microsoft.com'
headers = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': subscription_key,
}
params = urllib.parse.urlencode({
    'language': 'en',
})

block_blob_service.create_blob_from_path('aya', 'image', 'test.jpg',
        content_settings=ContentSettings(content_type='image/jpg'))
body = "{'url':'https://ayastore.blob.core.windows.net/aya/image'}"

try:
    conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/vision/v1.0/describe?%s" % params, body, headers)
    response = conn.getresponse()
    data = response.read()

    parsed = json.loads(data)
    print ("Response:")
    print (json.dumps(parsed, sort_keys=True, indent=2))
    conn.close()

except Exception as e:
    print('Error:')
    print(e)

block_blob_service.delete_blob('aya', 'image')
