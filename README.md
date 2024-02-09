# WorkRamp Homework

This repocitory contains X subprojects: 

## Subprojects

- 

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

To get all the dependencies installed, use [Homebrew](https://brew.sh) package manager. After installing Homebrew (Check the install steps [here](https://docs.brew.sh/Installation)), run the following command.

```bash
brew install pre-commit
brew install docker --cask
```

## Local Environment

docker-compose run workramp

cd app
source .venv/bin/activate
pip install -r requirements.txt
cdk synth