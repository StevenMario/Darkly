# Path Traversal

## Definition

Path Traversal (ou Directory Traversal) est une vulnérabilité web qui permet à un attaquant de lire des fichiers situés en dehors du répertoire prévu par l’application, en manipulant les chemins de fichiers avec des séquences `../`.

---

## How it works

Une application vulnérable utilise une entrée utilisateur pour construire un chemin de fichier sans validation correcte.

### Exemple normal

```http
http://site.com/?file=document.pdf
```

Le serveur lit :

```bash
/var/www/files/document.pdf
```

### Exemple d’attaque

L’attaquant remplace le nom du fichier par des séquences `../` pour remonter dans l’arborescence :

```http
http://site.com/?file=../../../etc/passwd
```

Le serveur lit alors :

```bash
/etc/passwd
```

Ce fichier est sensible sur les systèmes Linux.

---

## Stages of operation

### 1. Rechercher les paramètres vulnérables

Chercher des paramètres qui chargent des fichiers :

- `?file=`
- `?page=`
- `?path=`
- `?include=`

---

### 2. Cibler `/etc/passwd`

Pourquoi ce fichier ?

- Présent sur presque tous les systèmes Linux
- Lisible sans privilèges élevés
- Son contenu est facilement reconnaissable
- Permet d’identifier des noms d’utilisateurs utiles pour d’autres attaques

---

### 3. Tester la vulnérabilité

```http
http://IP/?page=../../../../../../../../etc/passwd
```

Si le contenu du fichier apparaît, la vulnérabilité est confirmée.

---

## Example output

```txt
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
user:x:1000:1000:user:/home/user:/bin/bash
```

---

## Mitigation

Pour se protéger contre le Path Traversal :

- Valider les entrées utilisateur
- Utiliser des listes blanches de fichiers autorisés
- Désactiver l’accès direct aux fichiers sensibles
- Utiliser des chemins absolus sécurisés
- Éviter l’utilisation directe des entrées utilisateur dans les chemins

---

## References

- OWASP Path Traversal
- CWE-22: Path Traversal