# Security utils
Standard authorization method from fastapi documentation

## Dependencies
- itsdangerous


### Requirements
You must have a class with a config in the system, which will be located in the app.core.config path.

app.core.config
```sh
class SecuritySettings(BaseConfig):
    SECURITY_TOKEN_EXPIRE_MINUTES = 24 * 60  # 1 day
```

### Using
#### Generate and check security token
Generate
```sh
from security_utils.security import generate_security_token

security_context = dict(email="Test@test.com", account_id=1)
token = generate_security_token(security_context)
```
Check
```sh
from security_utils.security import verify_security_token

security_context = verify_security_token(token)
print(security_context)
>>> dict(email="Test@test.com", account_id=1)
```
