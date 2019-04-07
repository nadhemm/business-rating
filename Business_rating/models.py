from django.db import models
from django.db.models import Model, CASCADE

from Business_rating.constants import CATEGORIES


class Business(Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=8, null=True, blank=True)
    category = models.CharField(max_length=255, choices=CATEGORIES, null=True, blank=True)
    logo = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_reviews(self):
        return [{"stars": review.stars, "comment": review.comment, "reviewer": review.reviewer} for review in
                self.review_set.all()]


class Review(Model):
    STARS = (
        ('1', 'Very bad'),
        ('2', 'Bad'),
        ('3', 'Fair'),
        ('4', 'Good'),
        ('5', 'Very good'),
    )
    stars = models.CharField(max_length=255, choices=STARS)
    comment = models.CharField(max_length=255, null=True, blank=True)
    business = models.ForeignKey(Business, on_delete=CASCADE)
    reviewer = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.id) + ' ' + str(self.business)
