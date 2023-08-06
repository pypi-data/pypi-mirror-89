# JSM User JWT Service

Middleware to intercept JWT auth token and more utils functions

## Local development

### Running tests

`docker-compose up integration-tests`

## Install - For Django users

`pip install jsm-user-services[drf]`

Add `jsm_user_services` to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "jsm_user_services",
    "app_test",
]
```

Add the Middleware:

```python
MIDDLEWARE = [
    ...
    "jsm_user_services.middleware.JsmJwtService",
]

# Dev url
USER_API_HOST = "http://ishtar-gate.dev.juntossomosmaisi.com.br/api/v1"
USER_API_TOKEN = "user_api_token"
```

## Install - For Flask users

`pip install jsm-user-services[flask]`

Add the middleware in your Flask app:

```python
from flask import Flask
from jsm_user_services.flask import middleware

app = Flask(__name__)

middleware.JsmJwtService(app)
app.config.update(
    USER_API_HOST="http://ishtar-gate.dev.juntossomosmaisi.com.br/api/v1", USER_API_TOKEN="user_api_token"
)
```

**DISCLAIMER**
- Currently, only the middleware is implemented for Flask apps

## Use

```python
from jsm_user_services.services.user import current_jwt_token
from jsm_user_services.services.user import get_jsm_token
from jsm_user_services.services.user import get_jsm_user_data_from_jwt
from jsm_user_services.services.user import get_ltm_token
from jsm_user_services.services.user import get_user_email_from_jwt
from jsm_user_services.services.user import get_user_id_from_jwt
from jsm_user_services.services.user import get_user_data_from_server
from jsm_user_services.services.user import get_user_data_from_cpf
from jsm_user_services.services.user import get_cpf_from_jwt

current_jwt_token()
"""
Response example:
"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTY1ODc4MjI4LCJqdGkiOiJiZDFmMzBiMGEzMTc0MmRmYjk3MTBiMzEzMTY0M2E2ZiIsInl1bnRpYW5kdSI6IjhyR0NjVHZGTE9VemR2LWRhTFk4SzdHZTF2MmVyQS01TWJOVkZ4TFBwTUNDTmRwTjQ2bDlJMHZFNG9aTmNNanRfZTh5SWJkTlczN0tKRUhWdzM3dmJjOEdLZmlfd0ZmZDJTRDlIYUJuNk80SVVabWVNUjlROVRqVTd0WFI1WDZPeFoyRDRiNXNHSWlKWGQwcGtPcXptOFpFSUl2Y2xtLUNuMjVJMklKNGJ2M2RaeTVtQUhqUnhaTmNMM2RyX1NkX1FGTFpVMWthNmtfQ0FFTkZxOE9CR1RoelNlRmtxeDFfTFBDLXE1dUVCUE9FSmpVdlF0bXhHTF8zUHNiZ0twLXFaazRfQUJ1enY1Zmk5XzFSaHJ5ZzZVWWF6WFRYNkVxcTdDdUJTUlBRMWFqM0FpU1VadGFmNjZjSTZJSThHMkxKYmd3bHhSZ19aRzY1QlpielJ3QnRvUTllUkNxY2FSRG56ZXhKVEhKMUJ0X2N6Z0J5NGxhRnFmbUZFYWZ6b3RNa0ZrZ2lLT1BNRnhMaFdaZlBEYVB0UFA0UjJjeXJEWWxaMkxNdGhrY09lZmVxMTNLa0doT0FRV2FQUHpEbzBNekRXa0VmbEVFUlpRTHo2NkItSE1TaDE1cHNBR09hUS1YcV85SWNLY05paUUzTVBfSWFpU3ZwbVQteGx2VXFiZFR5NDJkMUhhUWh6RmdPaHFoZ2F1cHoxejN0Z0VIWnNwaFdidmdBMlZQaVIyeUUzTnBLMEhPekkwMTk4NnhJRjFiRmlCOGdLMHhCQnBqRjd2bmcxU0N1OEl0TTJGRjNRQUV3czltakgyTXBMZEp5T0ViWmRGT2FLb29SeEZlY3hzRkhaV19LeEsweFdsRVBBZ2loV1NNWmNwRnpZTExiZGlLVDYtamtNckVXZ1NuRk9xajZPeWJxT05NdzRqdVZ3YTV2TTlmcVkzY0EyVlZsOU12dWlieWZRdWV1c3pJa2RaYlMyLW9YZ0oxYmZETERjckp4YWtjVXZMUE0wdmtlZjllZSIsImpzbV9pZGVudGl0eSI6ImV5SmhiR2NpT2lKSVV6STFOaUlzSW5SNWNDSTZJa3BYVkNKOS5leUpsYldGcGJDSTZJakV5TXpRMVFHeHZlV0ZzZEhsS1UwMHVZMjl0SWl3aWRXNXBjWFZsWDI1aGJXVWlPaUpoYzJRaUxDSjNaV0p6YVhSbElqb2lRMnhwWlc1MFFYQndiR2xqWVhScGIyNGlMQ0oxYVdRaU9pSTROVEEzTVdSa1pTMWlOVFk0TFRReFlXWXRZVFUzT1MwelpqUXlZekZrWmpBNU9UZ2lMQ0p6Wld4c1pYSnpJam9pTVdVellqZ3pNV1l0T1RWa01DMDBNV0UzTFdJelpURXRNV1psTURObVlXVXlNRFEySWl3aWNtOXNaU0k2SWtOMWMzUnZiV1Z5SWl3aVkyNXdhbk1pT2lJMk9DNDFPVGN1TWpnd0x6QXdNREV0TURraUxDSnVZbVlpT2pFMU5qRTFOVGd5T0Rjc0ltVjRjQ0k2TVRVMk1qRTJNekE0Tnl3aWFXRjBJam94TlRZeE5UVTRNamczTENKcGMzTWlPaUowWm5BNkx5OXBaR1Z1ZEdsMGVTNXFjMjB2WVhWMGFHOXlhWFI1SWl3aVlYVmtJam9pWW1Nd05URmtaVE10WVdWaFlTMDBZV001TFRobVltWXRNRFZoT0RabE1EZ3pabU5tSW4wLlBVQnRFbGE5ajJHSFFqNEk2TmxpVHV3cjZ4d1M4czZ2UkNWRGp6dy1QeEEifQ.oZvlK-XOBrgN9xZrChHHRdQ0rLMFTPp9jjuGvGM1U78"
"""

get_jsm_token()
"""
Response example:
"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6IjY0NzIyMzM4NjEyQGxveWFsdHlKU00uY29tIiwidW5pcXVlX25hbWUiOiJUZXN0IFVzZXIiLCJ3ZWJzaXRlIjoiQ2xpZW50QXBwbGljYXRpb24iLCJ1aWQiOiI4NzM1YmY4ZC01NDc5LTQ0NDgtODNjZi04OTk5N2Q3ZGY2MDgiLCJzZWxsZXJzIjoiMWUzYjgzMWYtOTVkMC00MWE3LWIzZTEtMWZlMDNmYWUyMDQ2Iiwicm9sZSI6IkN1c3RvbWVyIiwiY25wanMiOiI2OC41OTcuMjgwLzAwMDEtMDkiLCJuYmYiOjE1NjE1NTg2MzUsImV4cCI6MTU2MjE2MzQzNSwiaWF0IjoxNTYxNTU4NjM1LCJpc3MiOiJ0ZnA6Ly9pZGVudGl0eS5qc20vYXV0aG9yaXR5IiwiYXVkIjoiYmMwNTFkZTMtYWVhYS00YWM5LThmYmYtMDVhODZlMDgzZmNmIn0.4dT-6_PmJEbWGw5Q1F18mJBQcXcVmNugQwiLxp6e4Ew"
"""
get_ltm_token()
"""
Response example:
"b51yreTQ3_4l2Z7zGsEb7UCosv-xulOtzkfflxsxTwrbOYva7loVGhxHmD6Qv5P0x5enm3LuykiAOGvf9fjDkr7qUETk5_OPONonkw1roSwHBpCCjS_IiGWdk2t2mpR4o-SFKMPfKyATzQQkBi886wMJ5g8Sg7GJNaQBHimbHDoWsvSF4zZhMin3IkD-3aVruS3IpBM6-72f4mabCB2kbtRQfTfjU5BvMYYKQzEp79_AWHbUm34gpgh5OJEt9VynHVb0Wzj-_M5sNl8uzEEQ0kixlWyueha2e5gZPHPA2TiSb0dt4WdBUqSL9BPXpsCB9TBtyRkU6JeH-DXo05Px02joOUh_MrjqhbXxYtJXWTkX4E6krHI1kS2r75DFU3dUTfQtELrvn1lQxpNCG_FAX0gB5B_XMWiX2Pn6hWE-QO9uglJgnkllxwhBBiwC1K57ony1tgpZLPY7kapAQveGmJAgWAkFXKtR2s4DK9Bkz_Xz-dUdZRONlBIH6yP4QotiE58QT0DFEluRMXhQX6huPSKuVnyaGLRrbFxdocUPuVgLTigg4rk9zgXX-GmOdHD5sxvC-cd8OWep0r7Pn5URwIdkWFjY_vly8dQDb3Cx2TXx2lXQeXBlj4XwQNlrAJTBGdmnL-Nu6Sk3oyh1_r-u53JyaF4frbt8Q6ZZsNAeZtRNLvM3l1JJ591XpApteouRRFakC6Iu8ED3IRmuzYvCgajDIDede7vtpsBvEp4yxl0"
"""

get_jsm_user_data_from_jwt()
"""
Response example:
{
  "email": "64722338612@loyaltyJSM.com",
  "unique_name": "Test User",
  "website": "ClientApplication",
  "uid": "8735bf8d-5479-4448-83cf-89997d7df608",
  "sellers": "1e3b831f-95d0-41a7-b3e1-1fe03fae2046",
  "role": "Customer",
  "cnpjs": "68.597.280/0001-09",
  "nbf": 1561558635,
  "exp": 1562163435,
  "iat": 1561558635,
  "iss": "tfp://identity.jsm/authority",
  "aud": "bc051de3-aeaa-4ac9-8fbf-05a86e083fcf"
}
"""

get_user_email_from_jwt()
"""
Response example:
"64722338612@loyaltyJSM.com"
"""

get_user_id_from_jwt()
"""
Response example:
"85071dde-b568-41af-a579-3f42c1df0998"
"""

get_user_data_from_server()
"""
Response example:
{
    "id": "85071dde-b568-41af-a579-3f42c1df0998",
    "username": "44444444444",
    "cpf": "44444444444",
    "occupation": "owner",
    "name": "ca1bd09f-b109-435f-b6d5-206d28a3e5e2",
    "birthday": "1990-06-15",
    "phones": [{"number": "5511111111111", "type": "MOBILE"}],
    "emails": [{"email": "fernando@gmail.com", "type": "PERSONAL"}],
    "roles": ["Proprietário"],
    "gender": "male",
    "allow_contact": True,
    "mediums": ["SMS", "Push"],
    "rules_agreement": True,
    "addresses": [
        {
            "postal_code": "06763180",
            "street": "Rua Adolfino Arruda Castanho",
            "number": "200",
            "complement": "Ap 133",
            "district": "Jardim Bom Tempo",
            "city": "Taboao da Serra",
            "state": "SP",
            "country": "Brazil",
            "type": "HOME",
        }
    ]
}
"""

get_user_data_from_cpf(cpf)
"""
Response example:
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": "888707ab-9866-42a3-a67e-23a937cb3e7f",
            "created_at": "2019-10-18T20:06:44.552669Z",
            "updated_at": "2019-10-23T14:08:05.737326Z",
            "user_id_ref": "5cfd56c1-1bc1-4175-9fa9-00449ec448b8",
            "metadata": {
                "id": "5cfd56c1-1bc1-4175-9fa9-00449ec448b8",
                "cpf": "42879321964",
                "name": "Fernanda Gabrielly Duarte",
                "roles": [
                    "manager"
                ],
                "emails": [
                    {
                        "type": "personal",
                        "email": "fernandagabriellyduarte@ymail.com"
                    }
                ],
                "gender": "female",
                "phones": [
                    {
                        "type": "mobile",
                        "number": "5519991901717"
                    }
                ],
                "status": "active",
                "mediums": [
                    "sms"
                ],
                "birthday": "1982-06-04",
                "username": "42879321964",
                "addresses": [
                    {
                        "city": "Cascavel",
                        "type": "main",
                        "state": "PR",
                        "number": "217",
                        "street": "Rua Riachuelo",
                        "country": "Brazil",
                        "district": "Centro",
                        "postal_code": "85812110"
                    },
                    {
                        "city": "Cascavel",
                        "type": "shipping",
                        "state": "PR",
                        "number": "217",
                        "street": "Rua Riachuelo",
                        "country": "Brazil",
                        "district": "Centro",
                        "postal_code": "85812110"
                    }
                ],
                "occupation": "c85583ef-b602-4fea-b202-6fc5c58d8189",
                "allow_contact": true,
                "blocked_reason": null,
                "favorite_medium": "sms",
                "registered_date": "2019-10-18T20:06:31.705758+00:00",
                "rules_agreement": true,
                "rules_agreement_date": "2019-10-18T20:06:31.708640+00:00"
            },
            "emails": "fernandagabriellyduarte@ymail.com",
            "phones": "5519991901717"
        }
    ]
}
"""

get_cpf_from_jwt()
"""
Response example:
"09345699823"
"""

get_user_ip()
"""
Response example:
"192.168.0.1" or None
"""

```