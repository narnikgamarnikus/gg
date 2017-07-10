import factory


class AssignmentFactory(factory.django.DjangoModelFactory):
    slug = factory.Sequence(lambda n: 'testslug-{0}'.format(n))
    type = factory.Sequence(lambda n: '{0}'.format('IN'))
    state = factory.Sequence(lambda n: '{0}'.format('NEW'))


    class Meta:
        model = 'crm.Assignment'
