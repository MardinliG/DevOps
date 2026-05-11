# Exercice 1 - Installer Prometheus et accéder à l'interface web

- 1.1 Récupérer l'image :  ```docker pull prom/prometheus:latest```


- 1.2 La lancer : ```docker run -d --name prometheus -p 9090:9090 prom/prometheus:latest```

- 1.3 Ouvrir ```http://localhost:9090``` dans votre navigateur

- 1.5 Exécuter docker logs prometheus et lire la ligne de démarrage qui annonce le répertoire de stockage

    ```docker logs prometheus```

    
    ```time=2026-05-11T07:41:23.369Z level=INFO source=main.go:851 msg="Starting Prometheus Server" mode=server version="(version=3.11.3, branch=HEAD, revision=eb173f5256d4022afba1e9bc3d19740a76859fae)"```

