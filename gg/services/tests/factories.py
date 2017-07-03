import factory


class ServiceFactory(factory.django.DjangoModelFactory):
    slug = factory.Sequence(lambda n: 'service-{0}'.format(n))
    name = factory.Sequence(lambda n: 'service-{0}'.format(n))

    class Meta:
        model = 'services.Service'
        django_get_or_create = ('name', )
