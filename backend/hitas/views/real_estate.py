from uuid import UUID

from rest_framework import serializers

from hitas.exceptions import HitasModelNotFound, ModelConflict
from hitas.models import HousingCompany, RealEstate
from hitas.utils import lookup_id_to_uuid
from hitas.views.building import BuildingSerializer
from hitas.views.utils import HitasModelSerializer, HitasModelViewSet


class RealEstateHitasAddressSerializer(serializers.Serializer):
    street_address = serializers.CharField()
    postal_code = serializers.CharField(source="housing_company.postal_code.value", read_only=True)
    city = serializers.CharField(source="housing_company.city", read_only=True)


class RealEstateSerializer(HitasModelSerializer):
    address = RealEstateHitasAddressSerializer(source="*")
    buildings = BuildingSerializer(many=True, read_only=True)

    @property
    def validated_data(self):
        """Inject related Housing Company ID to the validated data"""
        validated_data = super().validated_data
        try:
            housing_company_uuid = UUID(hex=self.context["view"].kwargs.get("housing_company_uuid"))
            housing_company_id = HousingCompany.objects.only("id").get(uuid=housing_company_uuid).id
        except (HousingCompany.DoesNotExist, ValueError):
            raise HitasModelNotFound(model=HousingCompany)

        validated_data["housing_company_id"] = housing_company_id
        return validated_data

    class Meta:
        model = RealEstate
        fields = [
            "id",
            "address",
            "property_identifier",
            "buildings",
        ]


class RealEstateViewSet(HitasModelViewSet):
    serializer_class = RealEstateSerializer
    model_class = RealEstate

    def perform_destroy(self, instance: RealEstate) -> None:
        if instance.buildings.exists():
            raise ModelConflict(
                "Cannot delete a real estate with buildings.",
                error_code="buildings_on_real_estate",
            )

        super().perform_destroy(instance)

    def get_queryset(self):
        uuid = lookup_id_to_uuid(self.kwargs["housing_company_uuid"], HousingCompany)
        return (
            RealEstate.objects.filter(housing_company__uuid=uuid)
            .select_related("housing_company__postal_code")
            .prefetch_related("buildings")
            .order_by("id")
        )
