import dataclasses
import typing
import typing_extensions
import enum

class TxnResult(typing_extensions.Protocol):
	pass

class Command(typing_extensions.Protocol):
	pass

@dataclasses.dataclass
class CreateComputeCluster(Command):
	name: 'ComputeClusterRef'

@dataclasses.dataclass
class DeleteComputeCluster(Command):
	name: 'ComputeClusterRef'

class ComputeClusterRef(str):
	pass

@dataclasses.dataclass
class ComputeCluster(TxnResult):
	pass

@dataclasses.dataclass
class UIState(TxnResult):
	tables: typing.Dict[str, 'Table']
	schemas: typing.Dict['SchemaRef', 'Schema']
	users: typing.Dict['UserRef', 'User']
	roles: typing.Dict['RoleRef', 'Role']

@dataclasses.dataclass
class UIGetState(Command):
	pass

@dataclasses.dataclass
class AuthLoginRequest:
	account: str
	user: 'UserRef'
	password: str

@dataclasses.dataclass
class AuthLoginResponse:
	token: str

@dataclasses.dataclass
class TxnRequest:
	commands: typing.List['Command']

@dataclasses.dataclass
class TxnResponse:
	results: typing.List[typing.Optional['TxnResult']]

@dataclasses.dataclass
class QueryRequest:
	query: str

@dataclasses.dataclass
class CreateUser(Command):
	user: 'UserRef'
	password: str

@dataclasses.dataclass
class GetUser(Command):
	user: 'UserRef'

@dataclasses.dataclass
class DeleteUser(Command):
	user: 'UserRef'

@dataclasses.dataclass
class AssignUserRoles(Command):
	user: 'UserRef'
	roles: typing.List['RoleRef']

@dataclasses.dataclass
class CreateRole(Command):
	role: 'RoleRef'

@dataclasses.dataclass
class DeleteRole(Command):
	role: 'RoleRef'

@dataclasses.dataclass
class GrantSchemaPermissions(Command):
	role: 'RoleRef'
	schema: 'SchemaRef'
	permissions: 'SchemaPermissions'

@dataclasses.dataclass
class GrantGlobalSchemaPermissions(Command):
	role: 'RoleRef'
	permissions: 'SchemaPermissions'

@dataclasses.dataclass
class GrantComputeClusterPermissions(Command):
	role: 'RoleRef'
	compute_cluster: 'ComputeClusterRef'
	permissions: 'ComputeClusterPermissions'

@dataclasses.dataclass
class GrantGlobalComputeClusterPermissions(Command):
	role: 'RoleRef'
	permissions: 'ComputeClusterPermissions'

@dataclasses.dataclass
class GrantDatabasePermissions(Command):
	role: 'RoleRef'
	permissions: 'DatabasePermissions'

class DatabasePermissions(enum.IntFlag):
	MANAGE_ROLES = 1 << 0
	MANAGE_SCHEMAS = 1 << 1
	MANAGE_COMPUTE_CLUSTERS = 1 << 2

class SchemaPermissions(enum.IntFlag):
	MANAGE_ACCESS = 1 << 0
	MANAGE_TABLES = 1 << 1
	WRITE_TABLE = 1 << 2
	READ_TABLE = 1 << 3

class ComputeClusterPermissions(enum.IntFlag):
	USE = 1 << 0

class UserRef(str):
	pass

class RoleRef(str):
	pass

@dataclasses.dataclass
class User(TxnResult):
	roles: typing.Set['RoleRef']

@dataclasses.dataclass
class Role(TxnResult):
	database_permissions: 'DatabasePermissions'
	global_schema_permissions: 'SchemaPermissions'
	schema_permissions: typing.Dict['SchemaRef', 'SchemaPermissions']
	global_compute_cluster_permissions: 'ComputeClusterPermissions'
	compute_cluster_permissions: typing.Dict['ComputeClusterRef', 'ComputeClusterPermissions']

@dataclasses.dataclass
class CreateSchema(Command):
	name: 'SchemaRef'

@dataclasses.dataclass
class DeleteSchema(Command):
	name: 'SchemaRef'

class SchemaRef(str):
	pass

@dataclasses.dataclass
class Schema(TxnResult):
	tables: typing.Set[str]

@dataclasses.dataclass
class CreateTable(Command):
	table: 'TableRef'
	table_def: 'Table'

@dataclasses.dataclass
class GetTable(Command):
	table: 'TableRef'

@dataclasses.dataclass
class AlterTable(Command):
	table: 'TableRef'
	new_columns: typing.List['Column']

@dataclasses.dataclass
class DeleteTable(Command):
	table: 'TableRef'

@dataclasses.dataclass
class InsertData(Command):
	table: 'TableRef'
	data_ref: str

@dataclasses.dataclass
class TableRef:
	schema: 'SchemaRef'
	name: str

class ColumnType(str, enum.Enum):
	INT64 = 'Int64'
	STRING = 'String'
	TIMESTAMP = 'Timestamp'

@dataclasses.dataclass
class Column:
	name: str
	ty: 'ColumnType'
	nullable: bool

@dataclasses.dataclass
class Table(TxnResult):
	columns: typing.List['Column']
	sort_key: typing.Optional[str]
