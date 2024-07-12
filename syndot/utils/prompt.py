VALID_PROMPT_CHOICES = {'y': True,
                        'ye': True,
                        'yes': True,
                        'n': False,
                        'no': False}


def ask_to_proceed() -> bool:
    choice = ''
    while choice not in VALID_PROMPT_CHOICES:
        choice = input("Do you want to proceed (y/N)? ").lower()
        if choice == '':
            choice = 'n'

    return VALID_PROMPT_CHOICES[choice]
