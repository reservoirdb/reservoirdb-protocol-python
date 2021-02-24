import dataclasses
import typing
import typing_extensions
import enum

TxnResult = typing.Union['ComputeCluster', 'UIState', 'User', 'Role', 'Schema', 'Table']

Command = typing.Union['CreateComputeCluster', 'DeleteComputeCluster', 'UIGetState', 'CreateUser', 'GetUser',
						'DeleteUser', 'AssignUserRoles', 'CreateRole', 'DeleteRole', 'GrantSchemaPermissions',
						'GrantGlobalSchemaPermissions', 'GrantComputeClusterPermissions',
						'GrantGlobalComputeClusterPermissions', 'GrantDatabasePermissions', 'CreateSchema',
						'DeleteSchema', 'CreateTable', 'GetTable', 'AlterTable', 'DeleteTable', 'InsertData']

@dataclasses.dataclass
class CreateComputeCluster:
	type: typing.Literal['CreateComputeCluster']
	name: 'ComputeClusterRef'

@dataclasses.dataclass
class DeleteComputeCluster:
	type: typing.Literal['DeleteComputeCluster']
	name: 'ComputeClusterRef'

class ComputeClusterRef(str):
	pass

@dataclasses.dataclass
class ComputeCluster:
	type: typing.Literal['ComputeCluster']

@dataclasses.dataclass
class UIState:
	type: typing.Literal['UIState']
	tables: typing.Dict[str, 'Table']
	schemas: typing.Dict['SchemaRef', 'Schema']
	users: typing.Dict['UserRef', 'User']
	roles: typing.Dict['RoleRef', 'Role']

@dataclasses.dataclass
class UIGetState:
	type: typing.Literal['UIGetState']

@dataclasses.dataclass
class AuthLoginRequest:
	type: typing.Literal['AuthLoginRequest']
	account: str
	user: 'UserRef'
	password: str

@dataclasses.dataclass
class AuthLoginResponse:
	type: typing.Literal['AuthLoginResponse']
	token: str

@dataclasses.dataclass
class TxnRequest:
	type: typing.Literal['TxnRequest']
	commands: typing.List['Command']

@dataclasses.dataclass
class TxnResponse:
	type: typing.Literal['TxnResponse']
	results: typing.List[typing.Optional['TxnResult']]

@dataclasses.dataclass
class QueryRequest:
	type: typing.Literal['QueryRequest']
	query: str

@dataclasses.dataclass
class CreateUser:
	type: typing.Literal['CreateUser']
	user: 'UserRef'
	password: str

@dataclasses.dataclass
class GetUser:
	type: typing.Literal['GetUser']
	user: 'UserRef'

@dataclasses.dataclass
class DeleteUser:
	type: typing.Literal['DeleteUser']
	user: 'UserRef'

@dataclasses.dataclass
class AssignUserRoles:
	type: typing.Literal['AssignUserRoles']
	user: 'UserRef'
	roles: typing.List['RoleRef']

@dataclasses.dataclass
class CreateRole:
	type: typing.Literal['CreateRole']
	role: 'RoleRef'

@dataclasses.dataclass
class DeleteRole:
	type: typing.Literal['DeleteRole']
	role: 'RoleRef'

@dataclasses.dataclass
class GrantSchemaPermissions:
	type: typing.Literal['GrantSchemaPermissions']
	role: 'RoleRef'
	schema: 'SchemaRef'
	permissions: 'SchemaPermissions'

@dataclasses.dataclass
class GrantGlobalSchemaPermissions:
	type: typing.Literal['GrantGlobalSchemaPermissions']
	role: 'RoleRef'
	permissions: 'SchemaPermissions'

@dataclasses.dataclass
class GrantComputeClusterPermissions:
	type: typing.Literal['GrantComputeClusterPermissions']
	role: 'RoleRef'
	compute_cluster: 'ComputeClusterRef'
	permissions: 'ComputeClusterPermissions'

@dataclasses.dataclass
class GrantGlobalComputeClusterPermissions:
	type: typing.Literal['GrantGlobalComputeClusterPermissions']
	role: 'RoleRef'
	permissions: 'ComputeClusterPermissions'

@dataclasses.dataclass
class GrantDatabasePermissions:
	type: typing.Literal['GrantDatabasePermissions']
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
class User:
	type: typing.Literal['User']
	roles: typing.Set['RoleRef']

@dataclasses.dataclass
class Role:
	type: typing.Literal['Role']
	database_permissions: 'DatabasePermissions'
	global_schema_permissions: 'SchemaPermissions'
	schema_permissions: typing.Dict['SchemaRef', 'SchemaPermissions']
	global_compute_cluster_permissions: 'ComputeClusterPermissions'
	compute_cluster_permissions: typing.Dict['ComputeClusterRef', 'ComputeClusterPermissions']

@dataclasses.dataclass
class CreateSchema:
	type: typing.Literal['CreateSchema']
	name: 'SchemaRef'

@dataclasses.dataclass
class DeleteSchema:
	type: typing.Literal['DeleteSchema']
	name: 'SchemaRef'

class SchemaRef(str):
	pass

@dataclasses.dataclass
class Schema:
	type: typing.Literal['Schema']
	tables: typing.Set[str]

@dataclasses.dataclass
class CreateTable:
	type: typing.Literal['CreateTable']
	table: 'TableRef'
	table_def: 'Table'

@dataclasses.dataclass
class GetTable:
	type: typing.Literal['GetTable']
	table: 'TableRef'

@dataclasses.dataclass
class AlterTable:
	type: typing.Literal['AlterTable']
	table: 'TableRef'
	new_columns: typing.List['Column']

@dataclasses.dataclass
class DeleteTable:
	type: typing.Literal['DeleteTable']
	table: 'TableRef'

@dataclasses.dataclass
class InsertData:
	type: typing.Literal['InsertData']
	table: 'TableRef'
	data_ref: str

@dataclasses.dataclass
class TableRef:
	type: typing.Literal['TableRef']
	schema: 'SchemaRef'
	name: str

class ColumnType(str, enum.Enum):
	INT64 = 'Int64'
	STRING = 'String'
	TIMESTAMP = 'Timestamp'

@dataclasses.dataclass
class Column:
	type: typing.Literal['Column']
	name: str
	ty: 'ColumnType'
	nullable: bool

@dataclasses.dataclass
class Table:
	type: typing.Literal['Table']
	columns: typing.List['Column']
	sort_key: typing.Optional[str]
