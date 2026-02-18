class ScientificMemory:
    def __init__(self):
        self.papers = []
        self.concepts = set()
        self.relations = []

    def add_paper(self, extraction):
        self.papers.append(extraction)

        for m in extraction.materials:
            self.concepts.add(m)

        for method in extraction.methods:
            self.concepts.add(method)

    def summary(self):
        return {
            "num_papers": len(self.papers),
            "concepts": list(self.concepts)
        }
