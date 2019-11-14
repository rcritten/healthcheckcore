# What is healthcheckcore?

It is a plugin framework for executing checks against a server installation
to confirm that it is configured properly and working as expected.

Why not just code to prevent errors in the first place? Sure, that is
certainly best, but for some complex products it isn't always possible.

This can also be used to gather information and can be a first step
towards automated remediation and prevention.

# Writing a check module

Check modules and sources are expected to be in a separate project from healthcheckcore.

The base class for a check is healthcheckcore.plugin::Plugin

The only method that needs to be implemented is check(). This implements the tes
t against the system and should yield a Result object. Because check() is a gene
rator multiple results can be yielded from a single check.

Typically each source defines its own plugin.py which contains the registry. Thi
s looks like:



        from healthcheckcore.plugin import Registry

        registry = Registry()

A basic check module consists of:

        from healthcheckcore.plugin import Plugin, Result
        from healthcheckcore import constants
        from ipahealthcheck.mymodule.plugin import registry

        @registry
        class MyPlugin(Plugin):
            def check(self):
                yield Result(self, constants.SUCCESS)

# Return value

A check yields a Result. This contains the outcome of the check including:

* result as defined in ipahealthcheck/core/constants.py
* msg containing a message to be displayed to the user.
* kw, a python dictionary of name value pairs that provide details on the error

The kw dict is meant to provide context for the check. Err on the side of
too much information.

If a check is complex enough that it checks multiple values then it should
yield a SUCCESS Result() for each one.

A Result is required for every test done so that one can know that the
check was executed.

The run time duration of each check will be calculated. The mechanism
differs depending on complexity.

A check should normally use the @duration decorator to track the
duration it took to execute the check.


        @registry
        class MyPlugin(Plugin):
            @duration
            def check(self):
                yield Result(self, constants.SUCCESS)


# Registering a source

The list of sources is stored in setup.py in the top-level of the tree containing the checks. Do not update the healthcheckcore setup.py for this.

Assuming it is contained in-tree it takes the form of:

'myhealthcheck.<dir>': [
    'name = myhealthcheck.<dir>.<file>'
]

For example, to add replication to the src/myhealthcheck/ipa directory

    'myhealthcheck.base': [
        'config = myhealthcheck.base.config',
        'files = myhealthcheck.base.files',
    ],

If a new branch of sources is added a new registry is needed. This is
added into the myhealthcheck.registry section in setup.py. If we decided
that replication didn't belong under myhealthcheck.ipa but instead in
myhealthcheck.ds it would look like:

    'myhealthcheck.registry': [
        'myhealthcheck.base = ipahealthcheck.base.plugin:registry',
        'myhealthcheck.custom = ipahealthcheck.custom.plugin:registry',
    ],

and

    'myhealthcheck.custom': [
        'custom = myhealthcheck.ds.custom',
    ],

# Execution

It is possible to execute a single check or all checks in a single source by pas
sing --source and/or --check on the command-line. This is intended to help user'
s quickly ensure that something is fixed by re-running a check after making a ch
ange.

# Output

Output is controlled via Output plugins. These take the global Results object an
d iterate over it to produce output in the desired format. The result is returne
d as a string.

A custom Output class must implement the generate method which generates the out
put.

A bare-bones output class is:

        @output_registry
        class Basic(Output):
            def generate(self, data):
                output = [x for x in data.output()]

                return output

An output object can declare its own options by adding a tuple named options to 
the class in the form of (arg_name, dict(argparse options).

An example to provide an option to indent the text to make it more readable.
        options = (
            (--indent', dict(dest='indent', help='How deeply to indent')),
        )
