"""Main."""
import warnings
from typing import Union, List, Any
from types import ModuleType


def call_single(loading_data: dict, search_modules: List[ModuleType], **kwargs) -> Any:
    """From the list of modules, find the class written in yaml and instantiate it."""
    assert len(loading_data.keys()) == 1, "len(loading_data.keys()) != 1"
    if isinstance(loading_data, dict):
        for instance_or_function in _call_instance_or_function(
            loading_data, search_modules, **kwargs
        ):
            return instance_or_function
    else:
        TypeError


def call_multiple(
    loading_data: Union[dict, List[dict]], search_modules: List[ModuleType], **kwargs
) -> list:
    """From the list of modules, find the class written in yaml and instantiate it."""
    instance_list = []
    if isinstance(loading_data, list):
        for conf in loading_data:
            for instance in _call_instance_or_function(conf, search_modules, **kwargs):
                instance_list.append(instance)
    elif isinstance(loading_data, dict):
        for instance in _call_instance_or_function(
            loading_data, search_modules, **kwargs
        ):
            instance_list.append(instance)
    else:
        TypeError

    return instance_list


def yaml2instances(
    loading_data: Union[dict, List[dict]], search_modules: List[ModuleType], **kwargs
) -> list:
    """From the list of modules, find the class written in yaml and instantiate it."""
    warnings.warn("yaml2instances is deprecated. Use call_multiple_process.")
    instance_list = []
    if isinstance(loading_data, list):
        for conf in loading_data:
            for instance in _call_instance_or_function(conf, search_modules, **kwargs):
                instance_list.append(instance)
    elif isinstance(loading_data, dict):
        for instance in _call_instance_or_function(
            loading_data, search_modules, **kwargs
        ):
            instance_list.append(instance)
    else:
        TypeError

    return instance_list


def _call_instance_or_function(
    loading_data: dict, search_modules: List[ModuleType], **kwargs
):
    modules_dict = {}
    for module in search_modules:
        _modules = module.__dict__
        modules_dict.update(_modules)
    for _item, _kwargs in loading_data.items():
        base = {}
        base.update(kwargs or {})
        base.update(_kwargs or {})
        instance = modules_dict[_item](**base)
        yield instance
