import copy


class Collection:
    def __init__(self, countries: list):
        self.countries = countries

    def get_countries(self):
        return list(self)

    def get_years(self):
        years = {}
        for country in self.countries:
            for year in country.years:
                if year.id not in years:
                    years[year.id] = copy.deepcopy(year)
                else:
                    years[year.id].criteria.extend(copy.deepcopy(year.criteria))
        return list(years.values())

    def get_criteria(self):
        years = self.get_years()
        criteria = {}
        for year in years:
            for _criteria in year.criteria:
                if _criteria.id not in criteria:
                    criteria[_criteria.id] = copy.deepcopy(_criteria)
                else:
                    criteria[_criteria.id].frs.extend(copy.deepcopy(_criteria.frs))
        return list(criteria.values())

    def get_frs(self):
        frs = []
        criteria = self.get_criteria()
        for _criteria in criteria:
            frs.extend(copy.deepcopy(_criteria.frs))
        return frs

    def total_document(self):
        td = 0
        for country in self.countries:
            td += country.total_document()
        return td

    def total_countries(self):
        return len(self.countries)

    def total_years(self):
        return len(self.get_years())

    def total_criteria(self):
        return len(self.get_criteria())

    def total_frs(self):
        return len(self.get_frs())

    def __repr__(self):
        return f"Total Countries: {len(self)}"

    def __str__(self):
        return f"Total Countries: {len(self)}"

    def __iter__(self):
        return iter(self.countries)

    def __len__(self):
        return len(self.countries)
