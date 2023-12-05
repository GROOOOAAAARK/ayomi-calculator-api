from app.adapters.ports.presenter import Presenter
from app.usecases.get_calculation_results import GetCalculationResults


class GetCalculationResultsController:
    def __init__(self, presenter: Presenter):
        self.presenter = presenter

    def summon(self):

        uc_response = GetCalculationResults().execute()

        return self.presenter.present(uc_response)