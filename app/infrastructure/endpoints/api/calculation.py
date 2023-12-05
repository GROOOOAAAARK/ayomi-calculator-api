from fastapi import APIRouter, Response
from fastapi.responses import StreamingResponse

from app.adapters.get_calculation_results_controller import GetCalculationResultsController
from app.adapters.get_calculation_csv_results_controller import GetCalculationCsvResultsController
from app.adapters.evaluate_expression_controller import EvaluateExpressionController, EvaluateExpressionInput

from app.infrastructure.api_presenter import ApiPresenter


router = APIRouter(prefix='/calculation', tags=['calculation'])

@router.get("/results")
async def results(res: Response):
    controller = GetCalculationResultsController(ApiPresenter())

    gcr_response = controller.summon()

    res.status_code = gcr_response['code']

    return gcr_response['body']

@router.get("/csv_results", tags=['calculation'])
async def csv_results(response_class: StreamingResponse):
    controller = GetCalculationCsvResultsController(ApiPresenter())

    file_path = 'results.csv'

    gcr_response = controller.summon(file_path)

    def iter_csv():
        with open(file_path, encoding='utf-8') as csvfile:
            yield from csvfile

    res = StreamingResponse(
        content=iter_csv(),
        status_code=gcr_response['code'],
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=${file_path}"},
    )

    return res

@router.post("/evaluate", tags=['calculation'])
async def evaluate(
    data: EvaluateExpressionInput,
    res: Response,
):
    controller = EvaluateExpressionController(ApiPresenter())

    ee_response = controller.summon(data)

    res.status_code = ee_response['code']

    return ee_response['body']
