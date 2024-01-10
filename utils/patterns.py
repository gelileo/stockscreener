# https://ta-lib.github.io/ta-lib-python/
candlestick_patterns = {
    "CDL2CROWS": "Two Crows",
    "CDL3BLACKCROWS": "Three Black Crows",
    "CDL3INSIDE": "Three Inside Up/Down",
    "CDL3LINESTRIKE": "Three-Line Strike",
    "CDL3OUTSIDE": "Three Outside Up/Down",
    "CDL3STARSINSOUTH": "Three Stars In The South",
    "CDL3WHITESOLDIERS": "Three Advancing White Soldiers",
    "CDLABANDONEDBABY": "Abandoned Baby",
    "CDLADVANCEBLOCK": "Advance Block",
    "CDLBELTHOLD": "Belt-hold",
    "CDLBREAKAWAY": "Breakaway",
    "CDLCLOSINGMARUBOZU": "Closing Marubozu",
    "CDLCONCEALBABYSWALL": "Concealing Baby Swallow",
    "CDLCOUNTERATTACK": "Counterattack",
    "CDLDARKCLOUDCOVER": "Dark Cloud Cover",
    "CDLDOJI": "Doji",
    "CDLDOJISTAR": "Doji Star",
    "CDLDRAGONFLYDOJI": "Dragonfly Doji",
    "CDLENGULFING": "Engulfing Pattern",
    "CDLEVENINGDOJISTAR": "Evening Doji Star",
    "CDLEVENINGSTAR": "Evening Star",
    "CDLGAPSIDESIDEWHITE": "Up/Down-gap side-by-side white lines",
    "CDLGRAVESTONEDOJI": "Gravestone Doji",
    "CDLHAMMER": "Hammer",
    "CDLHANGINGMAN": "Hanging Man",
    "CDLHARAMI": "Harami Pattern",
    "CDLHARAMICROSS": "Harami Cross Pattern",
    "CDLHIGHWAVE": "High-Wave Candle",
    "CDLHIKKAKE": "Hikkake Pattern",
    "CDLHIKKAKEMOD": "Modified Hikkake Pattern",
    "CDLHOMINGPIGEON": "Homing Pigeon",
    "CDLIDENTICAL3CROWS": "Identical Three Crows",
    "CDLINNECK": "In-Neck Pattern",
    "CDLINVERTEDHAMMER": "Inverted Hammer",
    "CDLKICKING": "Kicking",
    "CDLKICKINGBYLENGTH": "Kicking - bull/bear determined by the longer marubozu",
    "CDLLADDERBOTTOM": "Ladder Bottom",
    "CDLLONGLEGGEDDOJI": "Long Legged Doji",
    "CDLLONGLINE": "Long Line Candle",
    "CDLMARUBOZU": "Marubozu",
    "CDLMATCHINGLOW": "Matching Low",
    "CDLMATHOLD": "Mat Hold",
    "CDLMORNINGDOJISTAR": "Morning Doji Star",
    "CDLMORNINGSTAR": "Morning Star",
    "CDLONNECK": "On-Neck Pattern",
    "CDLPIERCING": "Piercing Pattern",
    "CDLRICKSHAWMAN": "Rickshaw Man",
    "CDLRISEFALL3METHODS": "Rising/Falling Three Methods",
    "CDLSEPARATINGLINES": "Separating Lines",
    "CDLSHOOTINGSTAR": "Shooting Star",
    "CDLSHORTLINE": "Short Line Candle",
    "CDLSPINNINGTOP": "Spinning Top",
    "CDLSTALLEDPATTERN": "Stalled Pattern",
    "CDLSTICKSANDWICH": "Stick Sandwich",
    "CDLTAKURI": "Takuri (Dragonfly Doji with very long lower shadow)",
    "CDLTASUKIGAP": "Tasuki Gap",
    "CDLTHRUSTING": "Thrusting Pattern",
    "CDLTRISTAR": "Tristar Pattern",
    "CDLUNIQUE3RIVER": "Unique 3 River",
    "CDLUPSIDEGAP2CROWS": "Upside Gap Two Crows",
    "CDLXSIDEGAP3METHODS": "Upside/Downside Gap Three Methods",
}


import json
import os


# Function to find the corresponding pattern data in the JSON based on the name
def find_pattern_data(name, patterns_data):
    for pattern in patterns_data:
        if pattern["name"] == name:
            return pattern
    return None


def generate_new_candlestick_patterns():
    # Parse the JSON content to a Python object
    file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "../resources/patterns.json"
    )
    with open(file_path, "r") as file:
        patterns_data = json.load(file)

    # Creating the new dictionary
    new_candlestick_patterns = {}
    for key, value in candlestick_patterns.items():
        pattern_data = find_pattern_data(value, patterns_data)
        if pattern_data:
            new_candlestick_patterns[key] = pattern_data

    return new_candlestick_patterns


# Displaying the first 2 items for brevity (you can remove or modify this part as needed)
# print(list(new_candlestick_patterns.items())[:2])


if __name__ == "__main__":
    # Define the path for the new output Python file
    output_file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "patterns_and_desc.py"
    )

    # Write the new_candlestick_patterns dictionary to a Python file
    with open(output_file_path, "w") as file:
        file.write("# Generated using the utils/patterns.py script\n\n")
        file.write("pattern_details = ")
        file.write(repr(generate_new_candlestick_patterns()))
