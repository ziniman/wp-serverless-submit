# WordPress Serverless Submit (WPSS)

A simple API, backed by AWS Lambda, to receive form submissions from WordPress, using the
WP Serverless Forms plugin and process them.

This project contains source code and supporting files for a serverless application that you can deploy with the SAM CLI. Follow [README-SAM.md](README-SAM.md) for full details.

## Deploy the WPSS application



To build and deploy your application for the first time, run the following in your shell:

```bash
sam build --use-container
sam deploy --guided
```

The first command will build the source of your application. The second command will package and deploy your application to AWS, with a series of prompts:

* **Stack Name**: The name of the stack to deploy to CloudFormation. This should be unique to your account and region, and a good starting point would be something matching your project name.
* **AWS Region**: The AWS region you want to deploy your app to.
* **Confirm changes before deploy**: If set to yes, any change sets will be shown to you before execution for manual review. If set to no, the AWS SAM CLI will automatically deploy application changes.
* **Allow SAM CLI IAM role creation**: Many AWS SAM templates, including this example, create AWS IAM roles required for the AWS Lambda function(s) included to access AWS services. By default, these are scoped down to minimum required permissions. To deploy an AWS CloudFormation stack which creates or modified IAM roles, the `CAPABILITY_IAM` value for `capabilities` must be provided. If permission isn't provided through this prompt, to deploy this example you must explicitly pass `--capabilities CAPABILITY_IAM` to the `sam deploy` command.
* **Save arguments to samconfig.toml**: If set to yes, your choices will be saved to a configuration file inside the project, so that in the future you can just re-run `sam deploy` without parameters to deploy changes to your application.

You can find your APIHttp Gateway Endpoint URL in the output values displayed after deployment.

## Use the SAM CLI to build and test locally

Build your application with the `sam build --use-container` command.

```bash
wp-serverless-submit$ sam build --use-container
```

The SAM CLI installs dependencies defined in `code/requirements.txt`, creates a deployment package, and saves it in the `.aws-sam/build` folder.

Test a single function by invoking it directly with a test event. An event is a JSON document that represents the input that the function receives from the event source. Test events are included in the `events` folder in this project.

Run functions locally and invoke them with the `sam local invoke` command.

```bash
wp-serverless-submit$ sam local invoke -e events/event.json
```

## Environment Variables
```
aws kms create-key --description wpss
```
Get the "KeyId"

```
aws kms encrypt --key-id [KeyId] --plaintext "[SOME_TEXT]" --query CiphertextBlob --output text
```

### AllowedDomains
TBD
