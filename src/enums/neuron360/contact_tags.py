from enum import Enum


class ContactTag(str, Enum):
    """
    Enum for Neuron360 Contact Tags.
    Reference: https://docs.neuron360.io/docs/contact-tags
    """

    HAS_CURRENT_EXPERIENCE = "Contact Has Current Experience"
    HAS_EMAIL = "Contact Has Email"
    HAS_PHONE = "Contact Has Phone"
    HAS_DDI = "Contact Has ddI"
    HAS_MOBILE = "Contact Has Mobile"
