import inspect


class Empty:
    pass


def get_default_args(func):
    signature = inspect.signature(func)
    return {
        k: v.default
        for k, v in signature.parameters.items()
        if v.default is not inspect.Parameter.empty
    }


def positional_or_keyword_values(method, args, kwargs):
    """
    Takes a method and its arguments and returns a dictionary of all values that will be passed to it. This allows for
    easy inspection.
    """
    args_names = method.__code__.co_varnames[:method.__code__.co_argcount]
    defaults = get_default_args(method)
    args_dict = {**dict(zip(args_names, args)), **kwargs}
    defaults.update(args_dict)
    return defaults


def retrieve_variadic(method, original_args):
    signature = inspect.signature(method)
    args = [*original_args]
    for p in signature.parameters.values():
        if p.kind is inspect.Parameter.POSITIONAL_ONLY:
            args = args[1:]
        elif p.kind is inspect.Parameter.VAR_POSITIONAL:
            return tuple(args)
    return ()


def construct_valid_function_args(method, defaults, original_args, original_kwargs):
    signature = inspect.signature(method)
    args = [*original_args]
    self_or_cls, positional, variadic, keywords = None, [], [], {}
    for p in signature.parameters.values():
        if p.name in {'self', 'cls'}:
            self_or_cls = defaults.pop(p.name, None)
            if len(args) and p.name not in original_kwargs:
                args = args[1:]
            continue
        if p.kind is inspect.Parameter.POSITIONAL_ONLY:
            if len(args):
                positional.append(defaults.pop(p.name, None))
                args = args[1:]
        elif p.kind is inspect.Parameter.POSITIONAL_OR_KEYWORD:
            if p.name in original_kwargs:
                keywords[p.name] = defaults.pop(p.name, None)
            elif len(args):
                positional.append(defaults.pop(p.name, None))
                args = args[1:]
        elif p.kind is inspect.Parameter.VAR_POSITIONAL:
            variadic = [*args]
        elif p.kind is inspect.Parameter.KEYWORD_ONLY:
            keywords[p.name] = defaults.pop(p.name, None)
    keywords.update(defaults)
    return self_or_cls, positional, variadic, keywords
