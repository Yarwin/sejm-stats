import collections
import itertools
from typing import List, Dict, Tuple

from sejm_stats.stats import Voting, VoteType


def get_shared_votings(votings: List[Voting]) -> Tuple[collections.Counter, int]:
	n = 0
	counter = collections.Counter()
	for voting in votings:
		for i, votings in enumerate(voting.votes_by_club):
			n += 1
			d: Dict[VoteType, List[str]] = collections.defaultdict(list)
			for club in votings:
				d[voting.votes_by_club[i][club].get("dominating_option")].append(club)
			for vote_type, clubs in d.items():
				if len(clubs) > 1:
					counter.update(set(itertools.combinations(clubs, 2)))
	return counter, n
