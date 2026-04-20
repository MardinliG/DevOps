# Exercice 4 - Réseaux Docker

- 4.1 Listez les réseaux Docker existants sur votre machine. Quels sont les trois réseaux
créés par défaut ?

    ````docker network ls````

    ````
    cd9a13104935 bridge bridge local

    e11781696c9a host host local

    94b66865ec28 none null local
    ````

- 4.2 Créez un réseau bridge personnalisé nommé mon-reseau .

    ````docker network create mon-reseau````

- 4.3 Lancez un conteneur nginx:alpine nommé serveur-web connecté à mon-reseau ,
en arrière-plan.

    ````docker run -d --name serveur-web --network mon-reseau nginx:alpine````

- 4.4 Lancez un conteneur alpine nommé client connecté à mon-reseau en mode
interactif. Depuis client , effectuez un wget -qO- http://serveur-web . Que récupérezvous ? Pourquoi peut-on utiliser le nom serveur-web plutôt qu'une adresse IP ?

    ```` docker run -it --name client --network mon-reseau alpine sh`````

    ````wget -qO- http://serveur-web````

    *Ca me retourne*

    ````
    <!DOCTYPE html>
    <html>
    <head>
    <title>Welcome to nginx!</title>
    <style>
    html { color-scheme: light dark; }
    body { width: 35em; margin: 0 auto;
    font-family: Tahoma, Verdana, Arial, sans-serif; }
    </style>
    </head>
    <body>
    <h1>Welcome to nginx!</h1>
    <p>If you see this page, nginx is successfully installed and working.
    Further configuration is required for the web server, reverse proxy,
    API gateway, load balancer, content cache, or other features.</p>

    <p>For online documentation and support please refer to
    <a href="https://nginx.org/">nginx.org</a>.<br/>
    To engage with the community please visit
    <a href="https://community.nginx.org/">community.nginx.org</a>.<br/>
    For enterprise grade support, professional services, additional
    security features and capabilities please refer to
    <a href="https://f5.com/nginx">f5.com/nginx</a>.</p>

    <p><em>Thank you for using nginx.</em></p>
    </body>
    </html>
    ````

- 4.5 Quittez client . Lancez un nouveau conteneur alpine nommé client-externe
sans le connecter à mon-reseau (réseau par défaut). Essayez de joindre serveur-web
par son nom. Que se passe-t-il ? Pourquoi ?

    ````docker run -it --name client-externe nginx:alpine sh````

    ````wget -qO- http://serveur-web````

    *Ca retourne*

    ````wget: bad address 'serveur-web'````

- 4.6 Quelle commande permet de connecter client-externe à mon-reseau après son
démarrage ?

    ````docker network connect mon-reseau client-externe````

- 4.7 Nettoyez : arrêtez et supprimez tous les conteneurs créés dans cet exercice, puis
supprimez mon-reseau .

    ````
    docker rm -f client-externe
    docker rm -f client
    docker rm -f serveur-web

    docker network rm mon-reseau
    ````

    