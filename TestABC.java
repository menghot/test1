package io.trino.plugin.example;

import com.nimbusds.jose.jwk.source.JWKSource;
import com.nimbusds.jose.jwk.source.ImmutableJWKSet;
import com.nimbusds.jose.jwk.JWKSet;
import com.nimbusds.jose.proc.SecurityContext;
import com.nimbusds.jwt.proc.DefaultJWTProcessor;
import com.nimbusds.jwt.proc.ConfigurableJWTProcessor;
import com.nimbusds.jwt.SignedJWT;
import com.nimbusds.jwt.JWTClaimsSet;
import com.nimbusds.jose.proc.JWSKeySelector;
import com.nimbusds.jose.proc.JWSVerificationKeySelector;
import com.nimbusds.jose.JWSAlgorithm;

import java.text.ParseException;
import java.util.Date;
import java.io.IOException;

public class TestABC {

    public static void main(String[] args) throws Exception {
        String token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..."
                + ".<payload>.<signature>";

        String jwksJson = "{ \"keys\": [ { \"kty\": \"RSA\", \"kid\": \"abc123\", \"use\": \"sig\", \"n\": \"...\", \"e\": \"AQAB\" } ] }";

        // Step 1: Parse JWKS
        JWKSet jwkSet = JWKSet.parse(jwksJson);
        JWKSource<SecurityContext> jwkSource = new ImmutableJWKSet<>(jwkSet);

        // Step 2: Set up JWT Processor
        ConfigurableJWTProcessor<SecurityContext> jwtProcessor = new DefaultJWTProcessor<>();

        // Assume RS256 algorithm (adapt to your JWT if different)
        JWSKeySelector<SecurityContext> keySelector =
                new JWSVerificationKeySelector<>(JWSAlgorithm.RS256, jwkSource);

        jwtProcessor.setJWSKeySelector(keySelector);

        // Step 3: Process the JWT
        SecurityContext ctx = null; // no specific context needed
        JWTClaimsSet claimsSet = jwtProcessor.process(token, ctx);

        // Step 4: Access claims (and optionally check expiration, issuer, etc.)
        System.out.println("Subject: " + claimsSet.getSubject());
        System.out.println("Issuer: " + claimsSet.getIssuer());
        System.out.println("Expiration Time: " + claimsSet.getExpirationTime());

        if (claimsSet.getExpirationTime().before(new Date())) {
            System.out.println("Token is expired.");
        } else {
            System.out.println("Token is valid.");
        }
    }
}
