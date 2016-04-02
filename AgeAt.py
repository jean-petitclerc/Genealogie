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
        saved_day_of_month = workdate.day

        # Count number of full years
        while workdate.replace(year=workdate.year + 1) <= fait:
            nbr_ans += 1
            workdate = workdate.replace(year=workdate.year + 1)

        # Count number of months
        while workdate < fait:
            if workdate.month < 12:
                if workdate.month + 1 in [3, 5, 7, 8, 10, 12]:  # if next month has 31 days
                    if workdate.replace(month=workdate.month + 1) <= fait:
                        nbr_mois += 1
                        workdate = workdate.replace(month=workdate.month + 1, day=saved_day_of_month)
                    else:
                        break
                elif workdate.month + 1 in [4, 6, 9, 11]:  # if next month has 30 days
                    if saved_day_of_month > 30:  # Use day 30 to avoid invalid date like April 31
                        if workdate.replace(month=workdate.month + 1, day=30) <= fait:
                            nbr_mois += 1
                            workdate = workdate.replace(month=workdate.month + 1, day=30)
                        else:
                            break
                    else:  # Day 1-30 will not cause and invalid date
                        if workdate.replace(month=workdate.month + 1, day=saved_day_of_month) <= fait:
                            nbr_mois += 1
                            workdate = workdate.replace(month=workdate.month + 1, day=saved_day_of_month)
                        else:
                            break
                else:  # Next month is February, maybe a leap year
                    nbr_days_in_feb = 29 if is_bissextile(workdate.year) else 28
                    if saved_day_of_month > nbr_days_in_feb:
                        if workdate.replace(month=workdate.month + 1, day=nbr_days_in_feb) <= fait:
                            nbr_mois += 1
                            workdate = workdate.replace(month=workdate.month + 1, day=nbr_days_in_feb)
                        else:
                            break
                    else:
                        if workdate.replace(month=workdate.month + 1, day=saved_day_of_month) <= fait:
                            nbr_mois += 1
                            workdate = workdate.replace(month=workdate.month + 1, day=saved_day_of_month)
                        else:
                            break
            else:  # Next month is January, Dec and Jan have 31 days, no special hangling for the day of month
                if workdate.replace(year=workdate.year + 1, month=1) <= fait:
                    nbr_mois += 1
                    workdate = workdate.replace(year=workdate.year + 1, month=1)
                else:
                    break

        # Count number of days
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
        print("WTF, Value error ie, got an invalid date while processing.")

    return nbr_ans, nbr_mois, nbr_jours


def date_minus_ymd(deces, nbr_ans, nbr_mois, nbr_jours):
    try:
        assert nbr_ans >= 0
        assert 0 <= nbr_mois < 12
        assert 0 <= nbr_jours < 31
    except AssertionError:
        print("Invalid number of years, months or days")
        return deces

    result_date = datetime.date(deces.year, deces.month, deces.day)
    saved_day_of_month = deces.day

    # Deduct the number of full years
    if not is_bissextile(result_date.year - nbr_ans) and result_date.month == 2 and result_date.day == 29:
        result_date = result_date.replace(year=result_date.year - nbr_ans, day=28)
    else:
        result_date = result_date.replace(year=result_date.year - nbr_ans, day=saved_day_of_month)

    # Deduct the number of months. This may fall in the previous year
    if nbr_mois < result_date.month:
        result_month = result_date.month - nbr_mois
        year_to_sub = 0
    else:
        result_month = 12 - (nbr_mois - result_date.month)
        year_to_sub = 1

    if result_month in [1, 3, 5, 7, 8, 10, 12]:  # Months with 31 days
        result_date = result_date.replace(year=result_date.year - year_to_sub, month=result_month,
                                          day=saved_day_of_month)
    elif result_month in [4, 6, 9, 11]:  # Months with 30 days
        if saved_day_of_month <= 30:
            result_date = result_date.replace(year=result_date.year - year_to_sub, month=result_month,
                                              day=saved_day_of_month)
        else:
            result_date = result_date.replace(year=result_date.year - year_to_sub, month=result_month, day=30)
    else:  # Month is February
        nbr_of_days_in_feb = 29 if is_bissextile(result_date.year - year_to_sub) else 28
        if saved_day_of_month <= nbr_of_days_in_feb:
            result_date = result_date.replace(year=result_date.year - year_to_sub, month=result_month,
                                              day=saved_day_of_month)
        else:
            result_date = result_date.replace(year=result_date.year - year_to_sub, month=result_month, day=28)

    # Deduct the number of days, which could subtract a month which may subtract a year
    if nbr_jours < saved_day_of_month:
        result_date = result_date.replace(day=result_date.day - nbr_jours)
    else:
        if result_date.month == 1:
            result_date = result_date.replace(year=result_date.year - 1, month=12,
                                              day=31 - (nbr_jours - result_date.day))
        elif result_date.month - 1 in [1, 3, 5, 7, 8, 10]:  # Other months with 31 days
            result_date = result_date.replace(month=result_date.month - 1, day=31 - (nbr_jours - result_date.day))
        elif result_date.month - 1 in [4, 6, 9, 11]:  # Previous month has 30 days
            result_date = result_date.replace(month=result_date.month - 1, day=30 - (nbr_jours - result_date.day))
        else:  # Previous month is February
            nbr_of_days = 29 if is_bissextile(result_date.year) else 28
            result_date = result_date.replace(month=1, day=nbr_of_days - (nbr_jours - result_date.day))
    return result_date


def main():
    global date_naissance
    global date_deces
    try:
        date_naissance = datetime.date(1825, 12, 31)
        print("Date de naissance: " + str(date_naissance))
    except ValueError:
        print("La date de naissance n'est pas valide.")
        exit(4)

    try:
        date_deces = datetime.date(1875, 2, 15)
        print("Date de deces....: " + str(date_deces))
    except ValueError:
        print("La date de décès n'est pas valide.")
        exit(4)

    if date_deces < date_naissance:
        print("Le décès doit être après la naissance.")
        exit(4)

    (ans, mois, jours) = calc_age(date_naissance, date_deces)
    print("L'age au deces...: "  + str(ans) + " ans, " + str(mois) + " mois et " + str(jours) + " jour(s).")

    date_naissance = date_minus_ymd(date_deces, 49, 1, 15)
    print("Validation.......: " + str(date_naissance))

if __name__ == '__main__':
    main()
