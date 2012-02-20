# coding: utf-8
from django import forms
from captcha.fields import CaptchaField
import re

class AddForm(forms.Form):
    victim_name = forms.CharField()
    offender_name = forms.CharField()
    event = forms.CharField(widget=forms.Textarea(),max_length=4096)
    captcha = CaptchaField()

    def clean(self):
        event = self.cleaned_data.get("event")
        if event:
            for regex in (r""".*magnet:.*""",r""".*\.torrent.*""",r"""(http[s]?://[\S]+)"""):
                if re.search(regex, event,  re.MULTILINE|re.UNICODE):
                    self._errors["event"] = self.error_class([""])
                    break                
        return self.cleaned_data

class ReadForm(forms.Form):
    key = forms.CharField()
    captcha = CaptchaField()
