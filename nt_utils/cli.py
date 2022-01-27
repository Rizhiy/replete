from __future__ import annotations

import abc
import argparse
import datetime as dt
import functools
import inspect
from dataclasses import dataclass
from typing import Any, Callable, ClassVar, Dict, NamedTuple, Optional, Sequence, Tuple, Type, _GenericAlias

import docstring_parser


def pairs_to_dict(
    key_parse: Callable[[Any], Any] = str,
    val_parse: Callable[[Any], Any] = str,
    allow_empty: bool = True,
    name: str = "",
) -> Callable[[Any], Any]:
    def _pairs_to_dict_configured(items: Optional[Sequence[Any]]):
        if not items:
            if allow_empty:
                return {}
            raise ValueError("{name!r}: Must not be empty")
        if isinstance(items, dict):
            return items
        if len(items) % 2 != 0:
            raise ValueError("Must have key-value pairs (even number)", dict(items=items))
        keys = [key_parse(key) for key in items[::2]]
        values = [val_parse(val) for val in items[1::2]]
        return dict(zip(keys, values))

    return _pairs_to_dict_configured


def parse_bool(value: str) -> bool:
    if value in ("true", "True", "TRUE"):
        return True
    if value == ("false", "False", "FALSE"):
        return False
    raise ValueError(f"Not a valid bool: {value!r}; must be `true` or `false`")


class ParamInfo(NamedTuple):
    name: str
    required: bool = True
    default: Any = None
    type: Any = None
    # per-item type for sequences, (key_type, value_type) for dicts.
    contained_type: Any = None
    extra_args: bool = False
    extra_kwargs: bool = False
    doc: str = None

    @classmethod
    def from_arg_param(
        cls, arg_param: inspect.Parameter, annotations_ns: dict = None, default: Any = None, **kwargs: Any,
    ) -> ParamInfo:
        if default is not None:
            required = False
        else:
            required = arg_param.default is inspect.Signature.empty
            default = arg_param.default if not required else None

        value_type = arg_param.annotation
        if value_type is inspect.Signature.empty:
            value_type = None

        if not value_type and default is not None:
            value_type = type(default)
        if isinstance(value_type, str):
            try:
                value_type = eval(value_type, annotations_ns or {})
            except Exception:
                value_type = None

        value_contained_type = None
        if isinstance(value_type, _GenericAlias):
            type_name = value_type._name
            type_origin = value_type.__origin__
            type_args = value_type.__args__
            if type_origin is dict:
                value_type = dict
                if isinstance(type_args, tuple) and len(type_args) == 2:
                    value_contained_type = type_args
            elif type_origin in (list, tuple):
                value_type = type_origin
                if isinstance(type_args, tuple) and len(type_args) == 1:
                    value_contained_type = type_args[0]
            elif type_name in ("Sequence", "Iterable"):
                value_type = list
                if isinstance(type_args, tuple) and len(type_args) == 1:
                    value_contained_type = type_args[0]
            else:
                value_type = None

        return cls(
            name=arg_param.name,
            required=required,
            default=default,
            type=value_type,
            contained_type=value_contained_type,
            extra_args=arg_param.kind is inspect.Parameter.VAR_POSITIONAL,
            extra_kwargs=arg_param.kind is inspect.Parameter.VAR_KEYWORD,
            **kwargs,
        )


class ParamExtras(NamedTuple):
    param_info: ParamInfo = None
    name_norm: str = None
    arg_argparse_extra_kwargs: Dict[str, Any] = None
    arg_postprocess: Callable[[Any], Any] = None
    type_converter: Callable[[Any], Any] = None
    type_postprocessor: Callable[[Any], Any] = None

    def replace(self, **kwargs) -> ParamExtras:
        return self._replace(**kwargs)


@dataclass
class AutoCLIBase:
    """
    Base interface for an automatic function-to-CLI processing.

    Note that this docstring has to be here because of a conflict between
    dataclass and the `__wrapped__` property.
    """

    func: Callable
    argv: Optional[Optional[Sequence[Any]]] = None

    fail_on_unknown_args: bool = True  # safe default
    postprocess: Optional[Dict[str, Callable[[Any], Any]]] = None
    argparse_kwargs: Optional[Dict[str, Dict[str, Any]]] = None
    annotations_ns: Optional[Dict[str, Any]] = None
    TYPE_CONVERTERS: ClassVar[Dict[Any, Callable[[str], Any]]] = {
        dt.date: dt.date.fromisoformat,
        dt.datetime: dt.datetime.fromisoformat,
    }
    TYPE_AUTO_PARAMS: ClassVar[Dict[Any, Callable[[ParamInfo], ParamExtras]]] = {
        # TODO: actually make the boolean arguments into `--flag/--no-flag`.
        bool: lambda param_info: ParamExtras(arg_argparse_extra_kwargs=dict(type=parse_bool)),
        dict: lambda param_info: ParamExtras(
            arg_argparse_extra_kwargs=dict(nargs="*", type=str),
            arg_postprocess=pairs_to_dict(
                key_parse=param_info.contained_type[0] if param_info.contained_type else str,
                val_parse=param_info.contained_type[1] if param_info.contained_type else str,
            ),
        ),
        list: lambda param_info: ParamExtras(
            arg_argparse_extra_kwargs=dict(nargs="*", type=param_info.contained_type or str),
        ),
    }

    @abc.abstractmethod
    def __call__(self, *args, **kwargs):
        raise NotImplementedError

    @property
    def __wrapped__(self) -> Callable:  # see `inspect.unwrap`
        return self.func

    @classmethod
    def _make_param_infos(
        cls,
        func,
        params_docs: Optional[Dict[str, Any]] = None,
        annotations_ns: Optional[Dict[str, Any]] = None,
        defaults: Optional[Dict[str, Any]] = None,
        signature: inspect.Signature = None,
    ) -> Sequence[ParamInfo]:
        signature = signature or inspect.signature(func, follow_wrapped=False)
        params_docs = params_docs or {}
        defaults = defaults or {}
        return [
            ParamInfo.from_arg_param(
                arg_param, doc=params_docs.get(name), annotations_ns=annotations_ns, default=defaults.get(name),
            )
            for name, arg_param in signature.parameters.items()
        ]


class _TunedHelpFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter):

    _default_width: Optional[ClassVar[int]] = None
    _max_help_position: Optional[ClassVar[int]] = None

    def __init__(self, *args, **kwargs):
        if self._default_width is not None:
            kwargs["width"] = kwargs.get("width", self._default_width)
        if self._max_help_position is not None:
            kwargs["max_help_position"] = kwargs.get("max_help_position", self._max_help_position)
        super().__init__(*args, **kwargs)


def _indent(value: str, indentation: str = "    ") -> str:
    return indentation + value.replace("\n", "\n" + indentation).replace(indentation + "\n", "\n")


@dataclass
class AutoCLI(AutoCLIBase):
    """
    `argparse.ArgumentParser`-based automatic-function-to-CLI.

    Note that this docstring has to be here because of a conflict between
    dataclass and the `__wrapped__` property.
    """

    help_width: int = None
    max_help_position: int = None
    formatter_class: Type[argparse.HelpFormatter] = _TunedHelpFormatter
    signature_override: inspect.Signature = None
    _description_indent: str = "  "

    @classmethod
    def _base_param_extras(cls, param_info: ParamInfo) -> ParamExtras:
        param_type = param_info.type
        extras_factory = cls.TYPE_AUTO_PARAMS.get(param_type) or ParamExtras
        extras = extras_factory(param_info=param_info)
        if extras.param_info is None:  # For easier `TYPE_AUTO_PARAMS`.
            extras = extras.replace(param_info=param_info)
        if extras.type_converter is None and param_type in cls.TYPE_CONVERTERS:
            extras = extras.replace(type_converter=cls.TYPE_CONVERTERS[param_type])
        if extras.name_norm is None:
            extras = extras.replace(name_norm=cls._param_to_arg_name_norm(extras.param_info.name))
        return extras

    def _full_params_extras(self, param_infos: Sequence[ParamInfo]) -> Dict[str, ParamExtras]:
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
        self, defaults: dict,
    ) -> Tuple[argparse.ArgumentParser, Dict[str, ParamExtras]]:
        docs = docstring_parser.parse(self.func.__doc__)
        params_docs = {param.arg_name: param.description for param in docs.params} if docs.params else {}
        description = "\n\n".join(item for item in (docs.short_description, docs.long_description) if item)
        description = _indent(description, self._description_indent)
        parser = self._make_base_parser(description=description)
        param_infos = self._make_param_infos(
            self.func, params_docs, self.annotations_ns, defaults, self.signature_override
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
        formatter_cls = self.formatter_class
        formatter_cls = type(
            f"_Custom_{formatter_cls.__name__}",
            (formatter_cls,),
            dict(_default_width=self.help_width, _max_help_position=self.max_help_position),
        )
        return argparse.ArgumentParser(formatter_class=formatter_cls, description=description)

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
    def _add_argument(cls, parser, name, param, arg_extra_kwargs: Optional[Dict[str, Any]] = None) -> str:
        if param.required:
            arg_name = cls._pos_param_to_arg_name(name)
        else:
            arg_name = cls._opt_param_to_arg_name(name)

        type_converter = cls.TYPE_CONVERTERS.get(param.type) or param.type
        arg_kwargs = dict(type=type_converter, help=param.doc)
        if not param.required:
            arg_kwargs.update(dict(default=param.default, help=param.doc or " "))

        if param.extra_args:  # `func(*args)`
            # Implementation: `arg_kwargs.update(nargs="*")`
            raise Exception("Not currently supported: `**args` in function")
        if param.extra_kwargs:  # `func(**kwargs)`
            raise Exception("Not currently supported: `**kwargs` in function")
        arg_extra_kwargs = dict(arg_extra_kwargs or {})
        arg_extra_args = arg_extra_kwargs.pop("__args__", None) or ()
        arg_kwargs.update(arg_extra_kwargs)
        parser.add_argument(arg_name, *arg_extra_args, **arg_kwargs)

    def _make_overridden_defaults(self, args: tuple, kwargs: Dict[str, Any]) -> Tuple[Dict[str, Any], tuple]:
        if not args:
            return kwargs or {}, ()
        signature = inspect.signature(self.func)

        var_arg = next(
            (param for param in signature.parameters.values() if param.kind is inspect.Parameter.VAR_POSITIONAL), None,
        )
        var_kwarg = next(
            (param for param in signature.parameters.values() if param.kind is inspect.Parameter.VAR_KEYWORD), None,
        )
        if var_arg is not None:
            raise Exception("Not currently supported: `**args` in function")
        if var_kwarg is not None:
            raise Exception("Not currently supported: `**kwargs` in function")

        return signature.bind_partial(*args, **kwargs).arguments, ()

    def _postprocess_values(self, parsed_kwargs: dict, params_extras: Dict[str, ParamExtras]) -> dict:
        parsed_kwargs = parsed_kwargs.copy()
        for name, param_extras in params_extras.items():
            if param_extras.arg_postprocess and name in parsed_kwargs:
                parsed_kwargs[name] = param_extras.arg_postprocess(parsed_kwargs[name])
        return parsed_kwargs

    def __call__(self, *args, **kwargs):
        defaults, var_args = self._make_overridden_defaults(args, kwargs)

        parser, params_extras = self._make_full_parser_and_params_extras(defaults=defaults)
        params, unknown_args = parser.parse_known_args(self.argv)
        if unknown_args and self.fail_on_unknown_args:
            raise Exception("Unrecognized arguments", dict(unknown_args=unknown_args))
        parsed_args = params._get_args()  # generally, an empty list.
        parsed_kwargs = params._get_kwargs()
        arg_name_to_param_name = {
            extras.name_norm or param_name: param_name for param_name, extras in params_extras.items()
        }
        parsed_kwargs = {arg_name_to_param_name[key]: val for key, val in parsed_kwargs}
        parsed_kwargs = self._postprocess_values(parsed_kwargs, params_extras=params_extras)

        full_args = [*var_args, *parsed_args]
        full_kwargs = {**kwargs, **parsed_kwargs}
        return self.func(*full_args, **full_kwargs)


def autocli(func=None, **config):
    def autocli_wrap(func):
        actual_config = config.copy()
        if "annotations_ns" not in actual_config:
            caller = inspect.currentframe().f_back
            actual_config["annotations_ns"] = {**caller.f_globals, **caller.f_locals}
        manager = AutoCLI(func, **actual_config)

        @functools.wraps(func)
        def autoargparse_wrapped(*args, **kwargs):
            return manager(*args, **kwargs)

        for attr in ("func",):
            setattr(autoargparse_wrapped, attr, getattr(manager, attr))
        autoargparse_wrapped.autocli = manager
        return autoargparse_wrapped

    if func is not None:
        return autocli_wrap(func)
    return autocli_wrap
