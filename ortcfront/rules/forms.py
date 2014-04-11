# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 Rodolphe Quiédeville <rodolphe@quiedeville.org>
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Forms
#
import re
from django import forms
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from django.forms.widgets import Textarea, Select, TextInput, HiddenInput
from crispy_forms.helper import FormHelper
from crispy_forms import layout
from crispy_forms.bootstrap import PrependedText, FormActions, InlineRadios
from .models import Domain, Rule


def exclude_regex(value):
    """Exclude some too dangerous regex

    - TODO add more and improve
    """
    if value == ".*.*":
        raise ValidationError('%s is not a valid regex' % value)

def validate_regex(value):
    """Exclude some too dangerous regex

    - TODO add more and improve
    """
    try:
        res = re.compile(value)
    except:
        raise ValidationError('%s is an invalid regex' % value)


class DomainNewForm(forms.ModelForm):
    """Use to create a new domain
    """
    class Meta:
        model = Domain
        fields = ['name', 'description']

    name = forms.CharField(max_length=50,
                           required=True,
                           label="Nom",
                           widget=TextInput())

    description = forms.CharField(max_length=2500,
                                  required=False,
                                  widget=Textarea())

    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-lg-2'
    helper.field_class = 'col-lg-10'
    helper.layout = layout.Layout(
        layout.Field('name', css_class='input-large'),
        layout.Field('description'),
        FormActions(
            layout.Submit('save_changes', 'Enregistrer', css_class="btn-primary"),
            layout.Submit('cancel', 'Annuler', css_class="btn-danger"),
            )
        )


class RuleNewForm(forms.ModelForm):
    """Use to create a new rule
    """
    class Meta:
        model = Rule
        fields = ['name', 'tag_regex', 'domains', 
                  'node_applied', 'way_applied', 'relation_applied',
                  'create_applied', 'modify_applied', 'delete_applied']

    name = forms.CharField(max_length=50,
                           required=True,
                           label="Nom",
                           widget=TextInput())

    tag_regex = forms.CharField(max_length=100,
                                required=True,
                                validators=[MinLengthValidator(4),
                                            validate_regex,
                                            exclude_regex],
                                widget=TextInput())

    def clean(self):
        # example custom validation across forms in the formset
        act = self.cleaned_data['create_applied'] or self.cleaned_data['delete_applied'] or self.cleaned_data['modify_applied']
        obo = self.cleaned_data['node_applied'] or self.cleaned_data['way_applied'] or self.cleaned_data['relation_applied']
        if not act:
            raise ValidationError('One action (create, modify or delete) is required')
        if not obo:
            raise ValidationError('One object type (node, way or relation) is required')
        return super(RuleNewForm, self).clean()



    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-lg-2'
    helper.field_class = 'col-lg-10'
    helper.layout = layout.Layout(
        layout.Field('name', css_class='input-large'),
        layout.Field('tag_regex'),
        layout.Field('domains'),
        layout.Field('node_applied'),
        layout.Field('way_applied'),
        layout.Field('relation_applied'),
        layout.Field('create_applied'),
        layout.Field('modify_applied'),
        layout.Field('delete_applied'),

        FormActions(
            layout.Submit('save_changes', 'Enregistrer', css_class="btn-primary"),
            layout.Submit('cancel', 'Annuler', css_class="btn-danger"),
            )
        )


