import traceback
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Type

from .Strings import StringTools as Strings


class ErrorResponseKeys(str, Enum):
    class_name: str = 'class_name'
    method: str = 'method'
    task: str = 'task'

    status: str = 'status'
    message: str = 'message'
    suggestion: str = 'suggestion'

    stack_trace: str = 'stack_trace'
    major: str = 'major'
    warning: str = 'warning'

    @staticmethod
    def get_keys(title_case: Optional[bool] = False) -> List[str]:
        erk: Type[ErrorResponseKeys] = ErrorResponseKeys
        output: List[str] = [
            erk.class_name, erk.method, erk.task, erk.status, erk.message,
            erk.suggestion, erk.stack_trace, erk.major, erk.warning
        ]

        if title_case:
            return [Strings.regularize_string(x) for x in output]

        return output


@dataclass
class ErrorResponse:
    class_name: str
    method: str = 'Not Specified'
    task: str = 'Not Specified'

    status: str = ''
    message: str = ''
    suggestion: str = None

    stack_trace: str = None
    major: bool = False
    warning: bool = False

    def __copy__(self) -> 'ErrorResponse':
        return ErrorResponse(self.class_name, method=self.method, task=self.task,
                             status=self.status, message=self.message, suggestion=self.suggestion,
                             stack_trace=self.stack_trace, major=self.major, warning=self.warning)

    def transform_to_dict(self) -> dict:
        erk: Type[ErrorResponseKeys] = ErrorResponseKeys
        return {erk.class_name.value: self.class_name, erk.method.value: self.method,
                erk.task.value: self.task, erk.status.value: self.status,
                erk.message.value: self.message, erk.suggestion.value: self.suggestion,
                erk.stack_trace.value: self.stack_trace, erk.major.value: self.major,
                erk.warning.value: self.warning}

    def transform_to_row(self) -> List[str]:
        return [
            self.class_name, self.method, self.task, self.status, self.message,
            self.suggestion, self.stack_trace, str(self.major), str(self.warning)
        ]

    def transform_to_rows(self, include_header: Optional[bool] = False,
                          title_case: Optional[bool] = True) -> List[List[str]]:
        output: List[List[str]] = []

        if include_header:
            output.append(ErrorResponseKeys.get_keys(title_case=title_case))

        output.append(self.transform_to_row())
        return output

    def update_stack_trace(self, error: Optional[Exception] = None,
                           append_error: Optional[bool] = True) -> str:
        if error is not None:
            if self.stack_trace is not None and append_error:
                self.stack_trace += '\n\n{}'.format(str(error))
            else:
                self.stack_trace = '{}\n{}'.format(str(error), traceback.format_exc())
        else:
            self.stack_trace = traceback.format_exc()

        return self.stack_trace
