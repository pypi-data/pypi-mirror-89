from datetime import datetime
from .unixtool import UnixTool
from janis_core import (
    ToolOutput,
    ToolInput,
    Boolean,
    Stdout,
    String,
    File,
    ToolMetadata,
)

from janis_unix.data_types import Gunzipped


class UncompressArchive(UnixTool):
    def tool(self):
        return "UncompressArchive"

    def friendly_name(self):
        return "UncompressArchive"

    def tool_provider(self):
        return "GNU Project"

    def base_command(self):
        return "gunzip"

    def inputs(self):
        return [ToolInput("file", Gunzipped(), position=1), *self.additional_inputs]

    def outputs(self):
        return [ToolOutput("out", Stdout(File))]

    additional_inputs = [
        ToolInput(
            "stdout",
            Boolean(optional=True),
            prefix="-c",
            default=True,
            doc="write on standard output, keep original files unchanged",
        ),
        ToolInput("decompress", Boolean(optional=True), prefix="-d", doc="decompress"),
        ToolInput(
            "force",
            Boolean(optional=True),
            prefix="-f",
            doc="force overwrite of output file and compress links",
        ),
        ToolInput(
            "keep",
            Boolean(optional=True),
            prefix="-k",
            doc="keep (don't delete) input files",
        ),
        ToolInput(
            "list",
            Boolean(optional=True),
            prefix="-l",
            doc="list compressed file contents",
        ),
        ToolInput(
            "noName",
            Boolean(optional=True),
            prefix="-n",
            doc="do not save or restore the original name and time stamp",
        ),
        ToolInput(
            "name",
            Boolean(optional=True),
            prefix="-N",
            doc="save or restore the original name and time stamp",
        ),
        ToolInput(
            "quiet", Boolean(optional=True), prefix="-q", doc="suppress all warnings"
        ),
        ToolInput(
            "recursive",
            Boolean(optional=True),
            prefix="-r",
            doc="operate recursively on directories",
        ),
        ToolInput(
            "suffix",
            String(optional=True),
            prefix="-s",
            doc="use suffix SUF on compressed files",
        ),
        ToolInput(
            "test",
            Boolean(optional=True),
            prefix="-t",
            doc="test compressed file integrity",
        ),
        ToolInput("fast", Boolean(optional=True), prefix="-1", doc="compress faster"),
        ToolInput("best", Boolean(optional=True), prefix="-9", doc="compress better"),
        ToolInput(
            "rsyncable",
            Boolean(optional=True),
            prefix="--rsyncable",
            doc="Make rsync-friendly archive",
        ),
    ]

    def bind_metadata(self):
        return ToolMetadata(
            contributors=["Jiaan Yu"],
            dateCreated=datetime(2020, 6, 11),
            dateUpdated=datetime(2020, 6, 11),
            documentation="",
        )
