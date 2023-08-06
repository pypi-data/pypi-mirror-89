import psycopg2

from dataclasses import dataclass
import inspect
import pickle
import codecs

DEBUG = True

"""
TODO
- Map into user types (not only bytea) (? done ?)
- No hierarchy (only save and delete)
"""

def log(*msg):
    if DEBUG:
        print(*msg)

@dataclass
class DBConnectionInfo:
    """This is a data object that should contain the fileds necessary to connect
    to the underlying database: dbname, host, password, user.
    """
    dbname: str
    host: str
    password: str
    user: str
    port: int = 5432

class Py2SQL:
    __connection = None

    @staticmethod
    def db_connect(db: DBConnectionInfo):
        """Connect to the database.

        Parameters
        ----------
        db : DBConnectionInfo
            An object that contains necessary information for connecting to
            the database.
        """
        Py2SQL.__connection = psycopg2.connect(
            dbname=db.dbname,
            user=db.user,
            host=db.host,
            password=db.password,
            port=db.port
        )

    @staticmethod
    def db_disconnect():
        Py2SQL.__connection.close()

    @staticmethod
    def db_engine():
        """
        Returns a tuple that represents the name of the underlying
        database and its version.

        Examples:
        ---------
        #    >>> name, version = Py2SQL.db_engine()
        """
        cur = Py2SQL.__connection.cursor()
        string_cmd = "select version();"
        log("executing:", string_cmd)
        cur.execute(string_cmd)
        retval = cur.fetchone()[0].split(' ')[:2]
        log("retval:", retval)
        cur.close()
        return retval

    @staticmethod
    def db_name():
        """Returns the name of the current database.
        """
        cur = Py2SQL.__connection.cursor()
        string_cmd = "select current_database();"
        log("executing:", string_cmd)
        cur.execute(string_cmd)
        retval = cur.fetchone()[0]
        log("retval:", retval)
        cur.close()
        return retval

    @staticmethod
    def db_size():
        """Returns the size of the current database.
        """
        db_name = Py2SQL.db_name()
        cur = Py2SQL.__connection.cursor()
        # Attention - no double quotes!
        string_cmd = "select pg_database_size('{}');".format(db_name)
        log("executing:", string_cmd)
        cur.execute(string_cmd)
        retval = int(cur.fetchone()[0]) / 1024 / 1024
        log("retval:", retval)
        cur.close()
        return retval

    @staticmethod
    def db_tables():
        """Returns the names of the tables that currently exist in the system.
        This method does not respect the system tables (`information_schema` & `pg*`).
        """
        db_name = Py2SQL.db_name()
        cur = Py2SQL.__connection.cursor()
        # Reference: https://www.postgresql.org/docs/9.1/infoschema-tables.html
        string_cmd = "select table_name from information_schema.tables where table_schema not like 'pg_%' and table_schema != 'information_schema' order by table_name;"
        log("executing:", string_cmd)
        cur.execute(string_cmd)
        retval = [i[0] for i in cur.fetchall()]
        log("retval:", retval)
        cur.close()
        return retval

    @staticmethod
    def db_table_structure(table):
        """
        Returns a list describing the structure of the database. Each list element is
        a tuple of the following king: (column_number, column_name, column_type).

        Parameters
        ----------
        table : table name of user's interest.
        """
        cur = Py2SQL.__connection.cursor()
        # Reference: https://www.postgresql.org/docs/current/information-schema.html
        string_cmd = "select column_name, data_type from information_schema.columns where table_name = '{}' and table_schema != 'information_schema' and table_schema not like 'pg%' ".format(table)
        log("executing:", string_cmd)
        cur.execute(string_cmd)
        retval = cur.fetchall()
        cur.close()
        retval = [(i, attr[0], attr[1]) for i, attr in enumerate(retval)]
        log("retval:", retval)
        return retval

    @staticmethod
    def db_table_size(table):
        """Returns the size of the table.

        Parameters
        ----------
        table : table name of user's interest.
        """
        cur = Py2SQL.__connection.cursor()
        string_cmd = "select pg_total_relation_size('{}');".format(table)
        log("executing:", string_cmd)
        cur.execute(string_cmd)
        retval = int(cur.fetchone()[0]) / 1024 / 1024
        log("retval:", retval)
        cur.close()
        return retval

    @staticmethod
    def _create_table(table_name, schema):
        """Creates a sample table with the given name. Used in testing modules.
        """
        cur = Py2SQL.__connection.cursor()
        cur.execute("create table {} {};".format(table_name, schema))
        cur.close()
        Py2SQL.__connection.commit()

    @staticmethod
    def _select_from_table(table_name, params='column_name'):
        """Return information from database for selected table and params.
        It desired to use for debugging, unit tests.
        Parameters
        ----------
        table_name : table name of user's interest.
        params : table params such as: column_name, data_type...
        """
        cur = Py2SQL.__connection.cursor()
        cur.execute("select {} from information_schema.columns where table_name = '{}';".format(params, table_name.lower()))
        ret_val = cur.fetchall()
        #"select column_name, data_type from information_schema.columns where table_name = '{}' and table_schema != 'information_schema' and table_schema not like 'pg%' ".format(table)
        cur.close()
        Py2SQL.__connection.commit()
        return ret_val

    @staticmethod
    def _drop_table(table_name):
        """Drops the table. This should not be exported to the user,
        as this only runs in unit tests. But it can't be done, as unit tests
        rely on this method. So it remains here. This method is protected so that
        we have an easier time calling it in the test module.

        Parameters
        ----------
        table_name : table name of user's interest.
        """
        cur = Py2SQL.__connection.cursor()
        cur.execute("drop table if exists {};".format(table_name.lower()))
        cur.close()
        Py2SQL.__connection.commit()

    @staticmethod
    def save_class(class_):
        """Populates the database with the representation of a class, by
        reading its columns. Does not try to create a table with a duplicate
        name. The function pick ups parent classes members,
        which and put it into class representation into Database.

        Examples:
        ---------
     #       >>> class Foo:
     #       >>>     value str
     #       >>> foo = Foo()
     #       >>> Py2SQL.save_class(Foo)
        """

        Py2SQL.__save_class_with_foreign_key(class_)

    @staticmethod
    def _get_parent_classes(class_):
        ret = set()
        for i in class_.__bases__:
            if i == object: break
            ret.add(i)
            ret = ret.union(Py2SQL._get_parent_classes(i))
        return ret

    @staticmethod
    def __save_class_with_foreign_key(class_):
        """This is private method that contains the logic of creating
        a PostgreSQL table with the foreign keys defined by parents. This method
        uses reflection to check annotated attributes of the class and decide
        the layout of the to-be-created table.  The function pick ups parent classes
        members, which are modified by Object and put

        Parameters
        ----------
        class_ : the class that should be mapped onto the database.

        """
        cur = Py2SQL.__connection.cursor()
        cur.execute("drop table if exists {};".format(class_.__name__))
        annotated_data = dict()

        classes = Py2SQL._get_parent_classes(class_)
        classes.add(class_)

        for cur_class in classes:
            for t in inspect.getmembers(cur_class, lambda a:not(inspect.isroutine(a))):
                if t[0] == "__annotations__":
                    annotated_data.update(t[1])
                # `serial` is autoincremented!
        string_cmd = "create table if not exists {} (id serial primary key not null, ".format(class_.__name__)
        # Connect to already existing parent tables.
        for i in annotated_data.keys():
            if annotated_data[i] == str:
                string_cmd += "{} text, ".format(i)
            elif annotated_data[i] == int:
                string_cmd += "{} integer, ".format(i)
            elif annotated_data[i] == bool:
                string_cmd += "{} boolean, ".format(i)
            elif annotated_data[i] == float:
                string_cmd += "{} double precision, ".format(i)
            else:
                string_cmd += "{} bytea, ".format(i)
        string_cmd = string_cmd[:-2]
        string_cmd += ");"
        log("executing:", string_cmd)
        cur.execute(string_cmd)
        Py2SQL.__connection.commit()
        cur.close()

    @staticmethod
    def save_object(object_):
        """Writes a representation of the object to the database. It looks at the
        object't underlying type (via reflection) to decide where to write the object.
        This function uses the annotated attributes of the object's type to decide
        what data to store in the database (columns). The function pick ups parent classes
        members, which are modified by Object and put it into object representation into Database.

        Parameters
        ----------
        object_ : the object whose representation should appear in the database.

        Raises
        ------
        NotImplementedError
            If save_class() has not been previously called, then this method does not
            find the corresponding table and raises the exception.
        """
        table_name = type(object_).__name__
        cur = Py2SQL.__connection.cursor()

        # In PostgreSQL, tables are always created with lowercase names,
        # TODO should store metatdata about which names are already taken
        table_exists = cur.execute("select exists (select * from information_schema.tables where table_name = %s)", tuple([table_name.lower()]))
        fetched = cur.fetchone()
        if fetched[0] == False:
            raise NotImplementedError("This ORM requires a user to run save_class() before running save_object()")

        annotated_data = dict()
        for t in inspect.getmembers(object_, lambda a:not(inspect.isroutine(a))):
            if t[0] == "__dict__":
                annotated_data.update(t[1])

        specific_columns = ""
        for i in annotated_data.keys():
            specific_columns += str(i)
            specific_columns += ","
        specific_columns = specific_columns[:-1]

        string_cmd = "insert into {} ({}) values (".format(table_name, specific_columns)
        attr_values = []
        for i in annotated_data.keys():
            string_cmd += "%s , "
            if type(annotated_data[i]) not in [str, int, float, bool]:
                attr_values.append(pickle.dumps(object_.__dict__[i]))
            else:
                attr_values.append(object_.__dict__[i])
        string_cmd = string_cmd[:-2]
        string_cmd += ")"

        log("executing:", string_cmd, "with", attr_values)
        cur.execute(string_cmd, tuple(attr_values))
        cur.close()
        Py2SQL.__connection.commit()
        cur = Py2SQL.__connection.cursor()
        cur.close()

    @staticmethod
    def delete_class(class_):
        """Removes the representation of the class in the database.

        Parameters
        ----------
        class_ : the class that contains annotated attributes that define the
        schema of the to-be-created table.
        """
        Py2SQL._drop_table(class_.__name__)

    @staticmethod
    def delete_object(object_):
        """Removes the representation of the object in the database by looking at
        the table defined by its type, then trying to find the values in the
        database that represent it. More specifically, we first try to find
        an object by primary_key (if an object defines one), and if we fail,
        delete it by removing all rows from the table that have the same structure
        as the attributes of the class.

        Parameters
        ----------
            object_ : the object that guides the process of removal
        """
        class_name = object_.__class__.__name__

        sql_statement = 'delete from {} where '.format(class_name.lower())
        byte_repr = []
        annotated_attributes = object_.__annotations__
        for k in annotated_attributes.keys():
            sql_statement += "{} = %s and ".format(k)
            if annotated_attributes[k] not in [str, int, float, bool]:
                byte_repr.append(pickle.dumps(object_.__dict__[k]))
            else:
                byte_repr.append(object_.__dict__[k])

        sql_statement = sql_statement[:-4]
        sql_statement += ";"

        cur = Py2SQL.__connection.cursor()
        print("byte representation: ", byte_repr)
        print("executing:", sql_statement, "with the data: ", tuple(byte_repr))
        cur.execute(sql_statement, tuple(byte_repr))
        Py2SQL.__connection.commit()
        cur.close()

    @staticmethod
    def save_hierarchy(root_class):
        """Creates the representation of the hierarchy in the database by looking at
        the class subclass structure, then trying to find all derived class using __find_hierarchy
         and add them to database

        Parameters
        ----------
            root_class : the base class of class hierarchy
        """
        hierarchy = Py2SQL.__find_hierarchy(root_class)
        for i in hierarchy:
            Py2SQL.save_class(i)

    @staticmethod
    def __find_hierarchy(root_class):
        """Creates set of derived classes using recursion

        Parameters
        ----------
            root_class : the base class of class hierarchy
        """
        hierarchy = {root_class}
        for i in root_class.__subclasses__():
            hierarchy.update(Py2SQL.__find_hierarchy(i))
        return hierarchy

    @staticmethod
    def delete_hierarchy(root_class):
        """Deletes the representation of the hierarchy in the database by looking at
        the class subclass structure, then trying to find all derived class using __find_hierarchy
        and remove them from database

        Parameters
        ----------
            root_class : the base class of class hierarchy
        """
        hierarchy = Py2SQL.__find_hierarchy(root_class)
        for i in hierarchy:
            Py2SQL.delete_class(i)
