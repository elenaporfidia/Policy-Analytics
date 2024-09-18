import copy


class Country:
    def __init__(self, _id: int, name: str, years: list):
        self.id = _id
        self.name = name
        self.years = years

    def get_years(self):
        return list(self)

    def get_name(self):
        return self.name

    def get_id(self):
        return self.id

    def get_criteria(self):
        years = self.years
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
        return len(self.years)

    def total_years(self):
        return len(self.years)

    def total_criteria(self):
        return len(self.get_criteria())

    def total_frs(self):
        return len(self.get_frs())

    def __repr__(self):
        return f"Country: {self.name}\nTotal Years: {len(self)}"

    def __str__(self):
        return f"Country: {self.name}\nTotal Years: {len(self)}"

    def __iter__(self):
        return iter(self.years)

    def __len__(self):
        return len(self.years)
