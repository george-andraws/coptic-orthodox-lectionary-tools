# Coptic Orthodox lectionary rules summary

- Easter is computed annually from the Gregorian year using the Alexandrian formula in the source code.
- Great Lent runs from Easter minus 55 days through the day before Easter.
- Pentecost season runs from Easter through Easter + 49 days in the API helper, with week/day selection by weekday and days-from-Easter.
- Pascha week is not hardcoded per year: date -> Easter delta determines the day.
- If a date falls in Great Lent or Pascha, that branch is chosen before Sunday/annual readings.
- Special cases like Theophany Paramoun and the 29th of the month are handled before Lent/Pentecost/annual selection.
