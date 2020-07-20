Explanatory document for the use of \* GCP \*
=============================================

In this document you will learn how to use mainly \* GCP \* for TimeSide
but also for other use.

We will therefore see in this document:

-   What is \* GCP \*?
-   What to do now that we know what GCP is?
-   Explanation of the home page
-   Explanation of the main menu bar
-   Explanation of the menu navigation
-   Some additional points to know
-   Some commands and example
-   To create a \*\* VM LINUX \*\*
-   To create a \*\* VM WINDOWS \*\*
-   Creation \*\* KUBERNETES \*\*
-   TUTORIAL
-   \*\* Kompose \*\* a means of obtaining .yaml files
-   

### What is \* GCP \*?

First you need to know what \* GCP \* is before you continue. It is the
acronym of \*\* Google Cloud Platform \*\* and is a cloud computing
platform provided by Google, offering accommodation on the same
infrastructure as that which Google uses internally as for its search
engine. \* Cloud Platform \* provides developers with products to build
a range of programs from simple websites to complex applications.

-   GCP \* is part of a set of solutions for companies called \*\*
    Google Cloud \*\*, and provides modular cloud-based services, such
    as information storage, calculation, translation and forecasting
    applications , etc.

### What to do now that we know what GCP is?

One of the first things would be to understand the navigation menu and
the welcome.

##### is an example of the home and its explanation

![home
GCP](https://cloud.google.com/docs/images/overview/console.png?hl=fr)

The body of the page contains several different customizable widgets
that provide information, reports, statistics and help regarding the
current project and GCP in general. Each of them offers a contextual
menu which allows either to access the associated documentation, or to
hide this widget and almost all of them provide a navigation button at
the bottom which will lead to the associated service, some of them will
offer additional choices in according to their content, such as editing
the graph or adding others.

Going back to the description of the image:

1.  \*\* Project info \*\* - it specifies the basic information related
    to the current project, like \* name *, * ID *, * number \*.
2.  \*\* Resources \*\* - it lists the main resources / components used
    in the project.
3.  \*\* Trace \*\* - if Stackdriver Trace is enabled, it provides the
    latest trace data.
4.  \*\* Getting started \*\* - it links to quick tutorials of the most
    common operations.
5.  \*\* APIs \*\* - a graph showing the requests per second to the \*
    APIs \* used by the project.
6.  \*\* Computer Engine \*\* - it shows a graph related to the usage of
    one instance of \*\* Computer Engine \*\*, by default it's count /
    sec, but you can specify different parameters for the main graph or
    add a new one .
7.  \*\* Google Cloud Platform Status \*\* - as the name implies it
    reports the status of \*\* GCP \*\* \* services \*, in the unlikely
    scenario that some outage occurs.
8.  \*\* Billing \*\* - it shows an estimate of the charges related to
    this project in the current period.
9.  \*\* Error reporting \*\* - it shows the last 24 hours errors
    collected by Stackdriver error reporting.
10. \*\* News \*\* - It aggregates the feeds of news related to \*\* GCP
    \*\* and \*\* Cloud \*\* in general.
11. \*\* Documentation \*\* - Hot links to \*\* GCP \*\* documentation.

##### If we go to the top of the page we reach the main menu bar:

1.  \*\* Navigation menu \*\* - it expands and lists all the most
    relevant \*\* GCP \*\* component grouped by category, more on this
    later.
2.  \*\* Navigation link to the Dashboard \*\* - useful if you're in a
    product's page and you want to quickly navigate back.
3.  \*\* Project selector \*\* - it will display a pop-up window
    allowing you to select the current project.
4.  \*\* Search bar \*\* - it allows you to search full text among the
    products, services and functionalities offered by GCP.
5.  \*\* Cloud Shell \*\* - this button provides command-line access to
    a virtual machine instance in a terminal window that opens in the
    web console, more on this later.
6.  \*\* Help \*\* - it shows a contextual pop-up window with articles
    and support options.
7.  \*\* Notifications \*\* - it will aggregate and notify about
    relevant events regarding your project and account.
8.  \*\* Settings \*\* - it allows you to set your project preferences,
    a direct link to tools downloads, ect ...
9.  \*\* Google Account \*\* - as it's easy to guess it shows
    information related to the account with which you're currently
    logged in, allowing you to log out or add other accounts.

##### Explanation Navigation menu

Now let's take a closer look at the \*\* Navigation menu \*\*, by
clicking on it a menu opens and offers a lot of categories. We will
treat the categories in general and not point by point for more
information on these categories use this
[link](https://cloud.google.com/docs/overview/cloud-platform-services#top_of_page).

  Category                            Utility
  ----------------------------------- -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  \*\* Compute \*\*                   hosts a variety of machine types that support any type of workload. The different IT options allow you to decide to what extent you want to get involved in operational details and infrastructure, among others.
  \*\* Storage \*\*                   data storage and database options for structured or unstructured, relational or non-relational data.
  \*\* Networking \*\*                services that balance application traffic and provide, among other things, security rules.
  \*\* Cloud Operations \*\*          a suite of logging, monitoring, tracking, and other reliability tools for inter-cloud services
  \*\* Tools \*\*                     services for developers managing application creation deployments and pipelines.
  \*\* Big Data \*\*                  services that allow you to process and analyze large data sets.
  \*\* Artificial Intelligence \*\*   a suite of APIs that perform specific artificial intelligence and machine learning tasks on Google Cloud.

##### Some additional points to know:

In the navigation menu, near the top, is \*\* IAM and admin \*\*. This
will take you to a page that contains a list of users, which specifies
the permissions and roles granted to certain accounts.

Here is a table:

  Role name           Authorizations
  ------------------- -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  roles / spectator   Permissions for read-only actions that do not affect the state, such as viewing (but not editing) existing resources or data.
  roles / editor      All viewer permissions, plus permissions for actions that change the state, such as modifying existing resources.
  roles / owner       All permissions and permissions from the editor for the following actions: Manage roles and permissions for a project and all project resources; Configure billing for a project.

In the navigation menu near the top is \*\* API and services\> Library
\*\*. This will take you to a page that contains a list of \* APIs \*
and in the left menu different types of categories will be offered. If
you are looking for a particular API just search for it in the search
bar at the top of the page.

You can also learn more about the APIs by consulting the new practical
tool from Google Cloud called [Google APIs
Explorer](https://developers.google.com/apis-explorer/#p/).

\*\* GCP \*\* also has its own command prompt: \*\* CLOUD SHELL \*\*.
When you press the button, your personal Admin Machine will be
instantiated and you'll connect to it. You will have terminal access to
a command-line Linux environment, with persistent storage (5 Gb) from
which you can manage all your cloud resources. The most common
development tools are pre-installed as well as the most used admin tools
like Docker, Kubernetes, MySql. The Cloud Shell Environment is a docker
container, there is a default, Google maintained one, but it's possible
to specify a different one if you fancy so. Cloud Shell also includes a
few nice treats, like a Web Preview for your services and an online
visual code editor.

gcloud auth list This command displays an - authentication list - which
lists the accounts authenticated in our Google Cloud project.

### Some commands and example

After having seen the basis of \*\* GCP \*\* it is so much to see some
interesting examples and thus understand the facility to create what is
necessary with \*\* GCP \*\*.

##### To create a \*\* VM LINUX \*\* we have 2 ways:

-   With the cloud console: \*\* Navigation menu\> Compute Engine\> VM
    Instances \*\* then fill in the fields and end up doing \*\* create
    \*\* . Then the machine should appear in \*\* VM Instances \*\*.

-   With \*\* gcloud **: Just follow the following commands by entering
    them in ** CLOUD SHELL \*\*:
    `'' gcloud compute instances create gcelab2 --machine-type n1-standard-2 --zone us- central1-c`
    ''

`'' gcloud compute instances create --help` '' (if we want to see the
default values)

If we always work in the same region and zone enter these two commands
will avoid have to specify them during creation:
`'' gcloud config set compute / zone (name_zone)` ''

`'' gcloud config set compute / region (name_region)` ''

(We will no longer have to specify --zone every time.)

To use SSH with gcloud you have to do:
`'' gcloud compute ssh gcelab2 --zone us-central1-c` '' Then follow what
is said and finally exit with exit . To install an NGINX server:
`'' sudo su -` '' `'' apt-get update` '' (update the operating system)
`'' apt-get install nginx -y` '' (install nginx)
`'' ps auwx | grep nginx` '' (check nginx) Then open new page and go:
http: // EXTERNAL\_IP /

gcloud offers an order for more information on his project in particular
to know the default zones and regions:
`'' gcloud compute project-info describe --project <your_project_ID>` ''

Environment variable: `'' export PROJECT_ID = <your_project_ID>` ''

It would therefore be possible to issue this command to create a VM:
`' 'gcloud compute instances create gcelab2 --machine-type n1-standard-2 --zone $ ZONE`'
'

##### To create a \*\* VM WINDOWS \*\* follow this [tutorial](https:%20//%20google%20.qwiklabs.com%20/%20focuses%20/%20560?%20parent%20=%20catalog).

##### Creation \*\* KUBERNETES \*\*

-   Creation cluster \*:
    `'' gcloud container clusters create [CLUSTER-NAME]` ''

-   Authenticate cluster \*:
    `'' gcloud container clusters get-credentials [ CLUSTER-NAME]` ''

-   Deploy an application \*:
    `'' 'kubectl create deployment hello-server --image = gcr.io / google-samples / hello-app: 1.0`'
    '

-   Creation service \*:
    `'' kubectl expose deployment hello-server --type = LoadBalancer --port 8080`
    ''

-   Check svc \*: `'' 'kubectl get service`' '

-   To connect \*: \`\`' ' http: // [EXTERNAL-IP]: 8080''

-   To clean \*:
    \`\``'' 'gcloud container clusters delete [CLUSTER-NAME]`' '

##### TUTORIAL

[qwiklabs](https:%20/%20/www.qwiklabs.com/) offers tutorials for GCP but
beware some (almost all) require credits which are paid but can be
obtained on the internet with some free code offering some credit.
During these tutorials have a \*\* GCP \*\* account for a time
determined by a counter which defines the time necessary to do this
tutorial.

Or other tutorial can be found on
[cloud.google.com](https://cloud.google.com).

### \*\* Kompose \*\* a way to obtain .yaml files

To create a \*\* KUBERNETES \*\* .yaml files are necessary and in order
to make life easier there is a way set up by Kubernetes to transform a
.yml file in .yaml and it is \*\* Kompose \*\*.

Kompose is a tool for converting everything that composes (notably
Docker Compose) into container orchestrators (Kubernetes or OpenShift).
More information can be found on the [Kompose](http://kompose.io)
website.

Here are the commands to follow in order to reach our end:

First go to the directory containing the file “docker-compose.yml”.

then launch the command: `'' kompose up` '' (If more than one
docker-compose there is a possibility to do this:
`'' kompose --file ./examples/docker-compose.yml up` "\*\* beware a
running Kubernetes cluster with pre-configured kubectl must be
available. ** And only deployments and services are generated and
deployed in Kubernetes. If need other types of resources, use commands
`'' kompose convert` '' and `'' kubectl apply -f` '' instead. If problem
type:
`'' FATA Error while deploying application: Get https://127.0.0.1 : 6443 / api: dial tcp 127.0.0.1:6443: connect: connection refused`
'' add after ** up \*\* --server followed by the address of the
kubernetes cluster give by `` '' kubectl cluster-info` `` '')

Now convert the file “docker-compose.yml” into files usable with
kubectl, launch: `'' kompose --file 'name' convert` '' (will create all
the files (services, deployment) in .yaml, no need to mention --file
'name 'if alone in the directory but this command can also make several
examples: kompose -f docker-compose1.yml -f docker-compose2.yml convert
\*\* but be careful when several files of docker-compose are provided,
the configuration is merged \*\*.)

And then `'' kubectl apply -f <output file>` '' (This will correspond to
the existing deployment applied via kompose up).

Once deployed the application "composed" on Kubernetes,
`'' kompose down` '' will facilitate the deletion of the application by
deleting its deployments and services. If need to delete other
resources, the use of the \*\* kubectl \*\* command will be useful.

Here is some useful link to understand:

[Convert a Docker Compose file to Kubernetes
resources](https://kubernetes.io/en/docs/tasks/configure-pod-container/translate-compose-kubernetes/)

[To understand the different option for
labels](https://github.com/kubernetes/kompose/blob/master/docs/user-guide.md)

[tuto
KOMPOSE](https://www.katacoda.com/courses/kourses/-docker-compose-using-kompose)
