
# Exercice 3 - Ajouter node_exporter et scraper les métriques système

- Lancer node_exporter : ``` docker run -d --name node-exporter -p 9100:9100 prom/node-exporter:latest ```

- Ajouter un nouveau job nommé 'node' dans prometheus.yml pointant vers host.docker.internal:9100 (Mac/Windows) ou l'IP du conteneur (Linux)

    ```
    global:
    scrape_interval: 10s
    external_labels:
        environment: lab

    scrape_configs:
    - job_name: 'prometheus'
        static_configs:
        - targets: ['localhost:9090']

    - job_name: 'node'
        static_configs:
        - targets: ['172.17.0.1:9100'] //ip du conteneur docker
    ```

- Déclencher un rechargement (ou recréer le conteneur) puis confirmer que la cible est UP

    ``` curl -X POST http://localhost:9090/-/reload ```

    Ensuite va sur http://localhost:9090 → Status > Target Health
    et on verifie que le job node est bien UP

- Exécuter la requête : node_cpu_seconds_total dans l'expression browser

    On va sur http://localhost:9090/ et dans la barre de recherche on tape ```node_cpu_seconds_total```

    et on doit voir des trucs comme ca :

    node_cpu_seconds_total{cpu="0", instance="172.17.0.1:9100", job="node", mode="idle"} 6213.12

    ...

    node_cpu_seconds_total{cpu="1", instance="172.17.0.1:9100", job="node", mode="idle"}	6250.03

    ...

    
