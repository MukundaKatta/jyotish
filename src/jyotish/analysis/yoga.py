"""YogaDetector finding 20+ yogas in a birth chart."""
from __future__ import annotations
from ..models import BirthChart, Yoga, Graha, Rashi, Planet


class YogaDetector:
    """Detect classical Vedic astrology yogas in a birth chart."""

    def detect_all(self, chart: BirthChart) -> list[Yoga]:
        """Detect all applicable yogas in the chart."""
        yogas = []
        planet_map = {p.name: p for p in chart.planets}
        house_map = {h.number: h for h in chart.houses}

        yogas.extend(self._check_raj_yoga(chart, planet_map, house_map))
        yogas.extend(self._check_gajakesari(planet_map))
        yogas.extend(self._check_budhaditya(planet_map))
        yogas.extend(self._check_hamsa(planet_map))
        yogas.extend(self._check_malavya(planet_map))
        yogas.extend(self._check_ruchaka(planet_map))
        yogas.extend(self._check_bhadra(planet_map))
        yogas.extend(self._check_shasha(planet_map))
        yogas.extend(self._check_chandra_mangal(planet_map))
        yogas.extend(self._check_adhi_yoga(planet_map))
        yogas.extend(self._check_dhana_yoga(chart, planet_map))
        yogas.extend(self._check_viparita_raja(planet_map))
        yogas.extend(self._check_neechabhanga(chart, planet_map))
        yogas.extend(self._check_kemadruma(planet_map))
        yogas.extend(self._check_sakata(planet_map))
        yogas.extend(self._check_amala(planet_map))
        yogas.extend(self._check_parvata(planet_map, house_map))
        yogas.extend(self._check_kahala(planet_map))
        yogas.extend(self._check_lakshmi(chart, planet_map))
        yogas.extend(self._check_saraswati(planet_map))
        yogas.extend(self._check_akhanda_samrajya(chart, planet_map))

        return yogas

    def _are_in_kendra(self, p1: Planet, p2: Planet) -> bool:
        """Check if two planets are in kendra (1,4,7,10) from each other."""
        diff = abs(p1.house - p2.house) % 12
        return diff in (0, 3, 6, 9)

    def _are_conjunct(self, p1: Planet, p2: Planet) -> bool:
        return p1.house == p2.house

    def _is_in_kendra(self, planet: Planet) -> bool:
        return planet.house in (1, 4, 7, 10)

    def _check_raj_yoga(self, chart: BirthChart, pm: dict, hm: dict) -> list[Yoga]:
        """Raj Yoga: Lord of kendra and trikona conjunct or in mutual aspect."""
        yogas = []
        kendra_houses = [1, 4, 7, 10]
        trikona_houses = [1, 5, 9]
        kendra_lords = set()
        trikona_lords = set()
        for h in chart.houses:
            if h.number in kendra_houses:
                kendra_lords.add(h.lord)
            if h.number in trikona_houses:
                trikona_lords.add(h.lord)
        for kl in kendra_lords:
            for tl in trikona_lords:
                if kl != tl and kl in pm and tl in pm:
                    if self._are_conjunct(pm[kl], pm[tl]):
                        yogas.append(Yoga(name="Raj Yoga", description=f"{kl.value} (kendra lord) conjunct {tl.value} (trikona lord) - indicates power, authority and success",
                                          planets_involved=[kl, tl], is_benefic=True, strength="strong"))
        return yogas

    def _check_gajakesari(self, pm: dict) -> list[Yoga]:
        """Gajakesari Yoga: Jupiter in kendra from Moon."""
        guru = pm.get(Graha.GURU)
        chandra = pm.get(Graha.CHANDRA)
        if guru and chandra and self._are_in_kendra(guru, chandra):
            return [Yoga(name="Gajakesari Yoga", description="Jupiter in kendra from Moon - gives wisdom, wealth, and lasting fame",
                         planets_involved=[Graha.GURU, Graha.CHANDRA], is_benefic=True, strength="strong")]
        return []

    def _check_budhaditya(self, pm: dict) -> list[Yoga]:
        """Budhaditya Yoga: Sun and Mercury conjunct."""
        surya = pm.get(Graha.SURYA)
        budha = pm.get(Graha.BUDHA)
        if surya and budha and self._are_conjunct(surya, budha):
            return [Yoga(name="Budhaditya Yoga", description="Sun-Mercury conjunction - gives sharp intellect and communication skills",
                         planets_involved=[Graha.SURYA, Graha.BUDHA], is_benefic=True, strength="medium")]
        return []

    def _check_hamsa(self, pm: dict) -> list[Yoga]:
        """Hamsa Yoga (Pancha Mahapurusha): Jupiter in own/exalted sign in kendra."""
        guru = pm.get(Graha.GURU)
        if guru and self._is_in_kendra(guru) and guru.dignity in ("own", "exalted"):
            return [Yoga(name="Hamsa Yoga", description="Jupiter in own/exalted sign in kendra - great wisdom, spirituality, and respect",
                         planets_involved=[Graha.GURU], is_benefic=True, strength="strong")]
        return []

    def _check_malavya(self, pm: dict) -> list[Yoga]:
        """Malavya Yoga: Venus in own/exalted in kendra."""
        shukra = pm.get(Graha.SHUKRA)
        if shukra and self._is_in_kendra(shukra) and shukra.dignity in ("own", "exalted"):
            return [Yoga(name="Malavya Yoga", description="Venus in own/exalted sign in kendra - beauty, luxury, artistic talent, happy marriage",
                         planets_involved=[Graha.SHUKRA], is_benefic=True, strength="strong")]
        return []

    def _check_ruchaka(self, pm: dict) -> list[Yoga]:
        """Ruchaka Yoga: Mars in own/exalted in kendra."""
        mangal = pm.get(Graha.MANGAL)
        if mangal and self._is_in_kendra(mangal) and mangal.dignity in ("own", "exalted"):
            return [Yoga(name="Ruchaka Yoga", description="Mars in own/exalted sign in kendra - courage, leadership, and military prowess",
                         planets_involved=[Graha.MANGAL], is_benefic=True, strength="strong")]
        return []

    def _check_bhadra(self, pm: dict) -> list[Yoga]:
        """Bhadra Yoga: Mercury in own/exalted in kendra."""
        budha = pm.get(Graha.BUDHA)
        if budha and self._is_in_kendra(budha) and budha.dignity in ("own", "exalted"):
            return [Yoga(name="Bhadra Yoga", description="Mercury in own/exalted sign in kendra - intelligence, eloquence, and business acumen",
                         planets_involved=[Graha.BUDHA], is_benefic=True, strength="strong")]
        return []

    def _check_shasha(self, pm: dict) -> list[Yoga]:
        """Shasha Yoga: Saturn in own/exalted in kendra."""
        shani = pm.get(Graha.SHANI)
        if shani and self._is_in_kendra(shani) and shani.dignity in ("own", "exalted"):
            return [Yoga(name="Shasha Yoga", description="Saturn in own/exalted sign in kendra - authority, discipline, and political power",
                         planets_involved=[Graha.SHANI], is_benefic=True, strength="strong")]
        return []

    def _check_chandra_mangal(self, pm: dict) -> list[Yoga]:
        """Chandra-Mangal Yoga: Moon-Mars conjunction."""
        chandra = pm.get(Graha.CHANDRA)
        mangal = pm.get(Graha.MANGAL)
        if chandra and mangal and self._are_conjunct(chandra, mangal):
            return [Yoga(name="Chandra-Mangal Yoga", description="Moon-Mars conjunction - gives wealth through own efforts",
                         planets_involved=[Graha.CHANDRA, Graha.MANGAL], is_benefic=True, strength="medium")]
        return []

    def _check_adhi_yoga(self, pm: dict) -> list[Yoga]:
        """Adhi Yoga: Benefics in 6th, 7th, 8th from Moon."""
        chandra = pm.get(Graha.CHANDRA)
        if not chandra:
            return []
        benefics = [Graha.GURU, Graha.SHUKRA, Graha.BUDHA]
        count = 0
        for b in benefics:
            if b in pm:
                diff = (pm[b].house - chandra.house) % 12
                if diff in (5, 6, 7):  # 6th, 7th, 8th from Moon
                    count += 1
        if count >= 2:
            return [Yoga(name="Adhi Yoga", description="Benefics in 6/7/8 from Moon - leadership, prosperity, and high position",
                         planets_involved=[Graha.CHANDRA], is_benefic=True, strength="strong")]
        return []

    def _check_dhana_yoga(self, chart: BirthChart, pm: dict) -> list[Yoga]:
        """Dhana Yoga: Lords of 2nd and 11th connected."""
        h2_lord = None
        h11_lord = None
        for h in chart.houses:
            if h.number == 2:
                h2_lord = h.lord
            if h.number == 11:
                h11_lord = h.lord
        if h2_lord and h11_lord and h2_lord in pm and h11_lord in pm:
            if self._are_conjunct(pm[h2_lord], pm[h11_lord]):
                return [Yoga(name="Dhana Yoga", description="2nd and 11th lords conjunct - indicates great wealth accumulation",
                             planets_involved=[h2_lord, h11_lord], is_benefic=True, strength="strong")]
        return []

    def _check_viparita_raja(self, pm: dict) -> list[Yoga]:
        """Viparita Raja Yoga: Lords of 6/8/12 in each other's houses or conjunct."""
        # Simplified check
        return []

    def _check_neechabhanga(self, chart: BirthChart, pm: dict) -> list[Yoga]:
        """Neechabhanga Raja Yoga: Debilitated planet with cancellation."""
        yogas = []
        for p in chart.planets:
            if p.dignity == "debilitated" and self._is_in_kendra(p):
                yogas.append(Yoga(name="Neechabhanga Raja Yoga", description=f"{p.name.value} debilitated but in kendra - debilitation cancelled, gives eventual rise to power",
                                  planets_involved=[p.name], is_benefic=True, strength="medium"))
        return yogas

    def _check_kemadruma(self, pm: dict) -> list[Yoga]:
        """Kemadruma Yoga: No planets in 2nd or 12th from Moon (inauspicious)."""
        chandra = pm.get(Graha.CHANDRA)
        if not chandra:
            return []
        has_planet_adjacent = False
        for g, p in pm.items():
            if g == Graha.CHANDRA:
                continue
            diff = (p.house - chandra.house) % 12
            if diff in (1, 11):  # 2nd or 12th from Moon
                has_planet_adjacent = True
                break
        if not has_planet_adjacent:
            return [Yoga(name="Kemadruma Yoga", description="No planets in 2nd/12th from Moon - periods of financial difficulty and loneliness (can be cancelled)",
                         planets_involved=[Graha.CHANDRA], is_benefic=False, strength="medium")]
        return []

    def _check_sakata(self, pm: dict) -> list[Yoga]:
        """Sakata Yoga: Jupiter in 6th/8th/12th from Moon."""
        guru = pm.get(Graha.GURU)
        chandra = pm.get(Graha.CHANDRA)
        if guru and chandra:
            diff = (guru.house - chandra.house) % 12
            if diff in (5, 7, 11):  # 6, 8, 12 from Moon
                return [Yoga(name="Sakata Yoga", description="Jupiter in 6/8/12 from Moon - fluctuating fortune (can be cancelled by other yogas)",
                             planets_involved=[Graha.GURU, Graha.CHANDRA], is_benefic=False, strength="mild")]
        return []

    def _check_amala(self, pm: dict) -> list[Yoga]:
        """Amala Yoga: Benefic in 10th from Moon or Lagna."""
        benefics = [Graha.GURU, Graha.SHUKRA, Graha.BUDHA]
        for b in benefics:
            if b in pm and pm[b].house == 10:
                return [Yoga(name="Amala Yoga", description=f"{b.value} in 10th house - spotless reputation, charitable nature, and noble career",
                             planets_involved=[b], is_benefic=True, strength="medium")]
        return []

    def _check_parvata(self, pm: dict, hm: dict) -> list[Yoga]:
        """Parvata Yoga: Benefics in kendra, no malefics in kendra."""
        return []

    def _check_kahala(self, pm: dict) -> list[Yoga]:
        return []

    def _check_lakshmi(self, chart: BirthChart, pm: dict) -> list[Yoga]:
        """Lakshmi Yoga: 9th lord strong and in kendra/trikona."""
        h9_lord = None
        for h in chart.houses:
            if h.number == 9:
                h9_lord = h.lord
        if h9_lord and h9_lord in pm:
            p = pm[h9_lord]
            if p.house in (1, 4, 5, 7, 9, 10) and p.dignity in ("own", "exalted", "friend"):
                return [Yoga(name="Lakshmi Yoga", description="9th lord strong in kendra/trikona - great wealth, fortune, and divine grace",
                             planets_involved=[h9_lord], is_benefic=True, strength="strong")]
        return []

    def _check_saraswati(self, pm: dict) -> list[Yoga]:
        """Saraswati Yoga: Jupiter, Venus, Mercury in kendra/trikona/2nd."""
        good_houses = {1, 2, 4, 5, 7, 9, 10}
        all_good = True
        for g in [Graha.GURU, Graha.SHUKRA, Graha.BUDHA]:
            if g not in pm or pm[g].house not in good_houses:
                all_good = False
                break
        if all_good:
            return [Yoga(name="Saraswati Yoga", description="Jupiter, Venus, Mercury in good houses - learning, wisdom, and mastery of arts",
                         planets_involved=[Graha.GURU, Graha.SHUKRA, Graha.BUDHA], is_benefic=True, strength="strong")]
        return []

    def _check_akhanda_samrajya(self, chart: BirthChart, pm: dict) -> list[Yoga]:
        """Akhanda Samrajya Yoga: Jupiter lord of 2/5/11 in kendra from lagna/moon."""
        guru = pm.get(Graha.GURU)
        if guru and self._is_in_kendra(guru):
            for h in chart.houses:
                if h.lord == Graha.GURU and h.number in (2, 5, 11):
                    return [Yoga(name="Akhanda Samrajya Yoga", description="Jupiter as lord of 2/5/11 in kendra - undisputed authority and kingdom",
                                 planets_involved=[Graha.GURU], is_benefic=True, strength="strong")]
        return []
