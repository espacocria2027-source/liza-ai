"""
==========================================
Workflow Optimizer
==========================================
"""

class WorkflowOptimizer:

    def optimize(self, workflow):

        workflow.steps.sort(

            key=lambda step: step.id

        )

        return workflow


optimizer = WorkflowOptimizer()