from typing import Dict, Any

from app.adapters.ports.presenter import Presenter
from app.usecases.evaluate_expression import EvaluateExpression, EvaluateExpressionInput

class EvaluateExpressionController:
    def __init__(
        self,
        presenter: Presenter,
    ) -> None:
        self.__presenter = presenter

    def summon(
        self,
        checked_data: EvaluateExpressionInput,
    ) -> Dict[str, Any]:

        uc_response = EvaluateExpression().execute(
            data=checked_data,
        )

        return self.__presenter.present(response=uc_response)
