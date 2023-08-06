"""Fixtures factories."""

import factory

from kalabash.admin import factories as admin_factories

from . import models


class UserCalendarFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.UserCalendar

    name = factory.Sequence(lambda n: 'User calendar %s' % n)
    mailbox = factory.SubFactory(admin_factories.MailboxFactory)


class SharedCalendarFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.SharedCalendar

    name = factory.Sequence(lambda n: 'Shared calendar %s' % n)
    domain = factory.SubFactory(admin_factories.DomainFactory)


class AccessRuleFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.AccessRule

    mailbox = factory.SubFactory(admin_factories.MailboxFactory)
    calendar = factory.SubFactory(UserCalendarFactory)
