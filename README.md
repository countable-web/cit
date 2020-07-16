# Countable Modern Django

A Dockerized boilerplate for a Django API driven web app, with Vue CLI and Postgres based on Countable's standards [here](https://github.com/countable-web/open-source-corporation/tree/master/product/engineering)

## Installation

Clone the project.

```
git clone https://github.com/countable/cit
```

Install Docker and docker-compose.


Development
```
cp dc.dev.yml docker-compose.override.yml
```
Staging
```
cp dc.stage.yml docker-compose.override.yml
```
Production
```
cp dc.prod.yml docker-compose.override.yml
```
Spin up the project.

```
docker-compose up
```

For development

Your Vue app is served at `http://localhost:8080`

The Django app is served at `http://localhost/api`

Ports may be configured by editing the port in the `dc.*.yml` files.

To create a superuser:

```
docker-compose exec web ./setup.sh
```

You can visit the Django admin at `http://localhost/admin`. The username is `admin`, password is `pass`.


## Importing Data

Some data must be downloaded locally (data bc warehouse resources). Download all local datasets to the `data` folder. ie, the census subdiv geometry:
```
wget http://www12.statcan.gc.ca/census-recensement/2011/geo/bound-limit/files-fichiers/2016/lcsd000b16a_e.zip
mv lcsd000b16a_e.zip web/data/
```

To import all data, run:
```
docker-compose exec web python manage.py bootstrap
```

Alternatively, resources can be imported individually.

import local shapefiles
```
docker-compose exec web python manage.py import_shp all
```

import local csv files
```
docker-compose exec web python manage.py import_csv all
```

import data from databc
```
docker-compose exec web python manage.py import_databc all
```

Use the `all` parameter in the three above commands to import all resources from each source, or see `web/pipeline/constants.py` for a list of valid resources to import individually.

## VSCode (Front end Development)

If the editor of choice is Visual Studio Code during development, one can have automatic linting enabled

In Files -> Settings -> Workspace -> Open Settings
```
{
  "editor.formatOnSave": true,
  "vetur.validation.template": false,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  }
}
```

It is recommended that the Workspace is the `cit-web` folder, and not the `cit` project for this to behave correctly. Otherwise, it won't read the ESLint & Prettier config files properly (VSCode expects them in root workspace by default).

## Deployment (Also may apply to development)

We are currently using the **Service Principal** method to deploy PowerBI onto the website. A Service Principal is the `local representation` of a global application object. In other words, Service Principal is a concrete instance from the application object and inherits certain properties from that application object. This means that we first need an **Application Object** to use a Service Principal.

### App Registration (Application Object) & Security Groups
----

We first need an **App Registration**, which acts as a blueprint to create `Service Principal` objects. We can perform the follwing steps to achieve this.

1. Log in to the [Azure portal](https://portal.azure.com/).
2. Go to `App Registrations`
3. Click `New Registration`
4. Fill out the form. (Single Tenant recommended)

Once this is done, we should be given details such as `Application ID`, `Tenant ID` and etc. Since we have a application object now, we need to configure this application object to contain the permissions and settings that we intend to use it for, so the instances of our Service Principal will be valid for whatever we want to perform. For the **CIT** we want one main purpose. To use the **PowerBI Rest API**. In order to do this, we need to let this App Registration know about it.

1. Click `API Permissions` on from the left menu inside the App
2. Click `Add Permissions`
3. Click `Power Bi Service`
4. Click `Delegated Permissions`
5. Select everything besides **Tenant**, **UserState**, **Group** and **Metadata**
6. Click `Add Permissions`

We also need something called a **Client Secret**. This will be the proof that an owner has access to this App registration.

1. Click `Certificates & Secrets` from the left menu inside the App
2. Under Client Secrets, click `New Client Secret`
3. Fill out the form, we recommend `Never` as expiry date.
4. Click `Add`
5. You will be shown the **Client Secret Value** one time here, **make sure you save this value**

We have now defined the capabilities this application has, and we need now to give service principal **access** to it.
We believe this can be done in either two ways.

1. Create an [Azure AD Security Group](https://docs.microsoft.com/en-us/azure/active-directory/fundamentals/active-directory-groups-create-azure-portal), and add the service principal to that security group (More on the next section)
2. Or, in your application, click `Api Permissions` and click `Grant admin consent ******` button.

**This detail needs to confirmed, we may need to perform both actions**


### Adding service principal to the security group
---
1. Go to `Power BI Embedded` through the Azure Portal
2. Select `Add` and create an instance depending on the processing requirements (A1 low, A2 medium... etc)

 **This service is pay per use and will begin billing once started. It can be paused to save cost.**

 1. Log in to the [Power BI portal](powerbi.microsoft.com)
 2. Click the cog at the top right and select `Admin Portal`
 3. Click `Tenant Settings` then scroll to `Developer Settings`
 4. Expand `Allow service principals to use Power BI APIs`
 5. Make sure `Enabled` is selected. Then click `Apply to Specific Security Groups`
 6. Add the security group created above.
 7. Click `apply`
 9. Go back to the `Admin Portal` then select `Workspaces`
 10. Select a workspace, then click the `3 dots` then click `access`
 11. Enter the Service Principal (APP ID) in the box. Select `Admin` then click `Add`


### Assigning Capacity
---
 1. Log in to the [Power BI portal](powerbi.microsoft.com)
 2. Click the cog at the top right and select `Admin Portal`
 3. Click `Capacity Settings`
 4. Click `Power BI Embedded`

If the instance is already made in Azure, there should be a capacity shown here, if it is greyed out, it is probably Paused. Go to back to Azure Portal and Start it. Once its started you can hit the name on the far left, just under `Capacity Name`

At the bottom of the page on the right you can click `Assign workspaces`, You can select `Specific workspace` and type the one you like. Or you can go to the far left, in the main powerbi menu, select the workspace tab, and under the workspace you want you can select the 4 dots in the side menu and select worskpace settings, you should be able to set the capacity in the `Advanced` drop down, you can select the Azure capacity in a list.

*Note, if you want to pause the Azure Power BI Instance, it will prevent the page from loading. In a Dev environment, it is useful to run everything on the free service so you can leave it up 24/7 without paying. In order to unassign the workspace from the capacity, either go into the capacity settings (the capacity MUST be active for you to access this page), or in the workspace tab on the left, under the 4 dot menu, you can uncheck [Dedicated capacity] in the advanced tab.*

We should now be configured deploy the application. This is an extensive setup, however it should be a one-time setup.
The following information should be updated in `docker-compose.yml`
```
    environment:
      - TENANT_ID=
      - CLIENT_ID=
      - AUTHORITY=https://login.microsoftonline.com/
      - SCOPE=https://analysis.windows.net/powerbi/api/.default
      - CLIENT_SECRET=
```

`TENANT_ID`, `CLIENT_ID`, `CLIENT_SECRET` are all available in `App Registrations -> Application created above`.


## PowerBI REST API OAuth tokens
---

We use the [msal](https://github.com/AzureAD/microsoft-authentication-library-for-python) library for Python to generate OAuth access tokens. To generate a token, send a GET request to `/api/token/`, which will return a JSON object in the following format:

```
{
    "access_token": "[OAUTH ACCESS TOKEN]"
}
```

These access tokens have an expiry time of one hour and are cached in the session. If a token that expires in 30 minutes or later exists, calling the API again will return the existing token.
This token is used in the Authorization header when using the PowerBI REST API:

`Authorization: Bearer [OAUTH ACCESS TOKEN]`

This token is now consumed in the frontend and is added whenever we make a PowerBI Rest API Call.

