LiFi Environment Repository README
=======================================================================================

Requirements
-------------



Repository Structure
--------------------

The repository consists of the following components:

1. **LiFi Environment Script (`lifi_environment.py`)**:
   - This script defines the LiFi environment class, which inherits from the OpenAI Gym library. It is the core component of the repository and provides the simulation environment for LiFi communication experiments.
   - The environment simulates LiFi access points (APs), user positions, and communication channels, allowing agents to make decisions about which APs to connect to and how to allocate bandwidth.

2. **`results.py`**:
   - This script is used for training reinforcement learning models in the LiFi environment. It contains code for running simulations, training agents, and collecting results.

3. **`hyperparameter_tuning.py`**:
   - This script is responsible for hyperparameter tuning. It helps optimize the performance of reinforcement learning agents by finding the best combination of hyperparameters for training.

4. **`testing.py`**:
   - This script is used for testing trained reinforcement learning agents in the LiFi environment. It allows you to evaluate the performance of your trained models on different scenarios and collect testing results.

5. **`helpers` Directory**:
   - This directory contains utility code and helper classes, such as channel models for LiFi and WiFi, and other supporting functions required for simulation and analysis.


How to Use
~~~~~~~~~~

Historical pricing:
1. alter config_hist.yaml to set parameters

2. run hist_price.py script

SEC Filings data:
1. cik_tikr_mapping.py

2. master_index.py

3. master_report.py

4. desired_fs.py:
   - Gathers the financial statements and checks for the correct formatting in the mapping of all data
Dependencies
~~~~~~~~~~~~

Ensure that you have the required Python packages and libraries installed to run the code successfully. You can typically install these dependencies using `pip` or another package manager:

- NumPy
- OpenCV (cv2)
- Matplotlib
- Gym (OpenAI Gym)
- Pandas

Contact
-------

Matias Huber - ge35taq@tum.de
Hansini Vijayaraghavan - hansini.vijayaraghavan@tum.de

Notes
-----


Build Documentation
~~~~~~~~~~~~~~~~~~~~

-  To build the documentation, it needs to be able to import the project code.
   This means that it needs all of the required Python modules mentioned in the requirements.txt.
   To build Documentation do the following.

    - Install project requirements inside your python environment (if not already done)

    ::

        pip install -r requirements.txt


    - `Install Sphinx <https://www.sphinx-doc.org/en/master/usage/installation.html>`_

    ::

        pip install sphinx

    - Build the documentation as html or pdf

    ::

        make html
        make latexpdf