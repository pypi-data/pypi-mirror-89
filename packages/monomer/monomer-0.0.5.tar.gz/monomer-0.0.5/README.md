# Monomer

DRY AWS CDK Construct for Glue Catalogs with dataclasses 

## Purpose 
AWS CDK offers a spectacular way to create infrastructure via code. However, glue 
requires all data processed by Glue ETL to be defined in the data catalog. Defining the structure in an 
application's CDK stack would be duplicative assuming this data is modeled in
the application code already. Monomer attempts to help solve this by translating an application's models, 
to Glue tables. 

## Usage

```
audit_log = monomer.MonomerDatabase(self,'AppAuditLog, database_name='audit_log')
audit_log.add_table(SystemEvent)
audit_log.add_table(UserEvent)
```

## Current Features
* Auto generates S3 with sensible security for data storage
* Translation for most scalar types to Glue types
* Translation of list and dict python types to Glue array and map types
* Supports storage of computed value via properties 
* Provides indirection layer to some aws cdk to prevent cdk dependency for an application

