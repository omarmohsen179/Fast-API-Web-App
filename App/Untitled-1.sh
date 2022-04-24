SUBSCRIPTION="Azure subscription 1"
RESOURCEGROUP="test4App"
LOCATION="centralus"
PLANNAME="ASP-test4App-a5aa"
PLANSKU="P1v2"
SITENAME="FAG1"
RUNTIME="PYTHON|3.9"

# login supports device login, username/password, and service principals
# see https://docs.microsoft.com/en-us/cli/azure/?view=azure-cli-latest#az_login
az login
# list all of the available subscriptions
az account list -o table
# set the default subscription for subsequent operations
az account set --subscription $SUBSCRIPTION
# create a resource group for your application
az group create --name $RESOURCEGROUP --location $LOCATION
# create an appservice plan (a machine) where your site will run
#az appservice plan create --name $PLANNAME --location $LOCATION --is-linux --sku $PLANSKU --resource-group $RESOURCEGROUP
# create the web application on the plan
# specify the node version your app requires
#az webapp create --name $SITENAME --plan $PLANNAME --runtime $RUNTIME --resource-group $RESOURCEGROUP

# To set up deployment from a local git repository, uncomment the following commands.
# first, set the username and password (use environment variables!)
USERNAME="omarmohsen179"
PASSWORD="Thanks010066@"
az webapp deployment user set --user-name $USERNAME --password $PASSWORD

# now, configure the site for deployment. in this case, we will deploy from the local git repository
# you can also configure your site to be deployed from a remote git repository or set up a CI/CD workflow
az webapp deployment source config-local-git --name $SITENAME --resource-group $RESOURCEGROUP

# the previous command returned the git remote to deploy to
# use this to set up a new remote named "azure"
git remote add azure2 "https://$USERNAME@$SITENAME.scm.azurewebsites.net/$SITENAME.git"
# push master to deploy the site
git push azure2 master

# browse to the site
az webapp browse --name $SITENAME --resource-group $RESOURCEGROUP
