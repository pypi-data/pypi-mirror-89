# zgoubi-metadata

Useful metadata for creating zgoubi interfaces

Currently provides description of zgoubi elements in a yaml format.

Can be used by importing the module and using function that will return a dictionary of elements.

```
from zgoubi_metadata import elements

es_yaml = elements.get_raw_yaml()
es_parsed = elements.get_parsed()

```

Also the data files can be accessed through the `pkg_resources` interface.

```
import pkg_resources

pkg_resources.resource_listdir("zgoubi_metadata", "data/elements_yaml/")

drift_yaml = pkg_resources.resource_string("zgoubi_metadata", "data/elements_yaml/DRIFT.yaml")
```
