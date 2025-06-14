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
    CROSS_FUNCTIONAL_SOCIAL_AND_PERSONAL_ABILITIES = (
        "Cross-functional, Social, and Personal Abilities"
    )
    CUSTOMER_AND_CLIENT_SUCCESS = "Customer and Client Success"
    DESIGN = "Design"
    ECONOMICS_AND_SOCIAL_STUDIES = "Economics and Social Studies"
    EDUCATION = "Education"
    ENERGY_AND_UTILITIES = "Energy and Utilities"
    ENGINEERING = "Engineering"
    ENVIRONMENT = "Environment"
    FINANCE = "Finance"
    HEALTHCARE = "Healthcare"
    HOSPITALITY_AND_FOOD_SERVICES = "Hospitality and Food Services"
    HUMAN_RESOURCES = "Human Resources"
    INFORMATION_TECHNOLOGY = "Information Technology"
    LEGAL_REGULATION_AND_COMPLIANCE = "Legal, Regulation, and Compliance"
    MAINTENANCE_AND_REPAIR_SERVICES = "Maintenance and Repair Services"
    MANAGEMENT = "Management"
    MANUFACTURING = "Manufacturing"
    MARKETING_AND_PUBLIC_RELATIONS = "Marketing and Public Relations"
    PERSONAL_CARE_AND_SERVICES = "Personal Care and Services"
    REAL_ESTATE = "Real Estate"
    SALES = "Sales"
    SCIENCE_AND_RESEARCH = "Science and Research"
    SECURITY = "Security"
    SOCIAL_AND_HUMAN_SERVICES = "Social and Human Services"
    SPORT_RECREATION_AND_ARTS = "Sport, Recreation, and Arts"
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

    # Agriculture
    ANIMAL_HUSBANDRY = "Animal Husbandry"
    AQUACULTURE_AND_FISHERIES = "Aquaculture and Fisheries"
    CROP_MANAGEMENT = "Crop Management"
    FARMING_AND_GARDENING = "Farming and Gardening"
    FORESTRY_AND_SILVICULTURE = "Forestry and Silviculture"
    HORTICULTURE = "Horticulture"
    IRRIGATION_AND_WATER_MANAGEMENT = "Irrigation and Water Management"
    PEST_MANAGEMENT = "Pest Management"

    # Architecture and Construction
    BUILDING_AND_CONSTRUCTION = "Building and Construction"
    BUILDING_INFORMATION_MODELING_BIM = "Building Information Modeling"
    BUILDING_INSTALLATION_AND_MAINTENANCE = "Building Installation and Maintenance"
    CARPENTRY_AND_JOINERY = "Carpentry and Joinery"
    CONSTRUCTION_AND_BUILDING = "Construction and Building"
    CONSTRUCTION_TRADES = "Construction Trades"
    HEAVY_EQUIPMENT_OPERATION = "Heavy Equipment Operation"
    HOISTING_AND_LIFTING_EQUIPMENT_OPERATION = (
        "Hoisting and Lifting Equipment Operation"
    )
    INSPECTION_AND_CERTIFICATION = "Inspection and Certification"
    MASONRY_AND_CONCRETE_WORK = "Masonry and Concrete Work"
    PLUMBING_AND_PIPING_SYSTEMS = "Plumbing and Piping Systems"
    ROOFING_AND_WATERPROOFING = "Roofing and Waterproofing"
    SUSTAINABLE_URBAN_PLANNING_AND_BUILDING_DESIGN = (
        "Sustainable Urban Planning and Building Design"
    )

    # Communication and Media
    AUDIO_PRODUCTION_AND_SOUND_DESIGN = "Audio Production and Sound Design"
    BROADCASTING_AND_STREAMING_MEDIA = "Broadcasting and Streaming Media"
    COMMUNICATION = "Communication"
    CONTENT_CREATION_AND_JOURNALISM = "Content Creation and Journalism"
    LANGUAGE_LITERACY_AND_TRANSLATION = "Language, Literacy, and Translation"
    LINGUISTICS = "Linguistics"
    PHOTOGRAPHY = "Photography"
    PRESENTATION_AND_VISUALIZATION = "Presentation and Visualization"
    VIDEO_PRODUCTION_AND_POST_PRODUCTION = "Video Production and Post-Production"
    WRITING_AND_DOCUMENTATION = "Writing and Documentation"

    # Cross-functional, Social, and Personal Abilities
    ADAPTABILITY_AND_COGNITIVE_FLEXIBILITY = "Adaptability & Cognitive Flexibility"
    ADAPTABILITY_AND_RESILIENCE = "Adaptability & Resilience"
    COLLABORATION_AND_INTERPERSONAL_SKILLS = "Collaboration and Interpersonal Skills"
    CREATIVE_PROBLEM_SOLVING_AND_INNOVATION_SKILLS = (
        "Creative Problem-Solving and Innovation Skills"
    )
    CULTURAL_COMPETENCE_AND_DIVERSITY_AWARENESS = (
        "Cultural Competence and Diversity Awareness"
    )
    EMOTIONAL_AND_SOCIAL_INTELLIGENCE = "Emotional and Social Intelligence"
    INTERPERSONAL_MASTERY = "Interpersonal Mastery"

    # Customer and Client Success
    CONTACT_CENTER_OPERATIONS = "Contact Center Operations"
    CUSTOMER_EXPERIENCE_MANAGEMENT = "Customer Experience Management"
    CUSTOMER_SERVICE_AND_SUPPORT = "Customer Service and Support"

    # Design
    THREE_D_MODELING_AND_ANIMATION = "3D Modeling & Animation"
    DESIGN_TOOLS_AND_SOFTWARE = "Design Tools & Software"
    GRAPHIC_DESIGN_AND_VISUAL_COMMUNICATION = "Graphic Design & Visual Communication"
    GRAPHICS_AND_GAME_DEVELOPMENT = "Graphics and Game Development"
    IMAGE_MANIPULATION_AND_ENHANCEMENT = "Image Manipulation & Enhancement"
    INTERIOR_DESIGN = "Interior Design"
    PRINTING_AND_PRINTMAKING = "Printing and Printmaking"
    TECHNICAL_DRAWING_AND_DRAFTING = "Technical Drawing and Drafting"
    USER_EXPERIENCE_UX_DESIGN = "User Experience Design"
    VISUAL_ARTS = "Visual Arts"

    # Economics and Social Studies
    CORPORATE_SOCIAL_RESPONSIBILITY = "Corporate Social Responsibility"
    CULTURAL_STUDIES = "Cultural Studies"
    ECONOMICS = "Economics"
    POLITICAL_SCIENCE_AND_INTERNATIONAL_RELATIONS = (
        "Political Science and International Relations"
    )
    PUBLIC_POLICY_AND_ADMINISTRATION = "Public Policy and Administration"

    # Education
    ACADEMIC_SUPPORT_AND_STUDENT_SUCCESS = "Academic Support and Student Success"
    ASSESSMENT_AND_EVALUATION = "Assessment and Evaluation"
    CURRICULUM_AND_INSTRUCTION = "Curriculum and Instruction"
    EDUCATIONAL_TECHNOLOGY = "Educational Technology"
    INFORMATION_AND_LIBRARY_SCIENCE = "Information and Library Science"
    INSTRUCTIONAL_STRATEGIES = "Instructional Strategies"
    INSTRUCTOR_AND_TEACHING_CERTIFICATIONS = "Instructor & Teaching Certifications"
    READING_AND_LITERACY = "Reading and Literacy"
    SPECIAL_EDUCATION = "Special Education"
    TEACHER_AND_EDUCATIONAL_PROFESSIONAL_DEVELOPMENT = (
        "Teacher & Educational Professional Development"
    )
    TRAINING_AND_DEVELOPMENT = "Training and Development"

    # Energy and Utilities
    ENERGY_EFFICIENCY_AND_MANAGEMENT = "Energy Efficiency and Management"
    ENERGY_PRODUCTION_AND_DISTRIBUTION = "Energy Production and Distribution"
    HAZARDOUS_MATERIALS_MANAGEMENT = "Hazardous Materials Management"
    OIL_AND_GAS_PRODUCTION = "Oil and Gas Production"
    POWER_GENERATION_AND_DISTRIBUTION = "Power Generation and Distribution"
    RENEWABLE_ENERGY = "Renewable Energy"
    WASTE_MANAGEMENT = "Waste Management"
    WATER_RESOURCE_MANAGEMENT = "Water Resource Management"

    # Engineering
    AEROSPACE_ENGINEERING = "Aerospace Engineering"
    BIOMEDICAL_ENGINEERING = "Biomedical Engineering"
    CHEMICAL_ENGINEERING = "Chemical Engineering"
    COMPUTER_AIDED_DESIGN_AND_MANUFACTURING = (
        "Computer-Aided Design and Computer-Aided Manufacturing"
    )
    CONTROL_SYSTEMS_AND_AUTOMATION = "Control Systems and Automation"
    ELECTRICAL_ENGINEERING = "Electrical Engineering"
    ELECTRONICS_ENGINEERING = "Electronics Engineering"
    GEOTECHNICAL_ENGINEERING = "Geotechnical Engineering"
    MARINE_AND_NAVAL_ENGINEERING = "Marine and Naval Engineering"
    MECHANICAL_ENGINEERING = "Mechanical Engineering"
    MINING_ENGINEERING = "Mining Engineering"
    ROBOTICS_AND_AUTOMATION = "Robotics and Automation"
    STRUCTURAL_ENGINEERING = "Structural Engineering"
    SYSTEMS_ENGINEERING = "Systems Engineering"

    # Environment
    AIR_QUALITY_AND_EMISSIONS_MANAGEMENT = "Air Quality and Emissions Management"
    CLIMATE_CHANGE_MITIGATION_AND_ADAPTATION = (
        "Climate Change Mitigation and Adaptation"
    )
    ECOLOGY_AND_CONSERVATION = "Ecology and Conservation"
    ENVIRONMENTAL_IMPACT_AND_SUSTAINABILITY = "Environmental Impact and Sustainability"
    ENVIRONMENTAL_MANAGEMENT_AND_COMPLIANCE = "Environmental Management and Compliance"
    POLLUTION_CONTROL_AND_REMEDIATION = "Pollution Control and Remediation"

    # Finance
    ACCOUNTING_AND_FINANCIAL_MANAGEMENT = "Accounting and Financial Management"
    AUDITING = "Auditing"
    BANKING_OPERATIONS = "Banking Operations"
    BUDGETING = "Budgeting"
    CORPORATE_FINANCE = "Corporate Finance"
    CRYPTOCURRENCY = "Cryptocurrency"
    FINANCIAL_ANALYSIS_AND_VALUATION = "Financial Analysis and Valuation"
    FINANCIAL_PLANNING_AND_ANALYSIS = "Financial Planning and Analysis"
    FINANCIAL_REPORTING_AND_ANALYSIS = "Financial Reporting and Analysis"
    INSURANCE = "Insurance"
    INVESTMENT_MANAGEMENT = "Investment Management"
    TAXATION = "Taxation"
    TRADING_AND_INVESTING = "Trading and Investing"

    # Healthcare
    ADVANCED_PRACTICE_NURSING = "Advanced Practice Nursing"
    ANATOMY_AND_PHYSIOLOGY = "Anatomy and Physiology"
    AUDIOLOGY_AND_HEARING_HEALTHCARE = "Audiology and Hearing Healthcare"
    BEHAVIORAL_HEALTH_AND_REHABILITATION_SERVICES = (
        "Behavioral Health and Rehabilitation Services"
    )
    CARDIOLOGY = "Cardiology"
    CLINICAL_DATA_MANAGEMENT_AND_ANALYSIS = "Clinical Data Management and Analysis"
    CLINICAL_RESEARCH_AND_TRIALS = "Clinical Research and Trials"
    DENTISTRY = "Dentistry"
    DERMATOLOGY = "Dermatology"
    EMERGENCY_MEDICINE = "Emergency Medicine"
    HEALTHCARE_MANAGEMENT_AND_POLICY = "Healthcare Management and Policy"
    MENTAL_HEALTH_AND_ADDICTION_MEDICINE = "Mental Health and Addiction Medicine"
    NEUROLOGY = "Neurology"
    NURSING = "Nursing"
    NUTRITION_AND_DIETETICS = "Nutrition & Dietetics"
    ONCOLOGY = "Oncology"
    PATIENT_CARE_AND_MONITORING = "Patient Care and Monitoring"
    PHARMACY_PRACTICE = "Pharmacy Practice"
    REHABILITATION_THERAPY = "Rehabilitation Therapy"
    SURGERY = "Surgery"

    # Hospitality and Food Services
    BEVERAGE_SERVICE = "Beverage Service"
    CULINARY_ARTS_AND_BAKING = "Culinary Arts and Baking"
    FOOD_AND_BEVERAGE_MANAGEMENT = "Food and Beverage Management"
    FOOD_PREPARATION_AND_COOKING_TECHNIQUES = "Food Preparation and Cooking Techniques"
    FOOD_SAFETY_AND_QUALITY_MANAGEMENT = "Food Safety and Quality Management"
    TRAVEL_AND_TOURISM = "Travel and Tourism"

    # Human Resources
    DIVERSITY_EQUITY_AND_INCLUSION = "Diversity, Equity, and Inclusion"
    EMPLOYEE_AND_LABOR_RELATIONS = "Employee and Labor Relations"
    PAYROLL_AND_COMPLIANCE = "Payroll and Compliance"
    PERFORMANCE_AND_TALENT_MANAGEMENT = "Performance and Talent Management"
    TALENT_ACQUISITION = "Talent Acquisition"
    TALENT_DEVELOPMENT = "Talent Development"

    # Information Technology (IT)
    DOT_NET_TECHNOLOGY = ".NET Technology"
    AUGMENTED_REALITY_AND_VIRTUAL_REALITY = "Augmented Reality and Virtual Reality"
    BUSINESS_INTELLIGENCE_AND_ANALYTICS = "Business Intelligence and Analytics"
    CLOUD_COMPUTING_AND_VIRTUALIZATION = "Cloud Computing & Virtualization"
    CYBERSECURITY = "Cybersecurity"
    DATA_SCIENCE_AND_ANALYTICS = "Data Science and Analytics"
    DEVOPS_AND_AUTOMATION = "DevOps and Automation"
    MACHINE_LEARNING = "Machine Learning"
    NETWORKING_AND_COMMUNICATIONS = "Networking and Communications"
    SOFTWARE_DEVELOPMENT = "Software Development"
    WEB_DEVELOPMENT_AND_DESIGN = "Web Development and Design"

    # Legal, Regulation, and Compliance
    AUDIT_AND_COMPLIANCE = "Audit and Compliance"
    BUSINESS_CONTINUITY_AND_DISASTER_RECOVERY = (
        "Business Continuity and Disaster Recovery"
    )
    FORENSICS_AND_INVESTIGATION = "Forensics and Investigation"
    INTELLECTUAL_PROPERTY_LAW = "Intellectual Property Law"
    LAW_ENFORCEMENT_AND_PUBLIC_SAFETY = "Law Enforcement and Public Safety"
    REGULATORY_COMPLIANCE_AND_ETHICS = "Regulatory Compliance and Ethics"

    # Maintenance and Repair Services
    PLUMBING_AND_WATER_SYSTEM_MAINTENANCE = "Plumbing and Water System Maintenance"
    BUILDING_AUTOMATION_AND_CONTROLS = "Building Automation and Controls"
    ELECTRICAL_APPLIANCE_SYSTEM = "Electrical Appliance System"
    HVAC_HEATING_VENTILATION_AND_AIR_CONDITIONING = "HVAC"
    VEHICLE_MAINTENANCE_AND_REPAIR = "Vehicle Maintenance and Repair"

    # Management
    AGILE_PROJECT_MANAGEMENT = "Agile Project Management"
    ENTERPRISE_RESOURCE_PLANNING_ERP = "Enterprise Resource Planning"
    LEADERSHIP_AND_TEAM_MANAGEMENT = "Leadership and Team Management"
    MARKET_ANALYSIS = "Market Analysis"
    OPERATIONS_MANAGEMENT = "Operations Management"
    PRODUCT_DEVELOPMENT = "Product Development"
    PROJECT_MANAGEMENT = "Project Management"
    STRATEGIC_PLANNING = "Strategic Planning"

    # Manufacturing
    MACHINING = "Machining"
    MATERIALS_PROCESSING = "Materials Processing"
    METALWORKING = "Metalworking"
    PRECISION_MANUFACTURING = "Precision Manufacturing"
    PRODUCTION_AND_PROCESSING = "Production and Processing"
    QUALITY_CONTROL_AND_ASSURANCE = "Quality Control and Assurance"
    WELDING_AND_JOINING = "Welding and Joining"

    # Marketing and Public Relations
    ADVERTISING = "Advertising"
    BRAND_MANAGEMENT = "Brand Management"
    DIGITAL_MARKETING_AND_SEO = "Digital Marketing & SEO"
    EVENT_PLANNING_AND_MANAGEMENT = "Event Planning and Management"
    MARKETING_STRATEGY_AND_ANALYSIS = "Marketing Strategy and Analysis"
    PUBLIC_RELATIONS = "Public Relations"
    SOCIAL_MEDIA = "Social Media"

    # Personal Care and Services
    ANIMAL_CARE_AND_SERVICES = "Animal Care and Services"
    FUNERAL_AND_MORTUARY_SERVICES = "Funeral and Mortuary Services"
    HAIR_AND_BEAUTY_SERVICES = "Hair and Beauty Services"

    # Real Estate
    PROPERTY_MANAGEMENT = "Property Management"
    REAL_ESTATE_DEVELOPMENT_AND_TRANSACTIONS = (
        "Real Estate Development and Transactions"
    )
    REAL_ESTATE_PROFESSIONAL_CERTIFICATIONS = "Real Estate Professional Certifications"

    # Sales
    CRM_AND_SALES_SOFTWARE = "CRM and Sales Software"
    SALES_STRATEGY_AND_PLANNING = "Sales Strategy and Planning"
    SALESFORCE_SKILLS = "Salesforce Skills"
    TECHNICAL_SALES = "Technical Sales"

    # Science and Research
    ANALYTICAL_CHEMISTRY = "Analytical Chemistry"
    BIOCHEMISTRY = "Biochemistry"
    BIOINFORMATICS_AND_COMPUTATIONAL_BIOLOGY = (
        "Bioinformatics and Computational Biology"
    )
    CHEMISTRY = "Chemistry"
    GENETICS_AND_GENOMICS = "Genetics and Genomics"
    NEUROSCIENCE = "Neuroscience"
    RESEARCH_METHODS_AND_ANALYSIS = "Research Methods and Analysis"
    SPACE_AND_PHYSICS = "Space and Physics"

    # Security
    EMERGENCY_MANAGEMENT_AND_RESPONSE = "Emergency Management and Response"
    FIRE_SAFETY_AND_PREVENTION = "Fire Safety and Prevention"
    MILITARY_OPERATIONS_AND_STRATEGY = "Military Operations and Strategy"
    PHYSICAL_SECURITY = "Physical Security"
    SURVEILLANCE_AND_MONITORING = "Surveillance and Monitoring"

    # Social and Human Services
    FAMILY_AND_CHILD_SERVICES = "Family and Child Services"
    PSYCHOLOGY_AND_COUNSELING = "Psychology and Counseling"
    THERAPY_AND_COUNSELING = "Therapy and Counseling"

    # Sport, Recreation, and Arts
    DANCE = "Dance"
    FITNESS_AND_SPORTS_PERFORMANCE = "Fitness and Sports Performance"
    MUSIC = "Music"
    PERFORMANCE_ARTS = "Performance Arts"

    # Transportation
    AVIATION_OPERATIONS = "Aviation Operations"
    FREIGHT_AND_CARGO_TRANSPORTATION = "Freight and Cargo Transportation"
    INVENTORY_MANAGEMENT = "Inventory Management"
    LOGISTICS_AND_SUPPLY_CHAIN_MANAGEMENT = "Logistics & Supply Chain Management"
    MARITIME_TRANSPORTATION = "Maritime Transportation"
    RAIL_TRANSPORTATION = "Rail Transportation"
    TRAFFIC_MANAGEMENT_AND_CONTROL = "Traffic Management and Control"
    TRANSPORTATION_OPERATIONS_AND_MANAGEMENT = (
        "Transportation Operations and Management"
    )
    WAREHOUSING_AND_DISTRIBUTION = "Warehousing and Distribution"


SKILL_HIERARCHY = {
    SkillCategory.ADMINISTRATION: [
        SkillSubCategory.DATA_ENTRY_AND_TRANSCRIPTION,
        SkillSubCategory.DOCUMENT_MANAGEMENT,
        SkillSubCategory.OFFICE_MANAGEMENT_AND_COORDINATION,
        SkillSubCategory.OFFICE_PRODUCTIVITY_SOFTWARE,
    ],
    SkillCategory.AGRICULTURE: [
        SkillSubCategory.ANIMAL_HUSBANDRY,
        SkillSubCategory.AQUACULTURE_AND_FISHERIES,
        SkillSubCategory.CROP_MANAGEMENT,
        SkillSubCategory.FARMING_AND_GARDENING,
        SkillSubCategory.FORESTRY_AND_SILVICULTURE,
        SkillSubCategory.HORTICULTURE,
        SkillSubCategory.IRRIGATION_AND_WATER_MANAGEMENT,
        SkillSubCategory.PEST_MANAGEMENT,
    ],
    SkillCategory.ARCHITECTURE_AND_CONSTRUCTION: [
        SkillSubCategory.BUILDING_AND_CONSTRUCTION,
        SkillSubCategory.BUILDING_INFORMATION_MODELING_BIM,
        SkillSubCategory.BUILDING_INSTALLATION_AND_MAINTENANCE,
        SkillSubCategory.CARPENTRY_AND_JOINERY,
        SkillSubCategory.CONSTRUCTION_AND_BUILDING,
        SkillSubCategory.CONSTRUCTION_TRADES,
        SkillSubCategory.HEAVY_EQUIPMENT_OPERATION,
        SkillSubCategory.HOISTING_AND_LIFTING_EQUIPMENT_OPERATION,
        SkillSubCategory.INSPECTION_AND_CERTIFICATION,
        SkillSubCategory.MASONRY_AND_CONCRETE_WORK,
        SkillSubCategory.PLUMBING_AND_PIPING_SYSTEMS,
        SkillSubCategory.ROOFING_AND_WATERPROOFING,
        SkillSubCategory.SUSTAINABLE_URBAN_PLANNING_AND_BUILDING_DESIGN,
    ],
    SkillCategory.COMMUNICATION_AND_MEDIA: [
        SkillSubCategory.AUDIO_PRODUCTION_AND_SOUND_DESIGN,
        SkillSubCategory.BROADCASTING_AND_STREAMING_MEDIA,
        SkillSubCategory.COMMUNICATION,
        SkillSubCategory.CONTENT_CREATION_AND_JOURNALISM,
        SkillSubCategory.LANGUAGE_LITERACY_AND_TRANSLATION,
        SkillSubCategory.LINGUISTICS,
        SkillSubCategory.PHOTOGRAPHY,
        SkillSubCategory.PRESENTATION_AND_VISUALIZATION,
        SkillSubCategory.VIDEO_PRODUCTION_AND_POST_PRODUCTION,
        SkillSubCategory.WRITING_AND_DOCUMENTATION,
    ],
    SkillCategory.CROSS_FUNCTIONAL_SOCIAL_AND_PERSONAL_ABILITIES: [
        SkillSubCategory.ADAPTABILITY_AND_COGNITIVE_FLEXIBILITY,
        SkillSubCategory.ADAPTABILITY_AND_RESILIENCE,
        SkillSubCategory.COLLABORATION_AND_INTERPERSONAL_SKILLS,
        SkillSubCategory.CREATIVE_PROBLEM_SOLVING_AND_INNOVATION_SKILLS,
        SkillSubCategory.CULTURAL_COMPETENCE_AND_DIVERSITY_AWARENESS,
        SkillSubCategory.EMOTIONAL_AND_SOCIAL_INTELLIGENCE,
        SkillSubCategory.INTERPERSONAL_MASTERY,
    ],
    SkillCategory.CUSTOMER_AND_CLIENT_SUCCESS: [
        SkillSubCategory.CONTACT_CENTER_OPERATIONS,
        SkillSubCategory.CUSTOMER_EXPERIENCE_MANAGEMENT,
        SkillSubCategory.CUSTOMER_SERVICE_AND_SUPPORT,
    ],
    SkillCategory.DESIGN: [
        SkillSubCategory.THREE_D_MODELING_AND_ANIMATION,
        SkillSubCategory.DESIGN_TOOLS_AND_SOFTWARE,
        SkillSubCategory.GRAPHIC_DESIGN_AND_VISUAL_COMMUNICATION,
        SkillSubCategory.GRAPHICS_AND_GAME_DEVELOPMENT,
        SkillSubCategory.IMAGE_MANIPULATION_AND_ENHANCEMENT,
        SkillSubCategory.INTERIOR_DESIGN,
        SkillSubCategory.PRINTING_AND_PRINTMAKING,
        SkillSubCategory.TECHNICAL_DRAWING_AND_DRAFTING,
        SkillSubCategory.USER_EXPERIENCE_UX_DESIGN,
        SkillSubCategory.VISUAL_ARTS,
    ],
    SkillCategory.ECONOMICS_AND_SOCIAL_STUDIES: [
        SkillSubCategory.CORPORATE_SOCIAL_RESPONSIBILITY,
        SkillSubCategory.CULTURAL_STUDIES,
        SkillSubCategory.ECONOMICS,
        SkillSubCategory.POLITICAL_SCIENCE_AND_INTERNATIONAL_RELATIONS,
        SkillSubCategory.PUBLIC_POLICY_AND_ADMINISTRATION,
    ],
    SkillCategory.EDUCATION: [
        SkillSubCategory.ACADEMIC_SUPPORT_AND_STUDENT_SUCCESS,
        SkillSubCategory.ASSESSMENT_AND_EVALUATION,
        SkillSubCategory.CURRICULUM_AND_INSTRUCTION,
        SkillSubCategory.EDUCATIONAL_TECHNOLOGY,
        SkillSubCategory.INFORMATION_AND_LIBRARY_SCIENCE,
        SkillSubCategory.INSTRUCTIONAL_STRATEGIES,
        SkillSubCategory.INSTRUCTOR_AND_TEACHING_CERTIFICATIONS,
        SkillSubCategory.READING_AND_LITERACY,
        SkillSubCategory.SPECIAL_EDUCATION,
        SkillSubCategory.TEACHER_AND_EDUCATIONAL_PROFESSIONAL_DEVELOPMENT,
        SkillSubCategory.TRAINING_AND_DEVELOPMENT,
    ],
    SkillCategory.ENERGY_AND_UTILITIES: [
        SkillSubCategory.ENERGY_EFFICIENCY_AND_MANAGEMENT,
        SkillSubCategory.ENERGY_PRODUCTION_AND_DISTRIBUTION,
        SkillSubCategory.HAZARDOUS_MATERIALS_MANAGEMENT,
        SkillSubCategory.OIL_AND_GAS_PRODUCTION,
        SkillSubCategory.POWER_GENERATION_AND_DISTRIBUTION,
        SkillSubCategory.RENEWABLE_ENERGY,
        SkillSubCategory.WASTE_MANAGEMENT,
        SkillSubCategory.WATER_RESOURCE_MANAGEMENT,
    ],
    SkillCategory.ENGINEERING: [
        SkillSubCategory.AEROSPACE_ENGINEERING,
        SkillSubCategory.BIOMEDICAL_ENGINEERING,
        SkillSubCategory.CHEMICAL_ENGINEERING,
        SkillSubCategory.COMPUTER_AIDED_DESIGN_AND_MANUFACTURING,
        SkillSubCategory.CONTROL_SYSTEMS_AND_AUTOMATION,
        SkillSubCategory.ELECTRICAL_ENGINEERING,
        SkillSubCategory.ELECTRONICS_ENGINEERING,
        SkillSubCategory.GEOTECHNICAL_ENGINEERING,
        SkillSubCategory.MARINE_AND_NAVAL_ENGINEERING,
        SkillSubCategory.MECHANICAL_ENGINEERING,
        SkillSubCategory.MINING_ENGINEERING,
        SkillSubCategory.ROBOTICS_AND_AUTOMATION,
        SkillSubCategory.STRUCTURAL_ENGINEERING,
        SkillSubCategory.SYSTEMS_ENGINEERING,
    ],
    SkillCategory.ENVIRONMENT: [
        SkillSubCategory.AIR_QUALITY_AND_EMISSIONS_MANAGEMENT,
        SkillSubCategory.CLIMATE_CHANGE_MITIGATION_AND_ADAPTATION,
        SkillSubCategory.ECOLOGY_AND_CONSERVATION,
        SkillSubCategory.ENVIRONMENTAL_IMPACT_AND_SUSTAINABILITY,
        SkillSubCategory.ENVIRONMENTAL_MANAGEMENT_AND_COMPLIANCE,
        SkillSubCategory.POLLUTION_CONTROL_AND_REMEDIATION,
    ],
    SkillCategory.FINANCE: [
        SkillSubCategory.ACCOUNTING_AND_FINANCIAL_MANAGEMENT,
        SkillSubCategory.AUDITING,
        SkillSubCategory.BANKING_OPERATIONS,
        SkillSubCategory.BUDGETING,
        SkillSubCategory.CORPORATE_FINANCE,
        SkillSubCategory.CRYPTOCURRENCY,
        SkillSubCategory.FINANCIAL_ANALYSIS_AND_VALUATION,
        SkillSubCategory.FINANCIAL_PLANNING_AND_ANALYSIS,
        SkillSubCategory.FINANCIAL_REPORTING_AND_ANALYSIS,
        SkillSubCategory.INSURANCE,
        SkillSubCategory.INVESTMENT_MANAGEMENT,
        SkillSubCategory.TAXATION,
        SkillSubCategory.TRADING_AND_INVESTING,
    ],
    SkillCategory.HEALTHCARE: [
        SkillSubCategory.ADVANCED_PRACTICE_NURSING,
        SkillSubCategory.ANATOMY_AND_PHYSIOLOGY,
        SkillSubCategory.AUDIOLOGY_AND_HEARING_HEALTHCARE,
        SkillSubCategory.BEHAVIORAL_HEALTH_AND_REHABILITATION_SERVICES,
        SkillSubCategory.CARDIOLOGY,
        SkillSubCategory.CLINICAL_DATA_MANAGEMENT_AND_ANALYSIS,
        SkillSubCategory.CLINICAL_RESEARCH_AND_TRIALS,
        SkillSubCategory.DENTISTRY,
        SkillSubCategory.DERMATOLOGY,
        SkillSubCategory.EMERGENCY_MEDICINE,
        SkillSubCategory.HEALTHCARE_MANAGEMENT_AND_POLICY,
        SkillSubCategory.MENTAL_HEALTH_AND_ADDICTION_MEDICINE,
        SkillSubCategory.NEUROLOGY,
        SkillSubCategory.NURSING,
        SkillSubCategory.NUTRITION_AND_DIETETICS,
        SkillSubCategory.ONCOLOGY,
        SkillSubCategory.PATIENT_CARE_AND_MONITORING,
        SkillSubCategory.PHARMACY_PRACTICE,
        SkillSubCategory.REHABILITATION_THERAPY,
        SkillSubCategory.SURGERY,
    ],
    SkillCategory.HOSPITALITY_AND_FOOD_SERVICES: [
        SkillSubCategory.BEVERAGE_SERVICE,
        SkillSubCategory.CULINARY_ARTS_AND_BAKING,
        SkillSubCategory.FOOD_AND_BEVERAGE_MANAGEMENT,
        SkillSubCategory.FOOD_PREPARATION_AND_COOKING_TECHNIQUES,
        SkillSubCategory.FOOD_SAFETY_AND_QUALITY_MANAGEMENT,
        SkillSubCategory.TRAVEL_AND_TOURISM,
    ],
    SkillCategory.HUMAN_RESOURCES: [
        SkillSubCategory.DIVERSITY_EQUITY_AND_INCLUSION,
        SkillSubCategory.EMPLOYEE_AND_LABOR_RELATIONS,
        SkillSubCategory.PAYROLL_AND_COMPLIANCE,
        SkillSubCategory.PERFORMANCE_AND_TALENT_MANAGEMENT,
        SkillSubCategory.TALENT_ACQUISITION,
        SkillSubCategory.TALENT_DEVELOPMENT,
    ],
    SkillCategory.INFORMATION_TECHNOLOGY: [
        SkillSubCategory.DOT_NET_TECHNOLOGY,
        SkillSubCategory.AUGMENTED_REALITY_AND_VIRTUAL_REALITY,
        SkillSubCategory.BUSINESS_INTELLIGENCE_AND_ANALYTICS,
        SkillSubCategory.CLOUD_COMPUTING_AND_VIRTUALIZATION,
        SkillSubCategory.CYBERSECURITY,
        SkillSubCategory.DATA_SCIENCE_AND_ANALYTICS,
        SkillSubCategory.DEVOPS_AND_AUTOMATION,
        SkillSubCategory.MACHINE_LEARNING,
        SkillSubCategory.NETWORKING_AND_COMMUNICATIONS,
        SkillSubCategory.SOFTWARE_DEVELOPMENT,
        SkillSubCategory.WEB_DEVELOPMENT_AND_DESIGN,
    ],
    SkillCategory.LEGAL_REGULATION_AND_COMPLIANCE: [
        SkillSubCategory.AUDIT_AND_COMPLIANCE,
        SkillSubCategory.BUSINESS_CONTINUITY_AND_DISASTER_RECOVERY,
        SkillSubCategory.FORENSICS_AND_INVESTIGATION,
        SkillSubCategory.INTELLECTUAL_PROPERTY_LAW,
        SkillSubCategory.LAW_ENFORCEMENT_AND_PUBLIC_SAFETY,
        SkillSubCategory.REGULATORY_COMPLIANCE_AND_ETHICS,
    ],
    SkillCategory.MAINTENANCE_AND_REPAIR_SERVICES: [
        SkillSubCategory.PLUMBING_AND_WATER_SYSTEM_MAINTENANCE,
        SkillSubCategory.BUILDING_AUTOMATION_AND_CONTROLS,
        SkillSubCategory.ELECTRICAL_APPLIANCE_SYSTEM,
        SkillSubCategory.HVAC_HEATING_VENTILATION_AND_AIR_CONDITIONING,
        SkillSubCategory.VEHICLE_MAINTENANCE_AND_REPAIR,
    ],
    SkillCategory.MANAGEMENT: [
        SkillSubCategory.AGILE_PROJECT_MANAGEMENT,
        SkillSubCategory.ENTERPRISE_RESOURCE_PLANNING_ERP,
        SkillSubCategory.LEADERSHIP_AND_TEAM_MANAGEMENT,
        SkillSubCategory.MARKET_ANALYSIS,
        SkillSubCategory.OPERATIONS_MANAGEMENT,
        SkillSubCategory.PRODUCT_DEVELOPMENT,
        SkillSubCategory.PROJECT_MANAGEMENT,
        SkillSubCategory.STRATEGIC_PLANNING,
    ],
    SkillCategory.MANUFACTURING: [
        SkillSubCategory.MACHINING,
        SkillSubCategory.MATERIALS_PROCESSING,
        SkillSubCategory.METALWORKING,
        SkillSubCategory.PRECISION_MANUFACTURING,
        SkillSubCategory.PRODUCTION_AND_PROCESSING,
        SkillSubCategory.QUALITY_CONTROL_AND_ASSURANCE,
        SkillSubCategory.WELDING_AND_JOINING,
    ],
    SkillCategory.MARKETING_AND_PUBLIC_RELATIONS: [
        SkillSubCategory.ADVERTISING,
        SkillSubCategory.BRAND_MANAGEMENT,
        SkillSubCategory.DIGITAL_MARKETING_AND_SEO,
        SkillSubCategory.EVENT_PLANNING_AND_MANAGEMENT,
        SkillSubCategory.MARKETING_STRATEGY_AND_ANALYSIS,
        SkillSubCategory.PUBLIC_RELATIONS,
        SkillSubCategory.SOCIAL_MEDIA,
    ],
    SkillCategory.PERSONAL_CARE_AND_SERVICES: [
        SkillSubCategory.ANIMAL_CARE_AND_SERVICES,
        SkillSubCategory.FUNERAL_AND_MORTUARY_SERVICES,
        SkillSubCategory.HAIR_AND_BEAUTY_SERVICES,
    ],
    SkillCategory.REAL_ESTATE: [
        SkillSubCategory.PROPERTY_MANAGEMENT,
        SkillSubCategory.REAL_ESTATE_DEVELOPMENT_AND_TRANSACTIONS,
        SkillSubCategory.REAL_ESTATE_PROFESSIONAL_CERTIFICATIONS,
    ],
    SkillCategory.SALES: [
        SkillSubCategory.CRM_AND_SALES_SOFTWARE,
        SkillSubCategory.SALES_STRATEGY_AND_PLANNING,
        SkillSubCategory.SALESFORCE_SKILLS,
        SkillSubCategory.TECHNICAL_SALES,
    ],
    SkillCategory.SCIENCE_AND_RESEARCH: [
        SkillSubCategory.ANALYTICAL_CHEMISTRY,
        SkillSubCategory.BIOCHEMISTRY,
        SkillSubCategory.BIOINFORMATICS_AND_COMPUTATIONAL_BIOLOGY,
        SkillSubCategory.CHEMISTRY,
        SkillSubCategory.GENETICS_AND_GENOMICS,
        SkillSubCategory.NEUROSCIENCE,
        SkillSubCategory.RESEARCH_METHODS_AND_ANALYSIS,
        SkillSubCategory.SPACE_AND_PHYSICS,
    ],
    SkillCategory.SECURITY: [
        SkillSubCategory.EMERGENCY_MANAGEMENT_AND_RESPONSE,
        SkillSubCategory.FIRE_SAFETY_AND_PREVENTION,
        SkillSubCategory.MILITARY_OPERATIONS_AND_STRATEGY,
        SkillSubCategory.PHYSICAL_SECURITY,
        SkillSubCategory.SURVEILLANCE_AND_MONITORING,
    ],
    SkillCategory.SOCIAL_AND_HUMAN_SERVICES: [
        SkillSubCategory.FAMILY_AND_CHILD_SERVICES,
        SkillSubCategory.PSYCHOLOGY_AND_COUNSELING,
        SkillSubCategory.THERAPY_AND_COUNSELING,
    ],
    SkillCategory.SPORT_RECREATION_AND_ARTS: [
        SkillSubCategory.DANCE,
        SkillSubCategory.FITNESS_AND_SPORTS_PERFORMANCE,
        SkillSubCategory.MUSIC,
        SkillSubCategory.PERFORMANCE_ARTS,
    ],
    SkillCategory.TRANSPORTATION: [
        SkillSubCategory.AVIATION_OPERATIONS,
        SkillSubCategory.FREIGHT_AND_CARGO_TRANSPORTATION,
        SkillSubCategory.INVENTORY_MANAGEMENT,
        SkillSubCategory.LOGISTICS_AND_SUPPLY_CHAIN_MANAGEMENT,
        SkillSubCategory.MARITIME_TRANSPORTATION,
        SkillSubCategory.RAIL_TRANSPORTATION,
        SkillSubCategory.TRAFFIC_MANAGEMENT_AND_CONTROL,
        SkillSubCategory.TRANSPORTATION_OPERATIONS_AND_MANAGEMENT,
        SkillSubCategory.WAREHOUSING_AND_DISTRIBUTION,
    ],
}
