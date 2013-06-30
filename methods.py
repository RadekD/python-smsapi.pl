"""
Methods for SMSAPI
"""

methods = {
    'points': {
        'url': 'https://ssl.smsapi.pl/user.do?',
        'params': {'credits': 1},
    },
    'send': {
        'url': 'https://ssl.smsapi.pl/sms.do?',
        'required_params': ['message'],
        'valid_params': ['eco', 'fast', '_from', 'encoding', 'flash', 'test', 'details', 'idx', 'check_idx', 'nounicode', 'normalize', 'partner_id', 'max_parts', 'expiration_date', 'notify_url', 'to', 'group']
    },
    'schedule': {
        'url': 'https://ssl.smsapi.pl/sms.do?',
        'required_params': ['to', 'message', 'date']
    },
    'delete_schedule': {
        'url': 'https://ssl.smsapi.pl/sms.do?',
        'required_params': ['sch_del']
    },
    'directory_send': {
        'url': 'https://ssl.smsapi.pl/sms.do?',
        'required_params': ['group', 'message']
    },

    'wap_push': {
        'url': 'https://ssl.smsapi.pl/sms.do?',
        'params': {'datacoding':'bin', 'udh': '0605040b8423f0'},
        'required_params': ['message'],
        'valid_params': ['url']
    },
    'vcard': {
        'url': 'https://ssl.smsapi.pl/sms.do?',
        'params': {'datacoding':'bin', 'udh': '06050423F40000'},
        'required_params': ['first_name', 'last_name', 'telephone'],
        'valid_params': ['email', 'www']
    },
    'mms': {
        'url': 'https://ssl.smsapi.pl/mms.do',
        'required_params': ['subject', 'smil'],
        'valid_params': ['to', 'group', 'idx', 'check_idx', 'notify_url']
    },
    #
    'add_user': {
        'url': 'https://ssl.smsapi.pl/user.do?',
        'required_params': ['add_user', 'pass'],
        'valid_params': ['pass_api', 'limit', 'month_limit', 'senders', 'phonebook', 'active', 'info']
    },
    'edit_user': {
        'url': 'https://ssl.smsapi.pl/user.do?',
        'required_params': ['set_user'],
        'valid_params': ['pass', 'pass_api', 'limit', 'month_limit', 'senders', 'phonebook', 'active', 'info']
    },
    'user_info': {
        'url': 'https://ssl.smsapi.pl/user.do?',
        'params': {'format': 'json'},
        'required_params': ['get_user'],
    },
    'users': {
        'url': 'https://ssl.smsapi.pl/user.do?',
        'params': {'list': 1, 'format': 'json'}
    },
    'add_sender': {
        'url': 'https://ssl.smsapi.pl/sender.do?',
        'required_params': ['add']
    },
    'check_sender_status': {
        'url': 'https://ssl.smsapi.pl/sender.do?',
        'required_params': ['status']
    },
    'delete_sender': {
        'url': 'https://ssl.smsapi.pl/sender.do?',
        'required_params': ['delete']
    },
    'senders_list': {
        'url': 'https://ssl.smsapi.pl/sender.do?',
        'params': {'list': 1},
        'valid_params': ['with_nat_names'],
    },
    'set_default_sender': {
        'url': 'https://ssl.smsapi.pl/sender.do?',
        'required_params': ['default']
    },
}