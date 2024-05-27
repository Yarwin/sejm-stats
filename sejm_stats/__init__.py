from sejm_stats.stats import SejmClient
from sejm_stats.stats.stats import get_shared_votings


def _run(argv=None):
    votings = SejmClient(10).get_votings((1, 2))
    print(get_shared_votings(votings))

def main(argv=None):
    _run(argv)


__all__ = [
    'main',
]
