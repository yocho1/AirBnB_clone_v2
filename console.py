#!/usr/bin/python3
"""Command interpreter for AirBnB clone"""

import re
import cmd
import shlex
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


PARAM_RE = r'(\S+?)=("(?:\\.|[^"\\])*"|\S+)'


def parse_value(raw):
    """Convert a raw parameter value to str, float or int.

    Return None if the value is not valid (the parameter is skipped).
    """
    if raw.startswith('"'):
        if len(raw) < 2 or not raw.endswith('"'):
            return None
        inner = raw[1:-1]
        if re.search(r'(?<!\\)"', inner):
            return None
        return inner.replace('\\"', '"').replace('_', ' ')
    try:
        if '.' in raw:
            return float(raw)
        return int(raw)
    except ValueError:
        return None


class HBNBCommand(cmd.Cmd):
    """Command interpreter for AirBnB objects"""

    prompt = "(hbnb) "
    __classes = {
        'BaseModel': BaseModel,
        'User': User,
        'Place': Place,
        'State': State,
        'City': City,
        'Amenity': Amenity,
        'Review': Review
    }

    def emptyline(self):
        """Do nothing on empty line"""
        pass

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF command to exit the program"""
        return True

    def do_help(self, arg):
        """Show available commands"""
        cmd.Cmd.do_help(self, arg)

    def do_create(self, arg):
        """Create an instance: create <Class> <key>=<value> ..."""
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review
        classes = {"BaseModel": BaseModel, "User": User, "State": State,
                   "City": City, "Amenity": Amenity, "Place": Place,
                   "Review": Review}
        args = arg.split(None, 1)
        if not args:
            print("** class name missing **")
            return
        if args[0] not in classes:
            print("** class doesn't exist **")
            return
        obj = classes[args[0]]()
        rest = args[1] if len(args) > 1 else ""
        for key, raw in re.findall(PARAM_RE, rest):
            value = parse_value(raw)
            if value is None:
                continue
            setattr(obj, key, value)
        obj.save()
        print(obj.id)

    def do_show(self, arg):
        """Show an instance by class name and id"""
        if not arg:
            print("** class name missing **")
            return
        args = arg.split()
        class_name = args[0]
        if class_name not in self.__classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        obj_id = args[1]
        key = f"{class_name}.{obj_id}"
        all_objs = storage.all()
        if key not in all_objs:
            print("** no instance found **")
            return
        print(all_objs[key])

    def do_destroy(self, arg):
        """Delete an instance by class name and id"""
        if not arg:
            print("** class name missing **")
            return
        args = arg.split()
        class_name = args[0]
        if class_name not in self.__classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        obj_id = args[1]
        key = f"{class_name}.{obj_id}"
        all_objs = storage.all()
        if key not in all_objs:
            print("** no instance found **")
            return
        del all_objs[key]
        storage.save()

    def do_all(self, arg):
        """Show all instances, or all of a specific class"""
        all_objs = storage.all()
        if not arg:
            print([str(obj) for obj in all_objs.values()])
            return
        class_name = arg.split()[0]
        if class_name not in self.__classes:
            print("** class doesn't exist **")
            return
        filtered = [str(obj) for obj in all_objs.values()
                    if obj.__class__.__name__ == class_name]
        print(filtered)

    def do_update(self, arg):
        """Update an attribute of an instance"""
        if not arg:
            print("** class name missing **")
            return
        args = shlex.split(arg)
        class_name = args[0]
        if class_name not in self.__classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        obj_id = args[1]
        key = f"{class_name}.{obj_id}"
        all_objs = storage.all()
        if key not in all_objs:
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return
        attr_name = args[2]
        attr_value = args[3]

        obj = all_objs[key]
        cls = self.__classes[class_name]
        current = getattr(cls, attr_name, None)
        if current is None:
            current = getattr(obj, attr_name, None)
        if isinstance(current, bool):
            pass
        elif isinstance(current, int):
            try:
                attr_value = int(attr_value)
            except ValueError:
                pass
        elif isinstance(current, float):
            try:
                attr_value = float(attr_value)
            except ValueError:
                pass

        setattr(obj, attr_name, attr_value)
        obj.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
