from datetime import date
from dateutil.relativedelta import relativedelta
from src.enums.neuron360.job_seniorities import JobSeniority
from src.enums.neuron360.job_functions import JobFunction
from src.enums.neuron360.skills import SkillCategory, SKILL_HIERARCHY

# --- Static Parameters ---
STATIC_COUNTRY = {"value": ["United Kingdom"], "operator": "is one of"}


# --- Layer A: Date Ranges ---
def get_date_ranges():
    ranges = []
    # Start from "since 01-05-2025 and before 31-05-2025"
    end_date = date(2025, 6, 1)
    # End at "since 01-12-2024 and before 31-12-2024"
    for _ in range(6):
        start_date = end_date - relativedelta(months=1)
        ranges.append(
            [
                {"value": start_date.strftime("%Y-%m-%d"), "operator": "since"},
                {
                    "value": (end_date - relativedelta(days=1)).strftime("%Y-%m-%d"),
                    "operator": "before",
                },
            ]
        )
        end_date = start_date
    return ranges


DATE_RANGES = get_date_ranges()

# --- Layer B: Completion Score Ranges ---
COMPLETION_SCORE_RANGES = [
    [
        {"value": "0.4", "operator": "greater than"},
        {"value": "0.45", "operator": "less than"},
    ],
    [
        {"value": "0.45", "operator": "greater than"},
        {"value": "0.50", "operator": "less than"},
    ],
    [
        {"value": "0.50", "operator": "greater than"},
        {"value": "0.55", "operator": "less than"},
    ],
    [
        {"value": "0.55", "operator": "greater than"},
        {"value": "0.60", "operator": "less than"},
    ],
    [
        {"value": "0.6", "operator": "greater than"},
        {"value": "1.0", "operator": "less than"},
    ],
]

# --- Layers C-F: Enum-based Iterations ---
JOB_SENIORITIES = [{"value": [s.value], "operator": "is one of"} for s in JobSeniority]
JOB_FUNCTIONS = [{"value": [f.value], "operator": "is one of"} for f in JobFunction]
SKILL_CATEGORIES = [
    {"value": [sc.value], "operator": "is one of"} for sc in SkillCategory
]


def get_skill_subcategories_for_category(category_enum):
    return [
        {"value": [sub.value], "operator": "is one of"}
        for sub in SKILL_HIERARCHY.get(category_enum, [])
    ]


# --- Layers G-H: Toggle Parameters ---
CITIES_TOGGLE = [
    {"value": ["London"], "operator": "is one of"},
    {"value": ["London"], "operator": "is not one of"},
]

PROFILE_TAGS_TOGGLE = [
    {
        "value": [
            "Profile Has Phone",
            "Profile Has Address",
            "Profile Has Email",
        ],
        "operator": "is one of",
    },
    {
        "value": [
            "Profile Has Phone",
            "Profile Has Address",
            "Profile Has Email",
        ],
        "operator": "is not one of",
    },
]

# --- Full Parameter Hierarchy ---
# This defines the order of iteration.
PARAMETER_HIERARCHY = [
    "last_modified_date",
    "completion_score",
    "current_job_seniorities",
    "current_job_functions",
    "skill_categories",
    "skill_subcategories",
    "cities",
    "profile_tags",
]
