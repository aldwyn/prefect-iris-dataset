# Iris Project

References:

- https://towardsdatascience.com/orchestrate-a-data-science-project-in-python-with-prefect-e69c61a49074
- https://github.com/khuyentran1401/Data-science/tree/master/data_science_tools/prefect_example

## Prerequisites

- Python 3.6 or later (recommended is Python 3.9)
- A fully functioning EKS cluster.
- The Prefect agent pod and its related resources in `prefect-agent.yml` file. Make sure to replace `BASE64_ENCODED_PREFECT__CLOUD__API_KEY`.
- A private ECR repository for the Dockerized Prefect flows
- Make sure to include the used IAM role/user in the ConfigMap `aws-auth` of the EKS cluster. Reference: https://docs.aws.amazon.com/eks/latest/userguide/add-user-role.html

  ```bash
  kubectl get configmap aws-auth -n kube-system -o yaml
  ```

  The `aws-auth` ConfigMap must now look like the following:

  ```yaml
  apiVersion: v1
  data:
    ...
    mapUsers: |
      - "rolearn": "arn:aws:iam::<AWS_ACCT_ID>:role/github-actions-service-account-role"
        "username": "github-actions-service-account-role"
        "groups":
        - "system:masters"
  kind: ConfigMap
  ```

## Obtaining the IAM credentials for this Github Actions workflow

Note: This set-up happens in the AWS Management Console.

#### Create the IAM user

1. Navigate to Identity and Access Management (IAM).
2. Go to Users. Click `Add Users`.
3. Provide the username, e.g. `github-actions-service-account` and set the credentials type to programmatic access.
4. Skip the setting of permissions.
5. Optionally, you can set some tags for this user.
6. On the review screen, click `Create user`.
7. Safekeep the access key ID and secret access key. This will be used when settings the Github secrets.

#### Create the IAM role

1. Go to Roles. Click `Create role`.
2. On the use cases part, select `EC2` for now.
3. On the permissions part, select `AmazonEC2ContainerRegistryPowerUser`.
4. Optionally, you can set some tags for this role.
5. On the review screen, click `Create role`.

#### Attach the IAM role to the IAM user

1. Go to the created IAM role and go to its `Trust relationships` section.
2. Click `Edit trust relationship`.
3. Replace the value in input field with the following snippet. Apply values to the placeholders.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::<CURRENT_ACCOUNT_ID>:user/<IAM_USER_USERNAME>"
      },
      "Action": ["sts:AssumeRole", "sts:TagSession"]
    }
  ]
}
```

4. Go to the created IAM user. Click `Add inline policy`.
5. Click the `JSON` tab and paste the following snippet.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["sts:AssumeRole", "sts:TagSession"],
      "Resource": "arn:aws:iam::<CURRENT_ACCOUNT_ID>:role/<IAM_ROLE_NAME>"
    }
  ]
}
```

#### Provide the IAM credentials to Github Secrets

1. Go to the Github repository to where the Github actions workflow is set up.
2. Navigate to `Settings > Secrets`.
3. Click `New repository secret`.
4. Set the `Name` to `AWS_ACCESS_KEY_ID` and the `Value` to IAM user's access key ID.
5. Do the same step with `AWS_SECRET_ACCESS_KEY` and `AWS_ROLE_TO_ASSUME` (i.e. the ARN of the created IAM role).
6. For the test run, commit a sample change within any of the Prefect flow and inspect the Actions tab of the repository. It should not have any failure on the step `Configure IAM credentials`.
