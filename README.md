[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)
# Books_reviews
---
### Pré-requis
Avoir un OS **Linux** avec **Python 3.11** installé  
<br/>

### Installation
Executer ces commandes dans un terminal **bash**
pour installer installer le projet
```bash
git clone git@github.com:Jeremie-Silva/books_reviews.git
cd books_reviews
```
```bash
virtualenv -p3.11 .venv
source .venv/bin/activate
pip install -r requirements.txt
```
<br/>

lancer l'application en local :
```bash
python litrevu/manage.py runserver
google-chrome http://127.0.0.1:8000/
```
(remplacer google-chrome par le nom de votre navigateur)

<br/>

Générer le schema des modeles pour l'app `books_reviews` :
```bash
sudo apt install graphviz

./manage.py graph_models books_reviews -o books_reviews/Schemas/models_schema.png
```

<br/>

Activer la completion par tabulation pour la commande django-admin :
```bash
source django_bash_completion
```  

<br/>

Quitter l'environnement virtuel :
```bash
deactivate
```  

<br/>
<br/>

### Docker
```bash
git clone git@github.com:Jeremie-Silva/books_reviews.git
cd books_reviews
```


Build une image :
```bash
docker build -t books_reviews .
```

Lancer le container :
```bash
docker container run -v $(pwd):/app -it -p 8000:8000 books_reviews
```

Accéder au Front-end (depuis un autre terminal) :
```bash
google-chrome http://127.0.0.1:8000/
```
(remplacer google-chrome par le nom de votre navigateur)
