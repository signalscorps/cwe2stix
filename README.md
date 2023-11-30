# cwe2stix

A command line tool that turns MITRE CWEs into STIX 2.1 Objects.

## Overview

CWEs are [Common Weakness Enumerations (CWE's)](https://cwe.mitre.org/). CWE's are a community-developed list of software and hardware weakness types managed MITRE. They serve as a common language as a baseline for weakness identification, mitigation, and prevention efforts.

For example, [CWE-79: Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting')](https://cwe.mitre.org/data/definitions/79.html).

We had a requirement to have an up-to-date copy of MITRE CWEs in STIX 2.1 format, like already exists and maintained by MITRE for ATT&CK (e.g. [Enterprise](https://github.com/mitre/cti/tree/master/enterprise-attack)) and [CAPEC](https://github.com/mitre/cti/tree/master/capec/2.1) on GitHub.

The code in this repository is a similar to the MITRE implementations for ATT&CK and CAPEC that;

1. Downloads latest CWE XML
2. Checks version of CWE XML
3. Converts them to STIX 2.1 Objects, if new version
4. Stores the STIX 2.1 Objects in the file store

## Installing the script

To install cwe2stix;

```shell
# clone the latest code
git clone https://github.com/signalscorps/cwe2stix
# create a venv
cd cwe2stix
python3 -m venv cwe2stix-venv
source cwe2stix-venv/bin/activate
# install requirements
pip3 install -r requirements.txt
```

## Running the script

```shell
python3 cwe2stix.py --version <CWE VERSION NUMBER>
```

* `--version` (optional): by default the script will download the latest available CWE file from the CWE website. If you want a specific version, you can pass the `--version` flag. e.g. `--version 4.2`. Note, only version 4.x is currently supported.

For example, to download the 4.2 version of CWEs;

```shell
python3 cwe2stix.py --version 4.2
```

If no `--version` passed, the latest CWE file located at `https://cwe.mitre.org/data/xml/cwec_latest.xml.zip` will be downloaded.

On each script run, the objects and bundle will be removed (if difference detected in version), and regenerated.

To handle versions, on the first run a `CWE_VERSION` file is created, listing the version of CWEs in the `stix2_objects` directory. On subsequent runs, this version value will changes based on the version of CWEs converted.

## Useful supporting tools

* To generate STIX 2.1 Objects: [stix2 Python Lib](https://stix2.readthedocs.io/en/latest/)
* The STIX 2.1 specification: [STIX 2.1 docs](https://docs.oasis-open.org/cti/stix/v2.1/stix-v2.1.html)
* [MITRE CWE site](https://cwe.mitre.org/)

## Support

[Minimal support provided via Slack in the #support-oss channel](https://join.slack.com/t/signalscorps-public/shared_invite/zt-1exnc12ww-9RKR6aMgO57GmHcl156DAA).

## License

[Apache 2.0](/LICENSE).