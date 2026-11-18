import random
import argparse
import os

from lib import write_grid


# ---------------------------------------------------------------------------
# Bryan - Les Arguments du programme
# ---------------------------------------------------------------------------

#Fonction permettant de tester un int
def _to_int(value):
    try:
        return int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{value}' n'est pas un entier")


#Fonction testant si un entier est strictement positif ( > 0 )
def strictly_positive_int(value):

    number = _to_int(value)

    if number <= 0:
        raise argparse.ArgumentTypeError(
            f"'{value}' doit être un entier strictement positif"
        )
    return number

#Fonction testant si un entier n'est pas négatif ( >= 0)
def non_negative_int(value):

    number = _to_int(value)
    if number < 0:
        raise argparse.ArgumentTypeError(
            f"'{value}' doit être un entier positif ou nul"
        )
    return number


def parse_args(argv=None):

    parser = argparse.ArgumentParser(description="Jeu de la vie de Conway")
    parser.add_argument(
        "-n", "--nb_cells", type=strictly_positive_int, default=10,
        help="nombre de cellules par côté pour une grille aléatoire (défaut : 10)",
    )
    parser.add_argument(
        "-m", "--max_iterations", type=non_negative_int, default=20,
        help="numéro de la dernière itération à calculer (défaut : 20)",
    )
    parser.add_argument(
        "-s", "--seed", type=_to_int, default=42,
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

def main():

    args = parse_args() #parse_args permet de récupérer les arguments

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
