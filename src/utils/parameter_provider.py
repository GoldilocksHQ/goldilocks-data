import logging
from typing import Dict

import src.config.extraction_config as config
from src.enums.neuron360.skills import SkillCategory

logger = logging.getLogger(__name__)


class ParameterProvider:
    """
    Provides lists of filter values for a given hierarchy layer on demand.
    """

    def get_values_for_layer(self, layer_name: str, current_params: Dict) -> list:
        """
        Gets the list of filter values for a given parameter layer.
        The format of the returned values matches the structures in extraction_config.
        """
        if layer_name == "last_modified_date":
            return config.DATE_RANGES
        elif layer_name == "completion_score":
            return config.COMPLETION_SCORE_RANGES
        elif layer_name == "current_job_seniorities":
            return config.JOB_SENIORITIES
        elif layer_name == "current_job_functions":
            return config.JOB_FUNCTIONS
        elif layer_name == "skill_categories":
            return config.SKILL_CATEGORIES
        elif layer_name == "skill_subcategories":
            # This layer depends on the 'skill_categories' value
            skill_cat_param = current_params.get("skill_categories")
            if (
                not skill_cat_param
                or "value" not in skill_cat_param[0]
                or not skill_cat_param[0]["value"]
            ):
                return []

            skill_cat_value = skill_cat_param[0]["value"][0]
            category_enum = next(
                (sc for sc in SkillCategory if sc.value == skill_cat_value), None
            )

            subcategories = (
                config.get_skill_subcategories_for_category(category_enum)
                if category_enum
                else []
            )
            if not subcategories:
                logger.debug(f"No subcategories for category '{skill_cat_value}'.")
            return subcategories
        elif layer_name == "cities":
            return config.CITIES_TOGGLE
        elif layer_name == "profile_tags":
            return config.PROFILE_TAGS_TOGGLE
        return []
