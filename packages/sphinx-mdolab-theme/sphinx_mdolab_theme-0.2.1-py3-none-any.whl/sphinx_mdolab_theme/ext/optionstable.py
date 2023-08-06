from importlib import import_module
from docutils.parsers.rst import directives
from docutils.parsers.rst.directives.tables import Table
from docutils.statemachine import ViewList
from docutils import nodes
import yaml


class OptionsTable(Table):
    """
    This Table directive formats the defaultOptions dictionary in a nice table

    This is heavily adapted from
    https://github.com/BU-NU-CLOUD-SP16/Trusted-Platform-Module-nova/blob/master/api-ref/ext/rest_parameters.py
    """

    required_arguments = 0
    optional_arguments = 2
    has_content = True
    option_spec = {
        "filename": str,
        "widths": directives.positive_int_list,
    }

    # default options
    filename = "options.yaml"
    N_COLS = 4
    header = ["Name", "Type", "Default value", "Description"]
    col_widths = [15, 10, 15, 40]

    def get_options(self):
        # access the class name
        module_path, member_name = self.arguments[0].rsplit(".", 1)
        # import the class
        cls = getattr(import_module(module_path), member_name)
        # call the private function to get the default options
        self.defaultOptions = cls._getDefaultOptions()

    def get_descriptions(self):
        if "filename" in self.options:
            self.filename = self.options["filename"]

        with open(self.filename) as f:
            self.yaml = yaml.load(f, Loader=yaml.FullLoader)

    def set_width(self):
        # sets the self.col_widths
        if "widths" in self.options:
            widths = self.options["widths"]
            assert len(widths) == self.N_COLS
            self.col_widths = widths

    def run(self):
        # set the self.defaultOptions attribute
        self.get_options()
        # read the descriptions
        self.get_descriptions()
        # set width
        self.set_width()
        # build table
        table_node = self.build_table()
        return [table_node]

    def collect_rows(self):
        # Add a column for a field. In order to have the RST inside
        # these fields get rendered, we need to use the
        # ViewList. Note, ViewList expects a list of lines, so chunk
        # up our content as a list to make it happy.
        def add_col(value):
            entry = nodes.entry()
            result = ViewList(value.split("\n"))
            self.state.nested_parse(result, 0, entry)
            return entry

        rows = []
        groups = []
        # options
        for key, value in self.defaultOptions.items():
            trow = nodes.row()
            # first add the name column, with text = key
            # this is the name of the option, wrapped in double backticks
            trow += add_col("``" + key + "``")
            # this is the type of the option
            # __name__ extracts the name of the datatype (e.g. str, float etc.)
            # otherwise this will display <class 'str'> etc
            default_type = value[0]
            trow += add_col(str(default_type.__name__))
            # this is the default value
            # here we do some type checking if we get a list of possible choices
            # TODO: could potentially import baseclasses and use existing code there
            default_value = value[1]
            if isinstance(default_value, list) and default_type != list:
                default_value = value[1][0]
                choices = True  # we have a choice
            else:
                choices = False
            trow += add_col(str(default_value))
            # this is the description from the yaml file
            # for choices, we expect a field called desc containing general description
            # plus one field for each possible choice
            # TODO: can add better error message when yaml file does not match
            if choices:
                desc = self.yaml[key]["desc"] + "\n\n"
                for choice in value[1]:
                    desc += f"-  ``{choice}``: \t{self.yaml[key][choice]}\n\n"
            # if there are no choices, we just pick out the entry from yaml
            else:
                desc = self.yaml[key]
            trow += add_col(desc)
            rows.append(trow)
        return rows, groups

    def build_table(self):
        table = nodes.table()
        tgroup = nodes.tgroup(cols=len(self.header))
        table += tgroup

        tgroup.extend(
            nodes.colspec(colwidth=col_width, colname="c" + str(idx)) for idx, col_width in enumerate(self.col_widths)
        )

        thead = nodes.thead()
        tgroup += thead

        row_node = nodes.row()
        thead += row_node
        row_node.extend(nodes.entry(h, nodes.paragraph(text=h)) for h in self.header)

        tbody = nodes.tbody()
        tgroup += tbody

        rows, groups = self.collect_rows()
        tbody.extend(rows)
        table.extend(groups)

        return table


def setup(app):
    app.add_directive("optionstable", OptionsTable)
