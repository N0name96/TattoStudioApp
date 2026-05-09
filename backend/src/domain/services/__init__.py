"""Domain services __init__ for the TattoStudioApp.

Domain services contain business logic that doesn't naturally fit
within a single entity and operates across entities or value objects.
They are framework-agnostic and have no infrastructure dependencies.
"""

from domain.services.commission_calculator import CommissionCalculator

__all__ = ["CommissionCalculator"]
