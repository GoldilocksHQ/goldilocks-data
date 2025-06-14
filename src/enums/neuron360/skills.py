from enum import Enum


class SkillCategory(str, Enum):
    """
    Enum for Neuron360 Skill Categories.
    Reference: https://docs.neuron360.io/docs/enhanced-skills-taxonomy
    """

    ADMINISTRATION = "Administration"
    AGRICULTURE = "Agriculture"
    ARCHITECTURE_AND_CONSTRUCTION = "Architecture and Construction"
    COMMUNICATION_AND_MEDIA = "Communication and Media"
    CUSTOMER_AND_CLIENT_SUCCESS = "Customer and Client Success"
    DESIGN = "Design"
    ECONOMICS_AND_SOCIAL_STUDIES = "Economics and Social Studies"
    EDUCATION = "Education"
    ENGINEERING = "Engineering"
    FINANCE = "Finance"
    HEALTHCARE = "Healthcare"
    HOSPITALITY_AND_FOOD_SERVICES = "Hospitality and Food Services"
    HUMAN_RESOURCES = "Human Resources (HR)"
    INFORMATION_TECHNOLOGY = "Information Technology (IT)"
    LEGAL_REGULATION_AND_COMPLIANCE = "Legal, Regulation, and Compliance"
    MAINTENANCE_AND_REPAIR_SERVICES = "Maintenance and Repair Services"
    MANAGEMENT = "Management"
    MANUFACTURING = "Manufacturing"
    MARKETING_AND_PUBLIC_RELATIONS = "Marketing and Public Relations"
    SALES = "Sales"
    SCIENCE_AND_RESEARCH = "Science and Research"
    TRANSPORTATION = "Transportation"


class SkillSubCategory(str, Enum):
    """
    Enum for Neuron360 Skill Sub-Categories.
    Reference: https://docs.neuron360.io/docs/enhanced-skills-taxonomy
    """

    # Administration
    DATA_ENTRY_AND_TRANSCRIPTION = "Data Entry and Transcription"
    DOCUMENT_MANAGEMENT = "Document Management"
    OFFICE_MANAGEMENT_AND_COORDINATION = "Office Management and Coordination"
    OFFICE_PRODUCTIVITY_SOFTWARE = "Office Productivity Software"

    # Engineering
    AEROSPACE_ENGINEERING = "Aerospace Engineering"
    BIOMEDICAL_ENGINEERING = "Biomedical Engineering"
    CHEMICAL_ENGINEERING = "Chemical Engineering"
    COMPUTER_AIDED_DESIGN_AND_MANUFACTURING = (
        "Computer-Aided Design (CAD) and Computer-Aided Manufacturing (CAM)"
    )
    ELECTRICAL_ENGINEERING = "Electrical Engineering"
    MECHANICAL_ENGINEERING = "Mechanical Engineering"
    SYSTEMS_ENGINEERING = "Systems Engineering"

    # Information Technology
    DOT_NET_TECHNOLOGY = ".NET Technology"
    AUGMENTED_REALITY_AND_VIRTUAL_REALITY = (
        "Augmented Reality and Virtual Reality (AR/VR)"
    )
    BUSINESS_INTELLIGENCE_AND_ANALYTICS = "Business Intelligence and Analytics"
    CLOUD_COMPUTING_AND_VIRTUALIZATION = "Cloud Computing & Virtualization"
    CYBERSECURITY = "Cybersecurity"
    DATA_SCIENCE_AND_ANALYTICS = "Data Science and Analytics"
    DEVOPS_AND_AUTOMATION = "DevOps and Automation"
    MACHINE_LEARNING = "Machine Learning"
    NETWORKING_AND_COMMUNICATIONS = "Networking and Communications"
    SOFTWARE_DEVELOPMENT = "Software Development"
    WEB_DEVELOPMENT_AND_DESIGN = "Web Development and Design"
