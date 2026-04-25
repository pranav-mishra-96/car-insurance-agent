from langchain.tools import tool


@tool
def calculate_premium_estimate(age: int, vehicle_year: int, record_type: str) -> str:
    """Calculate an estimated monthly car insurance premium based on driver age,
    vehicle year, and driving record. Record type must be one of: clean, minor, major."""

    base = 100

    # Age factor
    if age < 25:
        base += 80
    elif age < 35:
        base += 20
    elif age < 60:
        base += 0
    else:
        base += 30

    # Vehicle age factor
    current_year = 2024
    vehicle_age = current_year - vehicle_year
    if vehicle_age <= 2:
        base += 40
    elif vehicle_age <= 5:
        base += 20
    elif vehicle_age <= 10:
        base += 0
    else:
        base -= 10

    # Driving record factor
    record_type = record_type.lower().strip()
    if record_type == "clean":
        multiplier = 1.0
    elif record_type == "minor":
        multiplier = 1.3
    elif record_type == "major":
        multiplier = 1.8
    else:
        multiplier = 1.0

    estimate = base * multiplier
    low = round(estimate * 0.9)
    high = round(estimate * 1.1)

    return (
        f"Estimated monthly premium: ${low} - ${high}/month. "
        f"Based on: age {age}, {current_year - vehicle_year} year old vehicle, "
        f"{record_type} driving record. "
        f"Note: This is an estimate only. Actual premiums vary by provider, "
        f"location, coverage level, and other factors."
    )


@tool
def check_coverage_requirements(province_or_state: str) -> str:
    """Check the minimum car insurance coverage requirements for a given
    Canadian province or US state."""

    requirements = {
        "ontario": (
            "Ontario minimums: $200,000 third-party liability, "
            "accident benefits, uninsured automobile coverage, "
            "and direct compensation property damage (DCPD). "
            "Comprehensive and collision are optional but recommended."
        ),
        "british columbia": (
            "BC minimums: $200,000 third-party liability through ICBC (mandatory), "
            "plus basic accident benefits. "
            "Optional: collision, comprehensive, and extended third-party liability."
        ),
        "alberta": (
            "Alberta minimums: $200,000 third-party liability, "
            "accident benefits, and uninsured motorist coverage. "
            "Collision and comprehensive are optional."
        ),
        "quebec": (
            "Quebec minimums: Bodily injury is covered by the public SAAQ plan. "
            "Private insurance covers $50,000 minimum property damage liability. "
            "Collision and comprehensive are optional."
        ),
        "california": (
            "California minimums: $15,000 bodily injury per person, "
            "$30,000 per accident, $5,000 property damage liability. "
            "Uninsured motorist coverage is optional but strongly recommended."
        ),
        "new york": (
            "New York minimums: $25,000 bodily injury per person, "
            "$50,000 per accident, $10,000 property damage, "
            "plus no-fault personal injury protection (PIP)."
        ),
        "texas": (
            "Texas minimums: $30,000 bodily injury per person, "
            "$60,000 per accident, $25,000 property damage liability. "
            "Known as 30/60/25 coverage."
        ),
    }

    key = province_or_state.lower().strip()
    if key in requirements:
        return requirements[key]

    return (
        f"Sorry, I don't have specific requirements for {province_or_state} on file. "
        f"Please check your local government or insurance regulator website for "
        f"the most accurate and up to date minimums. In general most jurisdictions "
        f"require at minimum third-party liability coverage."
    )


@tool
def explain_claim_process(claim_type: str) -> str:
    """Explain the step by step claims process for a given type of insurance claim.
    Claim type must be one of: collision, theft, weather, vandalism."""

    processes = {
        "collision": (
            "After a collision:\n"
            "1. Ensure everyone is safe and call 911 if there are injuries\n"
            "2. Move vehicles out of traffic if safe to do so\n"
            "3. Exchange information with the other driver (name, licence, insurance, plate)\n"
            "4. Take photos of all vehicles, damage, and the scene\n"
            "5. Get contact info from any witnesses\n"
            "6. Report to police if damage exceeds $2,000 or there are injuries\n"
            "7. Contact your insurance provider to open a claim within 24 hours\n"
            "8. Your insurer will assign an adjuster to assess the damage\n"
            "9. Get repair estimates from approved repair shops\n"
            "10. Pay your deductible — insurer covers the rest up to your limit"
        ),
        "theft": (
            "If your vehicle is stolen:\n"
            "1. Call police immediately and get a report number\n"
            "2. Contact your insurance provider with the police report number\n"
            "3. Provide your insurer with vehicle details (VIN, make, model, year)\n"
            "4. Your insurer will investigate — typically a 30 day waiting period\n"
            "5. If vehicle is not recovered, insurer pays actual cash value minus deductible\n"
            "6. If recovered with damage, collision or comprehensive covers repairs"
        ),
        "weather": (
            "For weather damage (hail, flood, falling trees):\n"
            "1. Ensure you are safe before assessing damage\n"
            "2. Document all damage with photos and video immediately\n"
            "3. Prevent further damage if possible (cover broken windows)\n"
            "4. Contact your insurer — weather damage falls under comprehensive coverage\n"
            "5. An adjuster will assess the damage\n"
            "6. Repairs are covered minus your deductible\n"
            "7. Note: comprehensive coverage is required for weather claims"
        ),
        "vandalism": (
            "For vandalism damage:\n"
            "1. Do not touch or clean anything before documenting\n"
            "2. Take photos of all damage\n"
            "3. File a police report — you will need the report number for your claim\n"
            "4. Contact your insurance provider with the police report number\n"
            "5. Vandalism falls under comprehensive coverage\n"
            "6. An adjuster will assess and approve repairs\n"
            "7. You pay your deductible — insurer covers the rest"
        ),
    }

    key = claim_type.lower().strip()
    if key in processes:
        return processes[key]

    return (
        f"I don't have a specific process for '{claim_type}'. "
        f"For any claim, the general steps are: ensure safety, document everything "
        f"with photos, file a police report if needed, and contact your insurer "
        f"within 24 hours. Your insurer will guide you through their specific process."
    )


@tool
def compare_coverage_types(coverage_a: str, coverage_b: str) -> str:
    """Compare two types of car insurance coverage. Coverage types available:
    liability, comprehensive, collision, uninsured_motorist, gap."""

    coverage_info = {
        "liability": {
            "description": "Covers damage or injury YOU cause to others",
            "covers": "Other people's medical bills, their vehicle damage, legal fees",
            "does_not_cover": "Your own vehicle damage or your own injuries",
            "required": "Yes — mandatory in all provinces and states",
            "best_for": "Everyone — it is legally required",
        },
        "comprehensive": {
            "description": "Covers damage to YOUR vehicle from non-collision events",
            "covers": "Theft, weather, fire, vandalism, falling objects, animal strikes",
            "does_not_cover": "Collision damage, mechanical breakdown",
            "required": "No — optional",
            "best_for": "Newer vehicles or if you live in an area with high theft or severe weather",
        },
        "collision": {
            "description": "Covers damage to YOUR vehicle from a collision",
            "covers": "Accidents with other vehicles, hitting objects, single car accidents",
            "does_not_cover": "Theft, weather, vandalism",
            "required": "No — optional but often required by lenders",
            "best_for": "Newer or higher value vehicles where repair costs would be significant",
        },
        "uninsured_motorist": {
            "description": "Covers you if the other driver has no insurance",
            "covers": "Your medical bills and vehicle damage when hit by uninsured driver",
            "does_not_cover": "Your own at-fault accidents",
            "required": "Varies by jurisdiction",
            "best_for": "Everyone — approximately 1 in 8 drivers is uninsured",
        },
        "gap": {
            "description": "Covers the difference between what you owe and what your car is worth",
            "covers": "The gap between loan balance and actual cash value if car is totalled",
            "does_not_cover": "Regular repairs or partial damage",
            "required": "No — optional",
            "best_for": "New car buyers who financed their vehicle and owe more than it is worth",
        },
    }

    key_a = coverage_a.lower().strip().replace(" ", "_")
    key_b = coverage_b.lower().strip().replace(" ", "_")

    result = []

    for key, label in [(key_a, coverage_a), (key_b, coverage_b)]:
        if key in coverage_info:
            info = coverage_info[key]
            result.append(
                f"{label.upper()}:\n"
                f"  What it is: {info['description']}\n"
                f"  Covers: {info['covers']}\n"
                f"  Does not cover: {info['does_not_cover']}\n"
                f"  Required: {info['required']}\n"
                f"  Best for: {info['best_for']}"
            )
        else:
            result.append(f"{label}: Coverage type not recognised.")

    return "\n\n".join(result)