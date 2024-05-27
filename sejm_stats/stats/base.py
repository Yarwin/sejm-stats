import inspect
from typing import Dict

from sejm_stats.stats.constants import camel_case_regex


class FromApiInput:
	@classmethod
	def from_dict(cls, input: dict):
		parsed_input: Dict = {}
		for k, v in input.items():
			snake_case_key = camel_case_regex.sub("_", k).lower()
			if snake_case_key in inspect.signature(cls).parameters:
				parsed_input[snake_case_key] = v

		return cls(**parsed_input)
