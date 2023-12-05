from app.adapters.ports.presenter import Presenter

from app.usecases.get_calculation_csv_results import GetCalculationCsvResults

class GetCalculationCsvResultsController:
    def __init__(self, presenter: Presenter):
        self.__presenter = presenter

    def summon(
        self,
        file_path: str,
    ):

        uc_response = GetCalculationCsvResults().execute(file_path)

        return self.__presenter.present(uc_response)