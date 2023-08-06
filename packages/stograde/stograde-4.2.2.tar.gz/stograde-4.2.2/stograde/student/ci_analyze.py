import logging
import re
from typing import TYPE_CHECKING

from ..common.run_status import RunStatus

if TYPE_CHECKING:
    from ..student.student_result import StudentResult

LAB_REGEX = re.compile(r'^LAB', re.IGNORECASE)


def ci_analyze(student_result: 'StudentResult', course: str) -> bool:
    passing = True

    for result in student_result.results:
        for file in result.file_results:
            if file.file_missing and not file.optional:  # Alert student about any missing files
                logging.error("{}: File {} missing".format(result.spec_id, file.file_name))
                if not (course == 'sd' and re.match(LAB_REGEX, result.spec_id)):
                    passing = False
            else:
                for compilation in file.compile_results:  # Alert student about any compilation errors
                    if compilation.status is not RunStatus.SUCCESS:
                        if file.compile_optional or file.optional:
                            logging.warning("{}: File {} compile error (This did not fail the build)"
                                            .format(result.spec_id, file.file_name))
                        else:
                            logging.error("{}: File {} compile error:\n\n\t{}"
                                          .format(result.spec_id, file.file_name,
                                                  compilation.output.replace("\n", "\n\t")))
                            if not (course == 'sd' and re.match(LAB_REGEX, result.spec_id)):
                                passing = False

    return passing
