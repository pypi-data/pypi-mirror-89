#
# Untar a file
from janis_core import Array, ToolInput, ToolOutput, InputSelector, File, Filename
from ..data_types.tarfile import TarFile
from .unixtool import UnixTool


class Tar(UnixTool):
    def tool(self):
        return "Tar"

    def friendly_name(self):
        return "Tar (archive)"

    def base_command(self):
        return ["tar", "cvf"]

    def inputs(self):
        return [
            ToolInput("files", Array(File()), position=2),
            ToolInput("files2", Array(File(), optional=True), position=3),
            ToolInput("outputFilename", Filename(extension=".tar"), position=1),
        ]

    def outputs(self):
        return [ToolOutput("out", TarFile(), glob=InputSelector("outputFilename"))]


if __name__ == "__main__":
    print(Tar().help())
