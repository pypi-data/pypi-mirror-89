# IoC container for Pip.Services in Python Changelog

## <a name="3.1.2-3.1.4"></a> 3.1.2-3.1.4 (2020-12-21)

### Bug Fixes
* a fixed config_path in ProcessContainer

## <a name="3.1.1"></a> 3.1.1 (2020-08-04)
* fixed config read in ContainerConfigReader.py and ProcessContainer.py

## <a name="3.0.0"></a> 3.0.0 (2018-10-30)

### New release
* Restructuring package

### Features
- **Build** - Container default factory
- **Config** - Container configuration
- **Refer** - Container references
- **Container**
- **Proccess Container**

## <a name="2.2.0"></a> 2.2.0 (2017-04-20)

### Features
* Migrated to pip-services-commons 2.4
* Added Container class
* Implemented IOpenable interface in ManagedReferences

### Bug Fixes
* Fixed except when closing container that hasn't been opened

## <a name="2.1.1"></a> 2.1.1 (2017-04-12)

### Features
* **container** Now supports IConfigurable, IReferenceable, IUnreferenceable and IOpenable interfaces

### Bug Fixes
* Container start and stop methods were renamed to open and close

## <a name="2.1.0"></a> 2.1.0 (2017-04-11)

### Bug Fixes
* **config** Added parameterization
* ProcessContainer now supports command line parameters

## <a name="2.0.0"></a> 2.0.0 (2017-04-05)

### Features
* **refer** Added ReferenceDecorator
* **refer** Added ManagedReferences

## <a name="1.0.0"></a> 1.0.0 (2017-01-28)

Initial public release

### Features
* **build** Container default factory
* **config** Container configuration
* **info** Container information block
* **refer** Container references
* **process** Container system process

### Bug Fixes
No fixes in this version
