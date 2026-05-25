from django import template

register = template.Library()

CAMBRIDGE_KNOWN_SUBJECTS = [
    'All', 'Science', 'Math', 'English',
    'Mathematics', 'Physics', 'Chemistry', 'Biology',
    'Economics', 'Accounting', 'Business', 'Computer Science',
    'Art & Design',
]


@register.filter
def is_custom_subject(value):
    return value and value not in CAMBRIDGE_KNOWN_SUBJECTS


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def mask(value):
    if not value:
        return '-'
    s = str(value)
    if len(s) <= 3:
        return s[0] + '***' if len(s) > 1 else s
    return s[0] + '***' + s[-1] if len(s) > 3 else s


@register.filter
def mask_email(value):
    if not value or value == '-':
        return '-'
    s = str(value)
    if '@' not in s:
        return mask(s)
    local, domain = s.split('@', 1)
    masked_local = local[0] + '***' + local[-1] if len(local) > 2 else local[0] + '***'
    domain_parts = domain.split('.')
    masked_domain = domain_parts[0][0] + '***.' + '.'.join(domain_parts[1:]) if len(domain_parts[0]) > 1 else domain
    return masked_local + '@' + masked_domain
