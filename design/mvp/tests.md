# Backfill a copy of all current CWEs

```shell
python3 cwe2stix.py --version 4.1 && mv stix2_objects/cwe-bundle.json local_bundle_store/cwe-bundle-4_01.json && \
python3 cwe2stix.py --version 4.2 && mv stix2_objects/cwe-bundle.json local_bundle_store/cwe-bundle-4_02.json && \
python3 cwe2stix.py --version 4.3 && mv stix2_objects/cwe-bundle.json local_bundle_store/cwe-bundle-4_03.json && \
# 4.4 currently produces an error
#python3 cwe2stix.py --version 4.4 && mv stix2_objects/cwe-bundle.json local_bundle_store/cwe-bundle-4_04.json && \
python3 cwe2stix.py --version 4.5 && mv stix2_objects/cwe-bundle.json local_bundle_store/cwe-bundle-4_5.json && \
python3 cwe2stix.py --version 4.6 && mv stix2_objects/cwe-bundle.json local_bundle_store/cwe-bundle-4_06.json && \
python3 cwe2stix.py --version 4.7 && mv stix2_objects/cwe-bundle.json local_bundle_store/cwe-bundle-4_07.json && \
python3 cwe2stix.py --version 4.8 && mv stix2_objects/cwe-bundle.json local_bundle_store/cwe-bundle-4_08.json && \
python3 cwe2stix.py --version 4.9 && mv stix2_objects/cwe-bundle.json local_bundle_store/cwe-bundle-4_09.json && \
python3 cwe2stix.py --version 4.10 && mv stix2_objects/cwe-bundle.json local_bundle_store/cwe-bundle-4_10.json && \
python3 cwe2stix.py --version 4.11 && mv stix2_objects/cwe-bundle.json local_bundle_store/cwe-bundle-4_11.json && \
python3 cwe2stix.py --version 4.12 && mv stix2_objects/cwe-bundle.json local_bundle_store/cwe-bundle-4_12.json && \
python3 cwe2stix.py --version 4.13 && mv stix2_objects/cwe-bundle.json local_bundle_store/cwe-bundle-4_13.json
```