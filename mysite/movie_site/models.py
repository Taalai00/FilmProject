from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import PositiveSmallIntegerField, ImageField
from phonenumber_field.modelfields import PhoneNumberField
from multiselectfield import MultiSelectField

STATUS_CHOICES = (
        ('pro', 'pro'),
        ('simple', 'simple')
    )

class Profile(AbstractUser):
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(18), MaxValueValidator(70)], null=True, blank=True)
    phone_number = PhoneNumberField(region='KG', null=True, blank=True)
    status = models.CharField(max_length=16,choices=STATUS_CHOICES, default='simple')

    def __str__(self):
        return f'{self.first_name} - {self.last_name}'

class Country(models.Model):
   country_name = models.CharField(max_length=32, unique=True)

   def __str__(self):
       return self.country_name

class Director(models.Model):
    director_name = models.CharField(max_length=64)
    bio = models.TextField()
    age = PositiveSmallIntegerField(validators=[MaxValueValidator(100)])
    director_image = ImageField(upload_to='director_images/')

    def __str__(self):
        return self.director_name

class Actor(models.Model):
    actor_name = models.CharField(max_length=64)
    bio = models.TextField()
    age =  PositiveSmallIntegerField(validators=[MaxValueValidator(100)])
    actor_image = ImageField(upload_to='actor_images/')

    def __str__(self):
        return self.actor_name

class Genre(models.Model):
    genre_name = models.CharField(max_length=64)

    def __str__(self):
        return self.genre_name

class Movie(models.Model):
    movie_name = models.CharField(max_length=62)
    year = models.DateField()
    country = models.ManyToManyField(Country)
    director = models.ManyToManyField(Director)
    actor = models.ManyToManyField(Actor, related_name='actor_films')
    genre = models.ManyToManyField(Genre)
    TYPES_CHOICES = (
        ('144p', '144p'),
        ('360p', '360p'),
        ('480p', '480p'),
        ('720p', '720p'),
        ('1080p', '1080p')
    )
    types = MultiSelectField(max_length=16, choices=TYPES_CHOICES, max_choices=5)
    movie_time = models.PositiveSmallIntegerField()
    description = models.TextField()
    movie_trailer = models.FileField(upload_to='movie_trailer/')
    movie_image = models.ImageField(upload_to='movie_image/')
    status_movie = models.CharField(max_length=16, choices=STATUS_CHOICES)
    def __str__(self):
        return self.movie_name

class MovieLanguages(models.Model):
    language = models.CharField(max_length=16)
    video = models.FileField(upload_to='videos/')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='videos')


class Moments(models.Model):
  movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='moments')
  movie_moments = models.ImageField(upload_to='moments')

class Rating(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    stars = models.IntegerField(choices=[(i, str(i))for i in range(1, 11)], null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.movie}'

class Favorite(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)

class FavoriteMovie(models.Model):
    cart = models.ForeignKey(Favorite, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

class History(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)
