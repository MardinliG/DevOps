# Exercice 5 - Containeriser un serveur Flask

- 5.1 Créez ````app.py```` :

    ````
    from flask import Flask
    import os

    app = Flask(__name__)

    @app.route("/")
    def home():
        env = os.environ.get("APP_ENV", "développement")
        return f"<h1>Flask fonctionne !</h1><p>Environnement : {env}</p>"

    @app.route("/health")
    def health():
        return {"status": "ok"}, 200

    if __name__ == "__main__":
        app.run(host="0.0.0.0", port=5000)

    `````

- 5.2 Créez ````requirements.txt```` avec Flask 3.0.3 comme unique dépendance.

    ````
    Flask==3.0.3
    ````

- 5.3 Écrivez un Dockerfile qui :
    - Part de python:3.12-slim
    - Définit /app comme répertoire de travail
    - Copie d'abord requirements.txt seul, installe les dépendances (sans cache pip), puis
    copie le reste des sources. Pourquoi cet ordre est-il important pour le cache Docker ?
    - Expose le port 5000
    - Définit la commande de démarrage avec flask run --host=0.0.0.0

    ```` Dockerfile ```` :

    ````
    FROM python:3.12-slim

    WORKDIR /app

    COPY requirements.txt .

    RUN pip install --no-cache-dir -r requirements.txt

    COPY . .

    EXPOSE 5000

    CMD ["flask", "run", "--host=0.0.0.0"]
    ````
    *L’ordre est important car Docker utilise un cache. Si requirements.txt est copié en premier, les dépendances ne sont pas réinstallées quand seul le code change, ce qui rend la construction de l'image plus rapide.*

- 5.4 Construisez l'image flask-app:v1 .

    ````docker build -t flask-app:v1 .````

- 5.5 Lancez un conteneur en passant la variable d'environnement APP_ENV=production et
en exposant le port 5000 . Vérifiez / et /health dans le navigateur ou avec curl .

    ````docker run -d -p 5000:5000 -e APP_ENV=production flask-app:v1````

    *Verification*

    ````
    curl http://localhost:5000/
    Flask fonctionne ! Environnement : production

    curl http://localhost:5000/health
    {"status":"ok"}
    ````

- 5.6 Relancez le conteneur sans passer APP_ENV . Quelle valeur s'affiche ? D'où vient-elle ?

    ````
    docker run -d -p 5000:5000 flask-app:v1
    `````
    ````
    curl http://localhost:5000/
    Flask fonctionne ! Environnement : développement
    ````
    *La valeur vient du code python*
    ````
    env = os.environ.get("APP_ENV", "développement")
    return f"Flask fonctionne ! Environnement : {env}"
    `````

- 5.7 Quelle est la taille de l'image flask-app:v1 ? Que pourrait-on faire pour la réduire
davantage (donnez deux pistes) ?

    ````
    docker images flask-app:v1
    ````

    *Ca me retourne*

    ````flask-app:v1   3eb0a8c5c43b        197MB         48.1MB````

    *Pour opitmiser l'espace on pourrait utiliser une image plus legere (ex: alpine) et utiliser un fichier .dockerignore : évite de copier des fichiers inutiles dans l'image.*