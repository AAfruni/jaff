import sys


# ****************
def parse_prizmo(line):
    srow = line.strip()

    # temperature ranges
    arow = srow.replace("[", "]").split("]")
    reaction, tlims, rate = [x.strip() for x in arow]

    tmin = tmax = ""
    if "," in tlims:
        tmin, tmax = [x.strip() for x in tlims.split(",")]

    if tmin == "":
        tmin = None
    else:
        tmin = float(tmin.replace("d", "e"))
        if tmin <= 0e0:
            tmin = None

    if tmax == "":
        tmax = None
    else:
        tmax = float(tmax.replace("d", "e"))
        if tmax >= 1e8:
            tmax = None

    reaction = reaction.replace("HE", "He")
    reaction = reaction.replace(" E", " e-")
    reaction = reaction.replace("E ", "e- ")
    reaction = reaction.replace("GRAIN0", "GRAIN")

    rate = rate.replace("user_crflux", "crate")
    rate = rate.replace("user_av", "av")

    rr, pp = reaction.split("->")
    rr = [x.strip() for x in rr.split(" + ")]
    pp = [x.strip() for x in pp.split(" + ")]

    return rr, pp, tmin, tmax, rate


# ****************
def parse_udfa(line):
    arow = line.split(":")
    rtype = arow[1]
    rr = arow[2:4]
    pp = arow[4:8]
    ka, kb, kc = [float(x) for x in arow[9:12]]
    tmin, tmax = [float(x) for x in arow[12:14]]

    if tmin <= 0e0:
        tmin = None
    if tmax >= 41000.0:
        tmax = None

    rate = None
    if rtype == "CR":
        rate = "%.2e * crate" % kc
    elif rtype == "PH":
        rate = "%.2e * exp(-%.2f * av)" % (ka, kc)
    else:
        rate = "%.2e" % ka
        if kb != 0e0:
            rate += " * (tgas / 3e2)**(%.2f)" % kb
        if kc != 0e0:
            rate += " * exp(-%.2f / tgas)" % kc

    skip_species = ["CR", "CRP", "PHOTON", "CRPHOT", ""]

    rr = [x.strip() for x in rr if x.strip() not in skip_species]
    pp = [x.strip() for x in pp if x.strip() not in skip_species]

    return rr, pp, tmin, tmax, rate


# ****************
def parse_kida(line):
    ignore = ["CR", "CRP", "Photon"]

    products_pos = 34
    a_pos = 91

    srow = line

    rr = [x for x in srow[:products_pos].split() if x != "+"]
    pp = [x for x in srow[products_pos:a_pos].split() if x != "+"]
    arow = srow[a_pos:].split()

    # Check if we have enough fields
    if len(arow) < 10:
        raise ValueError(f"Invalid KIDA format: insufficient fields in line: {line}")

    ka, kb, kc = [float(x) for x in arow[:3]]
    formula = int(arow[9])
    tmin = float(arow[7])
    tmax = float(arow[8])

    if float(tmin) <= 0e0:
        tmin = None
    if float(tmax) >= 9999.0:
        tmax = None

    rate = ""

    if formula == 1:
        rate += "%e * crate" % ka
    elif formula == 2:
        rate += "%.2e * exp(-%e*av)" % (ka, kc)
    elif formula == 3:
        rate += "%.2e" % ka
        if kb != 0e0:
            rate += " * (tgas / 3e2)**(% .2f)" % kb
        if kc != 0e0:
            rate += " * exp(-% .2f / tgas)" % kc
    elif formula == 4:
        rate += "%.2e" % (ka * kb)
        if kc != 0e0:
            rate += " * (0.62 + 0.4767 * %.2e * sqrt(3e2 / tgas))" % kc
    elif formula == 5:
        rate += "%.2e" % (ka * kb)
        if kc != 0e0:
            rate += (
                " * (1e0 + 0.0967 * %.2e * sqrt(3e2 / tgas + %e * 3e2 / 10.526 / tgas))"
                % (kc, kc**2)
            )
    else:
        # print("WARNING: KIDA formula %d not implemented, rate coefficient set to 0e0" % formula)
        rate = "0e0"

    rr = [x.strip() for x in rr if x.strip() not in ignore]
    pp = [x.strip() for x in pp if x.strip() not in ignore]

    return rr, pp, tmin, tmax, rate


# ****************
def parse_krome(line, fmt):
    line = line.replace(" ", "")

    afmt = [x.strip() for x in fmt.lower().strip().split(":")[1].split(",")]

    arow = [x.strip() for x in line.strip().split(",")]

    assert len(arow) == len(afmt), "ERROR: KROME format does not match line '%s'" % line

    tmin = tmax = None

    tminmax_reps = {
        "d": "e",
        ".le.": "",
        ".ge.": "",
        ".lt.": "",
        ".gt.": "",
        ">": "",
        "<": "",
    }

    rr = []
    pp = []
    for i, x in enumerate(afmt):
        if x == "r":
            rr.append(arow[i])
        elif x == "p":
            pp.append(arow[i])
        elif x == "tmin":
            if arow[i].strip().lower() != "none":
                tmin = arow[i].lower()
                for k, v in tminmax_reps.items():
                    tmin = tmin.replace(k, v)
                tmin = float(tmin)
        elif x == "tmax":
            if arow[i].strip().lower() != "none":
                tmax = arow[i].lower()
                for k, v in tminmax_reps.items():
                    tmax = tmax.replace(k, v)
                tmax = float(tmax)
        elif x == "rate":
            rate = arow[i].strip()
        elif x == "idx":
            pass
        else:
            print("ERROR: unknown KROME format %s in line '%s'" % (x, line))
            sys.exit(1)

    rate_reps = {"user_crflux": "crate", "user_crate": "crate", "user_av": "av"}

    for k, v in rate_reps.items():
        rate = rate.replace(k, v)

    rate = f90_convert(rate)

    if "auto" in rate:
        rate = rate.replace("auto", "PHOTO, 1e99")

    sp_reps = {"E": "e-", "e": "e-", "g": ""}

    rr = [sp_reps[x] if x in sp_reps else x for x in rr]
    pp = [sp_reps[x] if x in sp_reps else x for x in pp]

    sp_sreps = {"HE": "He"}

    for k, v in sp_sreps.items():
        rr = [x.replace(k, v) for x in rr]
        pp = [x.replace(k, v) for x in pp]

    rr = [x.strip() for x in rr if x.strip() != ""]
    pp = [x.strip() for x in pp if x.strip() != ""]

    return rr, pp, tmin, tmax, rate


# ****************
def parse_uclchem(line):
    srow = line.strip()

    print(
        "WARNING: UCLCHEM reaction format detected, but not implemented yet. Rate set to 0e0."
    )

    arow = [x.strip() for x in srow.strip().split(",")]
    # !Reactant 1,Reactant 2,Reactant 3,Product 1,Product 2,Product 3,Product 4,Alpha,Beta,Gamma,T_min,T_max,extrapolate
    rr = [x.strip() for x in arow[:3]]
    pp = [x.strip() for x in arow[3:7]]
    ka = arow[7].strip()
    kb = arow[8].strip()
    kc = arow[9].strip()
    extrapolate = arow[12].strip().lower() == "true"

    if extrapolate:
        tmin = 3e0
        tmax = 1e6
    else:
        tmin = float(arow[10])
        tmax = float(arow[11])

    if ",CRP," in srow:
        rate = "%.2e * crate" % float(ka)
    elif ",CRPHOT," in srow:
        rate = "%.2e * (tgas/3e2)**(%.2f) * crate" % (float(ka), float(kb))
    elif ",PHOTON," in srow:
        rate = "%.2e * fuv * exp(-%.2f * av)" % (float(ka), float(kc))
    elif ",FREEZE," in srow:
        rate = "(1e0 + %.2e * 1.671e-3/tgas/asize)*nuth*sigmah*sqrt(tgas/m)" % float(kb)
    else:
        rate = "0e0"

    # FIXME: this is because the parser needs to be finished
    rate = "0e0"

    def convert(sp):
        if sp.startswith("#"):
            sp = sp[1:] + "_DUST"
        if sp.startswith("@"):
            sp = sp[1:] + "_BULK"
        if sp == "E-":
            sp = "e-"

        reps = {"HE": "He", "SI": "Si", "CL": "Cl", "MG": "Mg"}

        for k, v in reps.items():
            sp = sp.replace(k, v)

        return sp

    ignore = ["CR", "CRP", "CRPHOT", "PHOTON", "NAN", ""]
    ignore += [
        "ER",
        "ERDES",
        "FREEZE",
        "H2FORM",
        "BULKSWAP",
        "DESCR",
        "DESOH2",
        "DEUVCR",
        "LH",
        "LHDES",
        "SURFSWAP",
        "THERM",
    ]

    rr = [convert(x.strip()) for x in rr if x.strip() not in ignore]
    pp = [convert(x.strip()) for x in pp if x.strip() not in ignore]

    return rr, pp, tmin, tmax, rate


# ****************
def f90_convert(line):
    import re

    # dexp -> exp
    line = line.replace("dexp(", "exp(")
    line = line.replace("(:)", "")
    # double precision exponential to standard scientific notation
    fa = re.findall(r"[0-9_.]d[0-9_+-]", line)
    # line = re.sub(r"([0-9_.]+)d([0-9_+-]+)", r"\1e\2", line)
    for a in fa:
        line = line.replace(a, a[0] + "e" + a[2])

    return line
