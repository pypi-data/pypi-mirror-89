"""PySeqtender"""

from pyspark.sql import SparkSession


class SeqTenderCommandBuilder:
    """
    Class for creating command to aligning reads using industry standard tools.
    :param session: session in which the alignment will be run and parallelized
    :type session: SparkSession
    :param command: command which will be run - generated
    by CommandBuilder object (it maps input parameters to the command)
    :type command: String

    """

    def __init__(self, session: SparkSession, reads_path, index_path,
                 tool, interleaved, read_group_id="",
                 read_group=""):
        """Creates a new SeqTenderCommandBuilder.
        """
        self.session = session
        reads_extension = session._jvm.org.biodatageeks.alignment.AlignmentTools.getReadsExtension(reads_path)
        self.command = session._jvm.org.biodatageeks.alignment.CommandBuilder.buildCommand(reads_extension, index_path,
                                                                                           tool,
                                                                                           None, interleaved,
                                                                                           read_group_id, read_group)

    def get_command(self):
        return self.command


class SeqTenderAlignment:
    """
    Class for running reads alignment using passed command.
    :param session: session in which the alignment will be run and parallelized
    :type session: SparkSession
    :param reads_path: path to reads which will be aligned
    :type reads_path: String
    :param command: command which will be run
    :type command: String

    """

    def __init__(self, session: SparkSession, reads_path, command):
        """Creates a new SeqTenderAlignment.
        """
        self.session = session
        self.reads_path = reads_path
        self.command = command

    def pipe_reads(self):
        return self.session._jvm.org.biodatageeks.alignment.SeqTenderAlignment.pipeReads(self.reads_path, self.command,
                                                                                         self.session._jsparkSession)

    def save_reads(self, path, rdd):
        reads = self.session._jvm.org.biodatageeks.alignment.CustomRDDSAMRecordFunctions.addCustomFunctions(rdd)
        self.session._jsparkSession.conf().set("org.biodatageeks.seqtender.bamIOLib", "disq")
        reads.saveAsBAMFile(path, self.session._jsparkSession)


class SeqTenderAnnotation:

    def __init__(self, session: SparkSession):
        """Creates a new SeqTenderAnnotation.
        """
        self.session = session

    def pipe_variants(self, path, command):
        return self.session._jvm.org.biodatageeks.annotation.SeqTenderVCF.pipeVCF(path,
                                                                                  command, self.session._jsparkSession)

    def save_variants(self, path, rdd):
        variants = self.session._jvm.org.biodatageeks.annotation.CustomVariantContextFunctions.addCustomFunctions(rdd)
        variants.saveDISQAsVCFFile(path, self.session._jsparkSession)
