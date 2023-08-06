#!/usr/bin/env python3

"""Module containing the AcpypeParamsCNS class and the command line interface."""
import argparse
from biobb_common.configuration import  settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_common.command_wrapper import cmd_wrapper
from biobb_chemistry.acpype.common import *

class AcpypeParamsCNS():
    """
    | biobb_chemistry AcpypeParamsCNS
    | This class is a wrapper of `Acpype <https://github.com/alanwilter/acpype>`_ tool for small molecule parameterization for CNS/XPLOR MD package.
    | Generation of topologies for CNS/XPLOR. Acpype is a tool based in Python to use Antechamber to generate topologies for chemical compounds and to interface with others python applications like CCPN or ARIA. `Visit the official page <https://github.com/alanwilter/acpype>`_.

    Args:
        input_path (str): Path to the input file. File type: input. `Sample file <https://github.com/bioexcel/biobb_chemistry/raw/master/biobb_chemistry/test/data/acpype/acpype.params.mol2>`_. Accepted formats: pdb (edam:format_1476), mdl (edam:format_3815), mol2 (edam:format_3816).
        output_path_par (str): Path to the PAR output file. File type: output. `Sample file <https://github.com/bioexcel/biobb_chemistry/raw/master/biobb_chemistry/test/reference/acpype/ref_acpype.cns.par>`_. Accepted formats: par (edam:format_3881).
        output_path_inp (str): Path to the INP output file. File type: output. `Sample file <https://github.com/bioexcel/biobb_chemistry/raw/master/biobb_chemistry/test/reference/acpype/ref_acpype.cns.inp>`_. Accepted formats: inp (edam:format_3878).
        output_path_top (str): Path to the TOP output file. File type: output. `Sample file <https://github.com/bioexcel/biobb_chemistry/raw/master/biobb_chemistry/test/reference/acpype/ref_acpype.cns.top>`_. Accepted formats: top (edam:format_3881).
        properties (dic - Python dictionary object containing the tool parameters, not input/output files):
            * **basename** (*str*) - ("BBB") A basename for the project (folder and output files).
            * **charge** (*int*) - (0) [-20~20|1] Net molecular charge, for gas default is 0.
            * **acpype_path** (*str*) - ("acpype") Path to the acpype executable binary.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **container_path** (*str*) - (None) Container path definition.
            * **container_image** (*str*) - ('mmbirb/acpype:latest') Container image definition.
            * **container_volume_path** (*str*) - ('/tmp') Container volume path definition.
            * **container_working_dir** (*str*) - (None) Container working directory definition.
            * **container_user_id** (*str*) - (None) Container user_id definition.
            * **container_shell_path** (*str*) - ('/bin/bash') Path to default shell inside the container.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_chemistry.acpype.acpype_params_cns import acpype_params_cns
            prop = { 
                'basename': 'BBB', 
                'charge': 0 
            }
            acpype_params_cns(input_path='/path/to/myStructure.mol2', 
                            output_path_par='/path/to/newPAR.par', 
                            output_path_inp='/path/to/newINP.inp', 
                            output_path_top='/path/to/newTOP.top', 
                            properties=prop)

    Info:
        * wrapped_software:
            * name: Acpype
            * version: 2019.10.05.12.26
            * license: GNU
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl

    """

    def __init__(self, input_path, output_path_par, output_path_inp, output_path_top, 
                properties=None, **kwargs) -> None:
        properties = properties or {}

        # Input/Output files
        self.io_dict = { 
            "in": { "input_path": input_path }, 
            "out": { "output_path_par": output_path_par, "output_path_inp": output_path_inp, "output_path_top": output_path_top } 
        }

        # Properties specific for BB
        self.basename = properties.get('basename', 'BBB')
        self.charge = properties.get('charge', '')
        self.acpype_path = get_binary_path(properties, 'acpype_path')
        self.properties = properties

        # container Specific
        self.container_path = properties.get('container_path')
        self.container_image = properties.get('container_image', 'mmbirb/acpype:latest')
        self.container_volume_path = properties.get('container_volume_path', '/tmp')
        self.container_working_dir = properties.get('container_working_dir')
        self.container_user_id = properties.get('container_user_id')
        self.container_shell_path = properties.get('container_shell_path', '/bin/bash')

        # Properties common in all BB
        self.can_write_console_log = properties.get('can_write_console_log', True)
        self.global_log = properties.get('global_log', None)
        self.prefix = properties.get('prefix', None)
        self.step = properties.get('step', None)
        self.path = properties.get('path', '')
        self.remove_tmp = properties.get('remove_tmp', True)
        self.restart = properties.get('restart', False)

    def check_data_params(self, out_log, err_log):
        """ Checks all the input/output paths and parameters """
        self.io_dict["in"]["input_path"] = check_input_path(self.io_dict["in"]["input_path"], out_log, self.__class__.__name__)
        self.io_dict["out"]["output_path_par"] = check_output_path(self.io_dict["out"]["output_path_par"], 'par', out_log, self.__class__.__name__)
        self.io_dict["out"]["output_path_inp"] = check_output_path(self.io_dict["out"]["output_path_inp"], 'inp', out_log, self.__class__.__name__)
        self.io_dict["out"]["output_path_top"] = check_output_path(self.io_dict["out"]["output_path_top"], 'top', out_log, self.__class__.__name__)
        self.output_files = {
            'par': self.io_dict["out"]["output_path_par"],
            'inp': self.io_dict["out"]["output_path_inp"],
            'top': self.io_dict["out"]["output_path_top"],
        }

    def create_cmd(self, container_io_dict, out_log, err_log):
        """Creates the command line instruction using the properties file settings"""
        instructions_list = []

        # generating output path
        if self.container_path:
            out_pth = self.container_volume_path + '/' + get_basename(self.basename, out_log) + '.' + self.unique_name
        else:
            out_pth = get_basename(self.basename, out_log) + '.' + self.unique_name

        # executable path
        instructions_list.append(self.acpype_path)

        # generating input 
        ipath = '-i ' + container_io_dict["in"]["input_path"]
        instructions_list.append(ipath)

        # generating output 
        basename = '-b ' + out_pth
        instructions_list.append(basename)

        # adding charge
        charge = '-n ' + get_charge(self.charge, out_log)
        instructions_list.append(charge)

        return instructions_list

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`AcpypeParamsCNS <acpype.acpype_params_cns.AcpypeParamsCNS>` acpype.acpype_params_cns.AcpypeParamsCNS object."""
        
        # Get local loggers from launchlogger decorator
        out_log = getattr(self, 'out_log', None)
        err_log = getattr(self, 'err_log', None)

        # check input/output paths and parameters
        self.check_data_params(out_log, err_log)

        # Check the properties
        fu.check_properties(self, self.properties)

        if self.restart:
            output_file_list = [container_io_dict["out"]["output_path_par"], 
                                container_io_dict["out"]["output_path_inp"], 
                                container_io_dict["out"]["output_path_top"]]
            if fu.check_complete_files(output_file_list):
                fu.log('Restart is enabled, this step: %s will the skipped' % self.step, out_log, self.global_log)
                return 0

        # copy inputs to container
        container_io_dict = fu.copy_to_container(self.container_path, self.container_volume_path, self.io_dict)

        # create unique name for temporary folder (created by acpype)
        self.unique_name = create_unique_name(6)

        # create command line instruction
        cmd = self.create_cmd(container_io_dict, out_log, err_log) 

        # execute cmd
        fu.log('Running %s, this execution can take a while' % self.acpype_path, out_log)
        cmd = fu.create_cmd_line(cmd, container_path=self.container_path, 
                                 host_volume=container_io_dict.get("unique_dir"), 
                                 container_volume=self.container_volume_path, 
                                 container_working_dir=self.container_working_dir, 
                                 container_user_uid=self.container_user_id, 
                                 container_image=self.container_image, 
                                 container_shell_path=self.container_shell_path, 
                                 out_log=out_log, global_log=self.global_log)
        returncode = cmd_wrapper.CmdWrapper(cmd, out_log, err_log, self.global_log).launch()

        # move files to output_path and removes temporary folder
        if self.container_path:
            process_output(self.unique_name, 
                           container_io_dict['unique_dir'], 
                           self.remove_tmp, 
                           self.basename, 
                           get_default_value(self.__class__.__name__), 
                           self.output_files, out_log)
        else:
            process_output(self.unique_name, 
                           self.basename + "." + self.unique_name + ".acpype", 
                           self.remove_tmp, 
                           self.basename, 
                           get_default_value(self.__class__.__name__), 
                           self.output_files, out_log)

        return returncode

def acpype_params_cns(input_path: str, output_path_par: str, output_path_inp: str, output_path_top: str, properties: dict = None, **kwargs) -> None:
    """Execute the :class:`AcpypeParamsCNS <acpype.acpype_params_cns.AcpypeParamsCNS>` class and
    execute the :meth:`launch() <acpype.acpype_params_cns.AcpypeParamsCNS.launch>` method."""

    return AcpypeParamsCNS(input_path=input_path, 
                    output_path_par=output_path_par, 
                    output_path_inp=output_path_inp,
                    output_path_top=output_path_top,
                    properties=properties).launch()

def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(description="Small molecule parameterization for CNS/XPLOR MD package.", formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    # Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_path', required=True, help='Path to the input file. Accepted formats: pdb, mdl, mol2.')
    required_args.add_argument('--output_path_par', required=True, help='Path to the PAR output file. Accepted formats: par.')
    required_args.add_argument('--output_path_inp', required=True, help='Path to the INP output file. Accepted formats: inp.')
    required_args.add_argument('--output_path_top', required=True, help='Path to the TOP output file. Accepted formats: top.')

    args = parser.parse_args()
    args.config = args.config or "{}"
    properties = settings.ConfReader(config=args.config).get_prop_dic()

    # Specific call of each building block
    AcpypeParamsCNS(input_path=args.input_path, 
                    output_path_par=args.output_path_par, 
                    output_path_inp=args.output_path_inp, 
                    output_path_top=args.output_path_top, 
                    properties=properties).launch()

if __name__ == '__main__':
    main()
