
# Exercice 6 - Règles d'alerte et Alertmanager

- Lancer un conteneur Alertmanager (prom/alertmanager) sur le port 9093

    ```
    docker run -d \
    --name alertmanager \
    -p 9093:9093 \
    prom/alertmanager:latest
    ```
- Créer alerts/api_alerts.yml avec une alerte HighErrorRate

    ```mkdir /home/prometheus/alerts```

    ```cd /home/prometheus/alerts```

    ```nano api_alerts.yml```

    ```
    groups:
    - name: api_alerts
        rules:
        - alert: HighCpuUsage
            expr: sum by (instance) (rate(node_cpu_seconds_total{mode!="idle"}[5m])) > 0.5
            for: 2m
            labels:
            severity: warning
            annotations:
            summary: "CPU élevé sur {{ $labels.instance }}"
            description: "Le CPU dépasse 50% depuis 2 minutes."
    ```

- Ajouter le fichier dans rule_files de prometheus.yml
- Dans prometheus.yml, ajouter alerting.alertmanagers pointant vers alertmanager:9093


    dans ```prometheus.yml```

    ```
    global:
        scrape_interval: 10s
        external_labels:
            environment: lab

        rule_files:
        - '/etc/prometheus/rules/*.yml'
        - '/etc/prometheus/alerts/*.yml'

        alerting:
        alertmanagers:
            - static_configs:
                - targets:
                    - 'alertmanager:9093'

        scrape_configs:
        - job_name: 'file-sd'
            file_sd_configs:
            - files:
                - '/etc/prometheus/sd/*.json'
                refresh_interval: 5s

    ```
- Recharger Prometheus puis injecter des erreurs dans demo-api pour déclencher l'alerte

    ```
    docker rm -f prometheus

    docker run -d \
    --name prometheus \
    -p 9090:9090 \
    -v /home/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml \
    -v /home/prometheus/targets.json:/etc/prometheus/sd/targets.json \
    -v /home/prometheus/rules:/etc/prometheus/rules \
    -v /home/prometheus/alerts:/etc/prometheus/alerts \
    prom/prometheus:latest \
    --config.file=/etc/prometheus/prometheus.yml \
    --web.enable-lifecycle
    ```

    Ensuite vérifie dans Status > Alerts que l'alerte HighCpuUsage apparaît en inactive.