from dependency_injector.wiring import inject, Provide

from app.usecases.ports.abstract_storage import AbstractStorage
from app.usecases.response import Response, ResponseMessage, ResponseStatus

@inject
class GetCalculationResults:
    def __init__(self, storage: AbstractStorage = Provide['storage']):
        self.__storage = storage

    def execute(self) -> Response:

        calculations = self.__storage.read('calculations', projection={'_id': 0})

        if len(calculations) == 0:
            return Response.failed(
                status=ResponseStatus.NOTFOUND,
                message=ResponseMessage.NO_CALCULATIONS,
            )

        return Response.succeeded(
            status=ResponseStatus.OK,
            data={
                'calculations': calculations
            },
        )
