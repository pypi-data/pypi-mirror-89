class WorkerTypeError(Exception):
    """
    Raise this exception if worker is not couroutine
    """

    ...


class UnsupportedSwaggerType(Exception):
    """
    Raise this exception if request arg is not supported by swagger
    """

    ...


class InvalidCronFormat(Exception):
    """
    Raise this exception if cron has invalid format
    """
