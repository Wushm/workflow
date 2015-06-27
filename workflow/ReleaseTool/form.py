# -*- coding: UTF-8 -*-
from django import forms
from django.forms import ModelForm, Textarea,Select

version_number1_choices=(
    ('','-'),
    ('1','1'),
    ('2','2'),
    ('3','3'),
    ('4','4'),
    ('5','5'),
    )
version_number2_choices=(
    ('','-'),
    ('1','1'),
    ('2','2'),
    ('3','3'),
    ('4','4'),
    ('5','5'),
    )

version_number3_choices=(
    ('','-'),
    ('1','1'),
    ('2','2'),
    ('3','3'),
    ('4','4'),
    ('5','5'),
    ('6','6'),
    ('7','7'),
    ('8','8'),
    ('9','9'),
    ('10','10'),
    ('11','11'),
    ('12','12'),
    ('13','13'),
    ('14','14'),
    ('15','15'),
    )

version_number4_choices=(
    ('','-'),
    ('1','1'),
    ('2','2'),
    ('3','3'),
    ('4','4'),
    ('5','5'),
    ('6','6'),
    ('7','7'),
    ('8','8'),
    ('9','9'),
    ('10','10'),
    ('11','11'),
    ('12','12'),
    ('13','13'),
    ('14','14'),
    ('15','15'),
    ('16','16'),
    ('17','17'),
    ('18','18'),
    ('19','19'),
    ('20','20'),
    ('21','21'),
    ('22','22'),
    ('23','23'),
    ('24','24'),
    ('25','25'),
    ('26','26'),
    ('27','27'),
    ('28','28'),
    ('29','29'),
    )

version_number5_choices=(
    ('','-'),
    ('_sp1','_sp1'),
    ('_sp2','_sp2'),
    ('_sp3','_sp3'),
    ('_sp4','_sp4'),
    ('_sp5','_sp5'),
    ('_sp6','_sp6'),
    ('_sp7','_sp7'),
    ('_sp8','_sp8'),
    ('_sp9','_sp9'),
    ('_sp10','_sp10'),
    ('_sp11','_sp11'),
    ('_sp12','_sp12'),
    ('_sp13','_sp13'),
    ('_sp14','_sp14'),
    ('_sp15','_sp15'),
    )

class CReleasToolForm(forms.Form):
    version_number1 = forms.ChoiceField(widget=forms.widgets.Select(attrs={}),\
            choices=version_number1_choices)
    version_number2 = forms.ChoiceField(widget=forms.widgets.Select(attrs={}),\
            choices=version_number2_choices)
    version_number3 = forms.ChoiceField(widget=forms.widgets.Select(attrs={}),\
            choices=version_number3_choices)
    version_number4 = forms.ChoiceField(widget=forms.widgets.Select(attrs={}),\
            choices=version_number4_choices)
    version_number5 = forms.ChoiceField(widget=forms.widgets.Select(attrs={}),\
            choices=version_number5_choices)
        