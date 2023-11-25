
from django import template
from django.utils.safestring import mark_safe
register = template.Library()

@register.filter(name='stars')
def star_ratings(value):
    """レビューの評価を星のアイコンで表示するためのフィルター。"""
    if not isinstance(value, (int, float)):
        # valueが数値でない場合は、デフォルトの評価として0を返す
        value = 0

    full_star_icon = '<i class="fas fa-star text-yellow-500"></i>'
    half_star_icon = '<i class="fas fa-star-half-alt text-yellow-500"></i>'
    empty_star_icon = '<i class="far fa-star text-yellow-500"></i>'
    
    full_stars = int(value)
    half_star = 1 if value - full_stars >= 0.5 else 0
    empty_stars = 5 - full_stars - half_star    
    
    html = full_star_icon * full_stars
    html += half_star_icon * half_star
    html += empty_star_icon * empty_stars
    
    
    return mark_safe(html)  
