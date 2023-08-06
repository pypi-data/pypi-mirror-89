#####
Setup
#####

.. warning::

   This plugin requires Radicale 2.0 or higher.

Once `Radicale is installed
<http://radicale.org/documentation/>`_ on your server, you must
tell Kalabash where it can find the file used to store rules.

Go to the *Kalabash > Parameters > Radicale* panel and fill the
**Radicale rights file path** setting (an absolute path is required).

When the configuration is done, Kalabash will completly handles the
file's content. It means every manual modification you could made on
this file would be overriden.

To do so, a new cron job must be created. You can use the following
example::

  */2 * * * * <kalabash_site>/manage.py generate_rights
  #
  # Or like this if you use a virtual environment:
  # */2 * * * * <virtualenv path/bin/python> <kalabash_site>/manage.py generate_rights

.. note::

   In some cases, the modifications you make on Kalabash may not be
   applied to the rights file. In order to force the generation,
   manually run the ``generate_rights`` command using the ``--force``
   option.
