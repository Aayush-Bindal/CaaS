import re


def check(row_num: int, hashed_cg: str):
    new_num = row_num
    new_hash = hashed_cg
    with open("data.txt", "r") as fp:
        line = fp.readline()
    extract_re = re.compile(r"(\d+):(.*)")
    matches = extract_re.match(line)

    old_num = -1
    old_hash = ""
    if matches:
        try:
            old_num = int(matches.group(1).strip())
            old_hash = matches.group(2)
        except Exception:
            old_num = -1

    if old_num == row_num:
        return False 
    else:
        if new_num == -1:
            return False
        if new_num > old_num or (new_num == old_num or old_hash != new_hash):
            update(f"{new_num}:{new_hash}")
            return True

def update(val: str):
    with open("data.txt", "w") as fp:
        fp.write(val)