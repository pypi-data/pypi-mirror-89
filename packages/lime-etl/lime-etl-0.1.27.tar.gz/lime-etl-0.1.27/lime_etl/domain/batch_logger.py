import abc

from lime_etl.domain import value_objects, job_logger

__all__ = ("BatchLogger",)


class BatchLogger(abc.ABC):
    @abc.abstractmethod
    def create_job_logger(
        self, /, job_id: value_objects.UniqueId
    ) -> job_logger.JobLogger:
        raise NotImplementedError

    @abc.abstractmethod
    def log_error(self, message: str, /) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def log_info(self, message: str, /) -> None:
        raise NotImplementedError
