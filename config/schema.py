import graphene
from graphene_django import DjangoObjectType
from tasks.models import Category, Task


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category


class TaskType(DjangoObjectType):
    class Meta:
        model = Task


class CreateCategoryMutation(graphene.Mutation):
    category = graphene.Field(CategoryType)

    class Arguments:
        name = graphene.String()

    def mutate(self, info, name):
        category = Category(name=name)
        category.save()
        return CreateCategoryMutation(category=category)


class CreateTaskMutation(graphene.Mutation):
    task = graphene.Field(TaskType)

    class Arguments:
        title = graphene.String()
        description = graphene.String()
        categoryId = graphene.ID()

    def mutate(self, info, title, description, categoryId):
        category = Category.objects.get(id=categoryId)
        task = Task(title=title, description=description, category=category)
        task.save()
        return CreateTaskMutation(task=task)


class Mutation(graphene.ObjectType):
    create_category = CreateCategoryMutation.Field()
    create_task = CreateTaskMutation.Field()


class Query(graphene.ObjectType):
    categories = graphene.List(CategoryType)
    tasks = graphene.List(TaskType)

    def resolve_categories(self, info):
        return Category.objects.all()

    def resolve_tasks(self, info):
        return Task.objects.all()


schema = graphene.Schema(query=Query, mutation=Mutation)
