def calculate_epley_1rm(weight: float, reps: int) -> float:
    """Beregner estimeret 1RM ud fra Epley-formlen."""
    return round(weight * (1 + reps / 30.0), 1)