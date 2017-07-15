import factory
from gg.services.tests.factories import ServiceFactory

class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: 'user-{0}'.format(n))
    email = factory.Sequence(lambda n: 'user-{0}@example.com'.format(n))
    password = factory.PostGenerationMethodCall('set_password', 'password')

    class Meta:
        model = 'users.User'
        django_get_or_create = ('username', )


class PriceListFactory(factory.django.DjangoModelFactory):
	user = factory.SubFactory(UserFactory)
	service = factory.SubFactory(ServiceFactory)
	from_price = 15.35
	to_price = 17.45
	above_price = 57.41

	class Meta:
		model = 'users.PriceList'