"""
====================================================
Detector Registry
====================================================
"""

from detectors.detector_manager import (
    detector_manager
)

from detectors.command_detector import (
    CommandDetector
)

from detectors.programmer_detector import (
    ProgrammerDetector
)

from detectors.research_detector import (
    ResearchDetector
)


# ==================================================
# COMMAND
# ==================================================

detector_manager.register(

    CommandDetector()

)


# ==================================================
# PROGRAMMER
# ==================================================

detector_manager.register(

    ProgrammerDetector()

)


# ==================================================
# RESEARCH
# ==================================================

detector_manager.register(

    ResearchDetector()

)

print("=================================")
print("DETECTORES REGISTRADOS")
print([
    detector.__class__.__name__
    for detector in detector_manager.detectors
])
print("=================================")