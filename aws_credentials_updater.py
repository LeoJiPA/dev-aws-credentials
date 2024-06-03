# Author: Leo Ji
# Description: This script updates the AWS credentials file with temporary credentials obtained using the AWS CLI.
# Make sure you have the AWS CLI installed and configured before running this script.
# Please add the following configuration to your AWS configuration file: ~/.aws/config

# [profile sso]
# region = us-east-1                    # replace with your region
# output = json                         # replace with your output format
# sso_session = sso-default
# sso_account_id = xxxxxxxxxx           # replace with your account id
# sso_role_name = xxxxxxxxxxx           # replace with your role name

# [sso-session sso-default]
# sso_start_url = https://my-sso-portal.awsapps.com/start           # replace with your SSO start URL
# sso_region = us-east-1                                            # replace with your region
# sso_registration_scopes = sso:account:access


import os
import sys
import subprocess
import configparser

def install(package):
    """Install a package using pip."""
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Ensure boto3 is installed before importing
try:
    import boto3
except ImportError:
    install('boto3')
    import boto3

def get_aws_credentials_path():
    """Get the AWS credentials file path based on the OS."""
    if os.name == 'nt':  # For Windows
        return os.path.join(os.environ['USERPROFILE'], '.aws', 'credentials')
    else:  # For Linux/Unix
        return os.path.join(os.environ['HOME'], '.aws', 'credentials')

def get_temporary_credentials(profile_name):
    """Get temporary AWS credentials using the AWS CLI and boto3."""
    command = f"aws sso login --profile {profile_name}"
    subprocess.run(command, shell=True, check=True)
    
    session = boto3.Session(profile_name=profile_name)
    return session.get_credentials().get_frozen_credentials()

def update_credentials_file(credentials, profile_name='default'):
    """Update the AWS credentials file with the temporary credentials."""
    config = configparser.ConfigParser()
    aws_credentials_path = get_aws_credentials_path()
    config.read(aws_credentials_path)

    if not config.has_section(profile_name):
        config.add_section(profile_name)

    config.set(profile_name, 'aws_access_key_id', credentials.access_key)
    config.set(profile_name, 'aws_secret_access_key', credentials.secret_key)
    config.set(profile_name, 'aws_session_token', credentials.token)

    with open(aws_credentials_path, 'w') as configfile:
        config.write(configfile)

    print(f"Credentials updated for profile: {profile_name}")

def main():
    sso_profile_name = 'sso'  # Replace with your AWS SSO profile name
    profile_name = 'default'  # Replace with the profile name in AWS credentials file
    try:
        credentials = get_temporary_credentials(sso_profile_name)
        update_credentials_file(credentials, profile_name)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
