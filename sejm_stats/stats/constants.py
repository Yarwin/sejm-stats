import re

camel_case_regex = re.compile(r'(?<!^)(?=([A-Z][a-z]+))')
