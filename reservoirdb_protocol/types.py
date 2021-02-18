
import typing
import enum
from dataclasses import dataclass

from . import Command, TxnResult, TaggedCommand, TaggedTxnResult


@dataclass
class AuthLoginResponse:
	token: str


@dataclass
class AuthLoginRequest:
	account: str; user: 'UserRef'; password: str


@dataclass
class TxnRequest:
	commands: typing.List['TaggedCommand']


@dataclass
class TxnResponse:
	results: typing.List[typing.Optional['TaggedTxnResult']]


@dataclass
class QueryRequest:
	query: str


@dataclass
class CreateTable(Command):
	table: 'TableRef'; table_def: 'Table'


@dataclass
class GetTable(Command):
	table: 'TableRef'


@dataclass
class AlterTable(Command):
	table: 'TableRef'; new_columns: typing.List['Column']


@dataclass
class DeleteTable(Command):
	table: 'TableRef'


@dataclass
class InsertData(Command):
	table: 'TableRef'; data_ref: str


@dataclass
class CreateSchema(Command):
	name: 'SchemaRef'


@dataclass
class CreateUser(Command):
	user: 'UserRef'; password: str


@dataclass
class GetUser(Command):
	user: 'UserRef'


@dataclass
class AssignUserRoles(Command):
	user: 'UserRef'; roles: typing.List['RoleRef']


@dataclass
class CreateRole(Command):
	role: 'RoleRef'


@dataclass
class GrantSchemaPermissions(Command):
	role: 'RoleRef'; schema: 'SchemaRef'; permissions: 'SchemaPermissions'


@dataclass
class GrantGlobalSchemaPermissions(Command):
	role: 'RoleRef'; permissions: 'SchemaPermissions'


@dataclass
class GrantDatabasePermissions(Command):
	role: 'RoleRef'; permissions: 'DatabasePermissions'


@dataclass
class TableRef:
	schema: 'SchemaRef'; name: str


class ColumnType(str, enum.Enum):
	INT64 = 'Int64'; STRING = 'String'; TIMESTAMP = 'Timestamp'


@dataclass
class Column:
	name: str; ty: 'ColumnType'; nullable: bool


@dataclass
class Table(TxnResult):
	columns: typing.List['Column']; sort_key: typing.Optional[str]


class SchemaRef(str):
	pass


@dataclass
class Schema(TxnResult):
	tables: typing.Set[str]


class DatabasePermissions(enum.IntFlag):
	MANAGE_ROLES = 1; MANAGE_SCHEMAS = 2


class SchemaPermissions(enum.IntFlag):
	MANAGE_ACCESS = 1; MANAGE_TABLES = 2; WRITE_TABLE = 4; READ_TABLE = 8


class UserRef(str):
	pass


class RoleRef(str):
	pass


@dataclass
class User(TxnResult):
	roles: typing.Set['RoleRef']


@dataclass
class Role(TxnResult):
	database_permissions: 'DatabasePermissions'; global_schema_permissions: 'SchemaPermissions'; schema_permissions: typing.Dict['SchemaRef', 'SchemaPermissions']
