import random
import argparse
import os
import sys

from lib import write_grid

# ---------------------------------------------------------------------------
# Bryan - Les Arguments du programme
# ---------------------------------------------------------------------------

#Fonction convertissant une valeur en entier (renvoie une erreur si ce n'est pas un entier)
def convertir_entier(value):
    try:
        return int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{value}' n'est pas un entier")


#Fonction testant si un entier est strictement positif ( > 0 )
def entier_strictement_positif(value):

    number = convertir_entier(value)

    if number <= 0:
        raise argparse.ArgumentTypeError(
            f"'{value}' doit être un entier strictement positif"
        )
    return number

#Fonction testant si un entier n'est pas négatif ( >= 0)
def entier_non_negatif(value):

    number = convertir_entier(value)
    if number < 0:
        raise argparse.ArgumentTypeError(
            f"'{value}' doit être un entier positif ou nul"
        )
    return number


def lire_argument(argv=None):

    parser = argparse.ArgumentParser(description="Jeu de la vie de Conway")
    parser.add_argument(
        "-n", "--nb_cells", type=entier_strictement_positif, default=10,
        help="nombre de cellules par côté pour une grille aléatoire (défaut : 10)",
    )
    parser.add_argument(
        "-m", "--max_iterations", type=entier_non_negatif, default=20,
        help="numéro de la dernière itération à calculer (défaut : 20)",
    )
    parser.add_argument(
        "-s", "--seed", type=convertir_entier, default=42,
        help="graine du générateur aléatoire (défaut : 42)",
    )
    parser.add_argument(
        "-o", "--output_directory", default="outputs",
        help="dossier dans lequel écrire les images (défaut : outputs)",
    )
    parser.add_argument(
        "-t", "--output_type", choices=["image", "text"], default="image",
        help="type de sortie : image ou text (défaut : image)",
    )
    parser.add_argument(
        "-p", "--periodic", action="store_true",
        help="active les conditions aux limites périodiques",
    )
    return parser.parse_args(argv)

# ---------------------------------------------------------------------------
# Bryan - fin
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# Lanja-compter-voisins
# ---------------------------------------------------------------------------

def compter_voisins(grille, l, c, periodique=False):
    """Compte les voisines vivantes de la cellule (l, c)."""

    nb_lig = len(grille) # Nombre de lignes de la grille
    nb_col = len(grille[0]) # Nombre de colonnes de la grille
    nb_voisins = 0 # Nombre de voisines vivantes

    # On parcourt les voisines autour de la cellule (l, c)
    for lv in range(l - 1, l + 2):
        for cv in range(c - 1, c + 2):
            # La cellule (l, c) elle-même n'est pas une voisine
            if lv == l and cv == c:
                continue

            if periodique:
                # Mode périodique : ce qui sort d'un côté revient de l'autre
                # Exemple avec 3 lignes : -1 % 3 = 2 et 3 % 3 = 0
                lv_test = lv % nb_lig
                cv_test = cv % nb_col
            else:
                # Mode fixe : en dehors de la grille, la voisine est considérée morte
                if not (0 <= lv < nb_lig and 0 <= cv < nb_col):
                    continue
                lv_test = lv
                cv_test = cv

            if grille[lv_test][cv_test] == 1:
                nb_voisins += 1

    return nb_voisins


def generation_suivante(monde,periodique=False):
    # Taille d'un côté de la grille (elle est carrée)
    n = len(monde)

    # Nouvelle grille vide, pour ne pas écraser l'ancienne pendant le calcul
    monde_suivant = [[0] * n for _ in range(n)]

    # Étape A : calcul de la nouvelle génération dans monde_suivant
    for l in range(n):
        for c in range(n):
            #On transmet le mode (fixe ou periodique) au comptage des voisines
            nb_voisins = compter_voisins(monde, l, c, periodique)

            if monde[l][c] == 1:
                # Règle 1 : une cellule vivante reste vivante si elle a 2 ou 3 voisins
                if nb_voisins == 2 or nb_voisins == 3:
                    monde_suivant[l][c] = 1
                else:
                    monde_suivant[l][c] = 0  # Mort par sous-population ou surpopulation
            else:
                # Règle 2 : une cellule morte naît si elle a exactement 3 voisins
                if nb_voisins == 3:
                    monde_suivant[l][c] = 1
                else:
                    monde_suivant[l][c] = 0

    # Étape B : copie de la nouvelle grille dans la grille d'origine
    for l in range(n):
        for c in range(n):
            monde[l][c] = monde_suivant[l][c]

# ---------------------------------------------------------------------------
# Lanja-Fin
# ---------------------------------------------------------------------------
#----------------------------------------------------------------------------
#Maxence : Geston des entrée/STDIN
#----------------------------------------------------------------------------


def conversion_grille(entree):
    #convertis en matrice la grille donner sur STDIN, 
    # en verifiant si les arguments sont correcte
    lignes = entree.splitlines()

    if not lignes:
        raise ValueError("Grille vide")

    try:
        taille = int(lignes[0])
    except ValueError:
        raise ValueError("Taille invalide")

    if taille <= 0:
        raise ValueError("La taille doit être positive")

    if len(lignes) != taille + 1:
        raise ValueError("Nombre de lignes incorrect")

    grille = []

    for i in range(taille):
        new = []
        valeurs = lignes[i + 1].split()

        if len(valeurs) != taille:
            raise ValueError("Nombre de colonnes incorrect")

        for j in range(taille):
            try:
                cellule = int(valeurs[j])
            except ValueError:
                raise ValueError("Cellule non entière")

            if cellule not in (0, 1):
                raise ValueError("Une cellule doit valoir 0 ou 1")

            new.append(cellule)

        grille.append(new)

    return grille

def obtenir_grille_initiale(args): 
    #reprise du prof pour générer une grille seulement si aucune grille 
    #n' as étais donnée en entrée

    entree = ""

    if not sys.stdin.isatty():
        entree = sys.stdin.read()

    if entree:
        return conversion_grille(entree)

    rng = random.Random(args.seed)

    return [
        [rng.choice([0, 1]) for _ in range(args.nb_cells)]
        for _ in range(args.nb_cells)
    ]
#----------------------------------------------------------------------------
#Maxence : Fin
#----------------------------------------------------------------------------


# --------------------------------------------------
# Amal : Gestion des sorties
# --------------------------------------------------

# Afficher la grille en texte
def afficher_texte(matrix, iteration):

    print("iteration:", iteration)

    for ligne in matrix:
        print(" ".join(str(cellule) for cellule in ligne))


# Enregistrer une image de la grille
def enregistrer_image(matrix, iteration, dossier):

    nom_fichier = os.path.join(
        dossier,
        "grid_" + str(iteration).zfill(4) + ".png"
    )

    write_grid(matrix=matrix, filename=nom_fichier)

# --------------------------------------------------
# Amal : Fin
# --------------------------------------------------

def main():
    args = lire_argument() #permet de recuperer les arguments

    try:
        matrix = obtenir_grille_initiale(args)
    except ValueError as erreur:
        print(f"Erreur : {erreur}", file=sys.stderr)
        sys.exit(1)


    os.makedirs(args.output_directory, exist_ok=True)

    # Parcourir toutes les générations
    for iteration in range(args.max_iterations + 1):

        # Afficher la grille en texte
        if args.output_type == "text":
            if iteration == args.max_iterations:
                afficher_texte(matrix, iteration)

        # Enregistrer les images
        else:
            enregistrer_image(
                matrix,
                iteration,
                args.output_directory
            )

        # Calculer la génération suivante
        if iteration < args.max_iterations:
            generation_suivante(matrix, args.periodic)
    if args.output_type == "image":
        print(
            f"Generation of {args.max_iterations + 1} "
            f"images in directory {args.output_directory}"
        )

if __name__ == "__main__":
    main()