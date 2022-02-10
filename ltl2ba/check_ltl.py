import os
import time
import subprocess

def check_bracket(ltl_str):
    n_br = 0
    for i in range(len(ltl_str)):
        if ltl_str[i] == "(":
            n_br += 1
        elif ltl_str[i] == ")":
            n_br -= 1
        if n_br < 0:
            return False
    if n_br == 0:
        return True
    else:
        return False

def next_inside(str_line):

def convert(ltl_str):
    # add space between GF, FG
    # merge verb noun, and possible comma
    # change G to []
    # change F to <>
    # change | to ||
    # change & to &&
    # change - to !
    if check_bracket(ltl_str) == False:
        return "BRACKET MISSING"

    spin_str = ltl_str.replace("GF", "G F")
    rev = {"F": "G", "G": "F"}
    need_format = True
    while need_format:
        need_format = False
        finished_mod = False
        for i in range(1, len(spin_str)):
            if finished_mod:
                break
            if spin_str[i] == "G" or spin_str[i] == "F":
                for j in range(i-1, -1, -1):
                    if spin_str[j] == rev[spin_str[i]]:
                        # TODO need_format = True
                        # s[..., j] = "...F"
                        # s[j+1, i] = "   G"
                        # s[i+1, k] = "
                        n_br = 0
                        opened=False
                        for k in range(i+1, len(spin_str)):
                            if spin_str[k] == "(":
                                n_br += 1
                                opened=True
                            elif spin_str[k] == ")":
                                n_br -=1
                            if n_br == 0 and opened:
                                break
                        spin_str = spin_str[:j+1] + "(" + spin_str[j+1:k+1] + ")" + spin_str[k+1:]
                        finished_mod = True
                        break
                    elif spin_str[j] == " ":
                        continue
                    else:
                        break

    # remove the verb noun
    # whenever encounter a verb
    #   1. if no noun -> pass
    #   2. if one noun -> link them
    #   3. if two nouns with || && -> distributed
    #   4. if two nouns with , -> connect nouns and verb

    # ( F ( grab_v ( ( apple_n ) & ( orange_n ) ) ) )
    # ( F ( ( take_v ( pear_n ) ) U ( put_v ( pear_n , bucket_n ) ) ) )
    # ( F ( take_v ( ( pear_n ) | ( orange_n ) ) ) )
    need_format = True
    while need_format:
        pieces = spin_str.split(" ")
        for pi, piece in enumerate(pieces):
            if is_v(piece):
                # single verb
                if pieces[pi + 1] != "(":
                    pieces[pi] = link(piece)
                else:
                    # logical words
                    if pieces[pi + 2] != "(": # open the bracket for nouns
                        if pieces[pi + 3] == ")":  # 1-(  2-single word  3-)
                            pieces[pi] = link(piece, pieces[pi+2])
                            del pieces[pi + 1:pi + 4]
                            break
                        else: # multiple words with comma or sth
                            assert pieces[pi + 5] == ")" # now assume at most 2 words with comma
                            # 1-( 2-word 3-comma 4-word 5-)
                            pieces[pi] = link(piece, pieces[pi+2], pieces[pi+4])
                            del pieces[pi + 1:pi + 6]
                            break
                    else: # pieces[pi + 2] == "(":  # multiple words with logics:
                        # (( a ) | (b) | (c) )  n words, n + n -1 + 2 * n + 2 = 4n+1
                        # (a | b | c )  n words, n + n - 1 + 2 = 2n+1
                        # find the next )
                        assert pieces[pi + 2] == "("
                        n_br = 0
                        opened = False
                        n_noun = 0
                        for k in range(len(pieces) - pi - 1):
                            if pieces[pi + k] == "(":
                                n_br += 1
                                opened = True
                            elif pieces[pi + k] == ")":
                                n_br -= 1
                            elif is_n(pieces[pi+k]):
                                n_noun+=1
                            # TODO handle & or | (what if more complicated?)
                            if opened and n_br == 0:
                                break



    spin_str = spin_str.replace("G", "[]")
    spin_str = spin_str.replace("F", "<>")
    spin_str = spin_str.replace("|", "||")
    spin_str = spin_str.replace("&", "&&")
    spin_str = spin_str.replace("-", "!")

    return spin_str

def is_v(s):
    return s[-2:] == "_v"

def is_n(s):
    return s[-2:] == "_n"

def link(v, n):
    return v[:-2] + "_" + n[:-2]

def link(v, n1, n2):
    return v[:-2] + "_" + n1[:-2] + "_" + n2[:-2]

def link(v):
    return v[:-2]

with open("ltl.txt") as f:
    lines = f.readlines()

n_total = len(lines)
n_valid = 0
n_real = 0

for li, line in enumerate(lines):
    spin_ltl = convert(line)
    cmd_line = ["gltl2ba -f \"([] p0) U (<> p1)\" -t"]
    # cmd_line = ["gltl2ba -f \"([] G p0) U (<> p1)\" -t"]
    # cmd_line = ["gltl2ba -f \"(p0) && (p0)\" -t"]

    # cmd_line = "gltl2ba -f \"%s\" -t" % (spin_ltl)

    print(li, line, spin_ltl)
    continue

    result = subprocess.run(cmd_line, shell=True, capture_output=True, text=True)

    print("stdout")
    print(result.stdout)
    print("stderr")
    print(result.stderr)

    if len(result.stdout) > 0:
        n_valid += 1
        if "accept" in result.stdout:
            n_real += 1

print("%04d total   %04d valid (%.2f%%)   %04d real (%.2f%%)" % (n_total, n_valid, n_valid / n_total * 100, n_real, n_real / n_total * 100))