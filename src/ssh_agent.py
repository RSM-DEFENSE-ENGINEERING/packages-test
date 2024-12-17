import boto3
import os
import subprocess


def get_ssh_key():
    """Retrieve the SSH private key from AWS Secrets Manager."""
    secret_name = "prod/package-manage-ssh"
    region_name = "us-east-1"
    secrets_client = boto3.client('secretsmanager', region_name=region_name)
    secret = secrets_client.get_secret_value(
        SecretId=secret_name)
    print(secret)
    return secret['SecretString']


def setup_ssh_agent(ssh_key):
    """Set up the SSH agent with the given private key."""
    os.environ['SSH_AUTH_SOCK'] = "/tmp/ssh-agent.sock"
    subprocess.run(
        ["ssh-agent", "-a", os.environ['SSH_AUTH_SOCK']], check=True)

    # Add the SSH private key
    proc = subprocess.Popen(["ssh-add", "-"], stdin=subprocess.PIPE)
    proc.communicate(input=ssh_key.encode())
    print("SSH key added to the agent.")
