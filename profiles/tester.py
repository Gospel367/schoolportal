from django.db import models

class Studentdata(models.Model):
    student = models.CharField(max_length=200)

class Exam(models.Model):
    student =models.ForeignKey(Studentdata, on_delete=models.CASCADE)
    scores = models.IntegerField()
    slug =models.SlugField(max_length=100)
    
    def __str__(self):
        return self.student.firstname

    def save(self,  *args,  **kwargs):
        self.slug = slugify(self.student)
        super(Exam,  self).save(*args,  **kwargs)
   
print (Exam.student.map_set.all())    
