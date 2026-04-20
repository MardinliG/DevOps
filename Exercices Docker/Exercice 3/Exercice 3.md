# Exercice 3 - Volumes et persistance des données

- 3.1 Lancez un conteneur alpine en mode interactif ( -it ) avec --rm . À l'intérieur, créez
le fichier /data/test.txt avec le contenu "bonjour" . Quittez ( exit ). Relancez un
nouveau conteneur alpine . Le fichier existe-t-il ? Expliquez pourquoi.

    ````docker run -it --rm alpine````

    ````mkdir -p /data && echo "bonjour" > /data/test.txt````

    ````exit````

    ````docker run -it --rm alpine ls /data/test.txt ls: /data/test.txt````

    *Ca nous return **No such file or directory** ca confirme donc que le fichier n'existe pas*

- 3.2 — Bind mount : Créez un dossier exercice-3/html/ sur votre machine. Placez-y un
fichier index.html . Lancez un conteneur nginx:alpine en montant ce dossier dans /
usr/share/nginx/html avec -v . Modifiez index.html sur votre machine (sans
redémarrer le conteneur) et rafraîchissez le navigateur. Que constatez-vous ?

    ````docker run -d -p 8080:80 -v "%cd%\html:/usr/share/nginx/html" nginx:alpine````


- 3.3 — Volume nommé : Créez un volume Docker nommé mes-donnees .

    ```` docker volume create mes-donnees ````

- 3.4 Lancez un conteneur alpine avec --rm en montant mes-donnees sur /data . Dans
le conteneur, créez /data/persistant.txt avec le contenu "je survis" . Quittez.

    ````docker run -it --rm -v mes-donnees:/data alpine````

    ````echo "je survis" > /data/persistant.txt````

    ````exit````

- 3.5 Lancez un nouveau conteneur alpine (différent du précédent) avec le même volume
monté. Le fichier /data/persistant.txt existe-t-il ? Qu'est-ce que cela démontre ?

    ````docker run --rm -v mes-donnees:/data alpine ls /data/persistant.txt````

    *Ca montre que les données survivent à la suppression du conteneur et peuvent être partagées entre plusieurs instances*

- 3.6 Listez les volumes Docker existants. Où Docker stocke-t-il physiquement ce volume sur
votre machine ?

    ```` docker volume ls ````

    Docker stocke physiquement le volume dans le repertoire */var/lib/docker/volumes/mes-donnees/_data"*

- 3.7 Supprimez le volume mes-donnees . Quelle précaution faut-il prendre avant de le
supprimer ?

    ````docker volume rm mes-donnees````

    *On ne peut pas supprimer un volume utilisé dans un conteneur actif, il faut s'assurer que tous les conteneurs qui utilisent ce volume soient arretés et supprimés*

