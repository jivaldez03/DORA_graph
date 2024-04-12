
class record_class:
    category: str
    domain: str
    article_heading: str
    section_heading : str
    chapter : str
    section : str
    article : int
    paragraph : int
    point: str
    sub_point : int
    related_to: list
    responsible: str
    stipulation: str
    full_text : str

class DataRecord:
    @classmethod
    def from_row(cls, row):
        instance = cls()
        for key, value in row.items():
            setattr(instance, key.lower(), value)
        return instance