class GPU:
    def __init__(self, name="", model="", sku="", price="", available=False, dict=None, **kwargs):
        self.name = name
        self.model = model
        self.sku = sku
        self.price = price
        self.available = available
        if dict != None:    
            self.name = dict["Name"]
            self.model = dict["Model"]
            self.sku = dict["Sku"]
            self.price = dict["Price"]
            self.available = dict["Available"]

    def getStringCSV(self):
        return f"{self.name},{self.model},{self.sku},{self.price},{self.available}"

    @staticmethod
    def getHeaderCSV():
        return "Name,Model,SKU,Price,Available"