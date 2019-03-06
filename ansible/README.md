# Deploy

Frankfurt
AMI: Ubuntu Server 16.04 LTS (HVM), SSD Volume Type - ami-086a09d5b9fa35dc7
Instance: p2.xlarge (11.75 ECUs, 4 vCPUs, 2.7 GHz, E5-2686v4, 61 GiB memory, EBS only)
Storage: 30Gb
Ports: Add nerus security group

ansible-playbook -i hosts worker.yml

# Ctl

ssh -v -i ~/.ssh/aws-default-frank.pem ubuntu@ec2-34-217-65-115.us-west-2.compute.amazonaws.com
