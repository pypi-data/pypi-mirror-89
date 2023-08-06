from typing import List, Callable, Any, Type, Dict, Tuple

# noinspection PyPackageRequirements
from graphql import (
    GraphQLSchema,
    GraphQLObjectType,
    GraphQLField,
    GraphQLString,
    is_named_type,
    ExecutionResult,
    GraphQLType
)

from graphql_api import GraphQLError

from graphql_api.executor import GraphQLExecutor, GraphQLBaseExecutor
from graphql_api.context import GraphQLContext
from graphql_api.reduce import GraphQLSchemaReducer, GraphQLFilter
from graphql_api.mapper import GraphQLTypeMapper


class GraphQLFieldContext:

    def __init__(self, meta, query=None):
        self.meta = meta
        self.query = query

    def __str__(self):
        query_str = ""
        if self.query:
            query_str = f', query: {query_str}' if self.query else ''
        return f"<Node meta: {self.meta}{query_str}>"


class GraphQLRequestContext:

    def __init__(self, args, info):
        self.args = args
        self.info = info


def decorate(
    func: Callable,
    _type: str,
    schema: "GraphQLAPI" = None,
    meta: Dict = None
):
    func.graphql = True
    func.defined_on = func

    if not meta:
        meta = {}

    api = {
        "defined_on": func,
        "meta": meta,
        "type": _type,
        "schema": schema
    }

    if not hasattr(func, "schemas"):
        func.schemas = {}

    if hasattr(func, "schemas"):
        func.schemas[schema] = api

    return func


def decorator(a, b, _type):
    func = a if callable(a) else b if callable(b) else None
    meta = a if isinstance(a, dict) else b if isinstance(b, dict) else None
    schema = a if isinstance(a, GraphQLAPI) else \
        b if isinstance(b, GraphQLAPI) else None

    if func:
        return decorate(
            func=func,
            _type=_type,
            schema=schema,
            meta=meta
        )

    return lambda _func: decorate(
        func=_func,
        _type=_type,
        schema=schema,
        meta=meta
    )


class GraphQLAPI(GraphQLBaseExecutor):

    def field(self=None, meta=None, mutable=False):
        _type = "query"
        if mutable:
            _type = "mutation"

        return decorator(self, meta, _type=_type)

    def type(
        self=None,
        meta=None,
        abstract=False,
        interface=False,
        root=False
    ):
        _type = "object"
        if interface:
            _type = "interface"
        elif abstract:
            _type = "abstract"
        elif root:
            return self.set_root

        return decorator(self, meta, _type=_type)

    def set_root(self, root_type):
        self.root_type = root_type
        return root_type

    def __init__(
        self,
        root: Type = None,
        middleware: List[Callable[[Callable, GraphQLContext], Any]] = None,
        filters: List[GraphQLFilter] = None
    ):
        super().__init__()
        if middleware is None:
            middleware = []

        self.root_type = root
        self.middleware = middleware
        self.filters = filters
        self.query_mapper = None
        self.mutation_mapper = None

    def graphql_schema(self) -> Tuple[GraphQLSchema, Dict]:
        schema_args = {}
        meta = {}

        if self.root_type:
            # Create the root query
            query_mapper = GraphQLTypeMapper(schema=self)
            query: GraphQLType = query_mapper.map(self.root_type)

            if not isinstance(query, GraphQLObjectType):
                raise GraphQLError(
                    f"Query {query} was not a valid ObjectType."
                )

            # Filter the root query
            filtered_query = GraphQLSchemaReducer.reduce_query(
                query_mapper,
                query,
                filters=self.filters
            )

            if query_mapper.validate(filtered_query, evaluate=True):
                schema_args['query'] = filtered_query
                query_types = query_mapper.types()
                registry = query_mapper.registry

            else:
                query_types = set()
                registry = None

            # Create the root mutation
            mutation_mapper = GraphQLTypeMapper(
                as_mutable=True,
                suffix="Mutable",
                registry=registry,
                schema=self
            )
            mutation: GraphQLType = mutation_mapper.map(self.root_type)

            if not isinstance(mutation, GraphQLObjectType):
                raise GraphQLError(
                    f"Mutation {mutation} was not a valid ObjectType."
                )

            # Filter the root mutation
            filtered_mutation = GraphQLSchemaReducer.reduce_mutation(
                mutation_mapper,
                mutation
            )

            if mutation_mapper.validate(filtered_mutation, evaluate=True):
                schema_args['mutation'] = filtered_mutation
                mutation_types = mutation_mapper.types()
            else:
                mutation_types = set()

            schema_args['types'] = list(query_types | mutation_types)
            schema_args['types'] = [
                type_
                for type_ in schema_args['types'] if is_named_type(type_)
            ]

            meta = {**query_mapper.meta, **mutation_mapper.meta}

            self.query_mapper = query_mapper
            self.mutation_mapper = mutation_mapper

        # Create a placeholder query (every GraphQL schema must have a query)
        if 'query' not in schema_args:
            placeholder = GraphQLField(
                type_=GraphQLString,
                resolve=lambda *_: ''
            )
            schema_args['query'] = GraphQLObjectType(
                name='PlaceholderQuery',
                fields={'placeholder': placeholder}
            )

        schema = GraphQLSchema(**schema_args)

        return schema, meta

    def execute(
        self,
        query,
        variables=None,
        operation_name=None
    ) -> ExecutionResult:
        return self.executor().execute(
            query=query,
            variables=variables,
            operation_name=operation_name
        )

    def executor(
        self,
        root_value: Any = None,
        middleware: List[Callable[[Callable, GraphQLContext], Any]] = None,
        middleware_on_introspection: bool = False
    ) -> GraphQLExecutor:
        schema, meta = self.graphql_schema()

        if callable(self.root_type) and root_value is None:
            root_value = self.root_type()

        return GraphQLExecutor(
            schema=schema,
            meta=meta,
            root_value=root_value,
            middleware=middleware,
            middleware_on_introspection=middleware_on_introspection
        )
