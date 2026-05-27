import json
from pathlib import Path
from django import template
from django.utils.safestring import mark_safe
from django.conf import settings

register = template.Library()

_translations = {}
_current_lang = None

def _load_translations(lang):
    global _translations, _current_lang
    if lang != _current_lang or lang not in _translations:
        path = Path(settings.BASE_DIR) / 'locale' / f'{lang}.json'
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                _translations[lang] = json.load(f)
        else:
            _translations[lang] = {}
        _current_lang = lang
    return _translations[lang]

@register.simple_tag(takes_context=True)
def t(context, text):
    lang = context.request.session.get('django_language', settings.LANGUAGE_CODE)
    translations = _load_translations(lang)
    return mark_safe(translations.get(text, text))

@register.simple_tag(takes_context=True)
def lang_code(context):
    return context.request.session.get('django_language', settings.LANGUAGE_CODE)

@register.simple_tag(takes_context=True)
def lang_name(context):
    lang = context.request.session.get('django_language', settings.LANGUAGE_CODE)
    names = {'en': 'English', 'id': 'Indonesia', 'zh-hans': '简体中文'}
    return names.get(lang, 'English')
