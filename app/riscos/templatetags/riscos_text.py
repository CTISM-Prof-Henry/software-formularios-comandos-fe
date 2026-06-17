from django import template

register = template.Library()


@register.filter
def limite_palavras(valor, total=3):
    palavras = str(valor or "").split()
    try:
        total = int(total)
    except (TypeError, ValueError):
        total = 3

    if len(palavras) <= total:
        return " ".join(palavras)
    return f"{' '.join(palavras[:total])}..."
