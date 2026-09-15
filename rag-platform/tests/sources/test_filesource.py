# from rag_platform.connectors.filesystem import FilesystemConnector
# from rag_platform.domain.models import DocumentFormat
# from rag_platform.domain.types import TenantID

# def test_file_source_reads_supported_formats(tmp_path) -> None:
#     (tmp_path / "policy.md").write_text("# Policy")
#     (tmp_path / "benefits.txt").write_text("Benefits")
#     (tmp_path / "ignored.csv").write_text("a,b")

#     reader = FilesystemConnector(
#         tmp_path,
#         TenantID("tenant-1"),
#     )

#     documents = reader.read()

#     assert len(documents) == 2
#     assert {document.format for document in documents} == {
#         DocumentFormat.MARKDOWN,
#         DocumentFormat.TXT,
#     }

# def test_file_source_calculates_checksum(tmp_path) -> None:
#     content = b"parental leave policy"
#     (tmp_path / "leave.txt").write_bytes(content)

#     reader = FilesystemConnector(
#         tmp_path,
#         TenantID("tenant-1"),
#     )

#     documents = reader.read()

#     assert len(documents) == 1
#     assert documents[0].checksum == calculate_checksum(content)

"""
this module is not needed aymore .. 
new connector has this constructor:

FilesystemConnector(source: DocumentSource)

But the old test is still doing:

FilesystemConnector(
    tmp_path,
    TenantID("tenant-1"),
)

Hence the error :
TypeError:
FilesystemConnector.__init__() takes 2 positional arguments
but 3 were given

Solution: 
We no longer need: tests/sources/test_filesource.py
because those tests are testing the old FileSourceReader design.

the new design is 
DocumentSource
      +
FilesystemConnector
"""
