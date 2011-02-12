# Custom Hadoop 0.20.0 Streaming

Because of an issue in `StreamXMLRecordReader`, there is by default no support for processing GZIPed XML files. With the Wikipedia XML dumps, this is a problem, since they can be as large as 25GB if they need to be unzipped.

Hence, this JAR file contains a modified version of `StreamXMLRecordReader`. The issue is known to the Hadoop developers ([MAPREDUCE-589)](https://issues.apache.org/jira/browse/MAPREDUCE-589)) and there is a patch ([https://issues.apache.org/jira/secure/attachment/12385103/HADOOP-3562.combined.patch]), which can be applied in our use case.

This folder contains two custom jar files for Hadoop 0.20.0:

- `hadoop-0.20.2-core.custom.jar` is the modified version of hadoop
  0.20.2 necessary for this patch to work. To see the implications of
  the changes to this file, please see [MAPREDUCE-589)](https://issues.apache.org/jira/browse/MAPREDUCE-589)
- `hadoop-0.20.2-streaming.custom.jar` contains a modified version of
  `StreamXMLRecordReader` with support for GZIP encoded input files.
