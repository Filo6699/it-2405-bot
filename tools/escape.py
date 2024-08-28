def escape_markdown_v2(text):
    replacements = {
        "_": "\\_",
        "*": "\\*",
        "`": "\\`",
        "[": "\\[",
        "]": "\\]",
        "(": "\\(",
        ")": "\\)",
        "~": "\\~",
        "|": "\\|",
        ">": "\\>",
    }
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    return text
