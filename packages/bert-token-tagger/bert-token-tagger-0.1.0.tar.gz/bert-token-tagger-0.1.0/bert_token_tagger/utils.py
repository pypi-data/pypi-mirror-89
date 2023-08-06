import string

def get_corrected_sentence(tokens, pred_labels, task):
    corr_line = ""
    if task == "casing":
        for token, pred in zip(tokens, pred_labels[1:]):
            # skip the first label - this is just [CLS]
            if token.startswith("##"):
                corr_line += token.replace("##", "")
            elif token in string.punctuation:
                corr_line += token
            elif pred == "KEEP":
                corr_line += " " + token
            elif pred == "UPPER":
                corr_line += " " + token.upper()
            elif pred == "TITLE":
                corr_line += " " + token.title()
            else:
                corr_line += token
    elif task == "punctuation":
        for token, pred in zip(tokens, pred_labels[1:]):
            if token.startswith("##"):
                token = token.replace("##", "")
            if pred == "PERIOD":
                token += "."
            elif pred == "COMMA":
                token += ","
            elif pred == "SEMICOLON":
                token += ";"
            elif pred == "COLON":
                token += ":"
            elif pred == "QUESTION_MARK":
                token += "?"
            elif pred == "HYPHEN":
                token += "-"
            elif pred == "DASH":
                token += "—"
            corr_line += " " + token

    return corr_line.strip()

def get_tag_values(task):
    if task == "punctuation":
        return [
                "PAD",
                "NONE",
                "PERIOD",
                "COMMA",
                "SEMICOLON",
                "COLON",
                "QUESTION_MARK",
                "HYPHEN",
                "DASH",
            ] 
    elif task == "casing":
        return ["PAD", "NONE", "KEEP", "UPPER", "TITLE"]
    else:
        raise NotImplementedError
