def  START():
    if lookahead == "(if)" or lookahead == "(func)" or lookahead == "(loop)":
        STATMENT()
    elif lookahead == "(id,\\d+)":
        ASSIGN()
    else:
        print("Syntax Error")
        exit()

def STATMENT():
    if lookahead == "(if)":
        S_match("(if)")
        S_match("({)")
        COMPARE()
        S_match("(})")
        S_match("(<)")
        CODE()
        S_match("(>)")
        CONDITIONS()
        START()
    elif lookahead == "(func)":
        S_match("(func)")
        S_match("(id,\\d+)")
        S_match("({)")
        PARAM()
        S_match("(})")
        S_match("(<)")
        CODE()
        S_match("(>)")
        START()
    elif lookahead == "(loop)":
        S_match("(loop)")
        S_match("({)")
        COMPARE()
        S_match("(})")
        S_match("(<)")
        CODE()
        S_match("(>)")
        START()
    else:
        print("Syntax Error")
        exit()

def S_match(expected_token):
    global lookahead, tokens, index
    
    # Check if it's a pattern (contains \d) or exact match
    if "\\d" in expected_token:
        # Simple pattern checking without regex
        if expected_token == "(id,\\d+)":
            # Check if token starts with "(id," and ends with ")" and has digits in between
            if lookahead.startswith("(id,") and lookahead.endswith(")") and lookahead[4:-1].isdigit():
                index += 1
                if index < len(tokens):
                    lookahead = tokens[index]
                return
        elif expected_token == "(num,\\d+)":
            if lookahead.startswith("(num,") and lookahead.endswith(")") and lookahead[5:-1].isdigit():
                index += 1
                if index < len(tokens):
                    lookahead = tokens[index]
                return
        elif expected_token == "(id,//d+)":  # Your typo
            if lookahead.startswith("(id,") and lookahead.endswith(")") and lookahead[4:-1].isdigit():
                index += 1
                if index < len(tokens):
                    lookahead = tokens[index]
                return
    else:
        # Exact string match
        if lookahead == expected_token:
            index += 1
            if index < len(tokens):
                lookahead = tokens[index]
            return
    
    print("Syntax Error")
    exit()

def COMPARE():
    if lookahead == "(id,\\d+)" or lookahead == "(num,\\d+)":
        AND_EXPR()
        COMPARE_TAIL()
    else:
        print("Syntax Error")
        exit()

def COMPARE_TAIL():
    if lookahead == "(|)":
        S_match("(|)")
        AND_EXPR()
        COMPARE_TAIL()
    else:
        return

def AND_EXPR():
    if lookahead == "(id,\\d+)" or lookahead == "(num,\\d+)":
        UNIT_COMP()
        UNIT_TAIL()
    else:
        print("Syntax Error")
        exit()

def UNIT_TAIL():
    if lookahead == "(&)":
        S_match("(&)")
        UNIT_COMP()
        UNIT_TAIL()
    else:
        return

def UNIT_COMP():
    if lookahead == "(id,\\d+)" or lookahead == "(num,\\d+)":
        VARIABLE()
        COMPARATOR()
        VARIABLE()
    else:
        print("Syntax Error")
        exit()

def COMPARATOR():
    if lookahead == "(<<)":
        S_match("(<<)")
    elif lookahead == "(>>)":
        S_match("(>>)")
    elif lookahead == "(?=)":
        S_match("?=")
    else:
        print("Syntax Error")
        exit()

def CODE():
    if lookahead == "(id,\\d+)":
        S_match("(id,\\d+)")
        ASSIGN()
    elif lookahead == "(ayo)":
        S_match("(ayo)")
        S_match("(id,\\d+)")
        S_match("({)")
        PARAM()
        S_match("(})")
    elif lookahead == "(sendback)":
        S_match("(sendback)")
        S_match("(id,\\d+)")
    elif lookahead == "(if)" or lookahead == "(func)" or lookahead == "(loop)":
        STATMENT()
    else:
        print("Syntax Error")
        exit()

def CONDITIONS():
    if lookahead == "(elif)":
        S_match("(elif)")
        S_match("({)")
        COMPARE()
        S_match("(})")
        S_match("(<)")
        CODE()
        S_match("(>)")
        CONDITIONS()
    elif lookahead == "(else)":
        S_match("(else)")
        S_match("(<)")
        CODE()
        S_match("(>)")
    else:
        return

def ASSIGN():
    if lookahead == ("(<--)"):
        S_match("(<--)")
        ASSIGN_TAIL()
    elif lookahead == "({)":
        S_match("({)")
        PARAM()
        S_match("(})")
        START()

def ASSIGN_TAIL():
    if lookahead == "(id,\\d+)" or lookahead == "(num,\\d+)":
        VARIABLE()
        OPERATION()
        START()
    elif lookahead == "(ayo)":
        S_match("(ayo)")
        S_match("(id,\\d+)")
        S_match("({)")
        PARAM()
        S_match("(})")
    else:
        print("Syntax Error")
        exit()

def VARIABLE():
    if lookahead == "(id,\\d+)":
        S_match("(id,\\d+)")
    elif lookahead == "(num,\\d+)":
        S_match("(num,\\d+)")
    else:
        print("Syntax Error")
        exit()

def OPERATION():
    if lookahead == "(+)":
        S_match("(+)")
        VARIABLE()
    elif lookahead == "(-)":
        S_match("(-)")
        VARIABLE()
    elif lookahead == "(*)":
        S_match("(*)")
        VARIABLE()
    elif lookahead == "(/)":
        S_match("(/)")
        VARIABLE()
    else:
        return

def PARAM():
    if lookahead == "(id,\\d+)" or lookahead == "(num,\\d+)":
        VARIABLE()
        PARAM()
    elif lookahead == "(,)":
        S_match("(,)")
        VARIABLE()
        PARAM()
    else:
        return


if __name__ == "__main__":
    with open ("./Lexical Analysis/result.txt", "r") as f:
        tokens = f.read()
    tokens = tokens.replace("\n", "")
    tokens = tokens.split(" ")
    if "(error)" in tokens:
        print("Lexical Error")
        exit()
    else:
        index = 0
        lookahead = tokens[index]
        START()
        if index == len(tokens):
            print("Syntax Correct")
        else:
            print("Syntax Error")