from django import forms
from .models import Compra, Producto, Venta, Detalleventa
from django.forms import formset_factory

class CompraForm(forms.ModelForm):
    productos = forms.ModelMultipleChoiceField(queryset=Producto.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Compra
        fields = ['fechaemision', 'descripcion', 'valortotal', 'idproveedor']
        exclude = ['valortotal', 'fechaemision']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for producto in Producto.objects.all():
            self.fields[f'cantidad_producto_{producto.idproducto}'] = forms.IntegerField(min_value=0, initial=0, label=f'Cantidad {producto.nomproducto}')

    def clean(self):
        cleaned_data = super().clean()
        productos_seleccionados = cleaned_data.get('productos', [])
        for producto in self.fields['productos'].queryset:
            if producto in productos_seleccionados:
                cantidad = cleaned_data.get(f'cantidad_producto_{producto.idproducto}', 0)
                if cantidad <= 0:
                    raise forms.ValidationError(f"Debe ingresar una cantidad mayor que cero para {producto.nomproducto}")
        return cleaned_data

class VentaForm(forms.ModelForm):
    productos = forms.ModelMultipleChoiceField(queryset=Producto.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Venta
        fields = ['fechaemision', 'valortotal']
        exclude = ['valortotal', 'fechaemision']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for producto in self.fields['productos'].queryset:
            cantidad_field_name = 'cantidad_producto_{}'.format(producto.idproducto)
            self.fields[cantidad_field_name] = forms.IntegerField(
                min_value=0,
                initial=0,
                label=f'Cantidad {producto.nomproducto}'
            )

    def clean(self):
        cleaned_data = super().clean()
        productos_seleccionados = cleaned_data.get('productos', [])
        for producto in self.fields['productos'].queryset:
            if producto in productos_seleccionados:
                cantidad = cleaned_data.get(f'cantidad_producto_{producto.idproducto}', 0)
                if cantidad <= 0:
                    raise forms.ValidationError(f"Debe ingresar una cantidad mayor que cero para {producto.nomproducto}")
        return cleaned_data
    

class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = Detalleventa
        fields = ['cantidad']
        widgets = {'cantidad': forms.NumberInput(attrs={'min': 0})}