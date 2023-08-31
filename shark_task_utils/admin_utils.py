from django import forms
from django.urls import reverse
from django.utils.html import format_html


def get_label(obj, field_name_info_list: list[list[str]]) -> str:
    result = ""
    for field_name_info in field_name_info_list:
        current_obj = obj
        if current_obj is None:
            continue
        full_field_name = ""
        for field_name in field_name_info:
            current_obj = getattr(current_obj, field_name)
            full_field_name += field_name + "."
        full_field_name = full_field_name[:-1] if full_field_name else full_field_name
        result += f"[{full_field_name}:{str(current_obj)}]"
    return result


class CustomChoiceField(forms.ModelChoiceField):
    def __init__(self, queryset, field_name_info_list: list[list[str]], **kwargs) -> None:
        super().__init__(queryset=queryset, **kwargs)
        self._field_name_info_list = field_name_info_list

    def label_from_instance(self, obj):
        return get_label(obj, self._field_name_info_list)


def get_linked_value(field, value: str):
    result = None
    if field:
        app_label = field._meta.app_label
        model_name = field._meta.model_name
        view_name = f"admin:{app_label}_{model_name}_change"
        link = reverse(view_name, args=[field.pk])
        result = format_html(f"<a href='{link}'>{value}</a>")
    return result
