#!/bin/bash

#SBATCH --job-name=Clocktower

#SBATCH --output=result_generic.txt

#SBATCH --error=error_generic.txt

#SBATCH --nodes=1

#SBATCH --ntasks-per-node=1

#SBATCH --partition=20core

echo "Running on node $ (hostname)"

pwd

echo "PATH is: $PATH"

ls -1 /usr/bin/python*

#python3 --version

#ls -l /usr/bin/python3.9

#which python3.9

#python3.9 --version

#/usr/bin/python3.9 -m venv myenvnew
#source myenvnew/bin/activate
#python3.9 -m pip install --upgrade pip
#pip --version

#pip install llama-cpp-python
#pip install pydantic
#pip install huggingface_hub
##python3.9 clocktower.py