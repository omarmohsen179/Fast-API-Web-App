SUBSCRIPTION="Azure subscription 1"
RESOURCEGROUP="test4App"
LOCATION="centralus"
PLANNAME="ASP-test4App-821a"
PLANSKU="P1v2"
SITENAME="ecommercy"
RUNTIME="PYTHON|3.9"
az login

az account list -o table
az account set --subscription $SUBSCRIPTION
USERNAME="omarmohsen179"
PASSWORD="Thanks010066@"

git remote add azure "https://$USERNAME@$SITENAME.scm.azurewebsites.net/$SITENAME.git"

git add .
git commit -m "omar"
git push azure master --force
