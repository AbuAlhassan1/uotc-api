import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth

config = {
  "type": "service_account",
  "project_id": "uotc-4c343",
  "private_key_id": "2c9f1e203a69aabc9a02b3bd2afc69cdf64d573f",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCTrTZo9ZQFUYxB\npZ3kUsco5hiRJ13SyZbP2g+9YgOOBOM7bYw71QLAeIjwicLwwO7LITFILqJ6m4EB\nKeKfMSgEM6RqPoS+YqAEHlc00VnnLuw0qCS91kO9B0ALy058LuyZOa1QjRwTbwrp\nUNk0hKDpt4vs8oZItc10ZlkAzBeH8nP2V2tIteqGZnGeUiXnnR/3nukKF0qTtyyu\nwjr/efvYH2ljrTmIOyl5HSqLEZvvBpVebQ2YdCmWOgNtOkZzBGpDfJep48Q7Xvlo\npcs84Bnp5u4nkvAevhi3nFQQyy+zZUW432O5uByxlCY0aYPxttUMmbLvs2icR3EB\n1K2VznxBAgMBAAECggEADVQucNsYK5djKeUECGt3l1eWnbn9tryZielxeeiX+osI\nDsFB+CqEhOZm3GhgDxvS0cRirtRVYkHugFzim/deAxcS1BYQJCDsYW1y9eJJaNuB\ngp/Z2m/gOEuoZQgfbYeiCj28SLobxR3vewSK6ORpo6lR41E2e+c7g9yIVFFCHx5z\nZqNyyraq1vNuQnbe7wSnQ4EEWr1CTsecpn1bhstmdMqiDro9Wrfz5KT9mawkXQPO\nCBknAAvNZgzRn/SsGL5M4E5PaTKTpOqUdXz25GdY7rJJQY5Je2aMLLxrdEJc6CBB\nzW3kdmIx/Zvh41VPgwrfZ5O8buRhRI0rwbDasafogwKBgQDKebh9L1t2jHh12LJ3\n6AO+GUUfJkbUqgKwspnqLCXHI89H/7NYVtOEiNqJ47L4h7Wqa4xk6fFcjE2AnoxL\ny2JJ40Qx0nBH+1KyD/wALUM0jDduZ/7BLdYqpHrLleH8D8IbI8UdX4cTzf9GV6fy\n1rDzWnr5OtBxp4n3ZJC/fbDPjwKBgQC6twvURr9CzoRH502il5Ug+QUTspgsvdh8\n52QA3nRmyKZrhor12IxAzVboS17eGNK3JgKtx6vrAErM2jF6k1U49Bha5iUMvkR3\nhuGBUBK6nodurLFuSvIea0c0w69AcWQcz9DmknQ+nQdNm4Mk6IPAoDuQHD5xAwR7\nW9Dt72EPLwKBgEfi12F6wtpgHRSaDyMLOOjxR907VcKDadkaUBMYAYGmcR16503h\n5c8UV6LFOPGMHS+YZ4wckxjsp0eXAvCWERtymO+naz3jOQUHL81QRKAPeE62lXg4\nseUJ6J8HY+h+H8hK9tzq4aZiaNOso3BQURrVcPuzqfXwKcev6MRT98Z5AoGARO3C\nXjFn9j/LMchALuAK28tShn0OFKZZP3MkxfVZv4Aff96BelThIiMsDEGW2iML1zUf\nFAx8eRr4gjuivH+bnJTwUM5ZqySqnf2bTmPDJkXT9ZWnQvJEA9rSxLXhAsdZkBFg\nK16xr1PFGG9qsLttuDTvCDqFCq90fh3dOZl/mV0CgYAG0VrAeJ0HHdrS21AlwvVP\n3FMhL3V0cUJMVw956Vxwfl7oraBBfW1czZXYKXg2gozCPwvysyKpPbjMjsdwwrKw\nXqVCGrr5B5jueV7kKovQ5vqPYJzN3pICA5z+IbMgcAhmG6C+cvCzs0JAVNSRp6Of\ngPkP/9kxd8wQ3sAdg0lrCQ==\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-odjja@uotc-4c343.iam.gserviceaccount.com",
  "client_id": "102573834754874101437",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-odjja%40uotc-4c343.iam.gserviceaccount.com"
}

# Create the credential certificate.
cred = credentials.Certificate(config)

# Connect to the Firebase app.
app = firebase_admin.initialize_app(cred)


def Firebase_validation(id_token):
    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        provider = decoded_token['firebase']['sign_in_provider']
        image = None
        name = None
        if "name" in decoded_token:
            name = decoded_token['name']
        if "picture" in decoded_token:
            image = decoded_token['picture']
        try:
            user = auth.get_user(uid)
            email = user.email
            if user:
                return {
                    "status": True,
                    "uid": uid,
                    "email": email,
                    "name": name,
                    "provider": provider,
                    "image": image
                }
            else:
                return False
        except Exception as e:
            print("user not exist " + str(e))
    except Exception as e:
        print("invalid token " + str(e))

id = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImIxYTgyNTllYjA3NjYwZWYyMzc4MWM4NWI3ODQ5YmZhMGExYzgwNmMiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI0MjAxODI0Njc3NDMtdDVxOWk2aTBuMTc1Nmd2aXF2MW8xaWVzNGlzN3I1bTIuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI0MjAxODI0Njc3NDMtaWwzcm92b3JrNnBrOHVxNGNqbTZmbGNmc3Y2cTlhNGwuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMTYwMzE4MjM0NTQ2MzAxODAxMDciLCJlbWFpbCI6InF3ZXFhejE1N0BnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwibmFtZSI6IkFCVSBBTEhBU1NBTiBBTENJR0VBUlkiLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EtL0FPaDE0R2plMkwyV2sxbUFrcDlEV3B2U0JrVDAzSnhfNzZBbGl6VndQOWNYSUJNPXM5Ni1jIiwiZ2l2ZW5fbmFtZSI6IkFCVSBBTEhBU1NBTiIsImZhbWlseV9uYW1lIjoiQUxDSUdFQVJZIiwibG9jYWxlIjoiYXIiLCJpYXQiOjE2NTIzMzY5NTUsImV4cCI6MTY1MjM0MDU1NX0.ZnjDm0O_hYUR3n3sqMJ5knJ-xqlOPRxx4pRJEI_ySFCesMz7BSlDZ6JsXQpPk_ipctVUChTkxbpfcUzUdFqHweuIZunoM5y-oc8p4JbmwQACWPY_abVPFjY0ZFhbtwlF9ZjqNGzuR6WyvxTxktnEan2HQRgHOtnpfiAPFujigNTFCpXlKpxicDuBCRpTYrxD_HLQC_W-NAw0cXBEZz_va36HTum8nWWxZtO9"

print(Firebase_validation(id))