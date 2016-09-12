# -*- coding: utf-8 -*-

from django import forms
import os

class StreamForm(forms.Form):
    StreamName = forms.FileField(label='Select a file')
    StreamType = forms.CharField()
    EncodedStreamType = forms.CharField(required=False,initial='Not Set')
    RawStreamType = forms.CharField(required=False,initial='Not Set')
    Resolution = forms.CharField(required=False,initial='Not Set')
    Frames = forms.CharField(required=False,initial='Not Set')
    ScanType = forms.CharField(required=False,initial='Not Set')
    Complexity = forms.CharField(required=False,initial='Not Set')
    FrameCount = forms.CharField(required=False,initial='Not Set')
    Conformance = forms.CharField(required=False,initial='Not Set')
    ContainerFormat = forms.CharField(required=False,initial='Not Set')
    Source = forms.CharField(required=False,initial='Not Set')