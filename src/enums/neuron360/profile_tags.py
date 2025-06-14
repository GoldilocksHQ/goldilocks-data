from enum import Enum


class ProfileTag(str, Enum):
    """
    Enum for Neuron360 Profile Tags.
    Reference: https://docs.neuron360.io/docs/profile-tags
    """

    HAS_PHONE = "Profile Has Phone"
    HAS_EMAIL = "Profile Has Email"
    HAS_ADDRESS = "Profile Has Address"
    HAS_SOCIAL_LINK = "Profile Has Social Link"
    HAS_EXPERTISE = "Profile Has Expertise"
    HAS_DDI = "Profile Has ddI"
    HAS_MOBILE = "Profile Has Mobile"
    HAS_PERSONAL_EMAIL = "Profile Has Personal Email"
