aws ecr create-repository `
--repository-name facturas `
--image-scanning-configuration scanOnPush=true `
--image-tag-mutability MUTABLE

docker build -t facturas .   

aws ecr get-login-password `
--region us-east-1 `
| docker login  `
--username AWS `
--password-stdin `
074391503972.dkr.ecr.us-east-1.amazonaws.com 

docker tag facturas:latest 074391503972.dkr.ecr.us-east-1.amazonaws.com/facturas:latest

docker push 074391503972.dkr.ecr.us-east-1.amazonaws.com/facturas:latest        