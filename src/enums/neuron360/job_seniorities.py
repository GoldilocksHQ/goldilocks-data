from enum import Enum


class JobSeniority(str, Enum):
    """
    Enum for Neuron360 Job Seniorities.
    Reference: https://docs.neuron360.io/docs/job-seniorities
    """

    BOARD_MEMBER = "Board Member"
    C_LEVEL = "C-Level"
    VP = "VP"
    DIRECTOR = "Director"
    MANAGER = "Manager"
    INDIVIDUAL_CONTRIBUTOR = "Individual Contributor"
    OTHER = "Other"
