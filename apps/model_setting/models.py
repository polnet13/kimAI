from django.db import models


class ConfigModel(models.Model):
    outdir = models.CharField(max_length=200)
    
    
class TubeModel(models.Model):
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True, blank=True, null=True)
    
    def __str__(self):
        return f"{self.title}({self.url})"
    
    
 
    
    




    
    

    

    