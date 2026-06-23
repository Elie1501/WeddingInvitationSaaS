# Protection contre l'injection de formules CSV (Excel / Google Sheets).
# Une valeur fournie par un invité (nom, message, régime via le RSVP public)
# commençant par = + - @ (ou tab/CR) serait interprétée comme une formule à
# l'ouverture du fichier. On la neutralise en la préfixant d'une apostrophe.

DANGEROUS_PREFIXES = ("=", "+", "-", "@", "\t", "\r")


def csv_safe(value) -> str:
    s = "" if value is None else str(value)
    if s and s[0] in DANGEROUS_PREFIXES:
        return "'" + s
    return s
