from rest_framework import serializers
from core.models import Nhatkysukien, Xulysukientb


class XulysukientbSerializer(serializers.ModelSerializer):
    """Serializer for Xulysukientb"""
    class Meta:
        model = Xulysukientb
        fields = [
            'id', 'title', 'Tomay', 'Noidung_xuly', 'Thoigian_xuly',
            'Quatrinh_kiemtra', 'Dexuat_lienquan', 'Chidao', 'Tinhtrang_xuly',
            'Quatrinh_Xuly', 'Phantich_Nguyennhan_Xl', 'Donvi_ghinhan',
            'Cavanhanh_ghinhan'
        ]
        read_only_fields = ['id']


class NhatkysukienSerializer(serializers.ModelSerializer):
    xulysukientbs = XulysukientbSerializer(many=True, required=False)

    class Meta:
        model = Nhatkysukien
        fields = [
            'id', 'title', 'Thoigian', 'Hethong_Thietbi', 'Hientuong_Dienbien',
            'Quatrinh_Kt', 'LoaiSc', 'Baocao_Chidao', 'DeNghi', 'CaVanHanh',
            'Donvi_khacPhuc', 'xulysukientbs'
        ]
        read_only_fields = ['id']

    def _get_or_create_xulysukientbs(self, xulysukientbs, nhatkysukien):
        """Handle getting or creating Xulysukientb as needed."""
        auth_user = self.context['request'].user
        for xulysukientb in xulysukientbs:
            xulysukientb_obj, created = Xulysukientb.objects.get_or_create(
                user=auth_user,
                Tomay=xulysukientb['Tomay']
            )
            nhatkysukien.xulysukientbs.add(xulysukientb_obj)

    def create(self, validated_data):
        """Create a Nhatkysukien."""
        xulysukientbs = validated_data.pop('xulysukientbs', [])
        nhatkysukien = Nhatkysukien.objects.create(**validated_data)
        self._get_or_create_xulysukientbs(xulysukientbs, nhatkysukien)
        return nhatkysukien

    def update(self, instance, validated_data):
        """CN Nhatkysukien and làm đúng Xulysukientb assignments."""
        xulysukientbs = validated_data.pop('xulysukientbs', None)
        if xulysukientbs is not None:
            # Get new Tomay names from request
            new_tomay_names = {
                xulysukientb['Tomay'] for xulysukientb in xulysukientbs
                }
            # Remove old Xulysukientbs not in the new list
            instance.xulysukientbs.exclude(Tomay__in=new_tomay_names).delete()

            for xulysukientb in xulysukientbs:
                xulysukientb_obj, created = Xulysukientb.objects.get_or_create(
                    user=self.context['request'].user,
                    Tomay=xulysukientb['Tomay']
                )
                instance.xulysukientbs.add(xulysukientb_obj)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class NhatkysukienDetailSerializer(NhatkysukienSerializer):
    """Serializer for Nhatkysukien detail view."""

    class Meta(NhatkysukienSerializer.Meta):
        fields = NhatkysukienSerializer.Meta.fields + [
            'Hethong_Thietbi', 'Hientuong_Dienbien', 'Quatrinh_Kt', 'LoaiSc',
            'Baocao_Chidao', 'DeNghi', 'CaVanHanh', 'Donvi_khacPhuc'
        ]
