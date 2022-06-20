# Projet 9

***********

- Créer un dossier où le repo sera téléchargé :
    ```
        mkdir projet_9
    ```

- Créer un environnement virtuel :
    ```
        python3 -m venv venv
    ```

- Se rendre sur le repo https://github.com/weekendatchewie/p9_litreview_book

- Cloner ou télécharger le repo

- Activer l'environnement virtuel :

    - Linux/Macos :

      ```
        source venv/bin/activate
      ```

    - Windows :
      ```
        venv\scripts\activate.bat
      ```

- Se rendre dans le dossier "litreview_book" :
    ```
      cd litreview_book
    ```

- Télécharger les packages :
    ```
      pip3 install -r requirements.txt
    ```
- Migrer les modèles dans la base de donnée :
    ```
      python3 manage.py migrate
    ```

- Recueillir les fichiers statiques :
    ```
      python3 manage.py collectstatic
    ```

- Lancer le serveur :
    ```
      python3 manage.py runserver
    ```