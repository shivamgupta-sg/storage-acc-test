# az login --service-principal -u 887ce85b-b289-42e7-a78d-1dbde039a0c8 -p sCp8Q~TKU~rPuOKpkrV_z6G44VKhqVOfn4StQc~k --tenant aa5fba84-fe75-490c-84db-382cd1342d45


Write-Host "Terraform Init"
terraform init

Write-Host "Terraform Plan"
terraform plan

Write-Host "Terraform Apply"
terraform apply --auto-approve