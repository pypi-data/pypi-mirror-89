from .yamlh import yaml_load, yaml_dump
from .plug import PlugBox
import os
import sys
from typing import Dict, Tuple

def panic(msg:str):
    print("panic: {}".format(msg))
    sys.exit(1)


def true_or_panic(test:bool, msg:str):
    if not test:
        panic(msg)


def file_exists(path, go_panic=False, msg="could not found {it}."):
    if not os.path.exists(path):
        if go_panic:
            panic(msg.format(it=path))
        else:
            return False
    return True


class Depend(object):
    def __init__(self, d):
        if not d.startswith("@"):
            parts = d.split(" ")
            self.name = parts[0]
            self.dtype = "direct"
            if len(parts) > 1:
                self.version = parts[1]
        else:
            # @(opt/path)
            self.dtype = "path"
            self.path = d[2:-1]

    def __repr__(self):
        if self.dtype == "direct":
            return "{} {}".format(self.name, self.version if hasattr(self, "version") else "*")
        elif self.dtype == "path":
            return "@({})".format(self.path)
        else:
            return "Depend@{}".format({"type": self.type})


class CompilingDesc(object):
    def __init__(self, sandbox: "Sandbox", **kvargs):
        self.sandbox = sandbox
        self.config = kvargs
        self.root = kvargs["root"]
        self.dependencies = list(map(self.make_depend_obj,kvargs.get("dependencies", [])))
        self.name = kvargs["name"]
        self.type = kvargs["type"]
        self.use = kvargs["use"]
        self.action_arg = kvargs.get("action_arg", None)
        self.action_default_arg = kvargs.get("action_default_arg", None)

    def make_depend_obj(self, s):
        return Depend(s)

    @property
    def gvars(self):
        return self.sandbox.gconfig['vars']
    
    def expand_path(self, path):
        return self.sandbox.expand_path(path)

class Sandbox(object):
    def __init__(self, confpath, **globalconf):
        self.plugbox = PlugBox()
        self.gconfig = globalconf
        self.confpath = os.path.realpath(confpath)
        file_exists(self.confpath, go_panic=True)
        self.root = os.path.split(os.path.realpath(confpath))[0]
        self.config = self.prepare_config(confpath)
        self.private_actions: Dict[str, function] = {}
    
    def add_private_action(self, name: str, action=None):
        true_or_panic(
            name.startswith('_'), "private action's name should be leaded by '_': {}".format(name)
        )
        if action:
            self.private_actions[name] = action
        else:
            def wrapper(f):
                self.add_private_action(name, f)
                return f
            return wrapper

    @staticmethod
    def prepare_config(confpath):
        with open(confpath, 'r') as f:
            return yaml_load(f.read())

    def ready(self):
        self.plug_search()
        self.plugbox.runhook("on_sandbox_load", self)

    def plug_check_and_load(self, user_request:str, check="compile", panic_if_notfound=True):
        if self.plugbox.exists(user_request):
            plugin = self.plugbox.load(user_request)
            if hasattr(plugin, check):
                return plugin
            else:
                panic("plugin {} requested in {} does not support {} hook".format(user_request, self.confpath, check))
        else:
            if panic_if_notfound:
                panic("could not found plugin {} requested in {}, all plugins: {}, searched paths: {}".format(user_request, self.confpath, self.plugbox.plugin_names(), self.plugbox.searchpaths))

    def plug_search(self):
        if "plugin_paths" in self.gconfig:
            for p in self.gconfig["plugin_paths"]:
                self.plugbox.searchpaths.append(self.expand_path(p))
        if "plugin_paths" in self.config:
            for p in self.config["plugin_paths"]:
                self.plugbox.searchpaths.append(self.expand_path(p))
        self.plugbox.searchpaths.append(self.expand_path("./makru/plugins"))

    def build_desc(self, *, action_default_arg=None):
        config = self.config
        config['root'] = self.root
        return CompilingDesc(self, action_default_arg=action_default_arg, **config)

    def compile(self):
        target_plugin = self.plug_check_and_load(self.config["use"])
        target_plugin.compile(self.build_desc())

    def get_actions_conf(self):
        return self.config.get("actions", {})

    @staticmethod
    def action_split(action_name:str) -> Tuple[str, str]:
        parts = action_name.split('(')
        name = parts[0]
        if len(parts) < 2:
            return (name, None)
        darg = parts[1][:-1]
        return (name, darg)
    
    def is_action_exists(self, name):
        actions = self.get_actions_conf()
        target_action_s = actions.get(name, None)
        if target_action_s:
            parts = target_action_s.split(":")
            true_or_panic(
                len(parts) == 2,
                "action defined in wrong format, the right format is <plugin name>:<function name>, recviced is {}".format(target_action_s)
            )
            plugin_name = parts[0]
            function_name, default_arg = self.action_split(parts[1])
            plugin = self.plug_check_and_load(plugin_name, check=function_name, panic_if_notfound=False)
            if not plugin:
                return False
            return getattr(plugin, function_name, None) != None
        elif name in self.gconfig["bulitin_actions"]:
            return True
        elif name in self.private_actions:
            return True
        else:
            return False

    def run_action(self, name, arg=None):
        actions = self.get_actions_conf()
        target_action_s = actions.get(name, None)
        if target_action_s:
            parts = target_action_s.split(":")
            true_or_panic(
                len(parts) == 2,
                "action defined in wrong format, the right format is <plugin name>:<function name>, recviced is {}".format(target_action_s)
            )
            plugin_name = parts[0]
            function_name, default_arg = self.action_split(parts[1])
            plugin = self.plug_check_and_load(plugin_name, check=function_name)
            return getattr(plugin, function_name)(self.build_desc(action_default_arg=default_arg))
        elif name in self.gconfig["bulitin_actions"]:
            return self.gconfig["bulitin_actions"][name]()
        elif name in self.private_actions:
            return self.private_actions[name](self.build_desc())
        else:
            panic("could not find action {}".format(name))

    def expand_path(self, s):
        if s.startswith("./"):
            return os.path.join(self.root, s[2:])
        elif not s.startswith('/'):
            return os.path.join(self.root, s)
        else:
            return s


class Makru(object):
    def __init__(self, arguments=None):
        self._autorun_compile = True
        self.arguments = arguments if arguments else sys.argv[1:]
        self.options = self.scanflags()
        self.globalconfig = {
            "plugin_paths": [],
            "root_config_path": self.options.get("config_path", "./makru.yaml"),
            "bulitin_actions": {
                "compile": self.compile,
                "list_actions": self.list_actions,
            },
            "vars": self.options["vars"],
        }

    def main(self):
        if len(self.options["actions"]) > 0:
            for aname in self.options["actions"]:
                if "(" in aname and aname.endswith(')'):
                    parts = aname.split("(")
                    true_or_panic(
                        len(parts) == 2,
                        "found too more ( in your action call {}, could not parse it correctly".format(aname)
                    )
                    name = parts[0]
                    arg = parts[1][:-1]
                    self.action(name, arg)
                else:
                    self.action(aname)
        if self.options["do_compile"] or self._autorun_compile:
            self.compile()

    def build_sandbox(self):
        sandbox = Sandbox(self.globalconfig["root_config_path"], **self.globalconfig)
        sandbox.ready()
        return sandbox

    def compile(self):
        self.build_sandbox().compile()
    
    def list_actions(self):
        sandbox = self.build_sandbox()
        action_conf: Dict[str, str] = sandbox.get_actions_conf()
        print("All actions declared in \"{}\":".format(sandbox.confpath))
        for k in action_conf.keys():
            if sandbox.is_action_exists(k):
                print("  {} -> {}".format(k, action_conf[k]))
            else:
                print("  {} -> {} (not found)".format(k, action_conf[k]))
        if self.options['vars']['all']:
            print("Private actions:")
            for k in sandbox.private_actions.keys():
                print("  {} -> {}".format(k, sandbox.private_actions[k]))

    def action(self, name, arg=None):
        sandbox = self.build_sandbox()
        if arg:
            sandbox.config["action_arg"] = arg
        return sandbox.run_action(name, arg)

    def scanflags(self):
        options = {
            "config_path": "./makru.yaml",
            "actions": [],
            "do_compile": False,
            "vars": {},
        }
        shell_like_action_arg = False
        for arg in self.arguments:
            if arg.startswith("-F"):
                options["config_path"] = self.correct_config_path(arg[2:])
            elif arg.startswith("--"):
                parts = arg[2:].split('=')
                if len(parts) == 1:
                    key = parts[0]
                    if key[0] == "!":
                        options['vars'][key[1:]] = False
                    else:
                        options['vars'][key] = True
                elif len(parts) == 2:
                    key = parts[0]
                    value = self.str2val(parts[1])
                    options['vars'][key] = value
                else:
                    panic("could not parse command line argument: undefined format {}".format(arg))
            elif arg.startswith(":"):
                options["actions"].append(arg[1:])
                self._autorun_compile = False
                shell_like_action_arg = True
            elif shell_like_action_arg and (not arg.startswith(":")) and (not arg.startswith("-")):
                a = options["actions"][-1]
                options["actions"][-1] = "{}({})".format(a, arg)
            elif arg == "-C":
                options["do_compile"] = True
            else:
                panic("could not parse command line argument: unknown option {}".format(arg))
            shell_like_actionn_arg = False
        return options

    @staticmethod
    def correct_config_path(path):
        if os.path.isdir(path):
            return os.path.join(path, "makru.yaml")
        else:
            return path

    @staticmethod
    def str2val(s):
        def isnum(s):
            number_strs = list(map(str, range(0,10)))
            is_num = False
            if len(s) == 1:
                return s in number_strs
            else:
                return (s[0] in number_strs) and isnum(s)
        if (s.startswith('""') and s.endswith('""')) or (s.startswith("''") and s.endswith("''")):
            return s[1:-1]
        if s == 'true':
            return True
        elif s == 'false':
            return False
        elif isnum(s):
            return int(s)
        else:
            return s
