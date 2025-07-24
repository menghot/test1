from authlib.jose import JsonWebToken
from authlib.jose.errors import JoseError
from authlib.jose import jwk
import json

# Example JWT token (replace this with your real token)
token = "eyJhbGciOiJSUzI1NiIsImtpZCI6InRlc3Qta2V5In0.eyJzdWIiOiJ1c2VyMSIsImV4cCI6MjUwMDAwMDAwMH0.SflKx..."

# JWKS JSON string (from your IDP or config)
jwks_json_str = '''

'''

# Step 1: Parse JWKS JSON string
jwks = json.loads(jwks_json_str)

# Step 2: Parse JWT header to get 'kid'
jwt_obj = JsonWebToken(["RS256"])
header = jwt_obj.decode_header(token)
kid = header.get("kid")

# Step 3: Find matching key
matching_jwk = next((k for k in jwks["keys"] if k["kid"] == kid), None)
if not matching_jwk:
    raise ValueError(f"No matching JWK for kid: {kid}")

# Step 4: Load the public key from JWK
key = jwk.loads(matching_jwk)

# Step 5: Verify the token
try:
    claims = jwt_obj.decode(token, key)
    claims.validate()  # Optional: add issuer, audience, exp checks
    print("✅ Token is valid.")
    print("Claims:", claims)
except JoseError as e:
    print("❌ Token verification failed:", str(e))
