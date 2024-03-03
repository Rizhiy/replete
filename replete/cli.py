from __future__ import annotations

import argparse
import collections.abc
import datetime as dt
import functools
import inspect
import typing
from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, ClassVar, Generic, NamedTuple, Sequence, TypeVar, Union, cast, overload

import docstring_parser


class CLIError(Exception):
    """Exception for all things CLI"""


T = TypeVar("T")
TRet = TypeVar("TRet")
TCallable = TypeVar("TCallable", bound=Union[Callable[..., TRet], Callable[..., None]])  # type: ignore
NoneType = type(None)


COMMON_ANNOTATIONS_NS: dict[str, Any] = {
    key: getattr(module, key)
    for module in (typing, collections.abc)
    for key in module.__all__
    if not key.startswith("_")
}


def pairs_to_dict(
    key_parse: Callable[[Any], Any] = str,
    val_parse: Callable[[Any], Any] = str,
    *,
    allow_empty: bool = True,
) -> Callable[[Any], Any]:
    """
    Convert list of keys and values into dict
    """

    def _pairs_to_dict_configured(items: Sequence[T] | None) -> dict[T, T]:
        if not items:
            if allow_empty:
                return {}
            raise ValueError("Got empty list of items")
        if isinstance(items, dict):
            return items
        if len(items) % 2 != 0:
            raise ValueError("Must have key-value pairs (even number)", {"items": items})
        keys = [key_parse(key) for key in items[::2]]
        values = [val_parse(val) for val in items[1::2]]
        return dict(zip(keys, values, strict=True))

    return _pairs_to_dict_configured


def parse_bool(value: str) -> bool:
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    raise ValueError(f"Not a valid bool: {value!r}; must be `true` or `false`")


def _resolve_type_annotation(type_annotation: Any, annotations_ns: dict[str, Any] | None = None) -> tuple[Any, Any]:
    if type_annotation is inspect.Signature.empty:
        return None, None
    if isinstance(type_annotation, str):
        try:
            type_annotation = eval(type_annotation, COMMON_ANNOTATIONS_NS | (annotations_ns or {}))  # noqa: S307
        except Exception:  # noqa: BLE001
            return None, None

    type_origin = getattr(type_annotation, "__origin__", None)
    if type_origin is None:
        return type_annotation, None
    # Otherwise, assuming something like e.g. `typing._GenericAlias`
    type_args: tuple[Any, ...] = getattr(type_annotation, "__args__", None) or ()

    # `Optional[X]` support
    if type_origin is Union and len(type_args) == 2 and NoneType in type_args:
        inner_type = next((item for item in type_args if item is not NoneType), None)
        if hasattr(inner_type, "__origin__"):
            return _resolve_type_annotation(inner_type, annotations_ns=annotations_ns)
        return inner_type, None

    type_name = getattr(type_annotation, "_name", None) or getattr(type_origin, "__name__", None)
    if type_origin is dict:
        if isinstance(type_args, tuple) and len(type_args) == 2:
            return type_origin, type_args
        return type_origin, None
    if type_origin in (list, tuple):
        if isinstance(type_args, tuple) and len(type_args) == 1:
            return type_origin, type_args[0]
        return type_origin, None
    if type_name in ("Sequence", "Iterable"):
        if isinstance(type_args, tuple) and len(type_args) == 1:
            return list, type_args[0]
        return list, None
    # Not recognized.
    return None, None


class ParamInfo(NamedTuple):
    name: str
    required: bool = True
    default: Any = None
    value_type: Any = None
    # per-item type for sequences, (dict_key_type, dict_value_type) for dicts.
    contained_type: Any = None
    extra_args: bool = False
    extra_kwargs: bool = False
    doc: str | None = None

    @classmethod
    def from_arg_param(
        cls,
        arg_param: inspect.Parameter,
        annotations_ns: dict[str, Any] | None = None,
        default: Any = None,
        **kwargs: Any,
    ) -> ParamInfo:
        if default is not None:
            required = False
        else:
            required = arg_param.default is inspect.Signature.empty
            default = arg_param.default if not required else None

        value_type, value_contained_type = _resolve_type_annotation(arg_param.annotation, annotations_ns=annotations_ns)
        if value_type is None and default is not None:
            value_type = type(default)

        return cls(
            name=arg_param.name,
            required=required,
            default=default,
            value_type=value_type,
            contained_type=value_contained_type,
            extra_args=arg_param.kind is inspect.Parameter.VAR_POSITIONAL,
            extra_kwargs=arg_param.kind is inspect.Parameter.VAR_KEYWORD,
            **kwargs,
        )


class ParamExtras(NamedTuple):
    param_info: ParamInfo | None = None
    name_norm: str | None = None
    arg_argparse_extra_kwargs: dict[str, Any] | None = None
    arg_postprocess: Callable[[Any], Any] | None = None
    type_converter: Callable[[Any], Any] | None = None
    type_postprocessor: Callable[[Any], Any] | None = None

    def replace(self, **kwargs: Any) -> ParamExtras:
        return self._replace(**kwargs)


@dataclass
class AutoCLIBase(Generic[TCallable], ABC):
    """Base interface for an automatic function-to-CLI processing"""

    func: TCallable
    argv: Sequence[Any] | None | None = None

    fail_on_unknown_args: bool = True  # safe default
    postprocess: dict[str, Callable[[Any], Any]] | None = None
    argparse_kwargs: dict[str, dict[str, Any]] | None = None
    annotations_ns: dict[str, Any] | None = field(default=None, repr=False)
    TYPE_CONVERTERS: ClassVar[dict[Any, Callable[[str], Any]]] = {
        dt.date: dt.date.fromisoformat,
        dt.datetime: dt.datetime.fromisoformat,
    }
    TYPE_AUTO_PARAMS: ClassVar[dict[Any, Callable[[ParamInfo], ParamExtras]]] = {
        # TODO: actually make the boolean arguments into `--flag/--no-flag`.
        bool: lambda _: ParamExtras(arg_argparse_extra_kwargs={"type": parse_bool}),
        dict: lambda param_info: ParamExtras(
            arg_argparse_extra_kwargs={"nargs": "*", "type": str},
            arg_postprocess=pairs_to_dict(
                key_parse=param_info.contained_type[0] if param_info.contained_type else str,
                val_parse=param_info.contained_type[1] if param_info.contained_type else str,
            ),
        ),
        list: lambda param_info: ParamExtras(
            arg_argparse_extra_kwargs={"nargs": "*", "type": param_info.contained_type or str},
        ),
    }

    @abstractmethod
    def __call__(self, *args: Any, **kwargs: Any) -> TRet | None:  # type: ignore
        raise NotImplementedError

    @classmethod
    def _make_param_infos(
        cls,
        func: Callable[..., Any],
        params_docs: dict[str, Any] | None = None,
        annotations_ns: dict[str, Any] | None = None,
        defaults: dict[str, Any] | None = None,
        signature: inspect.Signature | None = None,
    ) -> Sequence[ParamInfo]:
        signature = signature or inspect.signature(func, follow_wrapped=False)
        params_docs = params_docs or {}
        defaults = defaults or {}
        return [
            ParamInfo.from_arg_param(
                arg_param,
                doc=params_docs.get(name),
                annotations_ns=annotations_ns,
                default=defaults.get(name),
            )
            for name, arg_param in signature.parameters.items()
        ]


class _TunedHelpFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter):
    _default_width: ClassVar[int | None] = None
    _default_max_help_position: ClassVar[int | None] = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        if self._default_width is not None:
            kwargs["width"] = kwargs.get("width", self._default_width)
        if self._default_max_help_position is not None:
            kwargs["max_help_position"] = kwargs.get("max_help_position", self._default_max_help_position)
        super().__init__(*args, **kwargs)


def _indent(value: str, indentation: str = "    ") -> str:
    return indentation + value.replace("\n", "\n" + indentation).replace(indentation + "\n", "\n")


@dataclass
class AutoCLI(AutoCLIBase[TCallable]):
    """
    `argparse.ArgumentParser`-based automatic-function-to-CLI.
    """

    help_width: int | None = None
    max_help_position: int | None = None
    formatter_class: type[argparse.HelpFormatter] = _TunedHelpFormatter
    signature_override: inspect.Signature | None = None
    _description_indent: str = "  "
    # mock default for `dataclass`, gets filled in `__post_init__` with an actual value.
    __wrapped__: Callable[..., Any] = lambda: None  # noqa: E731

    @classmethod
    def _base_param_extras(cls, param_info: ParamInfo) -> ParamExtras:
        value_type = param_info.value_type
        extras_factory = cls.TYPE_AUTO_PARAMS.get(value_type) or ParamExtras
        extras = extras_factory(param_info)
        if extras.param_info is None:  # For easier `TYPE_AUTO_PARAMS`.
            extras = extras.replace(param_info=param_info)
        else:
            param_info = extras.param_info
        if extras.type_converter is None and value_type in cls.TYPE_CONVERTERS:
            extras = extras.replace(type_converter=cls.TYPE_CONVERTERS[value_type])
        if extras.name_norm is None:
            extras = extras.replace(name_norm=cls._param_to_arg_name_norm(param_info.name))
        return extras

    def __post_init__(self) -> None:
        functools.wraps(self.func)(self)

    def _full_params_extras(self, param_infos: Sequence[ParamInfo]) -> dict[str, ParamExtras]:
        """
        All the class and instance overrides combined into one structure.

        :return: {field_name: field_configuration}
        """
        argparse_kwargs = self.argparse_kwargs or {}
        postprocess = self.postprocess or {}
        result = {}
        for param_info in param_infos:
            name = param_info.name
            param_extras = self._base_param_extras(param_info)
            # AutoCLI instance kwargs take precedence over class-level kwargs.
            if name in argparse_kwargs:
                param_extras = param_extras.replace(arg_argparse_extra_kwargs=argparse_kwargs[name])
            if name in postprocess:
                param_extras = param_extras.replace(type_postprocessor=postprocess[name])
            result[name] = param_extras
        return result

    def _make_full_parser_and_params_extras(
        self,
        defaults: dict[str, Any],
    ) -> tuple[argparse.ArgumentParser, dict[str, ParamExtras]]:
        docs = docstring_parser.parse(self.func.__doc__ or "")
        params_docs = {param.arg_name: param.description for param in docs.params} if docs.params else {}
        description = "\n\n".join(item for item in (docs.short_description, docs.long_description) if item)
        description = _indent(description, self._description_indent)
        parser = self._make_base_parser(description=description)
        param_infos = self._make_param_infos(
            self.func,
            params_docs,
            self.annotations_ns,
            defaults,
            self.signature_override,
        )
        params_extras = self._full_params_extras(param_infos)
        for param in param_infos:
            param_extras = params_extras[param.name]
            self._add_argument(
                parser=parser,
                name=param_extras.name_norm or param.name,
                param=param,
                arg_extra_kwargs=param_extras.arg_argparse_extra_kwargs,
            )
        return parser, params_extras

    def _make_base_parser(self, description: str) -> argparse.ArgumentParser:
        formatter_class = self.formatter_class
        formatter_class = type(
            f"_Custom_{formatter_class.__name__}",
            (formatter_class,),
            {"_default_width": self.help_width, "_default_max_help_position": self.max_help_position},
        )
        return argparse.ArgumentParser(formatter_class=formatter_class, description=description)  # type: ignore

    @staticmethod
    def _param_to_arg_name_norm(name: str) -> str:
        return name.rstrip("_")

    @staticmethod
    def _pos_param_to_arg_name(name_norm: str) -> str:
        return name_norm

    @staticmethod
    def _opt_param_to_arg_name(name_norm: str) -> str:
        return "--" + name_norm.replace("_", "-")

    @classmethod
    def _add_argument(
        cls,
        parser: argparse.ArgumentParser,
        name: str,
        param: ParamInfo,
        arg_extra_kwargs: dict[str, Any] | None = None,
    ) -> None:
        arg_name = cls._pos_param_to_arg_name(name) if param.required else cls._opt_param_to_arg_name(name)

        type_converter = cls.TYPE_CONVERTERS.get(param.value_type) or param.value_type
        arg_kwargs = {"type": type_converter, "help": param.doc}
        if not param.required:
            arg_kwargs.update({"default": param.default, "help": param.doc or " "})

        if param.extra_args:  # `func(*args)`
            # Implementation: `arg_kwargs.update(nargs="*")`
            raise CLIError("Not currently supported: `**args` in function")
        if param.extra_kwargs:  # `func(**kwargs)`
            raise CLIError("Not currently supported: `**kwargs` in function")
        arg_extra_kwargs = dict(arg_extra_kwargs or {})
        arg_extra_args = arg_extra_kwargs.pop("__args__", None) or ()
        arg_kwargs.update(arg_extra_kwargs)
        parser.add_argument(arg_name, *arg_extra_args, **arg_kwargs)  # type: ignore  # very tricky typing.

    def _make_overridden_defaults(
        self,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
    ) -> tuple[dict[str, Any], tuple[Any, ...]]:
        var_args = cast(tuple[Any, ...], ())
        if not args:
            return kwargs or {}, var_args
        signature = inspect.signature(self.func)

        var_arg = next(
            (param for param in signature.parameters.values() if param.kind is inspect.Parameter.VAR_POSITIONAL),
            None,
        )
        var_kwarg = next(
            (param for param in signature.parameters.values() if param.kind is inspect.Parameter.VAR_KEYWORD),
            None,
        )
        if var_arg is not None:
            raise CLIError("Not currently supported: `**args` in function")
        if var_kwarg is not None:
            raise CLIError("Not currently supported: `**kwargs` in function")

        return signature.bind_partial(*args, **kwargs).arguments, var_args

    def _postprocess_values(
        self,
        parsed_kwargs: dict[str, Any],
        params_extras: dict[str, ParamExtras],
    ) -> dict[str, Any]:
        parsed_kwargs = parsed_kwargs.copy()
        for name, param_extras in params_extras.items():
            if param_extras.arg_postprocess and name in parsed_kwargs:
                parsed_kwargs[name] = param_extras.arg_postprocess(parsed_kwargs[name])
        return parsed_kwargs

    def __call__(self, *args: Any, **kwargs: Any) -> TRet | None:  # type: ignore
        defaults, var_args = self._make_overridden_defaults(args, kwargs)

        parser, params_extras = self._make_full_parser_and_params_extras(defaults=defaults)
        params, unknown_args = parser.parse_known_args(self.argv)
        if unknown_args and self.fail_on_unknown_args:
            raise SystemExit("Unrecognized arguments", {"unknown_args": unknown_args})
        parsed_args = params._get_args()  # generally, an empty list.  # noqa: SLF001
        parsed_kwargs_base = params._get_kwargs()  # noqa: SLF001
        arg_name_to_param_name = {
            extras.name_norm or param_name: param_name for param_name, extras in params_extras.items()
        }
        parsed_kwargs = {arg_name_to_param_name[key]: val for key, val in parsed_kwargs_base}
        parsed_kwargs = self._postprocess_values(parsed_kwargs, params_extras=params_extras)

        full_args = [*var_args, *parsed_args]
        full_kwargs = {**kwargs, **parsed_kwargs}
        return self.func(*full_args, **full_kwargs)  # type: ignore


def get_caller_ns(extra_stack: int = 0) -> dict[str, Any] | None:
    here = inspect.currentframe()
    # One step to get caller of this utility function,
    # extra step to get its caller.
    for _ in range(2 + extra_stack):
        if not here:
            return None
        here = here.f_back
    if not here:
        return None
    return {**here.f_globals, **here.f_locals}


@overload
def autocli(func: TCallable, **config: Any) -> AutoCLI[TCallable]: ...


@overload
def autocli(func: None = None, **config: Any) -> Callable[[TCallable], AutoCLI[TCallable]]: ...


def autocli(
    func: TCallable | None = None,
    **config: Any,
) -> AutoCLI[TCallable] | Callable[[TCallable], AutoCLI[TCallable]]:
    actual_config = config.copy()

    def autocli_wrap(func: TCallable) -> AutoCLI[TCallable]:
        if "annotations_ns" not in actual_config:
            actual_config["annotations_ns"] = get_caller_ns()
        return AutoCLI(func, **actual_config)

    if func is not None:
        if "annotations_ns" not in actual_config:
            actual_config["annotations_ns"] = get_caller_ns()
        return autocli_wrap(func)
    return autocli_wrap
