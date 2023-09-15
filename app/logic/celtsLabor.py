

"""
Sample Labor Result:

    {"B00568458":[
                {"jobType":"Primary",
                "laborEnd":"Mon, 18 Jul 2016 00:00:00 GMT",
                "laborStart":"Mon, 23 May 2016 00:00:00 GMT",
                "positionTitle":"Habitat for Humanity Coord.",
                "termCode":201513,"wls":"5"},
                {"jobType":"Primary",
                "laborEnd":"Tue, 13 Dec 2016 00:00:00 GMT",
                "laborStart":"Tue, 23 Aug 2016 00:00:00 GMT",
                "positionTitle":"Habitat for Humanity Coord.",
                "termCode":201611,"wls":"5"}
                 ],

"""

def getPositionAndTerm():
    return {"positionTitle": "Habitat for Humanity Coord.", "termName":"Fall 2016"}