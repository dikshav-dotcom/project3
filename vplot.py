import sys

# ---- Column numbers in the mapped.bed file (counting from 1) ----
SITE_COL       = 5    # e.g. chr1:91382-91550|carroll_ctcf...
FRAG_CHR_COL   = 8    # fragment chromosome
FRAG_START_COL = 9    # fragment start
FRAG_END_COL   = 10   # fragment end

# ---- Plot ranges ----
MIN_POS, MAX_POS = -500, 499   # offset from site centre: 1000 positions
MIN_LEN, MAX_LEN = 50, 400     # fragment lengths to keep

n_pos = MAX_POS - MIN_POS + 1  # 1000
n_len = MAX_LEN - MIN_LEN + 1  # 351

# Empty matrix: one row per length, one column per position
matrix = []
for i in range(n_len):
    matrix.append([0] * n_pos)

for line in sys.stdin:
    cols = line.split()
    if len(cols) < FRAG_END_COL:            # skip short lines
        continue
    try:
        # Site: "chr1:91382-91550|carroll..." -> chr1, 91382 and 91550
        site_text  = cols[SITE_COL - 1]
        location   = site_text.split("|")[0]    # "chr1:91382-91550"
        site_chr   = location.split(":")[0]     # "chr1"
        numbers    = location.split(":")[1]     # "91382-91550"
        parts      = numbers.split("-")         # ["91382", "91550"]
        site_start = int(parts[0])
        site_end   = int(parts[1])

        frag_chr   = cols[FRAG_CHR_COL - 1]
        frag_start = int(cols[FRAG_START_COL - 1])
        frag_end   = int(cols[FRAG_END_COL - 1])
    except (ValueError, IndexError):         # skip lines in the wrong format
        continue

    # Fragment must be on the same chromosome as the site
    if site_chr != frag_chr:
        continue

    site_centre = (site_start + site_end) // 2
    frag_mid    = (frag_start + frag_end) // 2

    x = frag_mid - site_centre               # offset (x-axis)
    y = frag_end - frag_start                # fragment length (y-axis)

    if MIN_POS <= x <= MAX_POS and MIN_LEN <= y <= MAX_LEN:
        matrix[y - MIN_LEN][x - MIN_POS] += 1

# Wide form: length, then the counts for -500 ... 499 (no header line)
for i in range(n_len):
    row = [str(MIN_LEN + i)]
    for count in matrix[i]:
        row.append(str(count))
    print("\t".join(row))
