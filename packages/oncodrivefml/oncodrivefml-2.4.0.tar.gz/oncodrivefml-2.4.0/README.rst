.. _readme:

OncodriveFML
============

Recent years saw the development of methods to detect signals of positive selection in the pattern of somatic mutations in genes across cohorts of tumors, and the discovery of hundreds of driver genes. The next major challenge in tumor genomics is the identification of non-coding regions which may also drive tumorigenesis. We present OncodriveFML, a method that estimates the accumulated functional impact bias of somatic mutations in any genomic region of interest based on a local simulation of the mutational process affecting it. It may be applied to all genomic elements to detect likely drivers amongst them. OncodriveFML can discover signals of positive selection when only a small fraction of the genome, like a panel of genes, has been sequenced.


.. _readme license:

License
-------
OncodriveFML is made available to the general public subject to certain conditions described in its `LICENSE <LICENSE>`_. For the avoidance of doubt, you may use the software and any data accessed through UPF software for academic, non-commercial and personal use only, and you may not copy, distribute, transmit, duplicate, reduce or alter in any way for commercial purposes, or for the purpose of redistribution, without a license from the Universitat Pompeu Fabra (UPF). Requests for information regarding a license for commercial use or redistribution of OncodriveFML may be sent via e-mail to innovacio@upf.edu.

Usage
-----

OncodriveFML is meant to be used through the command line.

By default, OncodriveFML is prepared to analyse mutations
using HG19 reference genome. For other genomes,
update the `configuration <https://oncodrivefml.readthedocs.io/en/latest/configuration.html>`_
accordingly.

.. _readme install:

Installation
------------

OncodriveFML depends on Python 3.6 and some external libraries.
The easiest way to install all this software stack is using the well known `Anaconda Python distribution <http://continuum.io/downloads>`_::

    $ conda install -c bbglab oncodrivefml

OncodriveFML can also be installed using ``pip``::

    pip install oncodrivefml

Finally, you can get the latest code from the repository and install with ``pip``::

        $ git clone git@bitbucket.org:bbglab/oncodrivefml.git
        $ cd oncodrivefml
        $ pip install .

.. note::

   OncodriveFML has a set up dependency with `Cython <http://cython.org/>`_,
   which is required to compile the ``*.pyx`` files.


The first time that you run OncodriveFML it will download the genome reference from our servers.
By default the downloaded datasets go to ``~/.bgdata`` if you want to move these datasets to another folder you have to define the system environment variable BGDATA_LOCAL with an export command.

The following command will show you the help::

	$ oncodrivefml --help

.. _readme example:

Run the example
---------------

Download and extract the example files (if you cloned the repository skip this step)::

   $ wget https://bitbucket.org/bbglab/oncodrivefml/downloads/oncodrivefml-examples_v2.2.tar.gz
   $ tar xvzf oncodrivefml-examples_v2.2.tar.gz

To run this example OncodriveFML needs all the precomputed CADD scores, that is a 17Gb file,
that will be downloaded automatically, together with the reference genome.

.. warning::

   CADD scores are originally from `<http://cadd.gs.washington.edu/>`_ and are freely available for all non-commercial applications.
   If you are planning on using them in a commercial application, please contact them at `<http://cadd.gs.washington.edu/contact>`_.

To run the example, we have included a bash script (``run.sh``)
than will execute OncodriveFML. The script should be executed in
the folder where the files have been extracted::

   $ ./run.sh

The results will be saved in a folder named ``cds``.


Run OncodriveFML
----------------

Although OncodriveFML includes a predefined configuration file,
it is highly recommended to create one yourself.
In fact, if you are interested in using a reference genome other than
HG19, or a score other than CADD 1.0,
it is mandatory.
See `the documentation <https://oncodrivefml.readthedocs.io/en/latest/configuration.html>`_
for more details.


.. _readme docs:

Documentation
-------------

Find OncodriveFML documentation in `ReadTheDocs <http://oncodrivefml.readthedocs.io/en/latest/>`_.

You can also compile the documentation yourself using `Sphinx <http://www.sphinx-doc.org/en/stable/>`_,
if you have cloned the repository.
To do so, install the optional packages in ``optional-requirements.txt`` and build the
documentation in the docs folder::

    $ cd docs
    $ make html
