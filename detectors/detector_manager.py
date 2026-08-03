"""
====================================================
Detector Manager
====================================================
"""


class DetectorManager:

    def __init__(self):

        self.detectors = []

    def register(self, detector):

        self.detectors.append(detector)

    def detect(self, message):

        for detector in self.detectors:

            resultado = detector.detect(message)

            if resultado is not None:

                return resultado

        return {

            "intent": "chat"

        }


detector_manager = DetectorManager()