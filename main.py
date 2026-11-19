import random
import argparse
import os

from lib import write_grid



# ---------------------------------------------------------------------------
# Bryan - Les Arguments du programme
# ---------------------------------------------------------------------------

#Fonction convertissant un entier en valeur (renvoi une erreur si ce n'est pas un entier)
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

def compter_voisins(grille, l, c):
    """Compte les voisines vivantes de la cellule (i,j)."""

    nb_lig = len(grille) # Nombre de ligne de la grille
    nb_col = len(grille[0]) # Nombre de cologne de la grille
    nb_voisins=0 # Nombre de voisines vivantes

    # On parcrous les voisins autour de la cellule (l,c)
    for lv in range (l-1, l+2):
        for cv in range (c-1, c+2): 
            # La voisine doit être DANS la grille (sinon elle est considérée morte)
            if 0 <= lv < nb_lig and 0 <= cv < nb_col :
                if grille[lv][cv]==1:
                    nb_voisins +=1

    # Le carré 3x3 contient aussi la cellule (l, c) elle-même :
    # si elle est vivante, on la retire du total
    if grille[l][c] == 1:
        nb_voisins -= 1

    return nb_voisins

# ---------------------------------------------------------------------------
# Lanja-Fin
# ---------------------------------------------------------------------------


def main():

    args = lire_argument() #lire_argument permet de récupérer les arguments

    rng = random.Random(args.seed)
    matrix = [
        [rng.choice([0, 1]) for _ in range(args.nb_cells)]
        for _ in range(args.nb_cells)
    ]

    os.makedirs(args.output_directory, exist_ok=True)
    iter = 0
    filename = os.path.join(args.output_directory, f"grid_{iter:04d}.png")
    write_grid(matrix=matrix, filename=filename)


if __name__ == "__main__":
    main()
