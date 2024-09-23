from django.db import models


class Location(models.Model):
    cep = models.CharField(max_length=9)
    street = models.CharField(max_length=255)
    number = models.CharField(max_length=10)
    neighborhood = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.street}, {self.number} - {self.city}/{self.state}"


class Event(models.Model):
    PUBLIC = 'public'
    PRIVATE = 'private'
    PRIVACY_CHOICES = [
        (PUBLIC, 'Público'),
        (PRIVATE, 'Privado'),
    ]

    INGRESSO_PAGO = 'pago'
    INGRESSO_GRATUITO = 'gratuito'
    INGRESSO_CHOICES = [
        (INGRESSO_PAGO, 'Pago'),
        (INGRESSO_GRATUITO, 'Gratuito'),
    ]

    LIVRE = 'livre'
    MAIS_12 = '+12'
    MAIS_16 = '+16'
    MAIS_18 = '+18'
    AGE_GROUP_CHOICES = [
        (LIVRE, 'Livre'),
        (MAIS_12, '+12 Anos'),
        (MAIS_16, '+16 Anos'),
        (MAIS_18, '+18 Anos'),
    ]
    CATEGORY_CHOICES = [
        ('culture', 'Cultura'),
        ('sport', 'Esporte'),
        ('education', 'Educacional'),
        ('music', 'Música'),
        ('vaquejada', 'Vaquejada'),
        ('literature', 'Literatura'),
        ('art', 'Arte'),
        ('lecture', 'Palestra'),
        ('food', 'Comida'),
        ('leisure', 'Lazer'),
        ('festival', 'Festival'),
        ('party', 'Festa'),
        ('theater', 'Teatro'),
        ('conference', 'Conferência'),
        ('seminar', 'Seminário'),
        ('workshop', 'Workshop'),
        ('course', 'Curso'),
        ('meeting', 'Reunião'),
        ('other', 'Outro'),
    ]
    EM_ANALISE = 'em_analise'
    APROVADO = 'aprovado'
    REPROVADO = 'reprovado'
    STATUS_CHOICES = [
        (EM_ANALISE, 'Em Análise'),
        (APROVADO, 'Aprovado'),
        (REPROVADO, 'Reprovado'),
    ]

    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(max_length=1000, null=False, blank=False)
    date = models.DateTimeField()
    time = models.TimeField(null=False, blank=False)
    category = models.CharField(
        max_length=50, choices=CATEGORY_CHOICES, null=False, blank=False, default='other')
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, null=False, blank=False)
    age_group = models.CharField(
        max_length=50, choices=AGE_GROUP_CHOICES, null=False, blank=False, default=LIVRE)
    privacy = models.CharField(
        max_length=50, choices=PRIVACY_CHOICES, null=False, blank=False, default=PUBLIC)
    ticket_type = models.CharField(
        max_length=50, choices=INGRESSO_CHOICES, null=False, blank=False, default=INGRESSO_PAGO)
    tickets = models.IntegerField(null=False, blank=False, default=1)
    price = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    max_capacity = models.IntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default=EM_ANALISE
    )

    def __str__(self):
        return self.title


class EventImage(models.Model):
    event = models.ForeignKey(
        Event, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='events/images/')
