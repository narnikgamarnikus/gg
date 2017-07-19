import factory
from django.conf import settings


class UserFactory(factory.django.DjangoModelFactory):
	username = factory.Sequence(lambda n: 'user-{0}'.format(n))
	email = factory.Sequence(lambda n: 'user-{0}@example.com'.format(n))
	password = factory.PostGenerationMethodCall('set_password', 'password')

	class Meta:
		model = settings.AUTH_USER_MODEL  
		django_get_or_create = ('username',)

class ServiceUserFactory(factory.django.DjangoModelFactory):
	user = factory.SubFactory(UserFactory)
	balance = 50

class ServiceFactory(factory.django.DjangoModelFactory):
	slug = factory.Sequence(lambda n: 'test-service-{0}'.format(n))
	name = factory.Sequence(lambda n: 'test-service-{0}'.format(n))
	title = factory.Sequence(lambda n: 'test-service-{0}'.format(n))
	description = factory.Sequence(lambda n: 'test-service-{0}'.format(n))

	class Meta:
		model = 'services.Service'
		django_get_or_create = ('name')


class PriceListFactory(factory.django.DjangoModelFactory):
	user = factory.SubFactory(ServiceUserFactory)
	service = factory.SubFactory(ServiceFactory)
	from_price = 15.35
	to_price = 17.45
	above_price = 57.41

	class Meta:
		model = 'services.PriceList'


class ProposalFactory(factory.django.DjangoModelFactory):
    slug = factory.Sequence(lambda n: 'testslug-{0}'.format(n))


    class Meta:
        model = 'services.Proposal'
