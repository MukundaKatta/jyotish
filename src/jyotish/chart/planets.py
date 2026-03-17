"""PlanetDatabase with 9 grahas and their properties/friendships/exaltation."""
from __future__ import annotations
from ..models import Graha, Rashi


class PlanetDatabase:
    """Database of 9 Vedic grahas with properties, friendships, and dignities."""

    def __init__(self) -> None:
        self._properties = self._load_properties()
        self._friendships = self._load_friendships()
        self._exaltation = self._load_exaltation()
        self._debilitation = self._load_debilitation()
        self._own_signs = self._load_own_signs()
        self._nakshatra_lords = self._load_nakshatra_lords()

    def _load_properties(self) -> dict[Graha, dict]:
        return {
            Graha.SURYA: {"english": "Sun", "nature": "malefic", "gender": "male", "element": "fire", "direction": "east", "day": "Sunday", "gem": "Ruby", "metal": "gold", "color": "red", "dasha_years": 6, "karaka": "soul, father, authority, government"},
            Graha.CHANDRA: {"english": "Moon", "nature": "benefic", "gender": "female", "element": "water", "direction": "northwest", "day": "Monday", "gem": "Pearl", "metal": "silver", "color": "white", "dasha_years": 10, "karaka": "mind, mother, emotions, public"},
            Graha.MANGAL: {"english": "Mars", "nature": "malefic", "gender": "male", "element": "fire", "direction": "south", "day": "Tuesday", "gem": "Red Coral", "metal": "copper", "color": "red", "dasha_years": 7, "karaka": "courage, siblings, property, surgery"},
            Graha.BUDHA: {"english": "Mercury", "nature": "neutral", "gender": "neutral", "element": "earth", "direction": "north", "day": "Wednesday", "gem": "Emerald", "metal": "bronze", "color": "green", "dasha_years": 17, "karaka": "intelligence, communication, trade, education"},
            Graha.GURU: {"english": "Jupiter", "nature": "benefic", "gender": "male", "element": "ether", "direction": "northeast", "day": "Thursday", "gem": "Yellow Sapphire", "metal": "gold", "color": "yellow", "dasha_years": 16, "karaka": "wisdom, children, dharma, wealth, guru"},
            Graha.SHUKRA: {"english": "Venus", "nature": "benefic", "gender": "female", "element": "water", "direction": "southeast", "day": "Friday", "gem": "Diamond", "metal": "silver", "color": "white", "dasha_years": 20, "karaka": "love, marriage, luxury, arts, vehicles"},
            Graha.SHANI: {"english": "Saturn", "nature": "malefic", "gender": "neutral", "element": "air", "direction": "west", "day": "Saturday", "gem": "Blue Sapphire", "metal": "iron", "color": "blue/black", "dasha_years": 19, "karaka": "longevity, discipline, karma, sorrow, service"},
            Graha.RAHU: {"english": "North Node", "nature": "malefic", "gender": "neutral", "element": "air", "direction": "southwest", "day": "Saturday", "gem": "Hessonite", "metal": "lead", "color": "smoky", "dasha_years": 18, "karaka": "obsession, foreign, illusion, technology"},
            Graha.KETU: {"english": "South Node", "nature": "malefic", "gender": "neutral", "element": "fire", "direction": "none", "day": "Tuesday", "gem": "Cat's Eye", "metal": "mixed", "color": "grey", "dasha_years": 7, "karaka": "moksha, spirituality, past karma, occult"},
        }

    def _load_friendships(self) -> dict[Graha, dict[str, list[Graha]]]:
        return {
            Graha.SURYA: {"friends": [Graha.CHANDRA, Graha.MANGAL, Graha.GURU], "enemies": [Graha.SHUKRA, Graha.SHANI], "neutral": [Graha.BUDHA]},
            Graha.CHANDRA: {"friends": [Graha.SURYA, Graha.BUDHA], "enemies": [], "neutral": [Graha.MANGAL, Graha.GURU, Graha.SHUKRA, Graha.SHANI]},
            Graha.MANGAL: {"friends": [Graha.SURYA, Graha.CHANDRA, Graha.GURU], "enemies": [Graha.BUDHA], "neutral": [Graha.SHUKRA, Graha.SHANI]},
            Graha.BUDHA: {"friends": [Graha.SURYA, Graha.SHUKRA], "enemies": [Graha.CHANDRA], "neutral": [Graha.MANGAL, Graha.GURU, Graha.SHANI]},
            Graha.GURU: {"friends": [Graha.SURYA, Graha.CHANDRA, Graha.MANGAL], "enemies": [Graha.BUDHA, Graha.SHUKRA], "neutral": [Graha.SHANI]},
            Graha.SHUKRA: {"friends": [Graha.BUDHA, Graha.SHANI], "enemies": [Graha.SURYA, Graha.CHANDRA], "neutral": [Graha.MANGAL, Graha.GURU]},
            Graha.SHANI: {"friends": [Graha.BUDHA, Graha.SHUKRA], "enemies": [Graha.SURYA, Graha.CHANDRA, Graha.MANGAL], "neutral": [Graha.GURU]},
            Graha.RAHU: {"friends": [Graha.SHUKRA, Graha.SHANI], "enemies": [Graha.SURYA, Graha.CHANDRA, Graha.MANGAL], "neutral": [Graha.BUDHA, Graha.GURU]},
            Graha.KETU: {"friends": [Graha.MANGAL, Graha.SHUKRA, Graha.SHANI], "enemies": [Graha.SURYA, Graha.CHANDRA], "neutral": [Graha.BUDHA, Graha.GURU]},
        }

    def _load_exaltation(self) -> dict[Graha, tuple[Rashi, float]]:
        """Exaltation sign and exact degree."""
        return {
            Graha.SURYA: (Rashi.MESHA, 10.0),
            Graha.CHANDRA: (Rashi.VRISHABHA, 3.0),
            Graha.MANGAL: (Rashi.MAKARA, 28.0),
            Graha.BUDHA: (Rashi.KANYA, 15.0),
            Graha.GURU: (Rashi.KARKA, 5.0),
            Graha.SHUKRA: (Rashi.MEENA, 27.0),
            Graha.SHANI: (Rashi.TULA, 20.0),
            Graha.RAHU: (Rashi.VRISHABHA, 20.0),
            Graha.KETU: (Rashi.VRISHCHIKA, 20.0),
        }

    def _load_debilitation(self) -> dict[Graha, tuple[Rashi, float]]:
        return {
            Graha.SURYA: (Rashi.TULA, 10.0),
            Graha.CHANDRA: (Rashi.VRISHCHIKA, 3.0),
            Graha.MANGAL: (Rashi.KARKA, 28.0),
            Graha.BUDHA: (Rashi.MEENA, 15.0),
            Graha.GURU: (Rashi.MAKARA, 5.0),
            Graha.SHUKRA: (Rashi.KANYA, 27.0),
            Graha.SHANI: (Rashi.MESHA, 20.0),
            Graha.RAHU: (Rashi.VRISHCHIKA, 20.0),
            Graha.KETU: (Rashi.VRISHABHA, 20.0),
        }

    def _load_own_signs(self) -> dict[Graha, list[Rashi]]:
        return {
            Graha.SURYA: [Rashi.SIMHA],
            Graha.CHANDRA: [Rashi.KARKA],
            Graha.MANGAL: [Rashi.MESHA, Rashi.VRISHCHIKA],
            Graha.BUDHA: [Rashi.MITHUNA, Rashi.KANYA],
            Graha.GURU: [Rashi.DHANU, Rashi.MEENA],
            Graha.SHUKRA: [Rashi.VRISHABHA, Rashi.TULA],
            Graha.SHANI: [Rashi.MAKARA, Rashi.KUMBHA],
            Graha.RAHU: [Rashi.KUMBHA],
            Graha.KETU: [Rashi.VRISHCHIKA],
        }

    def _load_nakshatra_lords(self) -> list[Graha]:
        """Vimshottari dasha lords in nakshatra order."""
        return [Graha.KETU, Graha.SHUKRA, Graha.SURYA, Graha.CHANDRA, Graha.MANGAL,
                Graha.RAHU, Graha.GURU, Graha.SHANI, Graha.BUDHA]

    def get_properties(self, graha: Graha) -> dict:
        return self._properties.get(graha, {})

    def get_friends(self, graha: Graha) -> list[Graha]:
        return self._friendships.get(graha, {}).get("friends", [])

    def get_enemies(self, graha: Graha) -> list[Graha]:
        return self._friendships.get(graha, {}).get("enemies", [])

    def get_exaltation(self, graha: Graha) -> tuple[Rashi, float] | None:
        return self._exaltation.get(graha)

    def get_debilitation(self, graha: Graha) -> tuple[Rashi, float] | None:
        return self._debilitation.get(graha)

    def get_own_signs(self, graha: Graha) -> list[Rashi]:
        return self._own_signs.get(graha, [])

    def get_dignity(self, graha: Graha, rashi: Rashi) -> str:
        if self._exaltation.get(graha, (None,))[0] == rashi:
            return "exalted"
        if self._debilitation.get(graha, (None,))[0] == rashi:
            return "debilitated"
        if rashi in self._own_signs.get(graha, []):
            return "own"
        rashi_lord = self._get_rashi_lord(rashi)
        if rashi_lord in self._friendships.get(graha, {}).get("friends", []):
            return "friend"
        if rashi_lord in self._friendships.get(graha, {}).get("enemies", []):
            return "enemy"
        return "neutral"

    def _get_rashi_lord(self, rashi: Rashi) -> Graha:
        lords = {
            Rashi.MESHA: Graha.MANGAL, Rashi.VRISHABHA: Graha.SHUKRA, Rashi.MITHUNA: Graha.BUDHA,
            Rashi.KARKA: Graha.CHANDRA, Rashi.SIMHA: Graha.SURYA, Rashi.KANYA: Graha.BUDHA,
            Rashi.TULA: Graha.SHUKRA, Rashi.VRISHCHIKA: Graha.MANGAL, Rashi.DHANU: Graha.GURU,
            Rashi.MAKARA: Graha.SHANI, Rashi.KUMBHA: Graha.SHANI, Rashi.MEENA: Graha.GURU,
        }
        return lords[rashi]

    def get_nakshatra_lord(self, nakshatra_index: int) -> Graha:
        """Get Vimshottari dasha lord for a nakshatra (0-26)."""
        return self._nakshatra_lords[nakshatra_index % 9]

    def get_dasha_years(self, graha: Graha) -> float:
        return self._properties[graha]["dasha_years"]

    def get_all_grahas(self) -> list[Graha]:
        return list(Graha)
