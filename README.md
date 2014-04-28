SMS-Viewer
==========

A GUI for "SMS to Text" (android) output (formated text file) 

### Text file format

        date    hour    in/out    num    msg

* Separator : `\t`
* Header : `FALSE`
* Date format : `YYYY-MM-DD`
* Hour format : `HH:MM:SS`
* in/out info : `in` or `out` *depending on the direction of the message*
* Message type : `string` with no `\n`


### Tuto Git

* Installer Git

        apt-get install git


* [Configurer Git](http://git-scm.com/book/fr/Personnalisation-de-Git-Configuration-de-Git)

* Créer un compte GitHub

    * Dans `Acount settings -> SSH keys` coller sa clef RSA, obtenue avec : 


            ssh-keygen -t rsa -C <votremailidentifiant> 
            cat ~/.ssh/id_rsa.pub

        Si plusieurs ordis, plusieurs clefs à mettre ;)

    * Me donner votre identifiant pour que je vous ajoute au projet. 

* Pour récupérer le code pour la première fois :

        git clone https://github.com/Fritzip/AGGP.git

    Ca crée le dossier AGGP avec les fichiers, vous pouvez maintenant tout modifier normalement.

* Une fois le dossier créer avant *chaque session de travail*, mettre à jour le dépot (pour prendre en compte les modifs des autres)

        git pull

    (il faut etre dans le dossier)


* Après chaque changement IMPORTANT, faire un commit :

        git commit -a -m 'un message explicite !'

* A la fin de la session de travail (et si tout fonctionne bien !), envoyer sur le dépot:

        git push -u origin master

    Cela met à jour le code sur le serveur, avant ce n'est que sur votre pc donc on en profite pas !

* Pour ajouter un fichier:
 
        git add <fichier>

* Pour voir l'état de git (ce qui est modif ou pas, ce qui est inclu dans le dépot ou pas ) :

        git status

Un peu (beaucoup) plus de doc partout sur internet pour une utilisation plus avancée.

*Merci à Antoine pour ce README.*

