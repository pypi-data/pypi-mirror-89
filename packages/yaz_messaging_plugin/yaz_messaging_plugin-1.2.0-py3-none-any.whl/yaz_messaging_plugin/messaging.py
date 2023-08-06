import collections
import copy
import difflib
import glob
import google.cloud.translate_v2
import io
import itertools
import os
import os.path
import re
import yaml
import yaml.constructor
import yaml.scanner
import yaz

from .loader import OrderedDictLoader
from .log import logger, set_verbose
from .version import __version__


class Messaging(yaz.BasePlugin):
    """
    Find and evaluate Symfony translation files.
    """
    dirs = ["src/*/Bundle/*/Resources/translations/", "src/Resources/translations/", "translations/"]

    def __init__(self):
        self.translator = None
        logger.debug("translation directories: %s", self.dirs)

    @yaz.task
    def version(self, verbose: bool = False, debug: bool = False):
        """Gives the software version."""
        set_verbose(verbose, debug)
        logger.info("using google-cloud-translate {}".format(google.cloud.translate_v2.__version__))
        logger.info("using pyyaml                 {}".format(yaml.__version__))
        logger.info("using yaz                    {}".format(yaz.version))
        return __version__

    @yaz.task(changes__choices=["ask", "overwrite", "fail"],
              duplicate__choices=["ask", "first", "last", "fail"],
              sync__choices=["ask", "google-translate", "use-key", "ignore", "fail"],
              depth__choices=["ask", "join", "fail"])
    def check(self, changes: str = "fail", duplicate: str = "fail", sync: str = "fail", depth: str = "fail", max_depth: int = 666, indent: int = 4, verbose: bool = False, debug: bool = False):
        """
        Find translation files and check them, any required changes will result in an error
        """
        set_verbose(verbose, debug)
        return self.cleanup(changes=changes, duplicate=duplicate, sync=sync, depth=depth, max_depth=max_depth, indent_length=indent)

    @yaz.task(changes__choices=["ask", "overwrite", "fail"],
              duplicate__choices=["ask", "first", "last", "fail"],
              sync__choices=["ask", "google-translate", "use-key", "ignore", "fail"],
              depth__choices=["ask", "join", "fail"])
    def fix(self, changes: str = "overwrite", duplicate: str = "first", sync: str = "google-translate", depth: str = "join", max_depth: int = 666, indent: int = 4, verbose: bool = False, debug: bool = False):
        """
        Find translation files and fix them in-line
        """
        set_verbose(verbose, debug)
        return self.cleanup(changes=changes, duplicate=duplicate, sync=sync, depth=depth, max_depth=max_depth, indent_length=indent)

    def cleanup(self, changes: str = "ask", duplicate: str = "ask", sync: str = "ask", depth: str = "ask", max_depth: int = 666, indent_length: int = 4):
        """
        Find translation files and resolve issues using strategies given by the arguments
        """
        for domain, files in self.get_message_files():
            domains = {}

            # Resolve duplicates
            for file in files:
                logger.debug("%s %s", domain, files)
                messages = self.get_messages_from_file(file)
                domains[file] = self.resolve_duplicate_keys(duplicate, messages)

            # Resolve sync
            domains = self.resolve_message_sync(sync, domains)

            # Resolve depth
            for file, messages in domains.items():
                # try:
                messages = self.resolve_message_depth(depth, max_depth, messages)
                # except Exception as error:
                #     raise RuntimeError("{} in file {}".format(error, file))

                # Resolve changes
                self.resolve_changes(changes, file, messages, indent_length)

        return True

    def resolve_duplicate_keys(self, strategy, messages):
        """Given a STRATEGY and a dict with possibly duplicate messages, return a non-duplicate dict

        When there are more than one possible messages,
        the STRATEGY will decide how the duplication is resolved.
        The following STRATEGY options are available:
        - fail: raises a yaz.Error
        - first: chooses the first defined message and ignores any others
        - last: chooses the last defined message and ignores any others
        - ask: lets the user choose the message

        MESSAGES is a dict in the form:
        { translation_key: [first_translation_value, second_translation_value, ...] }

        RETURNS a dict in the form:
        { translation_key: translation_value }
        """
        assert isinstance(strategy, str), type(strategy)
        assert isinstance(messages, dict), type(dict)
        assert all(isinstance(key, str) for key in messages.keys())
        assert all(isinstance(value, list) for value in messages.values())
        assert all(all(isinstance(message, str) for message in value) for value in messages.values())
        if strategy == "fail":
            for key, value in messages.items():
                if len(value) > 1:
                    raise yaz.Error("Translatable \"{}\" has multiple possible values \"{}\"".format(key, value))
            return dict((key, value[0]) for key, value in messages.items())
        elif strategy == "first":
            return dict((key, value[0]) for key, value in messages.items())
        elif strategy == "last":
            return dict((key, value[-1]) for key, value in messages.items())
        elif strategy == "ask":
            for key, value in messages.items():
                if len(value) > 1:
                    raise NotImplementedError("todo: implement duplicate_strategy=\"ask\" strategy")
            return dict((key, value[0]) for key, value in messages.items())

    def resolve_changes(self, strategy, file, messages, indent):
        buffer = io.StringIO()
        if messages:
            yaml.dump(messages, buffer, default_flow_style=False, width=1024 * 5, indent=indent, allow_unicode=True)

        with open(file, "r") as file_handle:
            buffer.seek(0)
            proposed_changes = "".join(difflib.context_diff(
                file_handle.readlines(),
                buffer.readlines(),
                fromfile="original {}".format(file),
                tofile="proposed {}".format(file),
                n=0
            ))

        if proposed_changes:
            buffer.seek(0)
            logger.debug("changes detected in file \"%s\"", file)

            if strategy == "fail":
                print(proposed_changes)
                raise yaz.Error("changes detected in file \"{}\"".format(file))
            if strategy == "overwrite":
                logger.info(proposed_changes)
                with open(file, "w") as output:
                    for line in buffer.readlines():
                        output.write(line)
            if strategy == "ask":
                print(proposed_changes)
                raise NotImplementedError("todo: implement syntax_changes_strategy=\"ask\" strategy")

    def resolve_message_depth(self, strategy, depth, messages):
        assert isinstance(strategy, str), type(strategy)
        assert isinstance(depth, int), type(depth)
        assert isinstance(messages, dict), type(dict)
        assert all(isinstance(key, str) for key in messages.keys())
        assert all(isinstance(value, str) for value in messages.values())
        root = dict()
        for keys, value in sorted(messages.items()):
            keys = keys.split(".", depth)
            layer = root
            prefix = ""
            for key in keys[:-1]:
                if prefix:
                    key = ".".join([prefix, key])
                    prefix = ""

                parent_layer = layer
                try:
                    layer = layer[key]
                except KeyError:
                    layer[key] = layer = dict()

                if isinstance(layer, str):
                    if strategy == "ask":
                        raise NotImplementedError("todo: implement depth_strategy=\"ask\" strategy")

                    if strategy == "join":
                        prefix = key
                        layer = parent_layer
                        continue

                    if strategy == "fail":
                        raise yaz.Error("Conflicting keys when expanding path \"{}\"".format(".".join(keys)))

            key = keys[-1]
            if prefix:
                key = ".".join([prefix, key])
            layer[key] = value

        return root

    def resolve_message_sync(self, strategy, domains):
        assert isinstance(strategy, str), type(strategy)
        assert isinstance(domains, dict), type(domains)
        assert all(isinstance(key, str) for key in domains.keys())
        assert all(isinstance(value, dict) for value in domains.values())
        assert all(all(isinstance(key, str) for key in value.keys()) for value in domains.values())
        assert all(all(isinstance(message, str) for message in value.values()) for value in domains.values())
        all_keys = set()
        all_keys.update(*domains.values())

        if all(len(all_keys) == len(messages) for messages in domains.values()):
            # all domains have all the messages, no need to do anything
            return domains

        if strategy == "ignore":
            return domains

        if strategy == "fail":
            for file, messages in domains.items():
                for key in all_keys.difference(messages.keys()):
                    raise yaz.Error("Translatable \"{}\" is not set in \"{}\"".format(key, file))

        domains = copy.deepcopy(domains)
        if strategy == 'google-translate':
            translator = self.init_google_translator()
            for file, messages in domains.items():
                destination_language = self.get_filename_match(file).group("language")
                for key in all_keys.difference(messages.keys()):
                    # get list of translation sources for this key
                    sources = [(self.get_filename_match(file).group("language"), messages[key]) for file, messages in domains.items() if key in messages]
                    # sort sources, prioritize english if available
                    sources = sorted(sources, key=lambda source: {"en": "0"}.get(source[0], source[0]))

                    # replace placeholders with translation-safe strings
                    replacements = []
                    def replace(match):
                        replacements.append(match.group("placeholder"))
                        return "[{id:06d}]".format(id=len(replacements) - 1)
                    source_text = sources[0][1]
                    source_text = re.sub(r"(?P<placeholder>%[^%]+%)", replace, source_text)
                    source_text = re.sub(r"(?P<placeholder>![a-zA-Z]+)", replace, source_text)
                    if source_text:
                        source_language = sources[0][0]

                        # call translation API
                        try:
                            translation = translator.translate(source_text, source_language=source_language, target_language=destination_language)["translatedText"]
                        except:
                            logger.error("\"google-translate\" Error while translating \"%s\" from \"%s\" into \"%s\"", source_text, source_language, destination_language)
                            raise

                        # return the placeholder replacements to their original placeholders
                        def un_replace(match):
                            return replacements[int(match.group("id"))]
                        translation = re.sub(r"\[(?P<id>\d{6})\]", un_replace, translation)
                    else:
                        translation = ''

                    messages[key] = translation
                    logger.info("\"google-translate\" strategy used to translate \"%s\" (%s) into \"%s\" (%s) and add \"%s\" to \"%s\"", sources[0][1], sources[0][0], translation, destination_language, key, file)

        if strategy == "use-key":
            for file, messages in domains.items():
                for key in all_keys.difference(messages.keys()):
                    messages[key] = key
                    logger.info("\"use-key\" strategy used to add \"%s\" to \"%s\"", key, file)

        if strategy == "ask":
            raise NotImplementedError("todo: implement duplicate_strategy=\"ask\" strategy")

        return domains

    def get_messages_from_file(self, file):
        """Read messages from a yml file and return a dict

        The returned dictionary contains a single key for every translatable string,
        however, as it is possible to have valid yml with duplicate keys, every key
        points to a list containing one or more translations.

        For example, the the yml file:
            foo.bar: A
            foo:
               bar: B

        Will return:
            {"foo.bar": ["A", "B"]}
        """
        assert isinstance(file, str), type(file)

        def recursion(messages, key, value):
            assert isinstance(messages, dict), type(messages)
            assert isinstance(key, str), type(key)
            assert value is None or isinstance(value, (dict, str)), type(value)

            if isinstance(value, dict):
                for postfix, value in value.items():
                    assert isinstance(postfix, str), [file, key, postfix, value]
                    recursion(messages, ".".join([key, postfix]), value)
            elif isinstance(value, str):
                messages[key[1:]].append(value)

            return messages

        try:
            with open(file, "r") as file_handle:
                return recursion(collections.defaultdict(list), "", yaml.load(file_handle, OrderedDictLoader))

        except (yaml.scanner.ScannerError, yaml.constructor.ConstructorError) as error:
            raise yaz.Error(error)

    def get_message_files(self):
        """Iterate over available message files grouped by directory and domain"""
        for dir_pattern in self.dirs:
            for dir in glob.glob(dir_pattern):
                files = [self.get_filename_match(filename) for filename in sorted(os.listdir(dir))]
                files = [file.groupdict() for file in files if file]
                for domain, files in itertools.groupby(files, lambda file: file["domain"]):
                    yield domain, [os.path.join(dir, file["filename"]) for file in files]

    def get_filename_match(self, filename):
        """Returns a match object with filename, domain, and language groups

        Can match the following types of strings:
        - "message.en.yml"          # yml extension
        - "message.en.yaml"         # yaml extension
        - "message.en_GB.yml"       # en or en_GB language
        - "/disk/message.en.yml"    # absolute file paths
        """
        assert isinstance(filename, str), type(filename)
        return re.match(r"(.*/)?(?P<filename>(?P<domain>\w+)[.](?P<language>\w{2}(_\w{2})?)[.](?P<extension>yml|yaml))$", filename)

    def init_google_translator(self):
        """Ensure that we only initialize the translator once"""
        if self.translator is None:
            self.translator = google.cloud.translate_v2.Client()
        return self.translator
