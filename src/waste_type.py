from enum import Enum


class WasteType(Enum):
    RESIDUAL_WASTE = "RESIDUAL_WASTE", "Restmüll"
    ORGANIC_WASTE = "ORGANIC_WASTE", "Biomüll"
    RECYCLABLE_WASTE = "RECYCLABLE_WASTE", "Wertstoffmüll"
    PAPER_WASTE = "PAPER_WASTE", "Papiermüll"
    BULKY_WASTE = "BULKY_WASTE", "Sperrmüll"
