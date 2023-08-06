import logging
import os
from glob import iglob
from typing import List, TYPE_CHECKING

from .stogradeignore import load_stogradeignore
from ..specs.util import check_architecture, check_spec_dependencies
from ..toolkit import global_vars

if TYPE_CHECKING:
    from stograde.specs.spec import Spec


def filter_assignments(assignments: List[str]) -> List[str]:
    """Removes any assignments ignored by a .stogradeignore file during a CI job"""
    if not global_vars.CI:
        return assignments
    else:
        filtered_assignments = set(assignments)

        ignored_assignments = load_stogradeignore()

        for assignment in ignored_assignments:
            if assignment in filtered_assignments:
                logging.warning('Skipping {}: ignored by stogradeignore'.format(assignment))

        filtered_assignments = filtered_assignments.difference(ignored_assignments)

        if not filtered_assignments:
            logging.warning('All assignments ignored by stogradeignore')

        return list(filtered_assignments)


def get_spec_paths(wanted_specs: List[str], spec_dir: str) -> List[str]:
    """Removes any missing specs from the list and returns a list of the paths
    of the remaining specs"""
    all_spec_files = find_all_specs(spec_dir)
    loadable_spec_files = {path.split('/')[-1].split('.')[0]: path for path in all_spec_files}
    specs_to_load = set(loadable_spec_files.keys()).intersection(wanted_specs)
    missing_spec_files = set(wanted_specs).difference(loadable_spec_files.keys())

    for spec in missing_spec_files:
        logging.warning("No spec for {}".format(spec))

    return list(loadable_spec_files[filename] for filename in specs_to_load)


def find_all_specs(spec_dir: str) -> List[str]:
    """Get a list of all .yaml files in the specs directory"""
    return list(iglob(os.path.join(spec_dir, '*.yaml')))


def filter_loaded_specs(specs: List['Spec']) -> List['Spec']:
    """Filters the loaded specs based on properties such as required architecture"""
    remaining_specs: List['Spec'] = []

    for spec_to_use in specs:
        if not check_spec_dependencies(spec_to_use) or not check_architecture(spec_to_use):
            continue
        remaining_specs.append(spec_to_use)

    return remaining_specs
