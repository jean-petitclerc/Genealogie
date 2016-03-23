import datetime

naissance = datetime.date(1834, 11, 26)
deces = datetime.date(1835, 2, 26)
workdate = datetime.date(naissance.year, naissance.month, naissance.day)

if deces < naissance:
    print("Le décès doit être après la naissance.")
    exit(0)

nbr_ans = 0
nbr_mois = 0
nbr_jours = 0

while workdate.replace(year=workdate.year + 1) <= deces:
    nbr_ans += 1
    workdate = workdate.replace(year=workdate.year + 1)

while workdate < deces:
    if workdate.month < 12:
        if workdate.replace(month=workdate.month + 1) <= deces:
            nbr_mois += 1
            workdate = workdate.replace(month=workdate.month + 1)
        else:
            break
    else:
        if workdate.replace(year=workdate.year + 1, month = 1) <= deces:
            nbr_mois += 1
            workdate = workdate.replace(year=workdate.year + 1, month = 1)
        else:
            break

print(nbr_ans)
print(nbr_mois)
print(nbr_jours)

