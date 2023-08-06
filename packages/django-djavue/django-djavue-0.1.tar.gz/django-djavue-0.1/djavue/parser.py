import re
import os


class VueParser:
    """
    Parses a vue file to be understood by python
    """

    def __init__(self, location, file_name, component_list):
        self.component_list = component_list
        self.template = ""
        self.script = ""
        self.name = file_name.replace(".vue", "")
        self.location = location
        self.file_name = file_name

        with open(os.path.join(self.location, self.file_name), "r") as f:
            self._raw = f.read()

        self._get_imports()

    def _get_imports(self):
        """
        Gets all import statements and sends the components to the list
        """

        results = re.findall(r"import (.*)", self._raw)

        for path in results:
            self.component_list.load(path, by=self)

    def _get_value_from_tag(self, tag, raw):
        """
        Gets all value inside a tag
        """

        result = re.search(f"<{tag}>(.*)</{tag}>", raw.replace("\n", ""))

        if result:
            return result.group(1)
        else:
            raise ValueError(f"Could parse {tag} tag.")

    def _get_script(self, raw):
        """
        Gets all value inside the script tag
        """

        script = self._get_value_from_tag("script", raw)
        result = re.search(r"export default {(.*)}", script)

        if result:
            return result.group(1)
        else:
            raise ValueError(f"Could parse script")

    def _replace_context(self, context):
        """
        Gets all $(key) and replaces them with the correct value.
        Raises an exception if can't find a value to the key.
        """

        replaced = self._raw
        results = re.findall(r"\$\((.*)\)", self._raw)

        for key in results:
            if key not in context:
                raise ValueError(f"Missing key {key} for component {self.name}")

            replaced = replaced.replace(f"$({key})", str(context[key]))

        return replaced

    def _load(self, raw):
        """
        Returns parsed script and template tag once raw has been replaced.
        """

        script = self._get_script(raw)
        template = self._get_value_from_tag("template", raw)

        return (script, template)

    def mount(self, context={}):
        """
        Replaces values and loads the component
        """

        replaced = self._replace_context(context)
        script, template = self._load(replaced)

        self.script = script
        self.template = template

        return self

    def to_component(self, context={}):
        """
        Returns in a component form.
        """
        self.mount(context)
        return f"Vue.component('{self.name}',{{ template:'{self.template}', {self.script} }})"
