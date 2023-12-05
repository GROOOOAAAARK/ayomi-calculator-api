import csv
from dependency_injector.wiring import inject, Provide

from app.usecases.ports.abstract_storage import AbstractStorage
from app.usecases.response import Response, ResponseMessage, ResponseStatus

@inject
class GetCalculationCsvResults:
    def __init__(self, storage: AbstractStorage = Provide['storage']):
        self.__storage = storage

    def execute(
        self,
        file_path: str,
    ) -> Response:

        calculation_results = self.__storage.read(
            'calculations',
            projection={'_id': 0}
        )

        if len(calculation_results) == 0:
            return Response.failed(
                status=ResponseStatus.NOTFOUND,
                message=ResponseMessage.NO_CALCULATIONS,
            )

        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = calculation_results[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for calculation in calculation_results:
                writer.writerow(calculation)

            return Response.succeeded(
                status=ResponseStatus.OK,
            )
