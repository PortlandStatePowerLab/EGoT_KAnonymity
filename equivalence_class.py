class EquivalenceClass:
    # set that holds the records
    records = set()
    def __init__(self, attributes:list) -> None:
        # track class attributes
        self.attrs = attributes 
        pass
    def add(self,record: tuple) -> bool:
        #@TODO: check attributes here before adding
        self.records.add(record)
        pass
    def remove(self,record: tuple) -> bool:
        # try removing
        try:
            self.records.remove(record)
        except:
            return False
        return True
    def __repr__(self) -> str:
        return f"{'-'*5}Eq. Class ({self.attrs}){'-'*5}\n{self.records}"