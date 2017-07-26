import factory
from django.conf import settings
from gg.users.test.factories import UserFactory

class ServiceUserFactory(factory.django.DjangoModelFactory):
	user = factory.SubFactory(UserFactory)
	balance = 50

	class Meta:
		model = 'services.ServiceUser'

class ServiceFactory(factory.django.DjangoModelFactory):
	slug = factory.Sequence(lambda n: 'test-service-{0}'.format(n))
	name = factory.Sequence(lambda n: 'test-service-{0}'.format(n))
	title = factory.Sequence(lambda n: 'test-service-{0}'.format(n))
	description = factory.Sequence(lambda n: 'test-service-{0}'.format(n))

	class Meta:
		model = 'services.Service'


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
