
from django.db import models


class Question(models.Model):
    description = models.TextField()
    pub_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.description
    

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    description = models.TextField()
    number_of_vote = models.IntegerField(default=0)

    def __str__(self):
        return self.description