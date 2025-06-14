from enum import Enum


class ResumeTag(str, Enum):
    """
    Enum for Neuron360 Resume Tags.
    Reference: https://docs.neuron360.io/docs/resume-tags
    """

    HAS_EXPERIENCE = "Resume Has Experience"
    HAS_EDUCATION = "Resume Has Education"
    HAS_CERTIFICATION = "Resume Has Certification"
    HAS_MEMBERSHIP = "Resume Has Membership"
    HAS_PUBLICATION = "Resume Has Publication"
    HAS_PATENT = "Resume Has Patent"
    HAS_AWARD = "Resume Has Award"
