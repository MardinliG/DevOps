
# Exercice 2 - Écrire votre premier prometheus.yml

- Arrêter le conteneur précédent : ```docker rm -f prometheus```

- Créer un fichier ```prometheus.yml``` sur l'hôte avec les paramètres demandés 

    ```nano prometheus.yml```

    ```
    global:
    scrape_interval: 15s
    external_labels:
        environment: lab

    scrape_configs:
    - job_name: 'prometheus'
        static_configs:
        - targets: ['localhost:9090']
    ```


- Lancer un nouveau conteneur avec --web.enable-lifecycle et le fichier monté sur /etc/prometheus/prometheus.yml

    ``` 
    docker run -d \
    --name prometheus \
    -p 9090:9090 \
    -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml \
    prom/prometheus:latest \
    --config.file=/etc/prometheus/prometheus.yml \
    --web.enable-lifecycle
    ```

- Modifier le fichier puis déclencher un rechargement : curl -X POST http://localhost:9090/-/reload

    ```nano prometheus.yml```
    
    On modifie scrape_interval a 10s

    
    ```
    global:
    scrape_interval: 10s
    external_labels:
        environment: lab

    scrape_configs:
    - job_name: 'prometheus'
        static_configs:
        - targets: ['localhost:9090']
    ```

Apres on execute curl -X POST http://localhost:9090/-/reload

Ensuite va sur http://localhost:9090 → Status > Target Health et on vérifie qu'on voit bien evaluation_interval: 10s.

