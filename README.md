# WorkRamp Homework

This repocitory contains X subprojects:

## Architecture



## Dependencies

You need the following tools installed in order to be able to work on this repo:

| Tool           | Version |
|----------------|---------|
| pre-commit     | 2.21.*  |
| docker         | 24.0.*  |
| docker-compose | 2.23.*  |
| python         | 3.12.*  |
| nodejs         | 20.11.* |

### Installing dependencies

To get all the dependencies installed, use [Homebrew](https://brew.sh) package manager. After installing Homebrew (Check the install steps [here](https://docs.brew.sh/Installation)), run the following commands.

```bash
brew install pre-commit
brew install docker --cask
pre-commit install -f
```

This will get your environment ready, and the git hooks installed.

NOTE: Eventhough Docker and NodeJS are listed as dependencies, you don't really need to install then to run this project locally since a docker container will be used for that.

## Local Environment

1. Start the docker container using docker-compose:

    ```bash
    docker-compose run workramp
    ```

2. Once on the docker container, move to the app folder and install the dependencies:

    ```bash
    cd app
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

3. Check the CDK is workins:

    ```bash
    cdk synth
    ```

## Deployment

In order to get all the AWS assets created on the Cloud, execute the following steps:

NOTE: It's assumed you have already executed all steps from the [Local Environment]
(#local-environment) section.

1. On the docker conteiner, set your AWS credentials:

    There are multiple options to do so, which are properly explained in [AWS official documentation](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html#getting_started_auth).

    For simplicity, in this case, we'll go with the environment varibles as follows:

    ```bash
    export AWS_ACCESS_KEY_ID=<AWS_KEY>
    export AWS_SECRET_ACCESS_KEY=<AWS_SECRET_KEY>
    ```

2. Run the diff command, and check the changes to be applied are the expected ones:

    *IMPORTANT*: If you're running the deployment for the very first time, you'll have to run the [bootstrap command first](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html#getting_started_bootstrap).

    ```bash
    cdk diff
    ```

3. Run the deploy command:

    ```bash
    cdk deploy
    ```

## Connect to Bastion

To connect to the Bastion server after deploying the stacks, follow these instructions:

1. From the stack ouputs, get the SSM Parameter name to the KeyPair private key.

    With the parameter name, run the following command to create the pem file:

    ```bash
    aws ssm get-parameter --name <PARAMETER_NAME> --with-decryption --query "Parameter.Value" --output text > bastion_key.pem
    ```

    i.e.:

    ```bash
    aws ssm get-parameter --name "/ec2/keypair/key-003d0ed025228a4c6" --with-decryption --query "Parameter.Value" --output text > bastion_key.pem
    ```

2. Set the right permissions for the PEM file:

    ```bash
    chmod 400 bastion_key.pem
    ```

3. From the stack outputs, get the server public IP address, and use the SSH command to login:

    ```bash
    ssh -i bastion_key.pem ec2-user@<BASTION_PUBLIC_IP>
    ```

    i.e.:

    ```bash
    ssh -i bastion_key.pem ec2-user@3.216.94.67
    ```

4. (Optional) Once you've logged in bastion, check you can connect with the server in the private subnet:

    Get the service instance IP from the stack output.

    ```bash
    curl <SERVICE_PRIVATE_IP>
    ```

    i.e.:

    ```bash
    curl 10.0.3.217
    ```
