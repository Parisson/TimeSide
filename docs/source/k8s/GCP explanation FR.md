Document explicatif pour l’utilisation de *GCP*
===============================================

Dans ce document vous allez apprendre à utiliser principalement *GCP*
pour TimeSide mais également pour d’autre utilisation.

Nous verrons donc dans ce document :

-   Qu’est ce que *GCP* ?
-   Que faire maintenant que l’on sait ce qu’est GCP ?
-   Explication de la page d’accueil
-   Explication de la barre de menu principal
-   Explication du navigation menu
-   Quelques points supplémentaire à savoir
-   Quelques commandes et exemple
-   Pour créer une **VM LINUX**
-   Pour créer une **VM WINDOWS**
-   Création **KUBERNETES**
-   TUTORIEL
-   **Kompose** un moyen d’obtenir des fichier .yaml
-   

### Qu’est ce que *GCP* ?

Premièrement vous devez savoir ce qu’est *GCP* avant de continuer. Il
s’agit du sigle de **Google Cloud Platform** et est une plateforme de
cloud computing fournie par Google, proposant un hébergement sur la même
infrastructure que celle que Google utilise en interne comme pour son
moteur de recherche. *Cloud Platform* fournit aux développeurs des
produits permettant de construire une gamme de programmes allant de
simples sites web à des applications complexes.

*GCP* fait partie d'un ensemble de solutions pour les entreprises appelé
**Google Cloud**, et fournit des services modulaires basés sur le cloud,
tels que le stockage d'informations, le calcul, des applications de
traduction et de prévision, etc.

### Que faire maintenant que l’on sait ce qu’est GCP ?

L’une des premières chose serait de comprendre le menu de navigation et
l’accueil.

##### Voici un exemple de la page d’accueil et son explication :

![accueil
GCP](https://cloud.google.com/docs/images/overview/console.png?hl=fr)

Le corps de la page contient plusieurs widgets personnalisables
différents qui fournissent des informations, des rapports, des
statistiques et de l'aide concernant le projet en cours et GCP en
général. Chacun d'eux propose un menu contextuel qui permet soit
d'accéder à la documentation associée, soit de masquer ce widget et
presque tous fournissent en bas un bouton de navigation qui mènera au
service associé, certains d'entre eux offriront des choix
supplémentaires en fonction de leur contenu, comme éditer le graphique
ou en ajouter d’autre.

Pour en revenir à la description de l’image :

1.  **Project info** — it specifies the basic information related to the
    current project, like *name*, *ID*, *number*.
2.  **Resources** — it lists the main resources/components used in the
    project.
3.  **Trace** — if Stackdriver Trace is enabled, it provides the latest
    trace data.
4.  **Getting started** — it links to quick tutorials of the most common
    operations.
5.  **APIs** — a graph showing the requests per second to the *APIs*
    used by the project.
6.  **Computer Engine** — it shows a graph related to the usage of one
    instance of **Computer Engine**, by default it’s count/sec, but you
    can specify different parameters for the main graph or add a new
    one.
7.  **Google Cloud Platform Status** — as the name implies it reports
    the status of **GCP** *services*, in the unlikely scenario that some
    outage occurs.
8.  **Billing** — it shows an estimate of the charges related to this
    project in the current period.
9.  **Error reporting** — it shows the last 24 hours errors collected by
    Stackdriver error reporting.
10. **News** — It aggregates the feeds of news related to **GCP** and
    **Cloud** in general.
11. **Documentation** — Hot links to **GCP** documentation.

##### Si nous montons en haut de la page nous atteignons la barre de menu principale :

1.  **Navigation menu** — it expands and lists all the most relevant
    **GCP** component grouped by category, more on this later.
2.  **Navigation link to the Dashboard** — useful if you’re in a
    product’s page and you want to quickly navigate back.
3.  **Project selector** — it will display a pop-up window allowing you
    to select the current project.
4.  **Search bar** — it allows you to search full text among the
    products, services and functionalities offered by GCP.
5.  **Cloud Shell** — this button provides command-line access to a
    virtual machine instance in a terminal window that opens in the web
    console, more on this later.
6.  **Help** — it shows a contextual pop-up window with articles and
    support options.
7.  **Notifications** — it will aggregate and notify about relevant
    events regarding your project and account.
8.  **Settings** — it allows you to set your project preferences, a
    direct link to tools downloads, ect...
9.  **Google Account** — as it’s easy to guess it shows information
    related to the account with which you’re currently logged in,
    allowing you to log out or add other accounts.

##### Explication Navigation menu

Maintenant penchons nous plus sur le **Navigation menu**, en cliquant
dessus un menu s’ouvre et propose beaucoup de catégories. Nous
traiterons les catégories en général et non point par point pour plus
d’information sur ces catégories utiliser ce [lien](https://cloud.google.com/docs/overview/cloud-platform-services\#top\_of\_page).

 | Catégorie | Utilité |
| ------------- | -------- |
|**Compute** | héberge une variété de types de machines qui prennent en charge tout type de charge de travail. Les différentes options informatiques vous permettent de décider dans quelle mesure vous souhaitez vous impliquer dans les détails opérationnels et l'infrastructure, entre autres.|
|**Storage** | stockage de données et options de base de données pour les données structurées ou non structurées, relationnelles ou non relationnelles.|
|**Networking** | services qui équilibrent le trafic applicatif et prévoient entre autres des règles de sécurité.|
|**Cloud Operations** | une suite d'outils de journalisation, de surveillance, de suivi et d'autres outils de fiabilité des services inter-cloud.|
|**Tools** | services pour les développeurs gérant les déploiements et les pipelines de création d'applications.|
|**Big Data** | services qui vous permettent de traiter et d'analyser de grands ensembles de données.|
|**Artificial Intelligence** | une suite d'API qui exécutent des tâches spécifiques d'intelligence artificielle et d'apprentissage automatique sur Google Cloud.|


##### Quelques points supplémentaire à savoir :

Dans le menu de navigation, près du haut, se trouve **IAM et admin**.
Cela amènera à une page qui contient une liste d'utilisateurs, qui
spécifie les autorisations et les rôles accordés à certains comptes.

En voici un tableau :

|Nom de rôle | Autorisations|
|---------------- | -----------------|
|rôles / spectateur | Autorisations pour les actions en lecture seule qui n'affectent pas l'état, telles que l'affichage (mais pas la modification) des ressources ou données existantes.|
|rôles / éditeur | Toutes les autorisations de visionneuse, plus les autorisations pour les actions qui modifient l'état, telles que la modification des ressources existantes.|
|rôles / propriétaire | Toutes les autorisations et autorisations de l'éditeur pour les actions suivantes: Gérer les rôles et les autorisations pour un projet et toutes les ressources du projet; Configurer la facturation d'un projet.|


Dans le menu de navigation, près du haut, se trouve **API et services \>
Bibliothèque**. Cela amènera à une page qui contient une liste des *API*
et dans le menu de gauche différentes types de catégories seront
proposées. Si l’on cherche une API en particulier il suffit de la
chercher dans la barre de recherche en haut de la page.

On peut également en savoir plus sur les API en consultant le nouvel
outil pratique de Google Cloud appelé [Google APIs Explorer](https://developers.google.com/apis-explorer/\#p/).

**GCP** possède également son propre invite de commande : **CLOUD
SHELL**. When you press the button, your personal Admin Machine will be
instantiated and you’ll connect to it. You will have terminal access to
a command-line Linux environment, with persistent storage (5 Gb) from
which you can manage all your cloud resources. The most common
development tools are pre-installed as well as the most used admin tools
like Docker, Kubernetes, MySql. The Cloud Shell Environment is a docker
container, there is a default, Google maintained one, but it’s possible
to specify a different one if you fancy so. Cloud Shell also includes a
few nice treats, like a Web Preview for your services and an online
visual code editor.

gcloud auth list Cette commande affiche une - liste d'authentification -
qui répertorie les comptes authentifiés dans notre projet Google Cloud.

### Quelques commandes et exemple

Après avoir vu la base de **GCP** il est tant de voir quelques exemples
intéressant et ainsi comprendre la facilité pour créer ce qui est
nécessaire avec **GCP**.

##### Pour créer une **VM LINUX** on a 2 façon :

-   Avec la console cloud : **menu Navigation \> Compute Engine \>
    Instances VM** puis remplir les champs et finir par faire **créer**.
    Puis la machine devrait apparaître dans **Instances VM**.

-   Avec **gcloud** : Il suffit de suivre les commandes suivante en les
    rentrant dans **CLOUD SHELL** :
    `'' gcloud compute instances create gcelab2 --machine-type n1-standard-2 --zone us-central1-c`
    ''

`''gcloud compute instances create --help` '' (si ont veut voir les
valeur par défaut)

Si l’on travail toujours dans le même région et zone rentrer ces deux
commande évitera de devoir les préciser lors de la création :
`''gcloud config set compute/zone (name_zone)` ''

`''gcloud config set compute/region (name_region)` ''

(On n’aura plus à préciser --zone a chaque fois.)

Pour utiliser le SSH avec gcloud il faut faire :
`''gcloud compute ssh gcelab2 --zone us-central1-c` '' Puis suivre ce
qui est dit et finir par sortir avec exit. Pour installer un serveur
NGINX : `''sudo su -` '' `''apt-get update` '' (mettre à jour le système
d’exploitation) `''apt-get install nginx -y` '' (installer nginx)
`''ps auwx | grep nginx` ''(verifier nginx) Puis ouvrir nouvelle page et
aller : http://EXTERNAL\_IP/

gcloud propose une commande pour plus d’information sur son projet
notamment pour savoir les zones et régions par défaut:
`''gcloud compute project-info describe --project <your_project_ID>` ''

Variable d’environnement : `''export PROJECT_ID=<your_project_ID>` ''

Il serait donc possible de faire cette commande pour créer une VM :
`''gcloud compute instances create gcelab2 --machine-type n1-standard-2 --zone $ZONE`
''

##### Pour créer une **VM WINDOWS** suivre ce [tuto](https://google.qwiklabs.com/focuses/560?parent=catalog).

##### Création **KUBERNETES**

*Création cluster* : `''gcloud container clusters create [CLUSTER-NAME]`
''

*Authentifier le cluster* :
`''gcloud container clusters get-credentials [CLUSTER-NAME]` ''

*Déployer une application* :
`''kubectl create deployment hello-server --image=gcr.io/google-samples/hello-app:1.0`
''

*Création service* :
`''kubectl expose deployment hello-server --type=LoadBalancer --port 8080`
''

*Vérifier le svc* : `''kubectl get service` ''

*Pour se connecter* : `''http://[EXTERNAL-IP]:8080` ''

*Pour nettoyer* : `''gcloud container clusters delete [CLUSTER-NAME]` ''

##### TUTORIEL

[qwiklabs](https://www.qwiklabs.com/) propose des tutoriels pour GCP
mais attention certains (presque tous) nécessite des crédits qui sont
payant mais peuvent être obtenue sur internet avec certains code gratuit
offrant quelque crédit. Durant ces tutoriels ont disposent d’un compte
**GCP** pendant un temps déterminé par un compteur qui définit le temps
nécessaire pour faire ce tutoriel.

Ou d’autre tuto sont trouvable sur [cloud.google.com](https://cloud.google.com).

### **Kompose** un moyen d’obtenir des fichier .yaml

Pour créer un **KUBERNETES** des fichier .yaml sont nécessaire et afin
de se faciliter la vie il existe un moyen mis en place par Kubernetes
pour transformer un fichier .yml en .yaml et il s’agit de **Kompose**.

Kompose c'est un outil de conversion de tout ce qui compose (notamment
Docker Compose) en orchestrateurs de conteneurs (Kubernetes ou
OpenShift). Vous trouverez plus d'informations sur le site web de
[Kompose](http://kompose.io).

Voici les commande a suivre afin d’arriver à nos fin :

Premièrement aller dans le répertoire contenant le fichier
“docker-compose.yml”.

puis lancer la commande : `''kompose up` '' (Si plusieurs docker-compose
il y a une possibilité de faire ça :
`''kompose --file ./examples/docker-compose.yml up` '' **attention un
cluster Kubernetes en cours d'exécution avec kubectl pré-configuré doit
être disponible.** Et seuls les déploiements et les services sont
générés et déployés dans Kubernetes. Si besoin d'autres types de
ressources, utiliser les commandes `''kompose convert` '' et
`''kubectl apply -f` '' à la place. Si probleme de type :
`''FATA Error while deploying application: Get https://127.0.0.1:6443/api: dial tcp 127.0.0.1:6443: connect: connection refused`
'' rajouter apres **up** --server suivi de l’adresse du cluster
kubernetes donner par `''kubectl cluster-info` '')

Maintenant convertir le fichier “docker-compose.yml” en fichiers
utilisable avec kubectl, lancer : `''kompose --file ‘name’ convert` ''
(va créer tout les fichiers(services,deployment) en .yaml. Pas besoin de
mentionner --file ‘name’ si seul dans le répertoire mais cette commande
peut aussi en faire plusieurs exemple : kompose -f docker-compose1.yml
-f docker-compose2.yml convert **mais attention lorsque plusieurs
fichiers de docker-compose sont fournis, la configuration est
fusionnée**.)

Et ensuite `''kubectl apply -f <output file>` '' (Cela correspondra au
déploiement existant appliqué via kompose up).

Une fois déployé l'application "composée" sur Kubernetes,
`''kompose down` '' facilitera la suppression de l'application en
supprimant ses déploiements et services. Si besoin de supprimer d'autres
ressources, l'utilisation de la commande **kubectl** sera alors utile.

Voici quelque lien utile pour comprendre :

[Convertir un fichier Docker Compose en ressources Kubernetes](https://kubernetes.io/fr/docs/tasks/configure-pod-container/translate-compose-kubernetes/)

[Pour comprendre les différentes option pour les labels](https://github.com/kubernetes/kompose/blob/master/docs/user-guide.md)

[tuto KOMPOSE](https://www.katacoda.com/courses/kubernetes/deploy-docker-compose-using-kompose)
