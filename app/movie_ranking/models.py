from django.db import models

class Movie(models.Model):
    title = models.CharField("Title", max_length=255, unique=True)
    critics_consensus = models.TextField("Consensus", blank=True)
    release_date = models.CharField('Release_date', max_length=255, blank=True)
    last_modified = models.DateTimeField('Last_modified', auto_now=True, blank=True, null=True)
    duration = models.CharField("Duration", max_length=255, blank=True)
    genre = models.CharField("Genre", max_length=255, blank=True)
    rating = models.DecimalField("Rating", max_digits=3, decimal_places=2, blank=True)
    images = models.ImageField("Images", blank=True)
    amount_reviews = models.CharField("Amount_reviews", max_length=255, blank=True)
    approval_percentage = models.PositiveIntegerField("Porcentae", blank=True, null=True)

    def __str__(self):
        return self.title

class MovieImage(models.Model):
    movie = models.ForeignKey(Movie, default=None, on_delete=models.CASCADE)
    images = models.ImageField(upload_to="./")

    def __str__(self):
        return self.movie.title


class PttMovie(models.Model):
    author = models.CharField("Author", max_length=255, blank=True)
    contenttext = models.TextField("Contenttext", blank=True)
    date = models.CharField("Date", max_length=255, blank=True)
    title = models.CharField("Title", max_length=255, blank=True)
    key_word = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return self.title


class CountGoodAndBad(models.Model):
    good_ray = models.IntegerField("Good_ray", default=0)
    bad_ray = models.IntegerField("Bad_ray", default=0)
    movie = models.ForeignKey(Movie, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return self.movie.title
