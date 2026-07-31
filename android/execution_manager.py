"""
====================================================
Execution Manager
====================================================
"""

from threading import Lock


class ExecutionManager:

    def __init__(self):

        self.lock = Lock()

        self.executions = {}

    def create(self, execution_id, package):

        with self.lock:

            self.executions[execution_id] = {

                "status": "pending",

                "package": package,

                "result": None

            }

    def finish(self, execution_id, result):

        with self.lock:

            if execution_id in self.executions:

                self.executions[execution_id]["status"] = "finished"

                self.executions[execution_id]["result"] = result

    def get(self, execution_id):

        return self.executions.get(execution_id)


manager = ExecutionManager()