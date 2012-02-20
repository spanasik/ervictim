# coding: utf-8
from django.conf import settings
from models import *
from forms import *
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from aes import *
import datetime
import uuid

def read(request):
    template_name = "ervictim/read.html"

    if request.POST:
        form = ReadForm(request.POST)

        if form.is_valid():
            message_uuid=form.cleaned_data['key'][:32]
            message = get_object_or_404(Message, uuid=message_uuid, deleted=False)
            text = decrypt_aes(form.cleaned_data['key'][32:], message.text)
            return render_to_response('ervictim/message.html',
                                      {'text': text,},
                                      context_instance=RequestContext(request))
    else:
        form = ReadForm()

    return render_to_response(template_name,
            {'form': form,},
            context_instance=RequestContext(request))

def add(request):

    if request.POST:
        form = AddForm(request.POST)

        if form.is_valid():
            message_context = {'cdate': datetime.datetime.now(),
                               'victim_name': form.cleaned_data['victim_name'],
                               'offender_name': form.cleaned_data['offender_name'],
                               'event': form.cleaned_data['event']}
            plain_text = render_to_string('ervictim/message.txt', message_context)
            encrypted_text, key = encrypt_aes(plain_text)
            message = Message(uuid=uuid.uuid4().hex,text=encrypted_text)
            message.save()
            return render_to_response('ervictim/message_added.html',
                                      {'uuid': message.uuid,
                                       'key': key,
                                       'message': plain_text,
                                       'message_encrypted': encrypted_text},
                                      context_instance=RequestContext(request))
    else:
        form = AddForm()

    return render_to_response("ervictim/add.html",
                              {'form': form,},
                              context_instance=RequestContext(request))


def messages(request):
    messages = Message.objects.filter(deleted=False)
    return render_to_response("ervictim/messages.html",
                              {'messages': messages,},
                              context_instance=RequestContext(request))

def replace_captcha(request):
    from captcha.helpers import random_char_challenge
    from captcha.models import CaptchaStore
    challenge, response = random_char_challenge()
    store = CaptchaStore.objects.create(challenge=challenge,response=response)
    return HttpResponse(store.hashkey)

