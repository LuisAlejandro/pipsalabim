=========
Use cases
=========

Here you can consult practical uses for some of the Pip Sala Bim functions.
For a more detailed review on what you can do with it, we recommend you to read
the :doc:`api` documentation.

The ``Module`` class
====================

The ``Module`` class is an abstraction of an Odoo Module. You can perform
several operations to access the module information::

    from pipsalabim.bundle import Module

    # Create a Module instance
    module = Module('path/to/module')

    # Query for data
    print(module.path)
    print(module.manifest)

    # Query information in manifest file
    print(module.properties.name)
    print(module.properties.version)
    print(module.properties.depends)


The ``Bundle`` class
====================

The ``Bundle`` class is an abstraction of a *Group* of modules, often referred
to as *Addons*. Here you can see how to interact with a bundle::

    from pipsalabim.bundle import Bundle

    # Create a Bundle instance
    bundle = Bundle('path/to/bundle')

    # Query for data
    print(bundle.name)
    print(bundle.path)
    print(bundle.modules)
    print(bundle.oca_dependencies)


The ``Environment`` class
=========================

The ``Environment`` class is an abstraction of a virtual Odoo Environment.
Think of it as an imaginary container inside of which you can add ``Bundles``
and ask for specific information about them. For example::

    from pipsalabim.environment import Environment

    # Create an Environment
    env = Environment()

    # Insert bundles
    # If any bundle has an oca_dependencies.txt file,
    # clone its dependencies and insert them as bundles
    env.addbundles(['./path-to-bundle', '../addons', '../etc'])

    # Make a report about dependencies that are not present in
    # the environment
    env.get_notmet_dependencies_report()

    # Make a report about record ids that reference modules
    # which are not present in the environment
    env.get_notmet_record_ids_report()

