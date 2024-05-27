import asyncio
from functools import cached_property
from typing import Tuple, List

import aiohttp

from .types import Voting, Vote
from .utils import flatten


async def fetch_data(session, url):
	async with session.get(url) as response:
		return await response.json()


class SejmClient:
	SEJM_API_URL = "http://api.sejm.gov.pl/sejm"
	term: int

	def __init__(self, term):
		self.term = term

	@cached_property
	def base_url(self):
		return f"{self.SEJM_API_URL}/term{self.term}"

	def get_votings(self, sittings_range: Tuple[int, int]) -> List[Voting]:
		return asyncio.run(self._get_votes_from_sittings(sittings_range))

	async def _get_votes_from_sittings(self, sittings_range: Tuple[int, int]):
		connector = aiohttp.TCPConnector(force_close=True)

		async with aiohttp.ClientSession(connector=connector) as session:
			votings: List[Voting] = flatten(await asyncio.gather(*[
					self._fetch_voting(session, sitting)
					for sitting in range(sittings_range[0], sittings_range[1])
			]))

			tasks = [
				self.fetch_individual_votes(session, voting.sitting, voting)
				for voting in votings
			]
			await asyncio.gather(*tasks)

		return votings

	async def _fetch_voting(self, session, sitting) -> List[Voting]:
		result = await fetch_data(session, f"{self.base_url}/votings/{sitting}")
		return [
			Voting.from_dict(vote)
			for vote in result
		]

	async def fetch_individual_votes(self, session, sitting, voting):
		votes = (await fetch_data(session, f"{self.base_url}/votings/{sitting}/{voting.voting_number}")).get("votes")
		voting.votes = [Vote.from_dict(v) for v in votes]
