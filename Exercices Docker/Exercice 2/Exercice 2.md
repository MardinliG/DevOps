# Exercice 2 - Construire sa première image avec un Dockerfile

- 2.1 Écrivez ```index.html``` avec le contenu HTML minimal suivant (titre : "Ma première
image Docker" , un <h1> avec votre prénom).

```` 
<!DOCTYPE html>
<html lang="fr">

<head>
    <meta charset="UTF-8">
    <title>Ma première image Docker</title>
</head>

<body>
    <h1>Guillaume</h1>
</body>

</html>
````

- 2.2 Écrivez un ```Dockerfile``` qui : 

    Part de l'image nginx:alpine

    Copie index.html dans /usr/share/nginx/html/index.html

    Expose le port 80

```` 
FROM nginx:alpine

COPY index.html /usr/share/nginx/html/index.html

EXPOSE 80
````

- 2.3 Construisez l'image avec le tag mon-site:v1 .

    ````docker build -t mon-site:v1 .````

- 2.4 Lancez un conteneur basé sur cette image, en exposant le port 9090 → 80 , avec --
rm . Vérifiez dans le navigateur.

    ```` docker run -d --rm -p 9090:80 mon-site:v1 ````

    *On verifie dans le navigateur http://localhost:9090/ et on voit bien la page html qu'on a créé avec notre prénom*

- 2.5 Listez les images locales. Quelle est la taille de mon-site:v1 ? Comparez avec
nginx:alpine .

    ```` docker images ````

    *mon-site:v1 23e5a98f8387 92.6MB 26MB*

    *nginx:alpine 5616878291a2 93.5MB 26.9MB*

    *On peut voir que l'image alpine de nginx et notre image **mon-site** font presque la meme taille puisque notre image est construite a partire de l'iamge nginx:alpine et qu'on a ajouté qu'une simple page html*

- 2.6 Inspectez les layers de l'image avec docker history mon-site:v1 . Combien de
layers ont été ajoutés par rapport à l'image de base ?

    ***2** layers ont été ajoutés par rapport a l'image de base.* 
    
    *Le 1er qui copie le fichier **index.html** et le 2ème pour l'exposition du port.* 

- 2.7 Modifiez index.html (changez le ````<h1>```` ). Reconstruisez l'image avec le tag monsite:v2 . Quelle étape a été rechargée depuis le cache ? Quelle étape a été réexécutée ?

    Dans la page **index.html** on modifie le ````h1````

    ````<h1>Shems</h1>````

    On rebuild l'image avec le tag v2 
    ````docker build -t mon-site:v2 .````

    *Lors de la reconstruction, seule l’étape COPY index.html a été réexécutée car le fichier a été modifié. Les autres étapes ont été réutilisées depuis le cache.*

- 2.8 Supprimez l'image mon-site:v1 (sans supprimer v2 )

    ````docker rmi mon-site:v2````

    