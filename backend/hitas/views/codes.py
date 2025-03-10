from rest_framework import serializers

from hitas.models.codes import AbstractCode, ApartmentType, BuildingType, Developer, FinancingMethod
from hitas.views.utils import HitasCharFilter, HitasFilterSet, HitasModelSerializer, HitasModelViewSet, UUIDRelatedField
from hitas.views.utils.serializers import ReadOnlySerializer


class AbstractCodeSerializer(HitasModelSerializer):
    value = serializers.CharField()
    description = serializers.CharField()
    code = serializers.CharField(source="legacy_code_number")

    class Meta:
        model = AbstractCode
        fields = ["id", "value", "description", "code"]
        read_only_fields = ["value"]
        abstract = True


class BuildingTypeSerializer(AbstractCodeSerializer):
    class Meta(AbstractCodeSerializer.Meta):
        model = BuildingType


class FinancingMethodSerializer(AbstractCodeSerializer):
    class Meta(AbstractCodeSerializer.Meta):
        model = FinancingMethod


class DeveloperSerializer(AbstractCodeSerializer):
    class Meta(AbstractCodeSerializer.Meta):
        model = Developer


class ApartmentTypeSerializer(AbstractCodeSerializer):
    class Meta(AbstractCodeSerializer.Meta):
        model = ApartmentType


def define_read_only_serializer(model_class):
    class DynamicReadOnlySerializer(ReadOnlySerializer):
        id = UUIDRelatedField(queryset=model_class.objects)
        value = serializers.CharField(read_only=True)
        description = serializers.CharField(read_only=True)
        code = serializers.CharField(source="legacy_code_number", read_only=True)

        def get_model_class(self):
            return model_class

        class Meta:
            fields = ["id", "value", "description", "code"]

    return DynamicReadOnlySerializer


ReadOnlyApartmentTypeSerializer = define_read_only_serializer(ApartmentType)
ReadOnlyDeveloperSerializer = define_read_only_serializer(Developer)
ReadOnlyFinancingMethodSerializer = define_read_only_serializer(FinancingMethod)
ReadOnlyBuildingTypeSerializer = define_read_only_serializer(BuildingType)


class AbstractCodeViewSet(HitasModelViewSet):
    def get_queryset(self):
        return self.model_class.objects.all().order_by("order", "id")

    def get_filterset_class(self):
        class CodeFilterSet(HitasFilterSet):
            value = HitasCharFilter(lookup_expr="icontains")

            class Meta:
                model = self.model_class
                fields = ["value"]

        CodeFilterSet.__name__ = f"{self.model_class}FilterSet"

        return CodeFilterSet


class BuildingTypeViewSet(AbstractCodeViewSet):
    serializer_class = BuildingTypeSerializer
    model_class = BuildingType


class FinancingMethodViewSet(AbstractCodeViewSet):
    serializer_class = FinancingMethodSerializer
    model_class = FinancingMethod


class DeveloperViewSet(AbstractCodeViewSet):
    serializer_class = DeveloperSerializer
    model_class = Developer


class ApartmentTypeViewSet(AbstractCodeViewSet):
    serializer_class = ApartmentTypeSerializer
    model_class = ApartmentType
