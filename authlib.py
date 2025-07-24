import json
import base64
from authlib.jose import JsonWebToken, jwk
from authlib.jose.errors import JoseError

# JWT token (replace with your actual token)
token = (
    "eyJhbGciOiJSUzI1NiIsImtpZCI6InRlc3Qta2V5In0."
    "eyJzdWIiOiJ1c2VyMSIsImV4cCI6MjUwMDAwMDAwMH0."
    "SflKx..."
)

# JWKS JSON string (replace with your actual JWK values)
jwks_json_str = '''
{
  "keys": [
    {
      "kty": "RSA",
      "kid": "test-key",
      "use": "sig",
      "alg": "RS256",
      "n": "sXchxwNJ_m6o_HU3W4pNqYaEZPY9cs9kE-GRKsl2G1MgL3n4Dtrdy_gkPgZThnN_LWjzCPVnzPZuwM3bRjF84gG0q7bzTYZ3p8Q6MkHrqUciN8F9lH6CRr5Md5EkRVSmnnDqogBZk0NbyOvJK4G9h5dxUYUwkkk_kTf-dt3AF7vU9h3FoHRgMIH8SHFqzvpyA3bviO1puALd7gEp_dknvKR_4Ajcwz5aYg7XJJzgU2xd0_MtUz77_y9Xj1ppxKpxyITRLEh-mJDwryH-tOexbXAw1IlZJ_hPf3gqWefr0AnBFZ-CQOs-j6GpADYVj9oObH0NZXW-ZTyyUAMU4fXqlQ",
      "e": "AQAB"
    }
  ]
}
'''

# Step 1: Parse JWKS JSON string
jwks = json.loads(jwks_json_str)

# Step 2: Decode JWT header (base64url decode the first part)
def decode_jwt_header(token):
    header_b64 = token.split('.')[0]
    # Add padding if necessary
    header_b64 += '=' * (-len(header_b64) % 4)
    header_json = base64.urlsafe_b64decode(header_b64).decode('utf-8')
    return json.loads(header_json)

header = decode_jwt_header(token)
kid = header.get('kid')

# Step 3: Find matching JWK
matching_jwk = next((k for k in jwks["keys"] if k["kid"] == kid), None)
if not matching_jwk:
    raise ValueError(f"No matching JWK found for kid: {kid}")

# Step 4: Load the JWK into a key object
key = jwk.loads(matching_jwk)

# Step 5: Decode and validate the token
jwt_obj = JsonWebToken([matching_jwk["alg"]])
try:
    claims = jwt_obj.decode(token, key)
    claims.validate()  # Optional: pass iss, aud, etc.
    print("✅ JWT is valid")
    print("Claims:", dict(claims))
except JoseError as e:
    print("❌ JWT verification failed:", e)
