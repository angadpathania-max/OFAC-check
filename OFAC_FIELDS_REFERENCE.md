# OFAC XML fields: what we use vs what’s available

## 1. Which files we use

- **We load both XMLs** in the `OFAC DB` folder: **sdn_advanced.xml** and **cons_advanced.xml** (and any other `.xml` in that folder).
- All name/alias records from all files are **merged into one list**. Search runs against this single list.
- We do **not** search one file at a time; every match is from the combined list.
- The only “which file” info we store is **source_file** (e.g. `sdn_advanced.xml` or `cons_advanced.xml`), so you can show it in the table.

---

## 2. What we currently extract and show

From **both** XMLs we only parse this path and these fields:

**XML path:**  
`DistinctParty` → `Profile` → `Alias` → `DocumentedName` → `DocumentedNamePart` → `NamePartValue`

| Column / field   | Source in XML                          | Shown in table? |
|------------------|----------------------------------------|------------------|
| **name**         | `<NamePartValue>` text                 | Yes (Listed name) |
| **fixed_ref**    | `DistinctParty` `FixedRef`             | Yes (Ref)        |
| **profile_id**   | `Profile` `ID`                        | No               |
| **alias_type_id**| `Alias` `AliasTypeID` (1400=A.K.A., 1401=F.K.A., 1402=N.K.A., 1403=Name) | Yes (Type) |
| **source_file**  | Our own: filename (sdn_advanced.xml / cons_advanced.xml) | Yes (Source) |

So: **we look up both XMLs**, merge all names, and **display**: Match score, Listed name, Type (alias type), Source (file name), Ref (fixed_ref). We do **not** currently pull Country, PartyType, Program, or Address from the XML.

---

## 3. Fields available in both XMLs (for the frontend table)

The advanced XMLs share the same schema. Below are the main **conceptual columns** you can add. “In reference tables” means the value is in a lookup list (e.g. CountryID → Country name); “in party/location tree” means we’d need to parse more of the tree and link Profile → Feature → Location etc.

| Column / concept      | Where it lives in the XML | Notes |
|-----------------------|---------------------------|--------|
| **Country**           | `Location` → `LocationCountry` `CountryID` (and/or `LocationAreaCode` `AreaCodeID`); lookup in `ReferenceValueSets` → `CountryValues` (ID → country name) or `AreaCodeValues` (ID → e.g. “AF”, “AL”). | Profile is linked to Features; one feature type is “Location” (FeatureType ID 25); that points to a `Location` which has `CountryID`. Need to add parsing for Features and Locations. |
| **Address**           | Same `Location` → `LocationPart` (e.g. street, city, region, postal code). | Same as Country: need Profile → Feature (Location) → Location → LocationPart. |
| **Party type**        | `Profile` has `PartySubTypeID`; reference: `PartySubTypeValues` / `PartyTypeValues` (e.g. Individual, Entity, Vessel, Aircraft). | Easy: we already visit `Profile`; just read `PartySubTypeID` (and optionally resolve via PartyTypeValues). |
| **Sanctions program** | Sanction details reference `SanctionsProgram`; lookup in `ReferenceValueSets` → `SanctionsProgramValues` (e.g. CUBA, IRAN, SDGT). | Need to parse sanction/measure references from the party and resolve program ID to name. |
| **List name**         | We already have it: **source_file** (sdn_advanced.xml vs cons_advanced.xml). | Already in table as “Source”. |
| **Alias type**        | Already have **alias_type_id**; we resolve to A.K.A. / F.K.A. / N.K.A. / Name in the UI. | Already in table as “Type”. |
| **Fixed ref / Ref**   | Already have **fixed_ref** from `DistinctParty`. | Already in table as “Ref”. |

So for the frontend table you can plan on:

- **Already shown:** Listed name, Type (alias), Source (which XML file), Ref.
- **Easy to add:** **Party type** (Individual / Entity / Vessel / Aircraft etc.) from `Profile` + reference table.
- **Need extra parsing:** **Country** (and **Address**) from Profile → Feature (Location) → Location → CountryID / LocationPart; **Sanctions program** from sanction references + program lookup table.

---

## 4. Summary

- **Lookup:** One combined list from **both** `sdn_advanced.xml` and `cons_advanced.xml`; **source_file** tells you which file each row came from.
- **Displayed today:** Match score, Listed name, Type (alias), Source (file), Ref.
- **Available to add:** Country, Address, Party type, Sanctions program; Country (and Address) need Location/Feature parsing; Party type is straightforward; Sanctions program needs sanction/program parsing and lookup.

If you tell me which of these you want in the table first (e.g. Country, Party type), I can outline the exact parser changes and new columns in the export/API/frontend.
