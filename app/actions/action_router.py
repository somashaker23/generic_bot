from app.actions.test_drive_action import TestDriveAction
from app.actions.callback_action import CallbackAction
from app.actions.car_valuation_action import CarValuationAction


class ActionRouter:
    def __init__(self):
        self.registry = {
            "book_test_drive": TestDriveAction,
            "request_callback": CallbackAction,
            "car_valuation": CarValuationAction,
        }

    def execute(self, intent: str, context: dict, db):
        action_cls = self.registry.get(intent)
        if not action_cls:
            return None

        action = action_cls()
        return action.run(context, db)
