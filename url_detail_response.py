class UrlResponse:
    code_meaning = {1: ["Dangerous", "Detected from database"],
                    2: ["Unsafe", "Detected from model"],
                    3: ["Generally safe", " Detected From model"],
                    4: ["Safe", "Detected from database"]}

    def __init__(self, code):
        self.response = {"threat_level": str(code),
                         "description": self.code_meaning[code][0],
                         "detected_from": self.code_meaning[code][1]}
