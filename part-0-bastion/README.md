# Deploy the Bastion

## Generate our Keypair
1. Log into the AWS Console
2. Ensure your region is set to 'ap-southeast-2'
3. Navigate to the EC2 Dashboard
4. Select 'Key Pairs' from the left hand menu
5. Create a new Key Pair with your own name in the Key Pair name
6. Select 'pem' or 'ppk' depending on your laptop 
  * pem for Linux/Mac/Windows SSH
  * ppk for Windows Putty
7. Save the keypair to your computer in the right place
  * ~/.ssh/handson.pem for SSH
  * anywhere really for Windows Putty

## Deploy the Bastion IAC
1. Log into the AWS Console
2. Ensure you region is set to 'ap-southeast-2'
3. Navigate to the CloudFormation Dashboard
4. Create a new Stack
5. Enter in the URL Box: https://awshandson-streaming-iac.s3.amazonaws.com/bastion.yml
6. Stack Name: 'streaming-<your-name>-bastion'
   Keypair: Select the one you created earlier from the dropdown  
   Resource Prefix: 'streaming-<your-name>' (no spaces, just '-' if possible)  
   SubnetId: Chose any option  
   VpcId: Chose the only option  


```bash
aws cloudformation deploy --template-file infrastructure-as-code/bastion.yml --stack-name streaming-<your-name>-bastion --parameter-overrides "ResourcePrefix=streaming-<your-name>" "Keypair=<keypair.name>" "VpcId=vpc-4afffa2d" "SubnetId=subnet-30688556" --capabilities CAPABILITY_IAM

# Example as Michael Robbins
aws cloudformation deploy --template-file infrastructure-as-code/bastion.yml --stack-name streaming-michaelr-bastion --parameter-overrides "ResourcePrefix=streaming-michaelr" "Keypair=michael.robbins" "VpcId=vpc-4afffa2d" "SubnetId=subnet-30688556" --capabilities CAPABILITY_IAM
```
