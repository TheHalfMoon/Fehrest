# Gotcha — index rebuild silently truncates on Windows paths

Project: core

Discovered after two days of debugging. When the vault root is a path containing a
trailing separator, the rebuild walker produced object paths with a doubled
separator, and the FTS insert silently accepted them. Queries then returned nothing
for those objects with no error anywhere.

Normalize the root before walking. This cost two days and leaves no trace in logs.
