"""HouseSystem with 12 bhavas and their significations."""
from __future__ import annotations
from ..models import House, Rashi, Graha


RASHI_LORDS: dict[Rashi, Graha] = {
    Rashi.MESHA: Graha.MANGAL, Rashi.VRISHABHA: Graha.SHUKRA, Rashi.MITHUNA: Graha.BUDHA,
    Rashi.KARKA: Graha.CHANDRA, Rashi.SIMHA: Graha.SURYA, Rashi.KANYA: Graha.BUDHA,
    Rashi.TULA: Graha.SHUKRA, Rashi.VRISHCHIKA: Graha.MANGAL, Rashi.DHANU: Graha.GURU,
    Rashi.MAKARA: Graha.SHANI, Rashi.KUMBHA: Graha.SHANI, Rashi.MEENA: Graha.GURU,
}

RASHIS = list(Rashi)


class HouseSystem:
    """12 Bhavas (houses) with significations and classification."""

    SIGNIFICATIONS: dict[int, list[str]] = {
        1: ["self", "body", "personality", "appearance", "health", "birth", "head", "complexion"],
        2: ["wealth", "family", "speech", "food", "right eye", "face", "early education", "values"],
        3: ["siblings", "courage", "communication", "short travel", "arms", "ears", "efforts", "hobbies"],
        4: ["mother", "home", "property", "vehicles", "education", "happiness", "chest", "comforts"],
        5: ["children", "intelligence", "creativity", "romance", "past merit", "stomach", "speculation"],
        6: ["enemies", "disease", "debt", "service", "competition", "obstacles", "maternal uncle"],
        7: ["marriage", "partnership", "spouse", "business", "foreign travel", "lower abdomen"],
        8: ["longevity", "transformation", "occult", "inheritance", "chronic illness", "hidden things"],
        9: ["dharma", "luck", "father", "guru", "long travel", "higher education", "religion", "fortune"],
        10: ["career", "reputation", "authority", "government", "karma", "fame", "knees"],
        11: ["gains", "income", "elder siblings", "friends", "aspirations", "fulfillment", "social circle"],
        12: ["losses", "expenses", "moksha", "foreign lands", "isolation", "sleep", "spirituality", "feet"],
    }

    HOUSE_TYPES: dict[str, list[int]] = {
        "kendra": [1, 4, 7, 10],       # Angular houses (most powerful)
        "trikona": [1, 5, 9],           # Trine houses (most auspicious)
        "upachaya": [3, 6, 10, 11],     # Growth houses
        "dusthana": [6, 8, 12],         # Difficult houses
        "maraka": [2, 7],               # Death-inflicting houses
        "trishadaya": [3, 6, 11],       # Mildly malefic houses
    }

    def build_houses(self, lagna_rashi: Rashi) -> list[House]:
        """Build 12 houses starting from the lagna (ascendant) rashi."""
        start_idx = RASHIS.index(lagna_rashi)
        houses = []
        for i in range(12):
            rashi = RASHIS[(start_idx + i) % 12]
            houses.append(House(
                number=i + 1,
                rashi=rashi,
                lord=RASHI_LORDS[rashi],
                significations=self.SIGNIFICATIONS[i + 1],
            ))
        return houses

    def get_house_type(self, house_number: int) -> list[str]:
        """Get classification(s) for a house number."""
        types = []
        for type_name, houses in self.HOUSE_TYPES.items():
            if house_number in houses:
                types.append(type_name)
        return types

    def get_house_lord(self, house_number: int, lagna: Rashi) -> Graha:
        """Get the lord of a specific house given lagna."""
        idx = (RASHIS.index(lagna) + house_number - 1) % 12
        return RASHI_LORDS[RASHIS[idx]]

    def get_kendra_lords(self, lagna: Rashi) -> list[Graha]:
        """Get lords of the four kendra houses."""
        return [self.get_house_lord(h, lagna) for h in self.HOUSE_TYPES["kendra"]]

    def get_trikona_lords(self, lagna: Rashi) -> list[Graha]:
        """Get lords of trikona houses."""
        return [self.get_house_lord(h, lagna) for h in self.HOUSE_TYPES["trikona"]]
