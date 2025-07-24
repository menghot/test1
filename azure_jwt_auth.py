import requests
import jwt
from cryptography.hazmat.primitives import serialization
import json

tenant_id = 'xxxx'
client_id = 'xxxx'
client_secret = 'xxxxx'

token_endpoint = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token" 
data = {
      "grant_type": "client_credentials",
      "client_id": f"{client_id}",  
      "client_secret": f"{client_secret}",  
      "scope": "api://your-client-id/.default"
    }
response = requests.post(token_endpoint, data=data)
access_token = response.json()["access_token"]
print(access_token)

response1 = requests.get("https://login.microsoftonline.com/fb134080-e4d2-45f4-9562-f3a0c218f3b0/discovery/keys")
keys = response1.json()['keys']

token_headers = jwt.get_unverified_header(response.json()['access_token'])
token_alg = token_headers['alg']
token_kid = token_headers['kid']
public_key = None
for key in keys:
     if key['kid'] == token_kid:
         public_key = key 


rsa_pem_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(public_key))
rsa_pem_key_bytes = rsa_pem_key.public_bytes(
    encoding=serialization.Encoding.PEM, 
    format=serialization.PublicFormat.SubjectPublicKeyInfo
) 


decoded_token = jwt.decode(
    response.json()['access_token'], 
    key=rsa_pem_key_bytes,
    verify=True,
    options={"verify_signature": True},
    algorithms=['RS256'],
    audience="api://client_id",
    issuer="https://sts.windows.net/tenant_id/"
)
s = json.dumps(decoded_token)
q = json.dumps(json.loads(s), indent=2)
print(q)
