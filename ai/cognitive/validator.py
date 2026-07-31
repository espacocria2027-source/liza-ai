"""
==========================================
Workflow Validator
==========================================
"""

class WorkflowValidator:

    def validate(self, workflow):

        if len(workflow.steps) == 0:

            raise Exception("Workflow vazio.")

        return workflow


validator = WorkflowValidator()