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
from django import forms
from django.forms.widgets import Textarea, Select, TextInput, HiddenInput
from crispy_forms.helper import FormHelper
from crispy_forms import layout
from crispy_forms.bootstrap import PrependedText, FormActions, InlineRadios
from leaflet.forms.widgets import LeafletWidget
from .models import Alert, Geozone, Report


class GeozoneNewForm(forms.ModelForm):
    """Use to create a new alert
    """
    class Meta:
        model = Geozone
        fields = ['name', 'description', 'geom']
        widgets = {'geom': LeafletWidget()}

    name = forms.CharField(max_length=50,
                           required=True,
                           label="Name",
                           widget=TextInput())

    description = forms.CharField(max_length=2500,
                                  required=False,
                                  widget=Textarea())

    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-lg-2'
    helper.field_class = 'col-lg-10'
    helper.layout = layout.Layout(
        layout.Field('name'),
        layout.Field('geom'),
        layout.Field('description', rows='3'),
        FormActions(
            layout.Submit('save_changes', 'Save', css_class="btn-primary"),
            layout.Submit('cancel', 'Cancel', css_class="btn-danger"),
            )
        )


class AlertNewForm(forms.ModelForm):
    """Use to create a new alert
    """
    class Meta:
        model = Alert
        fields = ['name', 'description', 'domain', 'geozone', 'stat']

    name = forms.CharField(max_length=50,
                           required=True,
                           label="Name",
                           widget=TextInput())

    description = forms.CharField(max_length=2500,
                                  required=False,
                                  widget=Textarea())

    stat = forms.BooleanField(label="Compute stats",
                              required=False)

    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-lg-2'
    helper.field_class = 'col-lg-10'
    helper.layout = layout.Layout(
        layout.Field('name', css_class='input-large'),
        layout.Field('description'),
        layout.Field('domain'),
        layout.Field('geozone'),
        layout.Field('stat'),
        FormActions(
            layout.Submit('save_changes', 'Save', css_class="btn-primary"),
            layout.Submit('cancel', 'Cancel', css_class="btn-danger"),
            )
        )


class ReportNewForm(forms.ModelForm):
    """Use to create a new report
    """
    class Meta:
        model = Report
        fields = ['status', 'comment']

    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-lg-2'
    helper.field_class = 'col-lg-10'
    helper.layout = layout.Layout(
        InlineRadios('status'),
        layout.Field('comment', rows="3"),
        FormActions(
            layout.Submit('save_changes', 'Save', css_class="btn-primary"),
            )
        )
