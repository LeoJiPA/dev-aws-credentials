# dev-aws-credentials
Update the local aws credentials file with temporary credentials obtained using the AWS CLI

- Make sure you have the Python3 installed
- Make sure you have the AWS CLI installed and configured before running this script.
- Please add the following configuration to your AWS configuration file: ~/.aws/config

```
[profile sso]
region = us-east-1                    # replace with your region
output = json                         # replace with your output format
sso_session = sso-default
sso_account_id = xxxxxxxxxx           # replace with your account id
sso_role_name = xxxxxxxxxxx           # replace with your role name

[sso-session sso-default]
sso_start_url = https://my-sso-portal.awsapps.com/start           # replace with your SSO start URL
sso_region = us-east-1                                            # replace with your region
sso_registration_scopes = sso:account:access
```
