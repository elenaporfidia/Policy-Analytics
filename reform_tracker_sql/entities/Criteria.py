class Criteria:
    def __init__(self, _id: int, title: str, frs: list):
        self.id = _id
        self.title = title
        self.frs = frs

    def get_frs(self):
        return list(self)

    def get_title(self):
        return self.title

    def get_id(self):
        return self.id

    def total_frs(self):
        return len(self)

    def __repr__(self):
        return f"Criteria: {self.title}\nTotal Finding and Recommendation: {len(self)}"

    def __str__(self):
        return f"Criteria: {self.title}\nTotal Finding and Recommendation: {len(self)}"

    def __iter__(self):
        return iter(self.frs)

    def __len__(self):
        return len(self.frs)
