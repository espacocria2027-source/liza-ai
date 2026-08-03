"""
====================================================
Detector Registry
====================================================
"""

from detectors.detector_manager import detector_manager

from detectors.command_detector import CommandDetector
from detectors.programmer_detector import ProgrammerDetector


detector_manager.register(

    CommandDetector()

)

detector_manager.register(

    ProgrammerDetector()

)