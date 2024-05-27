import collections
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from functools import cached_property
from typing import List, Optional, Dict, Any

from sejm_stats.stats.base import FromApiInput


class VoteType(Enum):
	YES = "YES"
	NO = "NO"
	ABSTAIN = "ABSTAIN"
	ABSENT = "ABSENT"
	VOTE_VALID = "VOTE_VALID"
	NO_VOTE = "NO_VOTE"
	VOTE_INVALID = "VOTE_INVALID"


@dataclass
class MP:
	id: int
	club: str
	votes: List[int] = field(default_factory=list)


@dataclass
class Vote(FromApiInput):
	mp: int
	club: str
	list_votes: Optional[Dict[int, VoteType]] = None
	vote: Optional[VoteType] = None

	def __post_init__(self):
		if list_votes := self.list_votes:
			self.list_votes = {
				int(k): VoteType[v]
				for k, v in list_votes.items()
			}
		else:
			self.vote = VoteType[self.vote]


@dataclass
class VotingOption(FromApiInput):
	option: str
	option_index: int
	votes: int


@dataclass
class Voting(FromApiInput):
	yes: int
	no: int
	total_voted: int
	abstain: int
	not_participating: int
	date: datetime
	title: str
	term: int
	sitting: int
	voting_number: int
	topic: Optional[str] = field(default=None)
	voting_options: Optional[List[VotingOption]] = field(default=None)
	votes: List[Vote] = field(default_factory=list, repr=False)

	def __post_init__(self):
		if voting_options := self.voting_options:
			self.voting_options = [
				VotingOption.from_dict(option)
				for option
				in voting_options
			]

	@staticmethod
	def get_list_votes(vote):
		return list((vote.club, o) for o in vote.list_votes.values())

	@staticmethod
	def count_votes(votes) -> Dict[str, Dict[Any, Any]]:
		votes_by_club: Dict[str, Dict[Any, Any]] = collections.defaultdict(lambda: collections.defaultdict(dict))
		c = collections.Counter(votes)
		for key in c.keys():
			votes_by_club[key[0]][key[1]] = c[key]
		for club in votes_by_club.keys():
			votes_by_club[club]["dominating_option"] = collections.Counter(votes_by_club[club]).most_common(1)[0][0]
		return votes_by_club

	@cached_property
	def votes_by_club(self) -> List[Dict[str, Dict[Any, Any]]]:
		if options := self.voting_options:
			votes = {
				option.option_index: [
					(v.club, v.list_votes.get(option.option_index))
					if v.list_votes.get(option.option_index)
					else (v.club, VoteType.ABSENT)
					for v in self.votes
				]
				for option in options
			}
			return [self.count_votes(v) for v in votes.values()]
		else:
			votes = [(v.club, v.vote) for v in self.votes]
			return [self.count_votes(votes)]

	def __str__(self):
		return f"głosowanie numer {self.voting_number} w sprawie {self.title}"
