from django import template

register = template.Library()

@register.filter
def amazon_url(isbn):
    isbn_clean = isbn.replace('-', '')
    return f"https://www.amazon.co.jp/dp/{isbn13_to_isbn10(isbn_clean)}"


def isbn13_to_isbn10(isbn13):
    if not isbn13.startswith('978') or len(isbn13) != 13:
        raise ValueError("ISBN-13 must start with '978' and be 13 characters long.")
    isbn10_base = isbn13[3:-1]  # 最初の3文字を取り除き、チェックディジットを除外
    checksum = 0
    for i, char in enumerate(isbn10_base, start=1):  # ISBN-10のチェックサム計算
        checksum += i * int(char)
    checksum %= 11
    if checksum == 10:
        checksum = 'X'
    else:
        checksum = str(checksum)
    return isbn10_base + checksum

