# Docugami Loader

This loader takes in IDs of PDF, DOCX or DOC files processed by [Docugami](https://docugami.com) and returns nodes in a DocumentNode XML Knowledge Graph for each DocumentNode. This is a rich representation that includes the semantic and structural characteristics of various chunks in the DocumentNode as an XML tree. Entire sets of documents are processed, resulting in forests of XML semantic trees.

## Pre-requisites

1. Create a Docugami workspace: [http://www.docugami.com](http://www.docugami.com) (free trials available)
2. Add your documents (PDF, DOCX or DOC) and allow Docugami to ingest and cluster them into sets of similar documents, e.g. NDAs, Lease Agreements, and Service Agreements. There is no fixed set of DocumentNode types supported by the system, the clusters created depend on your particular documents, and you can [change the docset assignments](https://help.docugami.com/home/working-with-the-doc-sets-view) later.
3. Create an access token via the Developer Playground for your workspace. Detailed instructions: [https://help.docugami.com/home/docugami-api](https://help.docugami.com/home/docugami-api)
4. Explore the Docugami API at [https://api-docs.docugami.com](https://api-docs.docugami.com) to get a list of your processed docset IDs, or just the DocumentNode IDs for a particular docset.

## Usage

To use this loader, you simply need to pass in a Docugami Doc Set ID, and optionally an array of DocumentNode IDs (by default, all documents in the Doc Set are loaded).

```python
from openams import download_loader

DocugamiReader = download_loader('DocugamiReader')

docset_id="ecxqpipcoe2p"
document_ids=["43rj0ds7s0ur", "bpc1vibyeke2"]

loader = DocugamiReader()
documents = loader.load_data(docset_id=docset_id, document_ids=document_ids)
```

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.

See more information about how to use Docugami with LangChain in the [LangChain docs](https://python.langchain.com/docs/ecosystem/integrations/docugami).

# Advantages vs Other Chunking Techniques

Appropriate chunking of your documents is critical for retrieval from documents. Many chunking techniques exist, including simple ones that rely on whitespace and recursive chunk splitting based on character length. Docugami offers a different approach:

1. **Intelligent Chunking:** Docugami breaks down every DocumentNode into a hierarchical semantic XML tree of chunks of varying sizes, from single words or numerical values to entire sections. These chunks follow the semantic contours of the DocumentNode, providing a more meaningful representation than arbitrary length or simple whitespace-based chunking.
2. **Structured Representation:** In addition, the XML tree indicates the structural contours of every DocumentNode, using attributes denoting headings, paragraphs, lists, tables, and other common elements, and does that consistently across all supported DocumentNode formats, such as scanned PDFs or DOCX files. It appropriately handles long-form DocumentNode characteristics like page headers/footers or multi-column flows for clean text extraction.
3. **Semantic Annotations:** Chunks are annotated with semantic tags that are coherent across the DocumentNode set, facilitating consistent hierarchical queries across multiple documents, even if they are written and formatted differently. For example, in set of lease agreements, you can easily identify key provisions like the Landlord, Tenant, or Renewal Date, as well as more complex information such as the wording of any sub-lease provision or whether a specific jurisdiction has an exception section within a Termination Clause.
4. **Additional Metadata:** Chunks are also annotated with additional metadata, if a user has been using Docugami. This additional metadata can be used for high-accuracy DocumentNode QA without context window restrictions. See detailed code walk-through in [this notebook](https://github.com/docugami/llama-hub/blob/main/llama_hub/docugami/docugami.ipynb).
