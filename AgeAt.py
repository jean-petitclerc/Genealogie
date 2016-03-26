import datetime

date_naissance = datetime.date.today()
date_deces = datetime.date.today()


def is_bissextile(year):
    """
    Une année bissextile:
    si l'annéee est divisible par 400
    si l'année est divisible par 1 mais non divisible par 100
    :param year: A year (integer)
    :return: True if year is bissextile or False otherwise
    """
    if year % 400 == 0:
        return True
    else:
        if year % 4 == 0:
            if year % 100 == 0:
                return False
            else:
                return True
        else:
            return False


def calc_age(naissance, fait):
    nbr_ans = 0
    nbr_mois = 0
    nbr_jours = 0
    try:
        workdate = datetime.date(naissance.year, naissance.month, naissance.day)

        while workdate.replace(year=workdate.year + 1) <= fait:
            nbr_ans += 1
            workdate = workdate.replace(year=workdate.year + 1)

        while workdate < fait:
            if workdate.month < 12:
                if workdate.replace(month=workdate.month + 1) <= fait:
                    nbr_mois += 1
                    workdate = workdate.replace(month=workdate.month + 1)
                else:
                    break
            else:
                if workdate.replace(year=workdate.year + 1, month=1) <= fait:
                    nbr_mois += 1
                    workdate = workdate.replace(year=workdate.year + 1, month=1)
                else:
                    break

        while workdate < fait:
            if workdate.month in [1, 3, 5, 7, 8, 10, 12]:  # Months with 31 days
                if workdate.day < 31:
                    if workdate.replace(day=workdate.day + 1) <= fait:
                        nbr_jours += 1
                        workdate = workdate.replace(day=workdate.day + 1)
                    else:
                        continue
                else:  # day 31
                    nbr_jours += 1
                    if workdate.month < 12:
                        workdate = workdate.replace(month=workdate.month + 1, day=1)
                    else:
                        workdate = workdate.replace(year=workdate.year + 1, month=1, day=1)
                    continue
            elif workdate.month in [4, 6, 9, 11]:  # Months with 30 days
                if workdate.day < 30:
                    if workdate.replace(day=workdate.day + 1) <= fait:
                        nbr_jours += 1
                        workdate = workdate.replace(day=workdate.day + 1)
                    else:
                        continue
                else:  # day 31
                    nbr_jours += 1
                    workdate = workdate.replace(month=workdate.month + 1, day=1)
                    continue
            else:
                if is_bissextile(workdate.year):  # February has 29 days
                    nbr_j_en_fev = 29
                else:  # February has 28 days
                    nbr_j_en_fev = 28
                if workdate.day < nbr_j_en_fev:
                    if workdate.replace(day=workdate.day + 1) <= fait:
                        nbr_jours += 1
                        workdate = workdate.replace(day=workdate.day + 1)
                    else:
                        continue
                else:
                    nbr_jours += 1
                    workdate = workdate.replace(month=3, day=1)
                    continue
    except ValueError:
        print("WTF!")
    return nbr_ans, nbr_mois, nbr_jours


def main():
    global date_naissance
    global date_deces
    try:
        date_naissance = datetime.date(1900, 1, 27)
    except ValueError:
        print("La date de naissance n'est pas valide.")
        exit(4)

    try:
        date_deces = datetime.date(1901, 4, 15)
    except ValueError:
        print("La date de décès n'est pas valide.")
        exit(4)

    if date_deces < date_naissance:
        print("Le décès doit être après la naissance.")
        exit(4)

    (ans, mois, jours) = calc_age(date_naissance, date_deces)
    print("Nombre d'années: " + str(ans))
    print("Nombre de mois:  " + str(mois))
    print("Nombre de jours: " + str(jours))

if __name__ == '__main__':
    main()
