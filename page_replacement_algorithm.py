
class page_replacement_algorithm :
    def __init__(self, params):
        self.learning_rate = None
        
    def __contains__(self, page):
        raise('Need to implement this method')
        
    def request(self,page) :
        raise('Need to implement this method')
        pass
    
    def page_color(self, p ) :
        raise('Need to implement this method')
        return 0 ## color white
    
    def get_list_labels(self) :
        raise('Need to implement this method')
        return []
    
    def get_data(self):
        raise('Need to implement this method')
        return []
    def page_label(self,page):
        raise('Need to implement this method')
        return str(page)
    
    def get_N(self) :
        raise('Need to implement this method')
    
    def getStats(self):
        raise('Need to implement this method')
        return None

    def visualize(self, plt):
        raise('Need to implement this method')
        pass
    
    def getWeights(self):
        raise('Need to implement this method')
        return None
    