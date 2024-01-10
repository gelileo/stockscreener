# screener

A custom stock screener and pattern alerts

### Misc

`resources/patterns.json` contains descriptions for each patterns. Information are gathered online, accuracy is not guaranteed.

`utils/patterns_and_desc.py` defines a dictionary that contains the pattern key and information pulled from this json file. So if you ever update the content of the json, you need to run `patterns.py` to regenerate `patterns_and_desc.py`
