from collections import Counter
from steamplus.tools import loadJson, heapSort
from steamplus.statistics import mode, median, mean


class Sample:
    """Statistics of a certain genre"""
    def __init__(self, name, _type):
        # data
        self.name = name
        self.data = loadJson()
        self.data = [i for i in self.data if self.name in i[1][_type]]

        # genres
        self.genres = [j for x in (i[1]["genres"].split(";") for i in self.data) for j in x]
        heapSort(self.genres)
        self.genreCounts = dict(Counter(self.genres))
        self.modeGenre = mode(self.genres)

        # categories
        self.categories = [j for x in (i[1]["categories"].split(";") for i in self.data) for j in x]
        heapSort(self.categories)
        self.categoryCounts = dict(Counter(self.categories))
        self.modeCategory = mode(self.genres)

        # steamspy tags
        self.ssTags = [j for x in (i[1]["steamspy_tags"].split(";") for i in self.data) for j in x]
        heapSort(self.ssTags)
        self.ssTagCounts = dict(Counter(self.ssTags))
        self.modeSsTag = mode(self.ssTags)

        # platforms
        self.platforms = [j for x in (i[1]["platforms"].split(";") for i in self.data) for j in x]
        heapSort(self.platforms)
        self.platformCount = dict(Counter(self.platforms))
        self.modePlatform = mode(self.platforms)

        # english
        self.english = [i[1]["english"] for i in self.data]
        self.englishCounts = dict(Counter(self.english))
        self.englishCounts["english"] = self.englishCounts.pop(1)
        self.englishCounts["non-english"] = self.englishCounts.pop(0)

        # price
        self.prices = [i[1]["price"] for i in self.data]
        heapSort(self.prices)
        self.meanPrice = round(mean(self.prices), 2)
        self.medianPrice = median(self.prices)
        self.modePrice = mode(self.prices)

        # achievements
        self.achievements = [i[1]["achievements"] for i in self.data]
        heapSort(self.prices)
        self.meanAchievements = int(round(mean(self.achievements), 0))
        self.medianAchievements = round(median(self.achievements), 0)
        self.modeAchievements = round(mode(self.achievements))


class Statistics:
    """Statistics of the whole database"""
    def __init__(self):
        # data
        self.data = loadJson()

        # genres
        self.genres = [j for x in (i[1]["genres"].split(";") for i in self.data) for j in x]
        self.genreCounts = dict(Counter(self.genres))
        self.modeGenre = mode(self.genres)

        # categories
        self.categories = [j for x in (i[1]["categories"].split(";") for i in self.data) for j in x]
        self.categoryCounts = dict(Counter(self.categories))
        self.modeCategory = mode(self.genres)

        # steamspy tags
        self.ssTags = [j for x in (i[1]["steamspy_tags"].split(";") for i in self.data) for j in x]
        self.ssTagCounts = dict(Counter(self.ssTags))
        self.modeSsTag = mode(self.ssTags)

        # platforms
        self.platforms = [j for x in (i[1]["platforms"].split(";") for i in self.data) for j in x]
        self.platformCount = dict(Counter(self.platforms))
        self.modePlatform = mode(self.platforms)

        # english
        self.english = [i[1]["english"] for i in self.data]
        self.englishCounts = dict(Counter(self.english))
        self.englishCounts["english"] = self.englishCounts.pop(1)
        self.englishCounts["non-english"] = self.englishCounts.pop(0)

        # price
        self.prices = [i[1]["price"] for i in self.data]
        self.meanPrice = round(mean(self.prices), 2)
        self.medianPrice = median(self.prices)
        self.modePrice = mode(self.prices)

        # achievements
        self.achievements = [i[1]["achievements"] for i in self.data]
        self.meanAchievements = int(round(mean(self.achievements), 0))
        self.medianAchievements = round(median(self.achievements), 0)
        self.modeAchievements = round(mode(self.achievements))
