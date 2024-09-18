class FindingRecommendation:
    def __init__(self, _id: int, finding: str, recommendation: str):
        self.id = _id
        self.finding = finding
        self.recommendation = recommendation

    def __str__(self):
        return f"Finding: {self.finding}\nRecommendation: {self.recommendation}"

    def __repr__(self):
        return f"Finding: {self.finding}\nRecommendation: {self.recommendation}"

    def get_finding(self):
        return self.finding

    def get_recommendation(self):
        return self.recommendation

    def get_id(self):
        return self.id
