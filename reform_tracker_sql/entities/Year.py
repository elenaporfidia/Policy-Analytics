import copy


class Year:
    def __init__(self, _id: int, name: str, criteria: list):
        self.id = _id
        self.name = name
        self.criteria = criteria

    def get_criteria(self):
        return list(self)

    def get_name(self):
        return self.name

    def get_id(self):
        return self.id

    def get_frs(self):
        frs = []
        criteria = self.criteria
        for _criteria in criteria:
            frs.extend(copy.deepcopy(_criteria.frs))
        return frs

    def total_criteria(self):
        return len(self.get_criteria())

    def total_frs(self):
        return len(self.get_frs())

    def __repr__(self):
        return f"Year: {self.name}\nTotal Criteria: {len(self)}"

    def __str__(self):
        return f"Year: {self.name}\nTotal Criteria: {len(self)}"

    def __iter__(self):
        return iter(self.criteria)

    def __len__(self):
        return len(self.criteria)
