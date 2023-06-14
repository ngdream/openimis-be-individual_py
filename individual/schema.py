import graphene
from django.contrib.auth.models import AnonymousUser
from django.db.models import Q

from core.schema import OrderedDjangoFilterConnectionField
from core.utils import append_validity_filter
from individual.apps import IndividualConfig
from individual.gql_mutations import CreateIndividualMutation, UpdateIndividualMutation, DeleteIndividualMutation, \
    CreateGroupMutation, UpdateGroupMutation, DeleteGroupMutation, CreateGroupIndividualMutation, \
    UpdateGroupIndividualMutation, DeleteGroupIndividualMutation, \
    CreateGroupIndividualsMutation
from individual.gql_queries import IndividualGQLType, IndividualDataSourceGQLType, GroupGQLType, GroupIndividualGQLType
from individual.models import Individual, IndividualDataSource, Group, GroupIndividual
import graphene_django_optimizer as gql_optimizer


class Query:
    individual = OrderedDjangoFilterConnectionField(
        IndividualGQLType,
        orderBy=graphene.List(of_type=graphene.String),
        applyDefaultValidityFilter=graphene.Boolean(),
        client_mutation_id=graphene.String()
    )

    individual_data_source = OrderedDjangoFilterConnectionField(
        IndividualDataSourceGQLType,
        orderBy=graphene.List(of_type=graphene.String),
        applyDefaultValidityFilter=graphene.Boolean(),
        client_mutation_id=graphene.String()
    )

    group = OrderedDjangoFilterConnectionField(
        GroupGQLType,
        orderBy=graphene.List(of_type=graphene.String),
        dateValidFrom__Gte=graphene.DateTime(),
        dateValidTo__Lte=graphene.DateTime(),
        applyDefaultValidityFilter=graphene.Boolean(),
        client_mutation_id=graphene.String(),
        first_name=graphene.String(),
        last_name=graphene.String(),
        search_id=graphene.String()
    )

    group_individual = OrderedDjangoFilterConnectionField(
        GroupIndividualGQLType,
        orderBy=graphene.List(of_type=graphene.String),
        dateValidFrom__Gte=graphene.DateTime(),
        dateValidTo__Lte=graphene.DateTime(),
        applyDefaultValidityFilter=graphene.Boolean(),
        client_mutation_id=graphene.String()
    )

    def resolve_individual(self, info, **kwargs):
        filters = append_validity_filter(**kwargs)

        client_mutation_id = kwargs.get("client_mutation_id")
        if client_mutation_id:
            filters.append(Q(mutations__mutation__client_mutation_id=client_mutation_id))

        Query._check_permissions(info.context.user,
                                 IndividualConfig.gql_individual_search_perms)
        query = Individual.objects.filter(*filters)
        return gql_optimizer.query(query, info)

    def resolve_individual_data_source(self, info, **kwargs):
        filters = append_validity_filter(**kwargs)

        client_mutation_id = kwargs.get("client_mutation_id")
        if client_mutation_id:
            filters.append(Q(mutations__mutation__client_mutation_id=client_mutation_id))

        Query._check_permissions(info.context.user,
                                 IndividualConfig.gql_individual_search_perms)
        query = IndividualDataSource.objects.filter(*filters)
        return gql_optimizer.query(query, info)

    def resolve_group(self, info, **kwargs):
        Query._check_permissions(
            info.context.user,
            IndividualConfig.gql_group_search_perms
        )
        filters = append_validity_filter(**kwargs)
        client_mutation_id = kwargs.get("client_mutation_id", None)
        if client_mutation_id:
            filters.append(Q(mutations__mutation__client_mutation_id=client_mutation_id))

        first_name = kwargs.get("first_name", None)
        if first_name:
            filters.append(Q(groupindividual__individual__first_name__icontains=first_name))

        last_name = kwargs.get("last_name", None)
        if last_name:
            filters.append(Q(groupindividual__individual__last_name__icontains=last_name))

        search_id = kwargs.get("search_id", None)
        if search_id:
            filters.append(Q(id__icontains=search_id))

        query = Group.objects.filter(*filters)
        return gql_optimizer.query(query, info)

    def resolve_group_individual(self, info, **kwargs):
        Query._check_permissions(
            info.context.user,
            IndividualConfig.gql_group_search_perms
        )
        filters = append_validity_filter(**kwargs)
        client_mutation_id = kwargs.get("client_mutation_id", None)
        if client_mutation_id:
            filters.append(Q(mutations__mutation__client_mutation_id=client_mutation_id))

        query = GroupIndividual.objects.filter(*filters)
        return gql_optimizer.query(query, info)

    @staticmethod
    def _check_permissions(user, perms):
        if type(user) is AnonymousUser or not user.id or not user.has_perms(perms):
            raise PermissionError("Unauthorized")


class Mutation(graphene.ObjectType):
    create_individual = CreateIndividualMutation.Field()
    update_individual = UpdateIndividualMutation.Field()
    delete_individual = DeleteIndividualMutation.Field()

    create_group = CreateGroupMutation.Field()
    update_group = UpdateGroupMutation.Field()
    delete_group = DeleteGroupMutation.Field()

    add_individual_to_group = CreateGroupIndividualMutation.Field()
    edit_individual_in_group = UpdateGroupIndividualMutation.Field()
    remove_individual_from_group = DeleteGroupIndividualMutation.Field()

    create_group_individuals = CreateGroupIndividualsMutation.Field()
