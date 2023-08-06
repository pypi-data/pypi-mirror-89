from unittest import TestCase
import os
from ppdp_anonops import Swapping
from pm4py.objects.log.importer.xes import factory as xes_importer


class TestSwapping(TestCase):
    def getTestXesLog(self):
        xesPath = os.path.join(os.path.dirname(__file__), 'resources', 'Sepsis Cases - Event Log.xes')
        return xes_importer.apply(xesPath)

    def test_01_EventLevelSwapping(self):
        for clusters in range(4, 7):
            log = self.getTestXesLog()

            s = Swapping()

            # Needs to be a numeric attribute
            matchAttribute = "CRP"

            log = s.SwapEventAttributeValuesBykMeanCluster(log, matchAttribute, ["org:resource"], clusters)

            # What to assert on a randomized cluster value?...

    def __getNumberOfDistinctEventAttributeValues(self, xesLog, attribute):
        values = []

        for case_index, case in enumerate(xesLog):
            for event_index, event in enumerate(case):
                if(attribute in event.keys() and event[attribute] not in values):
                    values.append(event[attribute])

        return len(values)
