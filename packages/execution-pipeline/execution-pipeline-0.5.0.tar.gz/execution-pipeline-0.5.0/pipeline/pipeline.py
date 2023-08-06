import functools

from typing import Optional
from pydantic import BaseModel
from pydantic.types import PositiveInt

from pipeline import helpers

from pipeline.validators import ErrorHandler, PipelineCache, CallableOrListOfCallables


class PipelineSetupError(BaseException):
    pass


class ExecutionPipeLine(BaseModel):

    pre_segment: Optional[CallableOrListOfCallables] = None
    post_segment: Optional[CallableOrListOfCallables] = None
    error_handlers: Optional[ErrorHandler] = None
    cache: Optional[PipelineCache] = None
    cache_lifetime: PositiveInt

    def __init__(self, pre=None, post=None, error=None, cache=None, cache_lifetime=600):
        """
        :param pre: function modifying the input of a method,
            should return a modifed set of the original *args and **kwargs
        :param post: function modifying the output of a method, should return a modified response object
        :param error: [{"exception_class": <ExceptionClass>, "handler": <HandlerFunc>,}, ]
        :param cache: {"cache": , "cache_lifetime":,}
        :param cache_lifetime:
        """
        super(ExecutionPipeLine, self).__init__(
            pre_segment=pre,
            post_segment=post,
            error_handlers=error if error else [],
            cache=cache,
            cache_lifetime=cache_lifetime
        )

    def __call__(self, method):
        @functools.wraps(method)
        def decorated(*args, **kwargs):
            # Get all args and kwargs in one dict. All params are now named.
            params = helpers.positional_or_keyword_values(method, args, kwargs)
            # params before they are modified by the pre segment
            cache_key = {key: params[key] for key in params if key != 'self'}
            local_cache_keys = [f'{id(method)}:{cache_key}']

            if self.pre_segment:
                self._pre(method, params, local_cache_keys)

            if self.cache:
                cached_obj = self._check_cache(local_cache_keys)
                if cached_obj is not None:
                    return cached_obj

            response = self._perform_function_call(method, params, args, kwargs)

            if self.post_segment:
                return self._post(response)

            if self.cache:
                self._set_cache(local_cache_keys, response)

            return response
        return decorated

    def _pre(self, method, params, local_cache_keys):
        """
        Modify the passed params by executing each of the functions in the pre execution-segment
        :param method: method wrapped by the pipeline
        :param params: parameters to be passed to the wrapped method
        :param local_cache_keys: list of keys to check the cache for in cache segment
        :return: params modified according to the pre-execution segment
        """
        # we will check the cache for any key in cache_keys before executing the function
        for func in self.pre_segment:
            modified_params = func(params)
            params.update(modified_params)
        post_pre_key_params = {key: params[key] for key in params if key != 'self'}  # params after pre
        local_cache_keys.append(f'{method.__name__}:{id(method)}:{post_pre_key_params}')
        return params

    def _check_cache(self, local_cache_keys):
        for key in local_cache_keys:
            hashed_key = hash(key)
            return self.cache.get(hashed_key)

    def _post(self, response):
        for func in self.post_segment:
            response = func(response)
        return response

    def _perform_function_call(self, method, params, original_args, original_kwargs):
        """
        Check to see if the pipeline includes a handler for the exception we run into. If not, we raise the original
        exception.
        """
        try:
            self_or_cls, positional, variadic, keywords = \
                helpers.construct_valid_function_args(method, params, original_args, original_kwargs)
            if self_or_cls:
                response = method(self_or_cls, *positional, *variadic, **keywords)
            else:
                response = method(*positional, *variadic, **keywords)
        except (Exception, BaseException) as e:
            response = helpers.Empty()
            for error_handler in self.error_handlers:
                if isinstance(e, error_handler.exception_classes):
                    response = error_handler.handler(e, response)
            if isinstance(response, helpers.Empty):
                raise e
        return response

    def _set_cache(self, local_cache_keys, response):
        for key in local_cache_keys:
            hashed_key = hash(key)
            self.cache.set(hashed_key, response, self.cache_lifetime)


class execution_pipeline(ExecutionPipeLine):
    pass
