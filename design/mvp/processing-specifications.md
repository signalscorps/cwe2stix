## The logic

### Data download

[MITRE maintain an XML file with the full CWE definitions here](https://cwe.mitre.org/data/downloads.html). This appears to be the best machine readable format to use based on the other alternatives MITRE use to distribute this data (HTML and PDF). Note, the XML is packages in a .zip file (size is about 13Mb's uncompressed).

The download link for the latest `.xml` file is static;

```shell
https://cwe.mitre.org/data/xml/cwec_latest.xml.zip
```

This file is versioned in the header. For example;

```xml
<?xml version="1.0" encoding="UTF-8"?><Weakness_Catalog Name="CWE" Version="4.11" Date="2023-04-27" xmlns="http://cwe.mitre.org/cwe-6" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://cwe.mitre.org/cwe-6 http://cwe.mitre.org/data/xsd/cwe_schema_v6.10.xsd" xmlns:xhtml="http://www.w3.org/1999/xhtml">
```

cwe2stix checks the `Version` value on update, if the version has increased from the last run (stored in the root directory file `CWE_VERSION`, then the code is executed to parse and store the CWEs as STIX 2.1 Objects.

The latest xml version of the CWE dictionary is stored in the file system in the format;

```shell
cwe2stix/cwe_dictionaries/<XML_FILE>
```

e.g.

```shell
cwe2stix/cwe_dictionaries/cwec_v4.11.xml
```

On each update, the old xml file is purged and replaced with the new one.

### Parsing the data

In this `.xml` file, each CWE is captured between `<Weaknesses ID...>` `</Weaknesses>` tags.

In v4.11 (latest at time this was written) there are 958 distinct CWEs.

Inside the `<Weakness>` is a lot of information defined in the [CWE schema](https://cwe.mitre.org/documents/schema/index.html), much of it is currently ignored by cwe2stix.

CWEs are represent vulnerabilities.

Therefore these can be modelled as [STIX 2.1 Vulnerability Objects](https://docs.oasis-open.org/cti/stix/v2.1/os/stix-v2.1-os.html#_q5ytzmajn6re).

The STIX 2.1 Vulnerability Objects in cwe2stix are created [using the STIX 2 Python Library](https://stix2.readthedocs.io/en/latest/).

cwe2stix models the STIX 2.1 Vulnerability Objects for each CWE in the .xml file as follows;

```json
{
    "type": "weakness",
    "spec_version": "2.1",
    "id": "weakness--<UUIDV5 GENERATION LOGIC>",
    "name": "<CWE NAME>",
    "created_by_ref": "<IMPORTED IDENTITY OBJECT>",
    "created": "<Weaknesses.Weakness.Submission_Date>",
    "modified": "<Weaknesses.Weakness.Modification_Date> (latest date)",
    "description": "<Weaknesses.Weakness.Description> <Weaknesses.Weakness.Extended_Description>",
    "external_references": [
        {
         	"source_name": "cwe",
          	"external_id": "CWE-<CWE ID>",
          	"url": "http://cwe.mitre.org/data/definitions/<CWE ID>.html"
        },
        {
         	"source_name": "<External_Reference.author>, <External_Reference.author>",
          	"description": "<External_Reference.title>",
          	"url": "<External_Reference.URL>",
            "external_id": "<Weaknesses.Weakness.External_Reference_ID>",
        },
        {
         	"source_name": "<Weaknesses.Weakness.Taxonomy_Mappings.Taxonomy_Name>",
          	"external_id": "<Weaknesses.Weakness.Taxonomy_Mappings.Entry_ID>",
          	"description": "<Weaknesses.Weakness.Taxonomy_Mappings.Entry_Name>"
        },
        {
         	"source_name": "capec",
          	"external_id": "CAPEC-<Weaknesses.Weakness.Related_Attack_Patterns.Related_Attack_Pattern>",
          	"url": "https://capec.mitre.org/data/definitions/<Weaknesses.Weakness.Related_Attack_Patterns.Related_Attack_Pattern>.html"
        }
    ],
    "labels": [
        "Likelihood of Exploit: <Likelihood_Of_Exploit>",
        "Impact: <Consequence.Impact>",
        "Phase: <Introduction.Phase>"
    ],
    "object_marking_refs": [
        "marking-definition--613f2e26-407d-48c7-9eca-b8e91df99dc9",
        "<IMPORTED MARKING DEFINITION OBJECT>"
    ],
    "extensions": {
        "<IMPORTED EXTENSION DEFINTION OBJECT>": {
            "extension_type" : "new-sdo"
        }
    }
}
```

Note, the `created` field will never be accurate, as previous versions before code execution might exist but cannot be captured (as no data about them is . On updates the `created` time remains the same.

To generate the id, a UUIDv5 is generated using the namespace `762246cb-c8a1-53a7-94b3-eafe3ed511c9` and CWE-ID.

Inside each weakness ID is also a property `Weaknesses.Related_Weaknesses`. For example, for CWE-521;

```xml
<Related_Weaknesses>
    <Related_Weakness Nature="ChildOf" CWE_ID="1391" View_ID="1000" Ordinal="Primary"/>
    <Related_Weakness Nature="ChildOf" CWE_ID="287" View_ID="1003" Ordinal="Primary"/>
</Related_Weaknesses>
```

cwe2stix models these using [STIX 2.1 Relationship Objects](https://docs.oasis-open.org/cti/stix/v2.1/os/stix-v2.1-os.html#_cqhkqvhnlgfh) as follows;

```json
{
 	"type": "relationship",
 	"spec_version": "2.1",
 	"id": "relationship--<UUIDV5 GENERATION LOGIC>",
 	"created_by_ref": "<IMPORTED IDENTITY OBJECT>",
 	"created": "<CREATED TIME OF MOST RECENT CWE OBJECT IN PAIR>",
 	"modified": "<CREATED TIME OF MOST RECENT CWE OBJECT IN PAIR>",
 	"relationship_type": "<Related_Weakness Nature>",
 	"source_ref": "weakness--<CURRENT VULNERABILITY>",
 	"target_ref": "weakness--<Weaknesses.Weakness.Related_Weaknesses.Related_Weakness.CWE_ID>",
    "object_marking_refs": [
        "marking-definition--613f2e26-407d-48c7-9eca-b8e91df99dc9",
        "<IMPORTED MARKING DEFINITION OBJECT>"
    ],
}
```

To generate the id of the SRO, a UUIDv5 is generated using the namespace `762246cb-c8a1-53a7-94b3-eafe3ed511c9` and `<Related_Weakness Nature>+SOURCE_CWEID+TARGET_CWEID`.

The CAPEC XML also contains category entries. e.g.

```xml
<Category ID="1020" Name="Verify Message Integrity" Status="Draft">
         <Summary>Weaknesses in this category are related to the design and architecture of a system's data integrity components. Frequently these deal with ensuring integrity of data, such as messages, resource files, deployment files, and configuration files. The weaknesses in this category could lead to a degradation of data integrity quality if they are not addressed when designing or implementing a secure architecture.</Summary>
         <Relationships>
            <Has_Member CWE_ID="353" View_ID="1008"/>
            <Has_Member CWE_ID="354" View_ID="1008"/>
            <Has_Member CWE_ID="390" View_ID="1008"/>
            <Has_Member CWE_ID="391" View_ID="1008"/>
            <Has_Member CWE_ID="494" View_ID="1008"/>
            <Has_Member CWE_ID="565" View_ID="1008"/>
            <Has_Member CWE_ID="649" View_ID="1008"/>
            <Has_Member CWE_ID="707" View_ID="1008"/>
            <Has_Member CWE_ID="755" View_ID="1008"/>
            <Has_Member CWE_ID="924" View_ID="1008"/>
         </Relationships>
         <References>
            <Reference External_Reference_ID="REF-9"/>
            <Reference External_Reference_ID="REF-10" Section="pages 69 - 78"/>
         </References>
         <Mapping_Notes>
            <Usage>Prohibited</Usage>
            <Rationale>This entry is a Category. Using categories for mapping has been discouraged since 2019. Categories are informal organizational groupings of weaknesses that can help CWE users with data aggregation, navigation, and browsing. However, they are not weaknesses in themselves.</Rationale>
            <Comments>See member weaknesses of this category.</Comments>
            <Reasons>
               <Reason Type="Category"/>
            </Reasons>
         </Mapping_Notes>
         <Content_History>
            <Submission>
               <Submission_Name>Joanna C.S. Santos, Mehdi Mirakhorli</Submission_Name>
               <Submission_Date>2017-06-22</Submission_Date>
               <Submission_Version>2.12</Submission_Version>
               <Submission_ReleaseDate>2017-11-08</Submission_ReleaseDate>
               <Submission_Comment>Provided the catalog, Common Architectural Weakness Enumeration (CAWE), and research papers for this view.</Submission_Comment>
            </Submission>
                <Modification>
                    <Modification_Name>CWE Content Team</Modification_Name>
                    <Modification_Organization>MITRE</Modification_Organization>
                    <Modification_Date>2023-04-27</Modification_Date>
                    <Modification_Comment>updated Mapping_Notes</Modification_Comment>
                </Modification>
                <Modification>
                    <Modification_Name>CWE Content Team</Modification_Name>
                    <Modification_Organization>MITRE</Modification_Organization>
                    <Modification_Date>2023-06-29</Modification_Date>
                    <Modification_Comment>updated Mapping_Notes</Modification_Comment>
                </Modification>
         </Content_History>
      </Category>
```

Grouping SDOs are also used to represent CWE Categories (e.g. OWASP Top Ten 2004).

Grouping SDOs are modelled from CWE entries as follows

```json
{
    "type": "grouping",
    "spec_version": "2.1",
    "id": "grouping--<UUIDV5 LOGIC>",
    "created_by_ref": "<IMPORTED IDENTITY OBJECT>",
    "created": "<Content_History.Submission_Date>",
    "modified": "<Modification.Modificaton Date> (latest)",
    "name": "<CATEGORY.NAME>",
    "description": "<CATEGORY.SUMMARY>",
    "context": "unspecified",
    "external_references": [
        {
            "source_name": "cwe_category",
            "external_id": "<CWE CATEGORY ID>"
        },
        {
            "source_name": "<External_Reference.author>, <External_Reference.author>",
            "description": "<External_Reference.title>",
            "url": "<External_Reference.URL>",
            "external_id": "<Weaknesses.Weakness.External_Reference_ID>",
        },
    ],
    "object_marking_refs": [
        "marking-definition--613f2e26-407d-48c7-9eca-b8e91df99dc9",
        "<IMPORTED MARKING DEFINITION OBJECT>"
    ],
    "object_refs": [
        "<STIX IDs OF ALL CWEs LISTED IN CATEGORY.Relationships>"
    ]
}
```

To generate the id of the SDO, a UUIDv5 is generated using the namespace `762246cb-c8a1-53a7-94b3-eafe3ed511c9` and `name` field. 

To demonstrate the `object_refs` payload, in example for category 1020 above, the `object_refs` list would contain the STIX vulnerability IDs for; CWE_ID="353 CWE_ID="354" CWE_ID="390" CWE_ID="391" CWE_ID="494" CWE_ID="565 CWE_ID="649" CWE_ID="707" CWE_ID="755" CWE_ID="924".

In some cases related weakness not exist, as the CWE record does not exist in the dataset. For example, Category 1001 has a referenced `Weakness ID="227"`, however, there is no CWE-227 in the CWE dictionary. 

```xml
      <Category ID="1001" Name="SFP Secondary Cluster: Use of an Improper API" Status="Incomplete">
         <Summary>This category identifies Software Fault Patterns (SFPs) within the Use of an Improper API cluster (SFP3).</Summary>
         <Relationships>
            <Has_Member CWE_ID="111" View_ID="888"/>
            <Has_Member CWE_ID="227" View_ID="888"/>
            <Has_Member CWE_ID="242" View_ID="888"/>
```

If a reference to a Vulnerability that does not exist (e.g. Weakness ID="227") is made, the entry is ignored in the Grouping `object_refs` dictionary.

To support the `_ref`s created in the objects shown above, three other objects are imported by cwe2stix on first run;

* https://raw.githubusercontent.com/signalscorps/stix4signalscorps/main/objects/identity/identity--762246cb-c8a1-53a7-94b3-eafe3ed511c9.json
* https://github.com/signalscorps/stix4signalscorps/blob/main/objects/marking-definition/marking-definition--762246cb-c8a1-53a7-94b3-eafe3ed511c9.json
* https://raw.githubusercontent.com/signalscorps/stix4signalscorps/main/objects/extension-definition/extension-definition--51650285-49b2-50ee-916c-20836485532d.json

These are hardcoded into the `data/stix_templates/` directory in this repository.

cwe2stix also creates a STIX 2.1 Bundle JSON object containing all the other STIX 2.1 Objects created at each run. The Bundle takes the format;

```json
{
    "type": "bundle",
    "id": "bundle--<UUIDV5 GENERATION LOGIC>",
    "objects": [
   		"<ALL STIX JSON OBJECTS>"
    ]
}
```

To generate the id of the SRO, a UUIDv5 is generated using the namespace `762246cb-c8a1-53a7-94b3-eafe3ed511c9` and a md5 hash of all files in the bundle.

Unlike the other STIX Objects, this means on every update a new bundle ID will be generated if any difference in objects or properties is observed.

### Storing the objects in the file store

To support a similar approach to object distribution as MITRE do for both ATT&CK and CAPEC (objects stored as json files on GihHub), this script also allows for the STIX 2.1 objects to be stored in the filesystem.

The objects are stored in the root directory. The directory structure is defined by the STIX 2 Library's filesystem API, [as described here](https://stix2.readthedocs.io/en/latest/guide/filesystem.html).

A static [STIX 2.1 Bundle file](https://stix2.readthedocs.io/en/latest/guide/creating.html#Creating-Bundles) (that contains all Objects for the latest version) is also created. This is so that there is a URL that never changes and always returns the most recent bundle of objects;

```shell
/stix2_objects/cwe-bundle.json
```

### CWE version updates

If after run cwe2stix checks the `Version` value on update, if the version has increased (or decreased) from the last run shown in `CWE_VERSION`, then the code is executed.

The current set of objects (for old version) are first purged, and the objects for the new version recreated.

Once the run is complete, the script updates the `CWE_VERSION` with the current version of objects.

### Backfill mode

Running this script normally will only download the most recent version of the CWE dictionary. For most use-cases that is sufficient.

To create a historical record of objects, the script allows a user to pass a specific version of the CWE dictionary for conversion. Note, cwe2stix does not support CWE versions below 4.0 (as the schema is different and we do not have any need for these).

To achieve this, the code downloads the version entered from the CWE archive:

```shell
https://cwe.mitre.org/data/xml/cwec_v<VERSION>.xml.zip
```

e.g.

```shell
https://cwe.mitre.org/data/xml/cwec_v4.9.xml.zip
```