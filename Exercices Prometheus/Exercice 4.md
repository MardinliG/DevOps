
# Exercice 4 - Découverte de service : par fichier 

- Créer un fichier targets.json contenant deux endpoints

    ``` nano targets.josn```

    ```
    [
    {
        "targets": ["172.17.0.1:9100"],
        "labels": {
        "job": "node"
        }
    },
    {
        "targets": ["172.17.0.1:9090"],
        "labels": {
        "job": "prometheus"
        }
    }
    ]
    ```
- Le monter sur /etc/prometheus/sd/targets.json

    Remplacer les static_configs d'un job par file_sd_configs pointant vers /etc/prometheus/sd/*.json

    ``` nano /home/prometheus/prometheus.yml ```

    ```
    global:
    scrape_interval: 10s
    external_labels:
        environment: lab

    scrape_configs:
    - job_name: 'file-sd'
        file_sd_configs:
        - files:
            - '/etc/prometheus/sd/*.json'
            refresh_interval: 5s
    ```

    ```docker rm -f prometheus```

    ```
    docker run -d \
    --name prometheus \
    -p 9090:9090 \
    -v /home/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml \
    -v /home/prometheus/targets.json:/etc/prometheus/sd/targets.json \
    prom/prometheus:latest \
    --config.file=/etc/prometheus/prometheus.yml \
    --web.enable-lifecycle
  ```

- Ajouter ou retirer une cible du JSON et confirmer que Prometheus la prend en compte sans rechargement

    On modifie ```targets.json```

    ```
    [
    {
        "targets": ["172.17.0.1:9100"],
        "labels": {
        "job": "node"
        }
    },
    {
        "targets": ["172.17.0.1:9090"],
        "labels": {
        "job": "prometheus"
        }
    },
    {
        "targets": ["172.17.0.1:8000"],
        "labels": {
        "job": "demo-api"
        }
    }
    ]
    ```

    Et on va voir sur http://localhost:9090/targets 
    le nouveau job doit apparaitre. 