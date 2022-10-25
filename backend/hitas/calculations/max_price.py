import datetime
from decimal import ROUND_HALF_UP, Decimal
from typing import List, Optional

from dateutil.relativedelta import relativedelta
from django.db.models import Prefetch, Sum

from hitas.models import (
    Apartment,
    ApartmentConstructionPriceImprovement,
    ApartmentMarketPriceImprovement,
    HousingCompany,
    HousingCompanyConstructionPriceImprovement,
    HousingCompanyMarketPriceImprovement,
    Ownership,
)


class IndexMissingException(Exception):
    pass


def calculate_max_price(
    housing_company_uuid: str,
    apartment_uuid: str,
    calculation_date: Optional[datetime.date],
    apartment_share_of_housing_company_loans: int,
):
    if calculation_date is None:
        calculation_date = datetime.date.today()

    # Fetch apartment
    apartment = fetch_apartment(housing_company_uuid, apartment_uuid, calculation_date)

    # Fetch housing company's total surface area
    total_surface_area = (
        HousingCompany.objects.annotate(sum_surface_area=Sum("real_estates__buildings__apartments__surface_area"))
        .only("id")
        .get(id=apartment.building.real_estate.housing_company.id)
        .sum_surface_area
    )

    # Check we found the necessary indices
    if (
        apartment.calculation_date_cpi_2005eq100 is None
        or apartment.completion_date_cpi_2005eq100 is None
        or apartment.calculation_date_mpi_2005eq100 is None
        or apartment.completion_date_mpi_2005eq100 is None
        or apartment.surface_area_price_ceiling is None
    ):
        raise IndexMissingException()

    # Do the max price calculations
    construction_price_index = calculate_index(
        apartment,
        apartment.calculation_date_cpi_2005eq100,
        apartment.completion_date_cpi_2005eq100,
        total_surface_area,
        apartment_share_of_housing_company_loans,
        apartment.construction_price_improvements.all(),
        apartment.building.real_estate.housing_company.construction_price_improvements.all(),
        calculation_date,
    )
    market_price_index = calculate_index(
        apartment,
        apartment.calculation_date_mpi_2005eq100,
        apartment.completion_date_mpi_2005eq100,
        total_surface_area,
        apartment_share_of_housing_company_loans,
        apartment.market_price_improvements.all(),
        apartment.building.real_estate.housing_company.market_price_improvements.all(),
        calculation_date,
    )
    surface_area_price_ceiling = {
        "max_price": roundup(apartment.surface_area_price_ceiling),
        "valid_until": calculation_date,  # FIXME: use how long index is valid
    }

    # Find and mark the maximum
    max_price = max(
        construction_price_index["max_price"],
        market_price_index["max_price"],
        surface_area_price_ceiling["max_price"],
    )
    surface_area_price_ceiling["maximum"] = max_price == surface_area_price_ceiling["max_price"]
    market_price_index["maximum"] = max_price == market_price_index["max_price"]
    construction_price_index["maximum"] = max_price == construction_price_index["max_price"]

    if market_price_index["maximum"]:
        max_index = "market_price_index"
    elif construction_price_index["maximum"]:
        max_index = "construction_price_index"
    else:
        max_index = "surface_area_price_ceiling"

    return {
        "calculations": {
            "construction_price_index": construction_price_index,
            "market_price_index": market_price_index,
            "surface_area_price_ceiling": surface_area_price_ceiling,
        },
        "max_price": max_price,
        "index": max_index,
        "apartment": {
            "shares": {
                "start": apartment.share_number_start,
                "end": apartment.share_number_end,
                "total": apartment.share_number_end - apartment.share_number_start + 1,
            },
            "rooms": apartment.rooms,
            "apartment_type": apartment.apartment_type.value,
            "surface_area": apartment.surface_area,
            "address": {
                "street_address": apartment.street_address,
                "floor": apartment.floor,
                "stair": apartment.stair,
                "apartment_number": apartment.apartment_number,
                "postal_code": apartment.postal_code.value,
                "city": apartment.postal_code.city,
            },
            "ownership": [
                {"percentage": ownership.percentage, "name": ownership.owner.name}
                for ownership in apartment.ownerships.all()
            ],
        },
        "housing_company": {
            "official_name": apartment.building.real_estate.housing_company.official_name,
            "archive_id": apartment.building.real_estate.housing_company.id,
            "property_manager": {
                "name": apartment.building.real_estate.housing_company.property_manager.name,
                "street_address": apartment.building.real_estate.housing_company.property_manager.street_address,
            },
        },
    }


def fetch_apartment(
    housing_company_uuid: str,
    apartment_uuid: str,
    calculation_date: Optional[datetime.date],
):
    return (
        Apartment.objects.only(
            "additional_work_during_construction",
            "share_number_start",
            "share_number_end",
            "street_address",
            "floor",
            "stair",
            "apartment_number",
            "rooms",
            "apartment_type_id",
            "surface_area",
            "completion_date",
            "debt_free_purchase_price",
            "primary_loan_amount",
            "apartment_type__value",
            "building__real_estate__housing_company__id",
            "building__real_estate__housing_company__official_name",
            "building__real_estate__housing_company__postal_code__value",
            "building__real_estate__housing_company__postal_code__city",
            "building__real_estate__housing_company__property_manager__name",
            "building__real_estate__housing_company__property_manager__street_address",
        )
        .select_related(
            "apartment_type",
            "building__real_estate__housing_company",
            "building__real_estate__housing_company__property_manager",
            "building__real_estate__housing_company__postal_code",
        )
        .prefetch_related(
            Prefetch(
                "ownerships",
                Ownership.objects.only("apartment_id", "percentage", "owner__name").select_related("owner"),
            ),
            Prefetch(
                "construction_price_improvements",
                ApartmentConstructionPriceImprovement.objects.only("value", "apartment_id", "depreciation_percentage"),
            ),
            Prefetch(
                "market_price_improvements",
                ApartmentMarketPriceImprovement.objects.only("value", "apartment_id"),
            ),
            Prefetch(
                "building__real_estate__housing_company__construction_price_improvements",
                HousingCompanyConstructionPriceImprovement.objects.only("value", "housing_company_id",).extra(
                    select={
                        "completion_date_index": """
    SELECT completion_date_index.value
    FROM hitas_constructionpriceindex2005equal100 AS completion_date_index
    WHERE completion_date_index.month
         = DATE_TRUNC('month', hitas_housingcompanyconstructionpriceimprovement.completion_date)
    """,
                    },
                ),
            ),
            Prefetch(
                "building__real_estate__housing_company__market_price_improvements",
                HousingCompanyMarketPriceImprovement.objects.only("value", "housing_company_id",).extra(
                    select={
                        "completion_date_index": """
    SELECT completion_date_index.value
    FROM hitas_marketpriceindex2005equal100 AS completion_date_index
    WHERE completion_date_index.month
         = DATE_TRUNC('month', hitas_housingcompanymarketpriceimprovement.completion_date)
    """,
                    },
                ),
            ),
        )
        .extra(
            select={
                "calculation_date_cpi_2005eq100": """
SELECT calculation_date_index.value
FROM hitas_constructionpriceindex2005equal100 AS calculation_date_index
WHERE calculation_date_index.month = DATE_TRUNC('month', %s)
""",
                "completion_date_cpi_2005eq100": """
SELECT completion_date_index.value
FROM hitas_apartment AS a
LEFT JOIN hitas_constructionpriceindex2005equal100 AS completion_date_index ON
    completion_date_index.month = DATE_TRUNC('month', a.completion_date)
WHERE a.id = hitas_apartment.id
""",
                "calculation_date_mpi_2005eq100": """
SELECT calculation_date_index.value
FROM hitas_marketpriceindex2005equal100 AS calculation_date_index
WHERE calculation_date_index.month = DATE_TRUNC('month', %s)
""",
                "completion_date_mpi_2005eq100": """
SELECT completion_date_index.value
FROM hitas_apartment AS a
LEFT JOIN hitas_marketpriceindex2005equal100 AS completion_date_index ON
    completion_date_index.month = DATE_TRUNC('month', a.completion_date)
WHERE a.id = hitas_apartment.id
""",
                "surface_area_price_ceiling": """
    SELECT ROUND(a.surface_area * sapc.value)
    FROM hitas_apartment AS a
    LEFT JOIN hitas_surfaceareapriceceiling AS sapc
        ON sapc.month = DATE_TRUNC('month', %s)
    WHERE a.id = hitas_apartment.id
""",
            },
            select_params=(calculation_date, calculation_date, calculation_date),
        )
        .get(uuid=apartment_uuid, building__real_estate__housing_company__uuid=housing_company_uuid)
    )


def calculate_index(
    apartment: Apartment,
    calculation_date_index: Decimal,
    completion_date_index: Decimal,
    total_surface_area: Decimal,
    apartment_share_of_housing_company_loans: int,
    apartment_improvements: List,
    housing_company_improvements: List,
    calculation_date: datetime.date,
):
    # Start calculations

    # 'perushinta'
    basic_price = apartment.acquisition_price + apartment.additional_work_during_construction

    # 'indeksin muutos'
    index_adjustment = ((calculation_date_index / completion_date_index) * basic_price) - basic_price

    # 'huoneistokohtaiset parannukset'
    apartment_improvements_sum = sum(map(lambda i: i.value, apartment_improvements))
    apartment_improvements_sum *= calculation_date_index / completion_date_index

    # 'yhtiön parannukset'
    apartment_housing_company_improvements = Decimal(0)
    for improvement in housing_company_improvements:
        # 'omavastuu'
        excess = 30 * total_surface_area
        if excess >= improvement.value:
            continue

        # 'arvon lisäys'
        value_addition = improvement.value - excess

        if improvement.completion_date_index is None:
            raise IndexMissingException()

        improvement_value = value_addition * (calculation_date_index / improvement.completion_date_index)
        apartment_housing_company_improvements += improvement_value / total_surface_area * apartment.surface_area

    # 'osakkeiden velaton hinta'
    shares_debt_free_shares_price = (
        basic_price
        + roundup(index_adjustment)
        + roundup(apartment_improvements_sum)
        + roundup(apartment_housing_company_improvements)
    )
    # 'Enimmäismyyntihinta'
    max_price = shares_debt_free_shares_price - apartment_share_of_housing_company_loans

    return {
        "calculation_variables": {
            "acquisition_price": apartment.acquisition_price,
            "additional_work_during_construction": apartment.additional_work_during_construction,
            "basic_price": basic_price,
            "index_adjustment": roundup(index_adjustment),
            "apartment_improvements": roundup(apartment_improvements_sum),
            "housing_company_improvements": roundup(apartment_housing_company_improvements),
            "debt_free_price": shares_debt_free_shares_price,
            "debt_free_price_m2": roundup(shares_debt_free_shares_price / apartment.surface_area),
            "apartment_share_of_housing_company_loans": apartment_share_of_housing_company_loans,
            "completion_date": apartment.completion_date,
            "completion_date_index": completion_date_index,
            "calculation_date": calculation_date,
            "calculation_date_index": calculation_date_index,
        },
        "max_price": max_price,
        "valid_until": calculation_date + relativedelta(months=3),
    }


def roundup(v: Decimal) -> int:
    return int(v.quantize(0, ROUND_HALF_UP))
