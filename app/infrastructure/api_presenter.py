from typing import Dict, TypedDict, Any, Optional

from app.adapters.ports.presenter import Presenter
from app.usecases.response import ResponseStatus, Response

class ApiResponse(TypedDict):
    code: int
    body: Dict[str, Any]

class ApiPresenter(Presenter):
    response_codes: Dict[ResponseStatus, int] = {
        ResponseStatus.OK: 200,
        ResponseStatus.CREATED: 201,
        ResponseStatus.BADREQUEST: 400,
        ResponseStatus.NOTFOUND: 404,
        ResponseStatus.TEAPOT: 418,
    }

    def present(
        self,
        response: Response,
    ) -> ApiResponse:
        return ApiResponse(
            code=self.response_codes[response.status],
            body=self.build_body(
                data=response.data,
                message=response.message,
            )
        )

    @staticmethod
    def build_body(
        data: Optional[Dict[str, Any] | str],
        message: Optional[str],
    ) -> Dict[str, Any]:
        body = data if data is not None else {}
        if message is not None:
            body['message'] = message

        return body
