# test1
#openssl genrsa -out ca.key 2048
#openssl req -new -x509 -days 3650 -key ca.key -subj "/C=CN/ST=GD/L=SZ/O=SC, Inc./CN=SC Root CA" -out ca.crt
#openssl x509 -req -extfile <(printf "subjectAltName=DNS:example.com,DNS:www.example.com") -days 720 -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt



openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/C=US/ST=State/L=City/O=Organization/OU=OrgUnit/CN=example.com"



openssl req -newkey rsa:2048 -nodes -keyout server.key -subj "/C=CN/ST=GD/L=SZ/O=MGG, Inc./CN=*.mgg.co" -out server.csr


openssl req -newkey rsa:2048 -nodes -keyout server.key -subj "/C=CN/ST=GD/L=SZ/O=MGG, Inc./CN=*.mgg.co" -out server.csr
openssl x509 -req -extfile <(printf "subjectAltName=DNS:*.sk.co") -days 365 -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt
kubectl create secret tls ingress-ssl3--key server.key --cert server.crt -nkube-system
================================
