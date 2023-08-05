import dataclasses

import typing

from lime_etl.domain import batch_status, value_objects


@dataclasses.dataclass(frozen=True)
class BatchDelta:
    current_results: batch_status.BatchStatus
    previous_results: typing.Optional[batch_status.BatchStatus]

    @property
    def common_jobs(self) -> typing.Set[value_objects.JobName]:
        if self.previous_results is None:
            return set()
        else:
            return self.previous_results.job_names & self.current_results.job_names

    @property
    def newly_broken_jobs(self) -> typing.Set[value_objects.JobName]:
        if self.previous_results is None:
            return self.current_results.broken_jobs
        else:
            return self.current_results.broken_jobs - self.previous_results.broken_jobs

    @property
    def newly_fixed_jobs(self) -> typing.Set[value_objects.JobName]:
        if self.previous_results is None:
            return self.current_results.broken_jobs
        else:
            return self.previous_results.broken_jobs - self.current_results.broken_jobs

    def __str__(self) -> str:
        return (
            "The following jobs are broken:\n    " + "\n    ".join(f"{j}\n    " for j in self.current_results.broken_jobs) +
            "The following jobs are newly broken:\n    " + "\n    ".join(f"{j}\n    " for j in self.newly_broken_jobs) +
            "The following jobs have been fixed:\n    " + "\n    ".join(f"{j}\n    " for j in self.newly_fixed_jobs)
        )
