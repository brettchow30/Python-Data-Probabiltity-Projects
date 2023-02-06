"""Rock paper scissors simulator
May 25, 2019
ECE 105
"""
import itertools
import importlib
import time
from pathlib import Path
from typing import Dict, List, Tuple, Callable
PlayerName = str
Choice = str
MyChoice = Choice
TheirChoice = Choice
Game = Tuple[MyChoice, TheirChoice]
History = List[Game]
Payoff = Dict[Tuple[Choice, Choice], Tuple[int, int]]


class Player:
    def __init__(self, name: str, strategy: Callable[[History], Choice]):
        self.name = name
        self.strategy = strategy
        self.history: Dict[PlayerName, History] = {}

    def play(self, other: 'Player') -> Choice:
        return self.strategy(self.history.setdefault(other.name, []))

    def update(self, other: 'Player', dself: Choice, dother: Choice) -> None:
        self.history[other.name].append((dself, dother))

    def total_score(self, payoff: Payoff) -> int:
        return sum(payoff[game][0]
                   for games in self.history.values() for game in games)


def get_player_types(tournament_path: Path) -> Dict[PlayerName, int]:
    # Obtain the player types and the number of each type to play
    with tournament_path.open() as f:
        return {player_config[0]:
                int(player_config[1]) if len(player_config) > 1 else 1
                for player_config in (line.split() for line in f)}


def create_players(player_dir: Path, player_types: Dict[PlayerName, int]) -> List[Player]:
    players: List[Player] = []
    players_available = [p.stem for p in player_dir.iterdir()]
    # Example: [PAlwaysC, PAlwaysP, PAlwaysS]
    for player in player_types:
        if player in players_available:
            mod = importlib.import_module(f'{player_dir.stem}.{player}')
            if hasattr(mod, 'strategy') and callable(mod.strategy):
                players += [Player(player if not i else f'{player}-{str(i+1)}', mod.strategy)
                            for i in range(player_types[player])]
            else:
                print(f"Warning! No strategy found for {player}")
        else:
            print(f"Warning! Cannot find player {player}")
    return players


def tournament(players: List[Player], rounds: int, payoff: Payoff, log_path: Path) -> None:
    # Does not return anything, but updates players in-place
    # and outputs outcomes to log file
    with log_path.open(mode='wt') as f:
        # iterate over each distinct pair of players
        for p1, p2 in itertools.combinations(players, 2):
            # have each pair of players play rounds
            for r in range(rounds):
                # Ask each player for an action
                # and have each player update history
                a1 = p1.play(p2)
                a2 = p2.play(p1)
                p1.update(p2, a1, a2)
                p2.update(p1, a2, a1)

                # Compute the outcomes of the action pair
                # and print game: players, actions, outcomes
                o1, o2 = payoff[(a1, a2)]
                outcome = (f'({p1.name}, {p2.name})'
                           f'\t{r+1}/{rounds}:'
                           f'\t({a1}, {a2})\t({o1}, {o2})')
                print(outcome, file=f)


def scoreboard(players: List[Player], rounds: int, payoff: Payoff, score_path: Path) -> None:
    # Write out final scores
    with score_path.open(mode='wt') as f:
        header = (f'{len(players)} players, {rounds} rounds\n'
                  'score\tpts/rnd\tname')
        print(header)
        print(header, file=f)

        normalization = (len(players) - 1) * rounds
        scores = {player.name: player.total_score(payoff) for player in players}
        for player_name in sorted(scores, key=scores.get, reverse=True):
            score = (f'{scores[player_name]: >6d}'
                     f'\t{scores[player_name]/normalization:+.5f}'
                     f'\t{player_name}')
            print(score)
            print(score, file=f)


if __name__ == "__main__":
    # The simulation

    # folder name where player strategy modules are stored
    players_dir = 'Players'
    players_path = Path('.').joinpath(players_dir)

    # file holding list of players to use:
    # choose one of these for different scenarios
    tournament_filename = 'LabHW9-RPS-PlayerFile-All.txt'
    # tournament_filename = 'LabHW9-RPS-PlayerFile-PvP1.txt'
    tournament_path = Path('.').joinpath(tournament_filename)

    # logfile to record all games
    log_filename = 'LabHW9-RPS-Logfile.txt'
    log_path = Path('.').joinpath(log_filename)

    # scorefile to record all scores
    score_filename = 'LabHW9-RPS-Scorefile.txt'
    score_path = Path('.').joinpath(score_filename)

    # number of rounds
    rounds = 1000

    # payoff matrix
    payoff = {('R', 'R'): (0, 0),
              ('R', 'P'): (-1, +1),
              ('P', 'R'): (+1, -1),
              ('P', 'P'): (0, 0),
              ('P', 'S'): (-1, +1),
              ('S', 'P'): (+1, -1),
              ('S', 'S'): (0, 0),
              ('S', 'R'): (-1, +1),
              ('R', 'S'): (+1, -1)}

    # ------------------------------------------ #
    # core steps: create, run, score
    # ------------------------------------------ #

    # extract player types we want to participate in the tournament
    player_types = get_player_types(tournament_path)

    # create the players from their type names and strategies
    players = create_players(players_path, player_types)

    # hold tournament among the players
    tournament(players, rounds, payoff, log_path)

    # print the scoreboard to screen and to file
    scoreboard(players, rounds, payoff, score_path)
