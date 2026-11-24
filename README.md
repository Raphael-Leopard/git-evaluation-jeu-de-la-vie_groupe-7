# Jeu de la vie de Conway

Implémentation en Python du [jeu de la vie](https://fr.wikipedia.org/wiki/Jeu_de_la_vie) sur une grille carrée, avec conditions aux limites fixes ou périodiques. Le programme part d'une grille aléatoire reproductible ou d'une grille lue sur l'entrée standard, calcule les générations successives, puis écrit le résultat sous forme d'images PNG ou de texte.

## Table des matières

- [Installation](#installation)
- [Exécution](#exécution)
- [Arguments](#arguments)
- [Vidéos](#vidéos)
- [Tests](#tests)
- [Auteurs](#auteurs)
- [Liens utiles](#liens-utiles)

## Installation

Le programme n'utilise que la bibliothèque standard de Python 3. Les vidéos nécessitent en plus `ffmpeg` et Gource. Les scripts de test utilisent `sh` et des commandes Unix (`cat`, `diff`, `find`, `mktemp`).

### Ubuntu ou Debian

```bash
sudo apt update
sudo apt install python3 git gource ffmpeg
```

### macOS

```bash
brew install gource ffmpeg
```

Python 3 et Git sont généralement déjà présents ; sinon, installez-les avec `brew install python git`.

### Windows

Installez [WSL](https://learn.microsoft.com/fr-fr/windows/wsl/install) pour disposer d'un terminal Unix. Depuis un PowerShell ouvert en tant qu'administrateur :

```powershell
wsl --install
```

Redémarrez si nécessaire, ouvrez ensuite la distribution Ubuntu et suivez les commandes de la section [Ubuntu ou Debian](#ubuntu-ou-debian). Depuis WSL, les disques Windows sont montés dans `/mnt` :

```bash
cd /mnt/c/Users/<nom>/chemin/vers/le/depot
```

### Vérifier l'installation

```bash
python3 --version
ffmpeg -version
gource --version
```

## Exécution

Toutes les commandes se lancent depuis la racine du dépôt. Lorsqu'une erreur est rencontrée, un message explicite est écrit sur `STDERR` et le programme se termine avec un code de sortie différent de `0`.

### Sans option

Le programme utilise les valeurs par défaut et crée 21 images dans `outputs`, de `grid_0000.png` à `grid_0020.png` :

```bash
$ python3 main.py
Generation of 21 images in directory outputs
$ echo $?
0
$ ls -p1 outputs | wc -l
     21
```

### Grille aléatoire de grande taille

Grille de 50 cellules par côté, graine `4200`, générations `0` à `200` incluses :

```bash
$ python3 main.py -n 50 -m 200 -s 4200
Generation of 201 images in directory outputs
$ echo $?
0
$ ls -p1 outputs | wc -l
    201
```

### Grille lue sur l'entrée standard

La première ligne donne la taille de la grille, suivie des lignes de la matrice, dont les cellules sont séparées par des espaces. Voici `tests/matrix3/input.txt` :

```text
3
1 0 1
0 0 1
1 0 1
```

Évolution d'une génération, conditions aux limites fixes, sortie texte :

```bash
$ cat tests/matrix3/input.txt | python3 main.py -m 1 -t text
iteration: 1
0 1 0
0 0 1
0 1 0
$ echo $?
0
```

### Grille périodique

L'option `-p` relie le bord gauche au bord droit et le bord supérieur au bord inférieur. Le résultat diffère pour la même grille :

```bash
$ cat tests/matrix3/input.txt | python3 main.py -m 1 -p -t text
iteration: 1
0 0 0
0 0 0
0 0 0
$ echo $?
0
```

### Erreurs

```bash
$ python3 main.py -n 0
$ echo $?
2
$ echo "abc" | python3 main.py
Erreur : Taille invalide
$ echo $?
1
```

## Arguments

Chaque option existe sous une forme courte et une forme longue.

| Option courte | Option longue | Description | Valeur par défaut |
|---|---|---|---|
| `-n N` | `--nb_cells N` | nombre de cellules par côté pour une grille aléatoire | `10` |
| `-m N` | `--max_iterations N` | numéro de la dernière itération à calculer | `20` |
| `-s N` | `--seed N` | graine du générateur de nombres aléatoires | `42` |
| `-o DOSSIER` | `--output_directory DOSSIER` | dossier dans lequel écrire les images | `outputs` |
| `-t TYPE` | `--output_type TYPE` | type de sortie : `image` ou `text` | `image` |
| `-p` | `--periodic` | active les conditions aux limites périodiques | désactivée |
| `-h` | `--help` | affiche l'aide du programme | — |

Précisions :

- La génération initiale porte le numéro `0` : `-m 20` produit donc 21 générations, de `0` à `20` incluses.
- `--max_iterations` doit être un entier positif ou nul, `--nb_cells` un entier strictement positif, `--seed` un entier quelconque.
- Avec `--output_type image`, une image `grid_XXXX.png` est écrite par génération dans le dossier de sortie, qui est créé s'il n'existe pas.
- Avec `--output_type text`, seule la dernière génération est affichée sur la sortie standard, précédée de `iteration: N`.
- Si une grille est fournie sur l'entrée standard, elle remplace la grille aléatoire : `--nb_cells` et `--seed` n'ont alors aucun effet.
- La taille d'une grille est limitée à 269 cellules par côté en sortie image (contrainte de `lib.py`).

## Vidéos

### Simulation du jeu de la vie

Lien YouTube : [https://www.youtube.com/watch?v=JUZvCt0cNXA](https://www.youtube.com/watch?v=JUZvCt0cNXA)

Graine utilisée : `4200` *(à vérifier : indiquer la graine effectivement utilisée)*

Commandes exactes de génération des images, puis de la vidéo, depuis la racine du dépôt et dans un terminal sans pipe ni redirection de l'entrée standard :

```bash
mkdir -p outputs/video-seed-4200
python3 main.py --nb_cells 50 --max_iterations 2000 --seed 4200 \
  --output_type image --output_directory outputs/video-seed-4200
ffmpeg -y -framerate 20 -start_number 0 \
  -i outputs/video-seed-4200/grid_%04d.png -frames:v 2001 \
  -c:v libx264 -pix_fmt yuv420p -movflags +faststart \
  outputs/video-seed-4200/game-of-life.mp4
```

Cette commande produit 2001 images (`grid_0000.png` à `grid_2000.png`) avec des conditions aux limites fixes, puis les assemble en une vidéo MP4. Avec la même graine et les mêmes paramètres, la simulation reproduit les mêmes générations à chaque exécution.

### Historique du dépôt avec Gource

Lien YouTube : **À COMPLÉTER** (vidéo publique)

Commande de génération :

```bash
gource -s 2 -r 60 --file-font-size 8 \
  --title 'Jeu de la vie' --filename-time 2 \
  --stop-at-end --hide date,usernames -o - | \
ffmpeg -y -r 60 -f image2pipe -vcodec ppm -i - \
  -vcodec libx264 -preset medium -pix_fmt yuv420p \
  -crf 18 -threads 0 -bf 0 gource.mp4
```

Les images et les vidéos générées ne sont pas versionnées dans Git (voir `.gitignore`).

## Tests

Deux scripts fournis vérifient le programme. Lancez-les depuis la racine du dépôt :

```bash
./check_script_options.sh
./check_tests.sh
```

Si le droit d'exécution n'est pas disponible, utilisez `sh check_script_options.sh` et `sh check_tests.sh`. Chaque script se termine par `Nb test success: N / N` lorsque tous les tests passent.

## Auteurs

| Nom | Prénom | Numéro étudiant |
|---|---|---|
| COUROUNADIN-MOUNY | Maxence | 45007424 |
| GONTHIER | Raphaël | 45003138 |
| LENDERS | Bryan | 46005449 |
| MADI M'HADJI | Amal | 45000802 |
| RAKOTONANAHARY | Lanja | 43901262 |

## Liens utiles

- [Workshop 3 : rebase et historique final](https://github.com/frozar/git-workshop-3) : organisation Git attendue pour ce projet,
- [Jeu de la vie](https://fr.wikipedia.org/wiki/Jeu_de_la_vie) : présentation des règles du jeu de Conway,
- [Documentation argparse](https://docs.python.org/fr/3/library/argparse.html) : analyse des arguments d'un script Python,
- [Documentation random](https://docs.python.org/fr/3/library/random.html) : génération de grilles aléatoires reproductibles,
- [Pipeline (Unix)](https://en.wikipedia.org/wiki/Pipeline_(Unix)) : description du pipe,
- [Installation de WSL](https://learn.microsoft.com/fr-fr/windows/wsl/install) : procédure officielle pour Windows,
- [Documentation ffmpeg](https://ffmpeg.org/documentation.html) : installation et utilisation de `ffmpeg`,
- [Site officiel de Gource](https://gource.io/) : présentation et téléchargement de Gource,
- [My Gource video production pipeline](https://dev.to/voieducode/my-gource-video-production-pipeline-5eb0) : exemple de création d'une vidéo Gource,
- [Documentation officielle de git rebase](https://git-scm.com/book/fr/v2/Les-branches-avec-Git-Rebaser-Rebasing) : fonctionnement du *rebase*.
