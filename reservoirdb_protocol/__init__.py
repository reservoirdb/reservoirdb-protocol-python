import dataclasses
import typing
import enum

@dataclasses.dataclass
class CreateComputeCluster:
	name: 'ComputeClusterRef'
	type: typing.Literal['CreateComputeCluster'] = 'CreateComputeCluster'

@dataclasses.dataclass
class DeleteComputeCluster:
	name: 'ComputeClusterRef'
	type: typing.Literal['DeleteComputeCluster'] = 'DeleteComputeCluster'

class ComputeClusterRef(str):
	pass

@dataclasses.dataclass
class ComputeCluster:

	type: typing.Literal['ComputeCluster'] = 'ComputeCluster'

@dataclasses.dataclass
class UIState:
	tables: dict[str, 'Table']
	schemas: dict['SchemaRef', 'Schema']
	users: dict['UserRef', 'User']
	roles: dict['RoleRef', 'Role']
	type: typing.Literal['UIState'] = 'UIState'

@dataclasses.dataclass
class UIGetState:

	type: typing.Literal['UIGetState'] = 'UIGetState'

@dataclasses.dataclass
class AuthLoginRequest:
	account: str
	user: 'UserRef'
	password: str
	type: typing.Literal['AuthLoginRequest'] = 'AuthLoginRequest'

@dataclasses.dataclass
class AuthLoginResponse:
	token: str
	type: typing.Literal['AuthLoginResponse'] = 'AuthLoginResponse'

@dataclasses.dataclass
class TxnRequest:
	commands: list['Command']
	type: typing.Literal['TxnRequest'] = 'TxnRequest'

@dataclasses.dataclass
class TxnResponse:
	results: list[typing.Optional['TxnResult']]
	type: typing.Literal['TxnResponse'] = 'TxnResponse'

@dataclasses.dataclass
class QueryRequest:
	query: str
	type: typing.Literal['QueryRequest'] = 'QueryRequest'

@dataclasses.dataclass
class CreateUser:
	user: 'UserRef'
	password: str
	type: typing.Literal['CreateUser'] = 'CreateUser'

@dataclasses.dataclass
class GetUser:
	user: 'UserRef'
	type: typing.Literal['GetUser'] = 'GetUser'

@dataclasses.dataclass
class DeleteUser:
	user: 'UserRef'
	type: typing.Literal['DeleteUser'] = 'DeleteUser'

@dataclasses.dataclass
class AssignUserRoles:
	user: 'UserRef'
	roles: list['RoleRef']
	type: typing.Literal['AssignUserRoles'] = 'AssignUserRoles'

@dataclasses.dataclass
class CreateRole:
	role: 'RoleRef'
	type: typing.Literal['CreateRole'] = 'CreateRole'

@dataclasses.dataclass
class DeleteRole:
	role: 'RoleRef'
	type: typing.Literal['DeleteRole'] = 'DeleteRole'

@dataclasses.dataclass
class GrantSchemaPermissions:
	role: 'RoleRef'
	schema: 'SchemaRef'
	permissions: 'SchemaPermissions'
	type: typing.Literal['GrantSchemaPermissions'] = 'GrantSchemaPermissions'

@dataclasses.dataclass
class GrantGlobalSchemaPermissions:
	role: 'RoleRef'
	permissions: 'SchemaPermissions'
	type: typing.Literal['GrantGlobalSchemaPermissions'] = 'GrantGlobalSchemaPermissions'

@dataclasses.dataclass
class GrantComputeClusterPermissions:
	role: 'RoleRef'
	compute_cluster: 'ComputeClusterRef'
	permissions: 'ComputeClusterPermissions'
	type: typing.Literal['GrantComputeClusterPermissions'] = 'GrantComputeClusterPermissions'

@dataclasses.dataclass
class GrantGlobalComputeClusterPermissions:
	role: 'RoleRef'
	permissions: 'ComputeClusterPermissions'
	type: typing.Literal['GrantGlobalComputeClusterPermissions'] = 'GrantGlobalComputeClusterPermissions'

@dataclasses.dataclass
class GrantDatabasePermissions:
	role: 'RoleRef'
	permissions: 'DatabasePermissions'
	type: typing.Literal['GrantDatabasePermissions'] = 'GrantDatabasePermissions'

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
	roles: set['RoleRef']
	type: typing.Literal['User'] = 'User'

@dataclasses.dataclass
class Role:
	database_permissions: 'DatabasePermissions'
	global_schema_permissions: 'SchemaPermissions'
	schema_permissions: dict['SchemaRef', 'SchemaPermissions']
	global_compute_cluster_permissions: 'ComputeClusterPermissions'
	compute_cluster_permissions: dict['ComputeClusterRef', 'ComputeClusterPermissions']
	type: typing.Literal['Role'] = 'Role'

@dataclasses.dataclass
class CreateSchema:
	name: 'SchemaRef'
	type: typing.Literal['CreateSchema'] = 'CreateSchema'

@dataclasses.dataclass
class DeleteSchema:
	name: 'SchemaRef'
	type: typing.Literal['DeleteSchema'] = 'DeleteSchema'

class SchemaRef(str):
	pass

@dataclasses.dataclass
class Schema:
	tables: set[str]
	type: typing.Literal['Schema'] = 'Schema'

@dataclasses.dataclass
class CreateTable:
	table: 'TableRef'
	table_def: 'Table'
	type: typing.Literal['CreateTable'] = 'CreateTable'

@dataclasses.dataclass
class GetTable:
	table: 'TableRef'
	type: typing.Literal['GetTable'] = 'GetTable'

@dataclasses.dataclass
class AlterTable:
	table: 'TableRef'
	new_columns: list['Column']
	type: typing.Literal['AlterTable'] = 'AlterTable'

@dataclasses.dataclass
class DeleteTable:
	table: 'TableRef'
	type: typing.Literal['DeleteTable'] = 'DeleteTable'

@dataclasses.dataclass
class InsertData:
	table: 'TableRef'
	data_ref: str
	type: typing.Literal['InsertData'] = 'InsertData'

@dataclasses.dataclass
class TableRef:
	schema: 'SchemaRef'
	name: str
	type: typing.Literal['TableRef'] = 'TableRef'

class ColumnType(str, enum.Enum):
	INT64 = 'Int64'
	STRING = 'String'
	TIMESTAMP = 'Timestamp'

@dataclasses.dataclass
class Column:
	name: str
	ty: 'ColumnType'
	nullable: bool
	type: typing.Literal['Column'] = 'Column'

@dataclasses.dataclass
class Table:
	columns: list['Column']
	sort_key: typing.Optional[str]
	type: typing.Literal['Table'] = 'Table'

TxnResult = typing.Union[ComputeCluster, UIState, User, Role, Schema, Table]

Command = typing.Union[CreateComputeCluster, DeleteComputeCluster, UIGetState, CreateUser, GetUser, DeleteUser,
						AssignUserRoles, CreateRole, DeleteRole, GrantSchemaPermissions, GrantGlobalSchemaPermissions,
						GrantComputeClusterPermissions, GrantGlobalComputeClusterPermissions, GrantDatabasePermissions,
						CreateSchema, DeleteSchema, CreateTable, GetTable, AlterTable, DeleteTable, InsertData]
