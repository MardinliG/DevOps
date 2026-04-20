# Exercice 1 — Premier contact avec Docker

- 1.1 Téléchargez l'image nginx:alpine depuis Docker Hub sans lancer de conteneur.

    ``` docker pull nginx:alpine ```

- 1.2 Lancez un conteneur nginx:alpine nommé mon-nginx en arrière-plan, en exposant
le port 8080 de votre machine sur le port 80 du conteneur

    ``` docker run -d --name mon-nginx -p 8080:80 nginx:alpine ```

- 1.3  Vérifiez que le conteneur tourne. Quelle commande permet de lister uniquement les
conteneurs en cours d'exécution ?

    ``` docker ps ```

- 1.4 Ouvrez http://localhost:8080 dans votre navigateur (ou avec curl ). Que voyezvous ?

    
    Je vois la page par défaut nginx 
    
    *Welcome to nginx!
    If you see this page, nginx is successfully installed and working. Further configuration is required for the web server, reverse proxy, API gateway, load balancer, content cache, or other features.*

    *For online documentation and support please refer to nginx.org.
    To engage with the community please visit community.nginx.org.
    For enterprise grade support, professional services, additional security features and capabilities please refer to f5.com/nginx.*

    *Thank you for using nginx.* 

- 1.5 Affichez les logs du conteneur mon-nginx

    ```` docker logs mon-nginx ````

- 1.6 Arrêtez le conteneur mon-nginx sans le supprimer.

    ```` docker stop mon-nginx ````

    Puis listez tous les conteneurs (y compris arrêtés).

    ```` docker ps -a ````

    Quelle est la différence avec la commande de la question 1.3 ?

    *La commande **docker ps** affiche les conteneurs qui sont en cours d'execution et **docker ps -a** affiche litteralement tous les conteneurs meme ceux qui sont arretés*

- 1.7 Supprimez le conteneur mon-nginx .

    ```` docker rm mon-nginx ````

     Vérifiez qu'il n'existe plus.

     ```` docker ps -a `````

     *Il existe plus*

- 1.8 Quelle commande aurait permis de lancer le conteneur de façon à ce qu'il soit
automatiquement supprimé à l'arrêt ?

    ```` docker run -d --rm --name mon-nginx -p 8080:80 nginx:alpine ````
    
    *l'option --rm permet de supprimer le conteneur automatiquement quand il s'arrete*
