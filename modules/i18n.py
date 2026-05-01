__all__ = ("LOCALES", "init", "t")

import logging as log

import i18n
from i18n import t
from discord.app_commands import Translator as BaseTranslator

LOCALES_PATH = "./locales"
# map our locales to Discord locales
LOCALES = {
    "uk": ["uk"],
    "en": ["en-GB", "en-US"],
}
LOCALES_INVERTED = {k: v for v, ks in LOCALES.items() for k in ks}


def init():
    i18n.load_path.append(LOCALES_PATH)
    i18n.set("filename_format", "{locale}.{format}")
    i18n.set("skip_locale_root_data", True)
    i18n.set("on_missing_translation", handle_missing_translation)
    i18n.set("enable_memoization", True)

    i18n.add_function("p", plural_uk, "uk")
    i18n.add_function("p", plural_en, "en")

    i18n.load_everything(lock=True)


def handle_missing_translation(key, locale, **_):
    log.error(f"No translation for {key!r} ({locale})")
    return key


def plural_uk(
    singular: str, plural1: str, plural2: str, /, *, count: int, **kwargs
) -> str:
    count = abs(count)
    rem = count % 10
    if rem >= 5 or rem == 0 or 11 <= count % 100 <= 19:
        return plural2
    elif rem == 1:
        return singular
    return plural1


def plural_en(singular: str, plural: str, /, *, count: int, **kwargs) -> str:
    if abs(count) == 1:
        return singular
    else:
        return plural


class Translator(BaseTranslator):
    async def translate(self, string, locale, context):
        return t(string.message, LOCALES_INVERTED.get(locale))
