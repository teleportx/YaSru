def verify_symbol(el: str) -> bool:
    return el.isnumeric() or el.isalpha() or el in [' ', '_', '-']


def verify_name(name: str):
    return all([verify_symbol(el) for el in name])
