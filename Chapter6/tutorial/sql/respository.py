from .models import Pet

class PetRepository:

    def get_by_name(self,name):
        return Pet.objects.get(name=name)
    
    def filter_by_breed(self,breed):
        return Pet.objects.filter(breed = breed)

