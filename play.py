"""Main script of project.

This script launch main functionality of the project.

Its name can be more explicit than main, but is has to be project root to
access all packages.
"""
from olgaming import games
from olgaming.gameobj import GameObject
from olutils.params import add_dft_args


def main(game_name, load_path, g_kwargs, g_params, p_params):
    """Launch game."""
    game_cls = getattr(games, game_name)
    kwargs = g_kwargs
    kwargs.update(g_params)
    kwargs['p_params'] = p_params
    game = game_cls(**kwargs)
    if load_path:
        game.load(load_path)
    game.play()


if __name__ == "__main__":
    from argparse import ArgumentParser

    # Game settings
    parser = ArgumentParser(
        "Play a game"
    )
    parser.add_argument(
        'game', type=str,
        help='game to play'
    )
    parser.add_argument(
        '-b', '--bots', type=int,
        nargs='*', required=False,
        help=(
            "Set bots as players (list of index starting from 0)"
        ),
    )
    parser.add_argument(
        '-l', '--load_path', type=str, required=False, default=None,
        help="path where to load game, default is None"
    )

    # Object parameters (for logs and all)
    dft_params = GameObject.dft_params()
    add_dft_args(
        parser=parser,
        dft_args=dft_params,
        flag_prefix="",
        help_prefix="game parameter ",
    )
    add_dft_args(
        parser=parser,
        dft_args=dft_params,
        flag_prefix="p_",
        help_prefix="player parameter ",
    )
    args = parser.parse_args()

    bots = []
    if args.bots:
        bots = args.bots

    main(
        game_name=args.game,
        load_path=args.load_path,
        g_kwargs={
            'bots': bots,
        },
        g_params={
            param: getattr(args, param)
            for param in dft_params
        },
        p_params={
            param: getattr(args, "p_" + param)
            for param in dft_params
        },
    )
