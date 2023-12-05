from dependency_injector.wiring import inject, Provide
from pydantic import BaseModel
from typing import Union

from app.usecases.response import Response, ResponseMessage, ResponseStatus
from app.usecases.ports.abstract_storage import AbstractStorage


class EvaluateExpressionInput(BaseModel):
    expression: str
    ref: str


@inject
class EvaluateExpression:
    def __init__(
        self,
        storage: AbstractStorage = Provide['storage'],
    ) -> None:
        self.__storage = storage
        self.__stack = []
        self.__operations = {
            '+': self._add,
            '-': self._sub,
            '/': self._div,
            '*': self._mul,
        }

    def execute(
        self,
        data: EvaluateExpressionInput,
    ) -> Response:
        '''Evaluate expression, calculate result, register it in DB and return '''

        result = 0

        try:

            for entry in data.expression.split():
                entry = self._get_number(entry)
                if isinstance(entry, int):
                    self.__stack.append(entry)
                elif isinstance(entry, float):
                    if entry.is_integer():
                        self.__stack.append(int(entry))
                    else:
                        self.__stack.append(entry)

                elif isinstance(entry, str):
                    if entry in self.__operations:
                        self.__operations[entry]()
                    else:
                        raise ValueError(f'Invalid entry {entry}')
        except ValueError:
            return Response.failed(
                status=ResponseStatus.BADREQUEST,
                message=ResponseMessage.INVALID_EXPRESSION,
            )
        except ZeroDivisionError:
            return Response.failed(
                status=ResponseStatus.BADREQUEST,
                message=ResponseMessage.DIVISION_BY_ZERO,
            )

        if len(self.__stack) != 1:
            return Response.failed(
                status=ResponseStatus.BADREQUEST,
                message=ResponseMessage.INVALID_EXPRESSION,
            )

        result = self.__stack.pop()

        calculation = {
            'expression': data.expression,
            'result': result,
            'ref': data.ref,
        }

        self.__storage.create(
            'calculations',
            [calculation],
        )


        return Response.succeeded(
            status=ResponseStatus.CREATED,
            message=ResponseMessage.EXPRESSION_EVALUATED,
            data={
                'expression': data.expression,
                'result': result,
            }
        )

    def _check_stack_size(self, num_entries: int) -> bool:
        '''Check if the stack has enough entries to perform an operation'''
        return len(self.__stack) >= num_entries

    def _add_to_stack(self, value) -> None:
        '''Add value to stack'''
        if isinstance(value, int):
            self.__stack.append(value)
        elif isinstance(value, float):
            if value.is_integer():
                self.__stack.append(int(value))
            else:
                self.__stack.append(value)
        else:
            raise ValueError(f'Invalid data type {type(value)}')

    def _get_number(self, entry: str) -> Union[int, float, str]:
        '''Convert string to int or float'''
        for cast_type in (int, float):
            try:
                return cast_type(entry)
            except ValueError:
                continue
        return entry

    def _add(self) -> None:
        if self._check_stack_size(2):
            self._add_to_stack(self.__stack.pop() + self.__stack.pop())

    def _sub(self) -> None:
        if self._check_stack_size(2):
            self._add_to_stack(self.__stack.pop() - self.__stack.pop())

    def _div(self) -> None:
        if self._check_stack_size(2):
            self._add_to_stack(self.__stack.pop() / self.__stack.pop())

    def _mul(self) -> None:
        if self._check_stack_size(2):
            self._add_to_stack(self.__stack.pop() * self.__stack.pop())
