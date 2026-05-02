import ast
import copy
from io import StringIO
from types import FunctionType
from inspect import iscoroutine
from traceback import print_exc
from contextlib import redirect_stdout
from typing import Any, Iterable, Sequence, TypeVar

from discord import ButtonStyle
from discord.ext.paginators import ButtonPaginator, PaginatorButton

T = TypeVar("T")


async def execute(code: str, globals: dict[str, Any] = {}) -> str:
    output = StringIO()
    try:
        code = compile(code, "<message>", "exec", ast.PyCF_ALLOW_TOP_LEVEL_AWAIT)
        func = FunctionType(code, globals)
        with redirect_stdout(output):
            coro = func()
            if iscoroutine(coro):
                await coro
    except Exception:
        print_exc(file=output)
    return output.getvalue()


def chunks(lst: Sequence[T], n: int) -> Iterable[Sequence[T]]:
    for i in range(0, len(lst), n):
        yield lst[i : i + n]  # noqa: E203


class ConstantPaginatorButton(PaginatorButton):
    @property
    def label(self):
        return super().label

    @label.setter
    def label(self, value):
        # ignore
        pass

    @property
    def style(self):
        return super().style

    @style.setter
    def style(self, value):
        # ignore
        pass

    def _copy(self):
        return copy.deepcopy(self)


class Paginator(ButtonPaginator):
    def __init__(self, pages: list):
        super().__init__(
            pages,
            buttons={
                "FIRST": ConstantPaginatorButton(label="<<", style=ButtonStyle.blurple),
                "LEFT": ConstantPaginatorButton(label="<", style=ButtonStyle.green),
                "PAGE_INDICATOR": PaginatorButton(disabled=True, style=ButtonStyle.gray),
                "RIGHT": ConstantPaginatorButton(label=">", style=ButtonStyle.green),
                "LAST": ConstantPaginatorButton(label=">>", style=ButtonStyle.blurple),
                "STOP": None,
            },
            disable_after=True,
            add_page_string=False,
        )

    @property
    def page_string(self) -> str:
        return f"{self.current_page + 1} / {self.max_pages}"

    async def send(self, context, dest=None):
        self.author_id = context.author.id
        return await super().send(dest or context)
