"""
Kerapu

:copyright: 2015-2016 Set Based IT Consultancy
:licence: MIT
"""
# ----------------------------------------------------------------------------------------------------------------------
from kerapu import *
from kerapu.Lbz.Diagnose import Diagnose
from kerapu.Lbz.Patient import Patient
from kerapu.Lbz.Specialisme import Specialisme
from kerapu.Lbz.ZorgActiviteit import ZorgActiviteit
from kerapu.Lbz.ZorgType import ZorgType
from kerapu.Lbz.ZorgVraag import ZorgVraag


# ----------------------------------------------------------------------------------------------------------------------
class Subtraject:
    """
    Klasse voor subtrajecten.
    """
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 subtraject_nummer,
                 specialisme_code,
                 diagnose_code,
                 zorg_type_code,
                 zorg_vraag_code,
                 begin_datum,
                 geboorte_datum,
                 geslacht_code):
        """
        Object constructor.

        :param str subtraject_nummer: Het substrajectnummer.
        :param str specialisme_code: Het (uitvoerend)specialismecode.
        :param str diagnose_code:  De Diagnosecode.
        :param str zorg_type_code: Het zorgtypecode.
        :param str zorg_vraag_code: De zorgvraagcode.
        :param str begin_datum:  De begindatum van het subtraject.
        :param str geboorte_datum: De geboortedatum van de patient.
        :param str geslacht_code: De code voor het geslacht van de patient.
        """
        self._subtraject_nummer = subtraject_nummer
        """
        Het subtrajectnummer.
        :type: str
        """

        self._specialisme = Specialisme(specialisme_code)
        """
        Het uitvoerend specialisme.
        :type: Specialisme
        """

        self._begin_datum = begin_datum
        """
        De begindatum van het subtraject.
        :type: str
        """

        self._patient = Patient(geboorte_datum, geslacht_code)
        """
        De patient.
        :type: Patient
        """

        self._zorg_type = ZorgType(specialisme_code, zorg_type_code)
        """
        Het zorgtype.
        :type: ZorgType
        """

        self._zorg_vraag = ZorgVraag(specialisme_code, zorg_vraag_code)
        """
        De zorgvraag.
        :type: ZorgVraag
        """

        self._diagnose = Diagnose(specialisme_code, diagnose_code)
        """
        De diagnose.
        :type: Diagnose
        """

        self._zorg_activiteiten = []
        """
        De zorgactiviteiten.
        :type: list[ZorgActiviteit]
        """

        self._zorg_product_groep_code = ''
        """
        De zorgproductgroepcode (zoals afgeleid door Kerapu).
        :type: str
        """

    # ------------------------------------------------------------------------------------------------------------------
    def add_zorg_activiteit(self, zorg_activiteit_code, aantal):
        """
        Voegt een zorgactiviteit toe and dit subtraject.

        :param str zorg_activiteit_code: De zorgactiviteitcode.
        :param int aantal: Het aantal malen (of eenheden) dat de zorgactiviteit is uitgevoerd.
        """
        self._zorg_activiteiten.append(ZorgActiviteit(zorg_activiteit_code, aantal))

    # ------------------------------------------------------------------------------------------------------------------
    def get_subtraject_nummer(self):
        """
        Geeft het subtrajectnummer van dit subtraject.

        :rtype: str
        """
        return self._subtraject_nummer

    # ------------------------------------------------------------------------------------------------------------------
    def get_begin_datum(self):
        """
        Geeft de begindatum van dit subtraject.

        :rtype: str
        """
        return self._begin_datum

    # ------------------------------------------------------------------------------------------------------------------
    def get_zorg_activiteit_cluster_telling(self, cluster_code, cluster_nummer, weeg_factor_nummer):
        """
        Geeft het aantal zorgactiviteiten (met inachtneming van weegfactor) dat in dit subtraject voorkomt in een
        zorgactiviteitcluster.

        :param str cluster_code: De zorgactiviteitclustercode.
        :param int cluster_nummer: Het clusternummer (1..10).
        :param int weeg_factor_nummer: Het weegfactornummer (0..2).

        :rtype: int
        """
        aantal = 0
        for zorg_activiteit in self._zorg_activiteiten:
            aantal += zorg_activiteit.get_zorg_activiteit_cluster_aantal(cluster_code,
                                                                         cluster_nummer,
                                                                         weeg_factor_nummer,
                                                                         self._begin_datum)

        return aantal

    # ------------------------------------------------------------------------------------------------------------------
    def get_zorg_activiteit_telling(self, zorg_activiteit_code, weeg_factor_nummer):
        """
        Geeft het aantal zorgactiviteiten (met inachtneming van weegfactor) dat in dit subtraject voldoet aan een
        zorgactiviteitcode.

        :param str zorg_activiteit_code: De zorgactiviteitcode.
        :param int weeg_factor_nummer: Het weegfactornummer (0..2).

        :rtype: int
        """
        aantal = 0
        zorg_activiteit_code = clean_code(zorg_activiteit_code, LEN_ZORG_ACTIVITEIT_CODE)
        for zorg_activiteit in self._zorg_activiteiten:
            aantal += zorg_activiteit.get_zorg_activiteit_aantal(zorg_activiteit_code,
                                                                 weeg_factor_nummer,
                                                                 self._begin_datum)

        return aantal

    # ------------------------------------------------------------------------------------------------------------------
    def get_behandel_klasse_telling(self, behandel_klasse_code, weeg_factor_nummer):
        """
        Geeft het aantal zorgactiviteiten (met inachtneming van weegfactor) dat in dit subtraject voorkomt in een
        behandelklasse.

        :param str behandel_klasse_code: De behandelklassecode waartegen getest moet worden.
        :param int weeg_factor_nummer: Het weegfactornummer (0..2).

        :rtype: int
        """
        aantal = 0
        for zorg_activiteit in self._zorg_activiteiten:
            aantal += zorg_activiteit.get_behandel_klasse_aantal(self._zorg_product_groep_code,
                                                                 behandel_klasse_code,
                                                                 weeg_factor_nummer,
                                                                 self._begin_datum)

        return aantal

    # ------------------------------------------------------------------------------------------------------------------
    def get_diagnose_cluster_telling(self, cluster_code, cluster_nummer):
        """
        Geeft het aantal malen (d.w.z. 0 of 1) dat in dit subtraject voldoet aan een diagnoseclustercode.

        :param str cluster_code: De cluster_code waartegen getest moet worden.
        :param int cluster_nummer: Het clusternummer (1..6).

        :rtype: int
        """
        return self._diagnose.get_diagnose_cluster_aantal(cluster_code, cluster_nummer, self._begin_datum)

    # ------------------------------------------------------------------------------------------------------------------
    def get_specialisme_cluster_telling(self, cluster_code, cluster_nummer):
        """
        Geeft het aantal malen (d.w.z. 0 of 1) dat het uitvoerend specialisme van dit subtraject voldoet aan een
        specialismecluster.

        :param str cluster_code: De clustercode waartegen getest moet worden.
        :param int cluster_nummer: Het clusternummer (1..2).

        :rtype: int
        """
        return self._specialisme.get_specialisme_cluster_aantal(cluster_code, cluster_nummer, self._begin_datum)

    # ------------------------------------------------------------------------------------------------------------------
    def get_zorg_vraag_cluster_telling(self, cluster_code, cluster_nummer):
        """
        Geeft het aantal malen (d.w.z. 0 of 1) dat de zorgvraag van een subtraject voorkomt in een zorgvraagcluster.

        :param str cluster_code: De cluster_code waartegen getest moet worden.
        :param int cluster_nummer: Het clusternummer (1..2).

        :rtype: int
        """
        return self._zorg_vraag.get_zorg_vraag_cluster_aantal(cluster_code, cluster_nummer, self._begin_datum)
    
    # ------------------------------------------------------------------------------------------------------------------
    def get_specialisme_telling(self, specialisme_code):
        """
        Geeft het aantal malen (d.w.z. 0 of 1) dat het uitvoerend specialisme van dit subtraject voldoet aan een
        specialismecode.

        :param str specialisme_code: De specialismecode.

        :rtype: int
        """
        return self._specialisme.get_specialisme_aantal(specialisme_code, self._begin_datum)

    # ------------------------------------------------------------------------------------------------------------------
    def get_diagnose_attribuut_telling(self, diagnose_attribuut_code):
        """
        Geeft het aantal malen (d.w.z. 0 of 1) dat de diagnose van dit subtraject voldoet aan een
        (specialismecode, diagnosecode) combinatie.

        :param str diagnose_attribuut_code: De attribuutcode voor de (specialismecode, diagnosecode) combinatie.

        :rtype: int
        """
        return self._diagnose.get_diagnose_attribute_aantal(diagnose_attribuut_code, self._begin_datum)

    # ------------------------------------------------------------------------------------------------------------------
    def set_zorg_product_groep_code(self, zorg_product_groep_code):
        """
        Zet de zorgproductgroepcode van dit subtraject.

        :param str zorg_product_groep_code: De zorgproductgroepcode.
        """
        self._zorg_product_groep_code = clean_code(zorg_product_groep_code, LEN_ZORG_PRODUCT_GROEP_CODE)

    # ------------------------------------------------------------------------------------------------------------------
    def get_zorg_vraag_attribuut_telling(self, zorg_vraag_attribuut_code):
        """
        Geeft het aantal malen (d.w.z. 0 of 1) dat de zorgvraag van dit subtraject voldoet aan een
        (specialismecode, zorgvraagcode) combinatie.

        :param str zorg_vraag_attribuut_code: De attribuutcode voor de (specialismecode, zorgvraagcode) combinatie.

        :rtype: int
        """
        return self._zorg_vraag.get_zorg_vraag_attribute_aantal(zorg_vraag_attribuut_code, self._begin_datum)

    # ------------------------------------------------------------------------------------------------------------------
    def get_zorg_type_attribuut_telling(self, zorg_type_attribuut_code):
        """
        Geeft het aantal malen (d.w.z. 0 of 1) dat de zorgtype van dit subtraject voldoet aan een
        (specialismecode, zorgtypecode) combinatie.

        :param str zorg_type_attribuut_code: De attribuutcode voor de (specialismecode, zorgtypecode) combinatie.

        :rtype: int
        """
        return self._zorg_type.get_zorg_type_attribute_aantal(zorg_type_attribuut_code, self._begin_datum)

    # ------------------------------------------------------------------------------------------------------------------
    def get_geslacht_code_telling(self, geslacht_code):
        """
        Geeft het aantal malen (d.w.z. 0 of 1) dat de patient van dit subtraject voldoet aan een geslacht.

        :param str geslacht_code: De geslachtscode waartegen getest moet worden.

        :rtype: int
        """
        if self._patient.get_geslacht_code() == geslacht_code:
            return 1

        return 0

    # ------------------------------------------------------------------------------------------------------------------
    def get_leeftijd(self):
        """
        Geeft de leeftijd van de patient van dit subtraject.

        :rtype: int
        """
        return self._patient.get_leeftijd(self._begin_datum)

# ----------------------------------------------------------------------------------------------------------------------