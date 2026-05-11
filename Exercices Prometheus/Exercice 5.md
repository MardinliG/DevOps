
# Exercice 5 - Règles d'enregistrement (recording rules)

- Créer rules/api_rules.yml avec un seul groupe et une seule règle

    ``` mkdir/rules```

    ``` cd rules/ ```

    ``` nano api_rules.yml```

    ```
    groups:
    - name: recording_rules
        interval: 30s
        rules:
        - record: job:node_cpu:rate5m
            expr: sum by (job) (rate(node_cpu_seconds_total[5m]))
    ```

- Dans prometheus.yml, ajouter rule_files: ['/etc/prometheus/rules/*.yml']

    ```
    global:
    scrape_interval: 10s
    external_labels:
        environment: lab

    rule_files:
    - '/etc/prometheus/rules/*.yml'

    scrape_configs:
    - job_name: 'file-sd'
        file_sd_configs:
        - files:
            - '/etc/prometheus/sd/*.json'
            refresh_interval: 5s
    ```

- Recharger Prometheus 

    ```
    docker rm -f prometheus

    docker run -d \
    --name prometheus \
    -p 9090:9090 \
    -v /home/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml \
    -v /home/prometheus/targets.json:/etc/prometheus/sd/targets.json \
    -v /home/prometheus/rules:/etc/prometheus/rules \
    prom/prometheus:latest \
    --config.file=/etc/prometheus/prometheus.yml \
    --web.enable-lifecycle
    ```

- Interroger la nouvelle métrique job:http_requests:rate5m et vérifier qu'elle renvoie des données

    On va sur http://localhost:9090/query

    et on interoge la nouvelle metric ```job:node_cpu:rate5m```

    ```job:node_cpu:rate5m{job="node"}	1.9942068965517283```